#!/usr/bin/env python3
"""Exercise safe installation and file inspection on disposable real files."""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script, *args, expected=0):
    result = subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True, text=True)
    assert result.returncode == expected, (result.returncode, result.stdout, result.stderr)
    return result.stdout


def main():
    installer = ROOT / 'scripts/install.py'
    with tempfile.TemporaryDirectory(prefix='personal-skills-check-') as temporary:
        base = Path(temporary)
        target = base / 'installed'
        output = run(installer, '--target', target)
        assert 'Preview only' in output and not target.exists(), 'Preview must not create directories'
        run(installer, '--target', target, '--apply')
        formal = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())['skills']
        assert len(list(target.iterdir())) == len(formal)
        for entry in target.iterdir():
            assert entry.is_symlink() and (entry / 'SKILL.md').is_file()
            assert 'in-progress' not in str(entry.resolve())
        again = run(installer, '--target', target, '--apply')
        assert 'Created 0 links' in again
        conflict = base / 'conflict'
        (conflict / 'brief').mkdir(parents=True)
        sentinel = conflict / 'brief/keep.txt'
        sentinel.write_text('User-owned content must survive.')
        output = run(installer, '--target', conflict, '--apply', expected=2)
        assert sentinel.read_text() == 'User-owned content must survive.'
        assert sorted(p.name for p in conflict.iterdir()) == ['brief'], 'Preflight must prevent partial installation'
        assert 'No changes made' in output
        aliases = base / 'aliases'
        (aliases / 'TangMonk').mkdir(parents=True)
        run(installer, '--target', aliases, '--skill', 'tang-monk', '--apply', expected=2)
        assert not (aliases / 'tang-monk').exists()
        run(installer, '--target', base / 'trial', '--skill', 'domain-modeling', '--apply', expected=2)
        assert not (base / 'trial').exists()
        workspace = base / 'workspace'
        workspace.mkdir()
        (workspace / 'a').mkdir()
        (workspace / 'b').mkdir()
        (workspace / 'a/same.txt').write_text('Exactly equal sample data.\n')
        (workspace / 'b/same.txt').write_text('Exactly equal sample data.\n')
        (workspace / 'unique.txt').write_text('Different data.\n')
        before = {str(p.relative_to(workspace)): hashlib.sha256(p.read_bytes()).hexdigest() for p in workspace.rglob('*') if p.is_file()}
        scripts = ROOT / 'skills/productivity/konmari/scripts'
        for name in ['init_workspace.py', 'scan_inventory.py', 'build_stats.py', 'find_exact_duplicates.py', 'build_review.py']:
            run(scripts / name, '--root', workspace)
        groups = json.loads((workspace / '_catalog/metadata/duplicates/exact_groups.json').read_text())
        assert groups['group_count'] == 1
        assert set(groups['items'][0]['paths']) == {'a/same.txt', 'b/same.txt'}
        summary = json.loads((workspace / '_catalog/metadata/stats/summary.json').read_text())
        assert summary['total_files'] == 3, 'Internal _catalog must not count as content'
        for rel, digest in before.items():
            assert hashlib.sha256((workspace / rel).read_bytes()).hexdigest() == digest, 'Inspection modified user content'
        assert sorted(p.name for p in workspace.iterdir()) == ['_catalog', 'a', 'b', 'unique.txt']
    print('Passed: preview, install, idempotence, conflict preservation, legacy-name conflict, trial exclusion, duplicate detection, internal-state isolation and unchanged user files.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
