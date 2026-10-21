#!/usr/bin/env python3
"""Build a release archive from an explicit file allowlist, never the workspace."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument('--target', required=True)
args = parser.parse_args()
allowed = {'aarch64-apple-darwin', 'x86_64-apple-darwin', 'x86_64-unknown-linux-gnu', 'aarch64-unknown-linux-gnu', 'x86_64-pc-windows-msvc'}
if args.target not in allowed:
    raise SystemExit('Unsupported target')
metadata = json.loads(subprocess.check_output(['cargo', 'metadata', '--locked', '--format-version', '1', '--no-deps'], cwd=ROOT))
version = metadata['packages'][0]['version']
windows = 'windows' in args.target
name = f'graffalo-agent-bridge-v{version}-{args.target}'
binary = 'graffalo-agent-bridge.exe' if windows else 'graffalo-agent-bridge'
out = ROOT / 'dist'
out.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as temporary:
    folder = Path(temporary) / name
    folder.mkdir()
    shutil.copy2(ROOT / 'target' / args.target / 'release' / binary, folder / binary)
    for filename in ['README.md', 'LICENSE', 'THIRD_PARTY_NOTICES.txt']:
        shutil.copy2(ROOT / filename, folder / filename)
    # rustc supplies platform runtime/library notices separately from Cargo crates.
    sysroot = Path(subprocess.check_output(['rustc', '--print', 'sysroot'], text=True).strip())
    rust_docs = sysroot / 'share' / 'doc' / 'rust'
    if not (rust_docs / 'COPYRIGHT.html').is_file():
        raise SystemExit('Toolchain COPYRIGHT.html missing; refusing an incomplete release')
    shutil.copy2(rust_docs / 'COPYRIGHT.html', folder / 'RUST_COPYRIGHT.html')
    license_dir = rust_docs / 'licenses'
    if license_dir.is_dir():
        shutil.copytree(license_dir, folder / 'rust-licenses')
    if windows:
        (folder / 'Start Graffalo.cmd').write_text('@echo off\r\ncd /d "%~dp0"\r\n"%~dp0graffalo-agent-bridge.exe"\r\npause\r\n', newline='')
    else:
        launcher = folder / ('Start Graffalo.command' if 'apple' in args.target else 'start-graffalo.sh')
        launcher.write_text(('#!/bin/zsh -l\n' if 'apple' in args.target else '#!/bin/sh\n') + 'set -eu\ncd -- "$(dirname -- "$0")"\nexec ./graffalo-agent-bridge\n')
        launcher.chmod(0o755)
    if windows:
        archive = out / f'{name}.zip'
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
            for item in sorted(folder.rglob('*')):
                if item.is_file():
                    bundle.write(item, item.relative_to(folder.parent))
    else:
        archive = out / f'{name}.tar.gz'
        with tarfile.open(archive, 'w:gz') as bundle:
            bundle.add(folder, arcname=name)
    print(archive.name)
