#!/usr/bin/env python3
"""Check data isolation, platform selection and preservation of design edits."""
import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).parent


def module(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + '.py'))
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


searcher = module('search_references')
saver = module('save_rules')

# A small external-interface fixture, not a copy of the upstream ranking engine.
CORE = '''from pathlib import Path
import csv
DATA_DIR = Path(__file__).parent.parent / 'data'
CSV_CONFIG = {'ux': {'file': 'ux.csv', 'search_cols': ['Issue']}}
STACK_CONFIG = {'react-native': {'file': 'stacks/react-native.csv'}}
_STACK_COLS = {'search_cols': ['Guideline']}
def search(query, domain, limit):
    with (DATA_DIR / CSV_CONFIG[domain]['file']).open() as f:
        rows = list(csv.DictReader(f))[:limit]
    return {'count':len(rows), 'results':rows, 'domain':domain}
def search_stack(query, stack, limit):
    with (DATA_DIR / STACK_CONFIG[stack]['file']).open() as f:
        rows = list(csv.DictReader(f))[:limit]
    return {'count':len(rows), 'results':rows, 'stack':stack}
'''


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.runtime = self.root / 'runtime'
        (self.runtime / 'scripts').mkdir(parents=True)
        (self.runtime / 'data/stacks').mkdir(parents=True)
        (self.runtime / 'scripts/core.py').write_text(CORE)
        self.table = self.runtime / 'data/ux.csv'
        self.table.write_text('Issue,Do\nKeyboard focus,Show focus\n')
        (self.runtime / 'data/stacks/react.csv').write_text('Guideline,Do\nState,Keep state local\n')
        self.proposed = self.root / 'proposed.md'
        self.proposed.write_text('# Confirmed rules\nUse clear focus states.\n')
        self.target = self.root / 'project/rules.md'

    def tearDown(self):
        self.tmp.cleanup()

    def test_malformed_rows_are_excluded_and_source_is_unchanged(self):
        with self.table.open('w', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(['Issue', 'Do'])
            writer.writerow(['Valid', 'Keep this exact text'])
            writer.writerow(['Wrong', 'extra', 'field'])
            writer.writerow(['Swallowed', 'text\n28,another,CSV,row'])
        before = self.table.read_bytes()
        result = searcher.search(self.runtime, 'focus', domain='ux')
        self.assertEqual(result['results'], [{'Issue': 'Valid', 'Do': 'Keep this exact text'}])
        self.assertEqual(len(result['data_quality']['skipped_records']), 2)
        self.assertEqual(self.table.read_bytes(), before)
        self.assertFalse(list(self.runtime.rglob('__pycache__')))

    def test_actual_stack_file_is_used_despite_old_configuration(self):
        result = searcher.search(self.runtime, 'state', stack='react')
        self.assertEqual(result['stack'], 'react')
        self.assertEqual(result['results'][0]['Guideline'], 'State')
        self.assertIn("'react-native'", (self.runtime / 'scripts/core.py').read_text())

    def test_unknown_stack_is_reported_without_fallback(self):
        with self.assertRaisesRegex(ValueError, 'unavailable'):
            searcher.search(self.runtime, 'state', stack='nonexistent')

    def test_invalid_headers_and_empty_tables_fail(self):
        for text in ('Issue,Issue\nA,B\n', 'Other\nA\n', 'Issue,Do\nA,B,C\n'):
            self.table.write_text(text)
            with self.subTest(text=text), self.assertRaises(ValueError):
                searcher.search(self.runtime, 'focus', domain='ux')

    def test_runtime_and_missing_configuration_are_explicit(self):
        with self.assertRaises(ValueError):
            searcher.load_runtime(self.root / 'missing')
        result = subprocess.run([sys.executable, str(HERE / 'search_references.py'), '--runtime', str(self.runtime), '--list'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['stacks'], ['react'])

    def test_preview_creates_no_project_directory(self):
        result = saver.save(self.proposed, self.target)
        self.assertIn('Preview only', result)
        self.assertFalse(self.target.parent.exists())

    def test_new_file_then_existing_file_is_preserved(self):
        saver.save(self.proposed, self.target, True)
        self.target.write_bytes(b'User edits with custom rules.\r\n')
        before = self.target.read_bytes()
        with self.assertRaisesRegex(ValueError, 'Existing file preserved'):
            saver.save(self.proposed, self.target, True)
        self.assertEqual(self.target.read_bytes(), before)
        self.assertIn('User edits', saver.save(self.proposed, self.target))

    def test_symlink_target_is_not_followed(self):
        original = self.root / 'original.md'
        original.write_text('Original decisions')
        link = self.root / 'link.md'
        link.symlink_to(original)
        with self.assertRaises(ValueError):
            saver.save(self.proposed, link, True)
        self.assertEqual(original.read_text(), 'Original decisions')

    def test_save_cli_and_repeat_conflict(self):
        command = [sys.executable, str(HERE / 'save_rules.py'), '--input', str(self.proposed), '--target', str(self.target), '--apply']
        created = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(created.returncode, 0, created.stderr)
        before = self.target.read_bytes()
        repeated = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(repeated.returncode, 2)
        self.assertEqual(self.target.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
