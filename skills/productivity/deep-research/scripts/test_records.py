#!/usr/bin/env python3
"""Exercise record integrity and CLI behavior without fetching sources."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('records.py')
spec = importlib.util.spec_from_file_location('research_records', SCRIPT)
records = importlib.util.module_from_spec(spec)
spec.loader.exec_module(records)


class RecordTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.ledger = self.root / 'research/evidence.jsonl'
        self.source = {'kind': 'source', 'title': 'Original material',
                       'location': 'materials/source.md', 'retrieved_at': '2026-10-20'}

    def tearDown(self):
        self.temp.cleanup()

    def excerpt(self, source_id, quote='The service never improved latency by 20%.'):
        return {'kind': 'evidence', 'source_id': source_id, 'quote': quote,
                'locator': 'Section 2, paragraph 1'}

    def test_source_identity_deduplicates_without_replacing_metadata(self):
        first = records.add(self.ledger, self.source)
        before = self.ledger.read_bytes()
        second = records.add(self.ledger, {**self.source, 'title': 'Revised metadata'})
        self.assertEqual(second, {'status': 'duplicate', 'id': first['id']})
        self.assertEqual(self.ledger.read_bytes(), before)

    def test_excerpts_preserve_negation_and_chinese_without_scoring(self):
        source = records.add(self.ledger, self.source)['id']
        quotes = ['The service never improved latency by 20%.', '大象生活在草原。\n这与咖啡无关。']
        for quote in quotes:
            records.add(self.ledger, self.excerpt(source, quote))
        result = list(records.load(self.ledger).values())
        self.assertEqual([r['quote'] for r in result[1:]], quotes)
        for row in result:
            self.assertTrue({'score', 'support_status', 'verified'}.isdisjoint(row))

    def test_unregistered_source_does_not_create_output(self):
        with self.assertRaises(ValueError):
            records.add(self.ledger, self.excerpt('unknown-source'))
        self.assertFalse(self.ledger.parent.exists())

    def test_invalid_record_does_not_change_ledger(self):
        records.add(self.ledger, self.source)
        before = self.ledger.read_bytes()
        for invalid in ({**self.source, 'retrieved_at': 'not-a-date'},
                        {**self.source, 'score': 1},
                        {**self.source, 'id': 'invented-id'}, []):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                records.add(self.ledger, invalid)
            self.assertEqual(self.ledger.read_bytes(), before)

    def test_existing_corruption_stops_append(self):
        records.add(self.ledger, self.source)
        with self.ledger.open('a') as stream:
            stream.write('not JSON\n')
        before = self.ledger.read_bytes()
        with self.assertRaisesRegex(ValueError, 'line 2'):
            records.add(self.ledger, {**self.source, 'location': 'other.md'})
        self.assertEqual(self.ledger.read_bytes(), before)

    def test_tampered_and_duplicate_ids_are_rejected(self):
        records.add(self.ledger, self.source)
        original = self.ledger.read_text()
        self.ledger.write_text(original + original)
        with self.assertRaisesRegex(ValueError, 'duplicate id'):
            records.load(self.ledger)
        obj = json.loads(original)
        obj['id'] = 'tampered'
        self.ledger.write_text(json.dumps(obj) + '\n')
        with self.assertRaisesRegex(ValueError, 'incorrect'):
            records.load(self.ledger)

    def test_missing_final_newline_and_duplicate_excerpt(self):
        source = records.add(self.ledger, self.source)['id']
        self.ledger.write_text(self.ledger.read_text().rstrip('\n'))
        evidence = self.excerpt(source)
        records.add(self.ledger, evidence)
        before = self.ledger.read_bytes()
        self.assertEqual(records.add(self.ledger, evidence)['status'], 'duplicate')
        self.assertEqual(self.ledger.read_bytes(), before)
        self.assertEqual(len(records.load(self.ledger)), 2)

    def test_symlink_does_not_change_target(self):
        target = self.root / 'original.jsonl'
        target.write_text('preserve this file')
        link = self.root / 'linked.jsonl'
        link.symlink_to(target)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            records.add(link, self.source)
        self.assertEqual(target.read_text(), 'preserve this file')

    def test_cli_roundtrip_and_missing_input(self):
        payload = self.root / 'record.json'
        payload.write_text(json.dumps(self.source))
        added = subprocess.run([sys.executable, str(SCRIPT), 'add', '--ledger', str(self.ledger),
                                '--record', str(payload)], capture_output=True, text=True)
        self.assertEqual(added.returncode, 0, added.stderr)
        self.assertEqual(json.loads(added.stdout)['status'], 'added')
        checked = subprocess.run([sys.executable, str(SCRIPT), 'check', '--ledger', str(self.ledger)],
                                  capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertEqual(json.loads(checked.stdout), {'status': 'valid-records', 'sources': 1, 'excerpts': 0})
        missing = subprocess.run([sys.executable, str(SCRIPT), 'check', '--ledger', str(self.root / 'missing')],
                                  capture_output=True, text=True)
        self.assertEqual(missing.returncode, 2)
        self.assertFalse((self.root / 'missing').exists())


if __name__ == '__main__':
    unittest.main()
