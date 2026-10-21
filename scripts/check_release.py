#!/usr/bin/env python3
"""A tag may only release the version declared by the package."""
import json
import os
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parent.parent
metadata = json.loads(subprocess.check_output(['cargo', 'metadata', '--locked', '--no-deps', '--format-version', '1'], cwd=root))
version = metadata['packages'][0]['version']
ref = os.environ.get('GITHUB_REF', '')
if ref.startswith('refs/tags/'):
    tag = ref.removeprefix('refs/tags/')
    if not re.fullmatch(r'v\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?', tag) or tag != f'v{version}':
        raise SystemExit('Release tag must match Cargo.toml version exactly')
print(f'Validated package version {version}')
