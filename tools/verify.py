"""Validate patches against extracted game data and exercise the new menu expressions.

The small evaluator implements only the operators used by the new blobs; it is
not the game's menu engine and does not substitute for a live gameplay test.
"""
from pathlib import Path
import copy
import hashlib
import json
import uuid
import zlib

from create_mod import ROOT, BASE, MOD, RIFLES, BLOB_PREFIX


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def apply_patch(document, operations):
    document = copy.deepcopy(document)
    for op in operations:
        if op['op'] == 'move':
            source_parts = [s.replace('~1', '/').replace('~0', '~') for s in op['from'].split('/')[1:]]
            source_parent = document
            for part in source_parts[:-1]:
                source_parent = source_parent[int(part)] if isinstance(source_parent, list) else source_parent[part]
            key = int(source_parts[-1]) if isinstance(source_parent, list) else source_parts[-1]
            value = source_parent.pop(key)
            document = apply_patch(document, [{'op': 'add', 'path': op['path'], 'value': value}])
            continue
        parts = [s.replace('~1', '/').replace('~0', '~') for s in op['path'].split('/')[1:]]
        parent = document
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        key = parts[-1]
        if isinstance(parent, list):
            index = len(parent) if key == '-' else int(key)
            if op['op'] == 'add':
                assert 0 <= index <= len(parent)
                parent.insert(index, copy.deepcopy(op['value']))
            elif op['op'] == 'remove':
                parent.pop(index)
            else:
                assert op['op'] == 'replace'
                parent[index] = copy.deepcopy(op['value'])
        elif op['op'] == 'remove':
            del parent[key]
        else:
            assert op['op'] in ('add', 'replace')
            if op['op'] == 'replace':
                assert key in parent
            parent[key] = copy.deepcopy(op['value'])
    return document


def evaluate(value, context, global_context):
    if isinstance(value, list):
        return [evaluate(v, context, global_context) for v in value]
    if isinstance(value, str):
        if value == '$.':
            return copy.deepcopy(context)
        if value.startswith('$not '):
            return not evaluate(value[5:], context, global_context)
        if value.startswith('$isnullorempty '):
            return evaluate(value[15:], context, global_context) in (None, [], '')
        if value.startswith('$isnull '):
            return evaluate(value[8:], context, global_context) is None
        if value.startswith('$eq('):
            left, right = value[4:-1].split(',', 1)
            return evaluate(left, context, global_context) == evaluate(right, context, global_context)
        if value.startswith('$.'):
            result = context
            for part in value[2:].split('.'):
                result = global_context if part == '@global' else result.get(part) if isinstance(result, dict) else None
            return copy.deepcopy(result)
        return value
    if not isinstance(value, dict):
        return value
    for key, cases in value.items():
        if key.startswith('$switch '):
            selector = evaluate(key[8:], context, global_context)
            for case in cases:
                if 'default' in case:
                    return evaluate(case['default'], context, global_context)
                match = evaluate(case['case'], context, global_context)
                # Keep URL strings distinct from JSON booleans.
                if type(selector) is type(match) and selector == match:
                    return evaluate(case['return'], context, global_context)
            return None
    if '$include' in value:
        return evaluate(read(MOD / 'newBlobs' / value['$include']), context, global_context)
    if '$datacontext' in value:
        block = value['$datacontext']
        return evaluate(block['do'], evaluate(block['in'], context, global_context), global_context)
    if '$and' in value:
        return all(evaluate(v, context, global_context) for v in value['$and'])
    if '$mergearrays' in value:
        arrays = evaluate(value['$mergearrays'], context, global_context)
        assert all(isinstance(v, list) for v in arrays), 'New blobs must merge arrays, never null/scalars'
        return [item for array in arrays for item in array]
    if '$mergeobjects' in value:
        result = {}
        for item in evaluate(value['$mergeobjects'], context, global_context):
            assert isinstance(item, dict)
            result.update(item)
        return result
    for key, branch in value.items():
        if key == '$if' or key.startswith('$if '):
            condition = branch['$condition'] if key == '$if' else key[4:]
            return evaluate(branch.get('$then' if evaluate(condition, context, global_context) else '$else'), context, global_context)
    return {k: evaluate(v, context, global_context) for k, v in value.items()}


def verify():
    checks = []
    manifest = read(MOD / 'manifest.json')
    assert manifest['incompatibilities'] == ['grappigegovert.extraloadoutslots']
    assert 'updateCheck' not in manifest
    checks.append('Separate mod ID, original-mod incompatibility and no upstream auto-update')
    originals = [p for p in BASE.rglob('*') if p.is_file() and p.name not in ('manifest.json', 'stashpointslot.JSON.patch.json')]
    for original in originals:
        assert original.read_bytes() == (MOD / original.relative_to(BASE)).read_bytes(), original
    checks.append(f'All {len(originals)} original non-manifest files preserved byte for byte')
    original_leaf = read(BASE / 'fileEdits/chunk0/stashpointslot.JSON.patch.json')
    new_leaf = read(MOD / 'fileEdits/chunk0/stashpointslot.JSON.patch.json')
    assert new_leaf['patch'][:len(original_leaf['patch'])] == original_leaf['patch']
    assert not (MOD / 'fileEdits/chunk0/stashpoint_page.JSON.patch.json').exists()
    checks.append('Original temporary-slot patch runs first; no stashpoint_page input override remains')
    for file in MOD.rglob('*.json'):
        read(file)
    baseline_paths = [ROOT / 'research/vanilla', ROOT / 'research/extracted/chunk0patch4/JSON']
    patched = {}
    for file in (MOD / 'fileEdits/chunk0').glob('*.JSON.patch.json'):
        patch = read(file)
        candidates = [p for directory in baseline_paths for p in directory.rglob(patch['file'] + '.JSON')]
        assert len(candidates) == 1, (file, candidates)
        patched[patch['file']] = apply_patch(read(candidates[0]), patch['patch'])
    checks.append('All three RFC6902 patches apply to unmodified game resources')
    category = read(MOD / 'newBlobs' / BLOB_PREFIX / 'extraslots_snipertrio_category.json')
    leaf = patched['00595CD49B4ACA64']['$if']
    original_render = apply_patch(read(ROOT / 'research/vanilla/chunk0patch4/JSON/00595CD49B4ACA64.JSON'), original_leaf['patch'])
    original_categories = original_render['$if $isnullorempty $.Items']['$else']['$datacontext']['do']['children']
    merged_children = leaf['$else']['$datacontext']['do']['children']['$mergearrays']
    assert merged_children[1] == original_categories
    assert merged_children[0] == {'$include': BLOB_PREFIX + 'extraslots_snipertrio_category.json'}
    checks.append('New category attaches to the installed original mod leaf; native inventory category tree is preserved')
    expected_ids = [rifle[1] for rifle in RIFLES]
    scenarios = 0
    for items in (None, [], [{'SlotId': 'case-a', 'Item': {'InstanceId': 'owned-item'}, 'Unrelated': 42}]):
        for slot in ('12345678-1234-1234-1234-123456789abc', '6', 6, '2', 2, '3', '4', '5', None, '', '9fff18d3-6d6f-433c-a3f4-794b9cdfa8a5'):
            for allow in (True, False, None, 'true', 'false'):
                data = {'SlotId': slot, 'Items': copy.deepcopy(items), 'OtherField': {'Keep': 1}}
                before = copy.deepcopy(data)
                global_context = {'args': {'allowlargeitems': allow, 'slotid': slot, 'usecacheonreturn': True}}
                result = evaluate(category, data, global_context)
                assert data == before
                eligible = slot == '12345678-1234-1234-1234-123456789abc' or (slot in ('6', 6) and allow in (True, 'true'))
                if eligible:
                    assert len(result) == 1 and result[0]['id'] == 'els_sa_container'
                    added = result[0]['children'][0]['children']
                    equips = [tile['actions']['accept'][1]['loadout'] for tile in added]
                    assert [equip['instance']['Unlockable']['Properties']['RepositoryId'] for equip in equips] == expected_ids
                    assert all(equip['slotid'] == slot for equip in equips)
                    assert evaluate(leaf['$condition'], data, global_context) is False
                    for equip in equips:
                        item = equip['instance']
                        uuid.UUID(item['InstanceId'])
                        uuid.UUID(item['Unlockable']['Guid'])
                        assert item['Unlockable']['Subtype'] == 'sniperrifle'
                        for text in ('Name', 'Description'):
                            assert all(item['Unlockable']['Properties'][text] in loc for loc in manifest['localisation'].values())
                else:
                    assert result == []
                    assert evaluate(leaf['$condition'], data, global_context) == (not items)
                scenarios += 1
    checks.append(f'{scenarios} menu-expression cases: dynamic briefcase slots, large/small stash, reserved slots, empty inventory, boolean/string flags')
    repo_file = ROOT / 'research/extracted/chunk0patch4/REPO/00204D1AFD76AB13.REPO'
    repo = {x['ID_']: x for x in read(repo_file)}
    weapons = []
    for map_id, repo_id, name_en, name_cn, runtime in RIFLES:
        weapon = repo[repo_id]
        assert f'{int(weapon["Runtime"]):016X}' == runtime
        assert weapon['ItemSize'] == 'ITEMSIZE_LARGE'
        magazines = [repo[key] for key in weapon['PrimaryConfiguration']['MagazineConfigs']]
        tags = {tag for magazine in magazines for tag in magazine['Tags']}
        assert tags == {'bodypiercingmag', 'wallpenetratingmag', 'shockwavemag'}
        ammo = [repo[magazine['AmmoConfig']] for magazine in magazines]
        behaviours = [repo[key] for config in ammo for key in config.get('Behaviours', [])]
        assert any(b.get('PenetratesEnvironment') and b.get('PenetratesBodies') for b in behaviours)
        assert any(b.get('MassImpulseType') == 'eMIT_ShockWave' for b in behaviours)
        weapons.append({
            'map': map_id, 'name': name_en, 'repositoryId': repo_id,
            'runtime': runtime, 'primaryConfiguration': weapon['PrimaryConfiguration']['ID_'],
            'magazines': magazines, 'ammunition': ammo, 'behaviours': behaviours,
        })
    checks.append('All three original repository IDs resolve to normal, wall-piercing and shockwave magazines')
    roundtrip_root = ROOT / 'build' / ('roundtrip-' + manifest['version'])
    roundtrip = roundtrip_root / 'chunk0patch300'
    if roundtrip.exists():
        for resource, expected in patched.items():
            assert read(roundtrip / 'JSON' / (resource + '.JSON')) == expected
        blobs = read(roundtrip / 'ORES/00858D45F5F9E3CA.ORES.JSON')
        for path in (MOD / 'newBlobs').rglob('*.json'):
            relative = path.relative_to(MOD / 'newBlobs').as_posix().lower()
            resource = '00' + hashlib.md5(f'[assembly:/_pro/online/default/cloudstorage/resources/{relative}].pc_json'.encode()).hexdigest()[2:16].upper()
            assert blobs[resource] == relative
            assert read(roundtrip / 'JSON' / (resource + '.JSON')) == read(path)
        localisation = read(roundtrip_root / 'localisation.json')['languages']
        for language, short in [('english', 'en'), ('chineseSimplified', 'cn'), ('chineseTraditional', 'tc')]:
            for key, text in manifest['localisation'][language].items():
                crc = f'{zlib.crc32(key.upper().encode()):08X}'
                assert localisation[short][crc] == text
        checks.append('Re-extracted SMF RPKG: three patched menus, seven registered blobs and EN/CN/TC localisation match source')
    output = ROOT / 'research/verification.json'
    result = {
        'gameVersion': '3.280.0.0', 'checks': checks,
        'modVersion': manifest['version'],
        'scope': 'Static checks, a limited menu-expression simulator and separate SMF deployment. No live gameplay validation.',
        'repositorySha256': hashlib.sha256(repo_file.read_bytes()).hexdigest(),
        'weapons': weapons,
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('\n'.join('PASS ' + check for check in checks))


if __name__ == '__main__':
    verify()
