#!/usr/bin/env python3
"""Exercise runtime isolation, pin failures and an actual child-shell environment."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import runtime


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'upstream'
        self.root.mkdir()
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        subprocess.run(['git', '-C', str(self.root), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '--allow-empty', '-qm', 'fixture'], check=True)
        commit = subprocess.check_output(['git', '-C', str(self.root), 'rev-parse', 'HEAD'], text=True).strip()
        (self.root / 'entry.md').write_text('Read ' + str(self.root) + '/section.md\n')
        (self.root / 'section.md').write_text('Review the selected plan.\n')
        self.bun = self.base / 'toolchain/bun'
        self.bun.parent.mkdir()
        self.bun.write_text('#!/bin/sh\nprintf "1.4.2\\n"\n')
        self.bun.chmod(0o755)
        self.config = {'runtime_root': str(self.root), 'state_root': str(self.base / 'state'), 'bun_path': str(self.bun)}
        fingerprint = hashlib.sha256((self.root / 'entry.md').read_text().replace(str(self.root), '<GSTACK_RUNTIME>').encode()).hexdigest()
        self.spec = {'upstream_commit': commit, 'bun_version': '1.4.2', 'required_files': ['entry.md', 'section.md'], 'normalized_sha256': {'entry.md': fingerprint}, 'entrypoint': 'entry.md', 'preamble': 'section.md'}

    def test_shell_gets_private_tools_and_keeps_working_directory(self):
        before = os.environ.copy()
        info = runtime.verify(self.config, self.spec)
        result = subprocess.run(['bash'], input='pwd\nprintf "%s\\n" "$GSTACK_STATE_ROOT"\nbun --version\nexit 7\n', text=True, env=runtime.environment(info), cwd=self.base, capture_output=True)
        self.assertEqual(result.returncode, 7)
        self.assertEqual(result.stdout.splitlines(), [str(self.base.resolve()), str((self.base / 'state').resolve()), '1.4.2'])
        self.assertEqual(os.environ.copy(), before)
        self.assertFalse((self.base / 'state').exists())

    def test_missing_required_section_fails(self):
        (self.root / 'section.md').unlink()
        with self.assertRaises(FileNotFoundError):
            runtime.verify(self.config, self.spec)

    def test_changed_document_fails(self):
        (self.root / 'entry.md').write_text('Different review instructions.\n')
        with self.assertRaisesRegex(ValueError, 'document changed'):
            runtime.verify(self.config, self.spec)

    def test_wrong_revision_fails(self):
        self.spec['upstream_commit'] = '0' * 40
        with self.assertRaisesRegex(ValueError, 'revision differs'):
            runtime.verify(self.config, self.spec)

    def test_wrong_bun_fails(self):
        self.bun.write_text('#!/bin/sh\nprintf "1.2.10\\n"\n')
        with self.assertRaisesRegex(ValueError, 'Expected Bun'):
            runtime.verify(self.config, self.spec)

    def test_state_cannot_modify_pinned_checkout(self):
        self.config['state_root'] = str(self.root / 'state')
        with self.assertRaisesRegex(ValueError, 'outside'):
            runtime.verify(self.config, self.spec)

    def test_missing_binding_is_reported_without_installing(self):
        missing = self.base / 'missing.json'
        result = subprocess.run(['python3', str(Path(runtime.__file__)), 'check', '--config', str(missing)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('Runtime unavailable', result.stderr)
        self.assertFalse(missing.exists())


if __name__ == '__main__':
    unittest.main()
