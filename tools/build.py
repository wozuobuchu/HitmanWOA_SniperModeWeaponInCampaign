"""Package the checked-in SMF mod; Python standard library only."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mod/Extra Loadout Slots - Sniper Trio'


def build():
    manifest = json.loads((MOD / 'manifest.json').read_text(encoding='utf-8'))
    dest = ROOT / 'dist'
    dest.mkdir(exist_ok=True)
    archive = dest / f'Extra.Loadout.Slots.Sniper.Trio-{manifest["version"]}.zip'
    files = sorted(p for p in MOD.rglob('*') if p.is_file())
    for file in files:
        if file.suffix == '.json':
            json.loads(file.read_text(encoding='utf-8'))
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as package:
        for file in files:
            name = (Path(MOD.name) / file.relative_to(MOD)).as_posix()
            entry = zipfile.ZipInfo(name, date_time=(2026, 10, 25, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            package.writestr(entry, file.read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix('.zip.sha256').write_text(f'{digest}  {archive.name}\n', encoding='utf-8')
    print(f'{archive}\n{len(files)} files; {archive.stat().st_size} bytes\nSHA256 {digest}')


if __name__ == '__main__':
    build()
