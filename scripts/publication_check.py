#!/usr/bin/env python3
"""Fail closed on unexpected tracked files or obvious credentials/private paths."""
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parent.parent
exact = {'Cargo.toml', 'Cargo.lock', 'LICENSE', 'THIRD_PARTY_NOTICES.txt', 'README.md', 'SECURITY.md', 'AGENTS.md', '.gitignore', 'rust-toolchain.toml', '.github/dependabot.yml', '.github/workflows/build.yml', 'src/lib.rs', 'src/main.rs', 'tests/protocol_fixture.py', 'scripts/notices.py', 'scripts/package.py', 'scripts/check_release.py', 'scripts/publication_check.py', 'docs/PROTOCOL.md', 'docs/RELEASING.md', 'docs/RELEASE_NOTES.md', 'docs/REPOSITORIES.md'}
files = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
for name in filter(None, files):
    if name not in exact:
        raise SystemExit(f'File needs publication review: {name}')
    path = root / name
    if path.is_symlink() or path.stat().st_size > 2_000_000:
        raise SystemExit(f'Unexpected file type/size: {name}')
    text = path.read_text(encoding='utf-8')
    # Names of credential variables are allowed, credential values are not.
    patterns = [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', r'gh[pousr]_[A-Za-z0-9]{20,}', r'github_pat_[A-Za-z0-9_]{30,}', r'sk-(?:proj-|live_|test_)?[A-Za-z0-9_-]{24,}', r'AKIA[0-9A-Z]{16}', r'/(?:Volumes/raid0|Users/monomyth)/', r'libsql://[A-Za-z0-9-]+\.', r'eyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}']
    if any(re.search(pattern, text) for pattern in patterns):
        raise SystemExit(f'Potential secret or private path in {name}; inspect locally')
print(f'Publication allowlist and credential-pattern checks passed for {len(list(filter(None, files)))} files')
