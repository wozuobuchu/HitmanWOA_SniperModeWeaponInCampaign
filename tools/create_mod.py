"""Reproduce the fork's sources from the user-supplied Extra Loadout Slots 2.1.0."""
from pathlib import Path
import copy
import json
import shutil
import uuid

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'ref/Extra Loadout Slots-724-2-1-0-1759945258/extraloadoutslots'
MOD = ROOT / 'mod/Extra Loadout Slots - Sniper Trio'
MOD_ID = 'enjoy.ExtraLoadoutSniperTrio'
BLOB_PREFIX = 'menusystem/pages/planning/content/'
RIFLES = [
    ('HIMMELSTEIN', '5f5e10e1-4c38-4fd0-ac16-8f42526ab232',
     'Sieger 300 Ghost [SA - Himmelstein]', 'Sieger 300 幽灵 [狙击模式·Himmelstein]',
     '0001BD7A2263A50C'),
    ('HANTU', 'c8b2d7ab-c952-4ad3-99fe-4627047318b9',
     'Druzhina 34 ICA [SA - Hantu Port]', 'ICA 亲卫兵 34 [狙击模式·Hantu Port]',
     '00B2EF154AF811DA'),
    ('SIBERIA', '2f209936-1427-43b6-9812-d6f60b24336f',
     'Druzhina 34 ICA Arctic [SA - Siberia]', 'ICA 亲卫兵 34 北极型 [狙击模式·西伯利亚]',
     '00B2EF154AF811DA'),
]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def create():
    original = json.loads((BASE / 'manifest.json').read_text(encoding='utf-8'))
    assert original['version'] == '2.1.0' and original['id'] == 'grappigegovert.extraloadoutslots'
    shutil.copytree(BASE, MOD, dirs_exist_ok=True)
    manifest = copy.deepcopy(original)
    manifest.update({
        'id': MOD_ID,
        'name': 'Extra Loadout Slots - Sniper Trio',
        'version': '2.1.2',
        'description': 'Extra Loadout Slots 2.1.0 plus a Sniper Assassin category in briefcase and large stash selections, containing all three Agent 47 rifles. Includes the original extra slots and quantity controls. Disable the original Extra Loadout Slots mod.',
        'authors': ['grappigegovert (Extra Loadout Slots 2.1.0)', 'enjoy (local Sniper Trio fork)'],
        'incompatibilities': ['grappigegovert.extraloadoutslots'],
    })
    # An upstream auto-update must not replace this local fork.
    manifest.pop('updateCheck', None)
    english, chinese, traditional = {}, {}, {}
    english['UI_ELS_SA_DESCRIPTION'] = 'Sniper Assassin original: normal, wall-piercing and shockwave magazines. Use the game\'s ammunition-switch controls (Z/X on the reported keyboard setup).'
    chinese['UI_ELS_SA_DESCRIPTION'] = '狙击手模式原版：保留普通、穿墙与震荡弹匣。使用游戏的弹药切换按键（当前键位为 Z/X）。'
    traditional['UI_ELS_SA_DESCRIPTION'] = '狙擊手模式原版：保留普通、穿牆與震盪彈匣。使用遊戲的彈藥切換按鍵（目前鍵位為 Z/X）。'
    english['UI_ELS_SA_CATEGORY'] = 'Sniper Assassin'
    chinese['UI_ELS_SA_CATEGORY'] = '狙击模式'
    traditional['UI_ELS_SA_CATEGORY'] = '狙擊模式'
    items = []
    for map_id, repo_id, name_en, name_cn, runtime in RIFLES:
        item_id = f'ELS_SA_{map_id}'
        name_key = f'UI_{item_id}_NAME'
        guid = str(uuid.uuid5(uuid.NAMESPACE_URL, f'{MOD_ID}/{map_id}/unlockable'))
        instance = str(uuid.uuid5(uuid.NAMESPACE_URL, f'{MOD_ID}/{map_id}/instance'))
        english[name_key], chinese[name_key] = name_en, name_cn
        traditional[name_key] = name_cn.replace('亲卫兵', '親衛兵').replace('狙击模式', '狙擊模式').replace('极', '極').replace('幽灵', '幽靈').replace('亚', '亞')
        # Match the native stashpoint row shape. SlotId is evaluated in
        # LoadoutItemsData, so the same entry works in any briefcase/stash slot.
        items.append({
            'SlotId': '$.SlotId',
            'Item': {
                'InstanceId': instance,
                'Unlockable': {
                    'Id': item_id, 'Guid': guid, 'Type': 'weapon', 'Subtype': 'sniperrifle',
                    'ImageId': '', 'RMTPrice': 0, 'GamePrice': 0,
                    'IsPurchasable': False, 'IsPublished': True, 'IsDroppable': False,
                    'Capabilities': [], 'Qualities': {}, 'Rarity': 'common',
                    'Properties': {
                        'Name': name_key, 'Description': 'UI_ELS_SA_DESCRIPTION',
                        'Quality': 4, 'Rarity': 'common', 'LoadoutSlot': 'carriedweapon',
                        'RepositoryId': repo_id,
                    },
                },
                'Properties': {},
            },
        })
    manifest['localisation'] = {language: english.copy() for language in
        ['english', 'french', 'italian', 'german', 'spanish', 'russian', 'japanese']}
    manifest['localisation']['chineseSimplified'] = chinese
    manifest['localisation']['chineseTraditional'] = traditional
    write_json(MOD / 'manifest.json', manifest)
    # Work in the leaf component already patched by Extra Loadout Slots.
    # Online responses can supply a page template without loading the local
    # stashpoint_page.json. Do not rely on replacing that page's input.
    # Use literal switch cases for both JSON booleans and URL-style strings.
    large_stash = {'$switch $.@global.args.allowlargeitems': [
        {'case': True, 'return': True}, {'case': 'true', 'return': True},
        {'default': False},
    ]}
    slot_cases = [{'case': value, 'return': False} for value in
                  [None, '', 0, 1, 2, 3, 4, 5, '0', '1', '2', '3', '4', '5',
                   '9fff18d3-6d6f-433c-a3f4-794b9cdfa8a5']]
    slot_cases.extend([{'case': 6, 'return': large_stash},
                       {'case': '6', 'return': large_stash},
                       {'default': True}])  # Game-issued dynamic briefcase slot.
    eligible_path = BLOB_PREFIX + 'extraslots_snipertrio_eligible.json'
    write_json(MOD / 'newBlobs' / eligible_path,
               {'$switch $.@global.args.slotid': slot_cases})
    tiles = []
    for row in items:
        instance = row['Item']
        unlockable = instance['Unlockable']
        properties = unlockable['Properties']
        repo_id = properties['RepositoryId']
        # Bind presentation directly to known repository IDs and localisation.
        # Equipping passes the full instance, like the original mod's compound item.
        display = {
            'header': '$loc UI_ELS_SA_CATEGORY',
            'title': '$loc ' + properties['Name'],
            'image': '$res {$repository ' + repo_id + '}.Image',
            'icon': 'sniperrifle', 'rarity': 'common',
            'perks': '{$repository ' + repo_id + '}.Perks',
        }
        tiles.append({
            'id': unlockable['Id'], 'view': 'menu3.basic.ItemTileSmall',
            'nrows': 1.5, 'ncols': 2, 'pressable': True,
            'data': display,
            'actions': {
                'select': {'replace-children': {
                    'target': 'headline_container',
                    'children': [{'view': 'menu3.basic.ItemHeadlineElement', 'data': display}],
                }},
                'deselect': {'replace-children': {'target': 'headline_container', 'children': []}},
                'accept': [
                    {'$if $.@global.args.set-stashpoint': {
                        '$then': {'set-loadout-agencypickup': {'id': '$.@global.args.stashpoint'}},
                    }},
                    {
                        'loadout': {'mode': 'equip', 'slotid': '$.@global.args.slotid', 'instance': instance},
                        'request-back': {
                            'target': ['contractcreation_planning', 'planning', 'multiplayer', 'gamemode_versus'],
                            'usecache': {'$if $isnull $.@global.args.usecacheonreturn': {
                                '$then': False, '$else': '$.@global.args.usecacheonreturn',
                            }},
                        },
                    },
                ],
            },
        })
    category_path = BLOB_PREFIX + 'extraslots_snipertrio_category.json'
    write_json(MOD / 'newBlobs' / category_path, {
        '$if': {
            '$condition': {'$include': eligible_path},
            '$then': [{
                'id': 'els_sa_container', 'view': 'menu3.basic.SubCategoryElement',
                'controller': 'categoryitem', 'data': {'title': '$loc UI_ELS_SA_CATEGORY'},
                'children': [{
                    'controller': 'group', 'view': 'menu3.containers.ScrollingListContainer',
                    'id': 'els_sa_scroll_container', 'layoutchildren': True,
                    'row': 1, 'nrows': 3, 'ncols': 10, 'direction': 'horizontal',
                    'data': {'direction': 'horizontal'}, 'children': tiles,
                }],
            }],
            '$else': [],
        },
    })
    leaf_path = MOD / 'fileEdits/chunk0/stashpointslot.JSON.patch.json'
    leaf_patch = json.loads(leaf_path.read_text(encoding='utf-8'))
    prefix = '/$if/$else/$datacontext'
    # Apply the original temporary-slot fix first, then rename its root
    # conditional and splice the new category ahead of the native categories.
    leaf_patch['patch'].extend([
        {'op': 'move', 'from': '/$if $isnullorempty $.Items', 'path': '/$if'},
        {'op': 'add', 'path': '/$if/$condition', 'value': {
            '$and': ['$isnullorempty $.Items', {'$if': {
                '$condition': {'$include': eligible_path}, '$then': False, '$else': True,
            }}],
        }},
        {'op': 'replace', 'path': prefix + '/datavalues/GroupedItems/$arraygroupby/source/$arraysort/source',
         'value': {'$if $isnullorempty $.Items': {'$then': [], '$else': '$.Items'}}},
        {'op': 'add', 'path': prefix + '/do/children/$mergearrays',
         'value': [{'$include': category_path}, {}]},
        {'op': 'move', 'from': prefix + '/do/children/$each',
         'path': prefix + '/do/children/$mergearrays/1/$each'},
    ])
    write_json(leaf_path, leaf_patch)
    if (ROOT / 'README.md').exists():
        shutil.copyfile(ROOT / 'README.md', MOD / 'README.zh-CN.md')
    print(f'Created {MOD.relative_to(ROOT)}')


if __name__ == '__main__':
    create()
