#!/usr/bin/env python3
"""Filesystem regression cases; these do not evaluate an AI's judgment of PARA meaning."""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

import apply_actions
from workspace_lib import default_profile, top_level_context_adjustments

SCRIPTS = Path(__file__).resolve().parent


class ParaRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / 'workspace'
        self.root.mkdir()
        (self.root / 'source.txt').write_text('keep these original bytes\n')
        (self.base / 'outside.txt').write_text('outside scope\n')

    def content(self):
        return {str(p.relative_to(self.root)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.root.rglob('*') if p.is_file() and not p.is_symlink()
                and p.relative_to(self.root).parts[0] != '_catalog'}

    def run_script(self, name, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / name), '--root', str(self.root), *args],
                              text=True, capture_output=True)

    def apply(self, items, plan_type='move', confirm=True):
        plan = self.base / 'plan.json'
        plan.write_text(json.dumps({'items': items}))
        args = ['--plan-type', plan_type, '--plan-file', str(plan)]
        if confirm:
            args.append('--confirm')
        return self.run_script('apply_actions.py', *args)

    def reject_unchanged(self, items, plan_type='move'):
        before = self.content()
        result = self.apply(items, plan_type)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('Plan rejected before execution', result.stderr)
        self.assertEqual(self.content(), before)
        self.assertEqual((self.base / 'outside.txt').read_text(), 'outside scope\n')
        self.assertFalse((self.root / '_catalog').exists())

    def test_path_scope_and_internal_state(self):
        for source, target in [('../outside.txt', 'moved.txt'), (str(self.base / 'outside.txt'), 'moved.txt'),
                               ('source.txt', '../escaped.txt'), ('source.txt', str(self.base / 'escaped.txt')),
                               ('source.txt', '_catalog/secret.txt'), ('.', 'everything')]:
            with self.subTest(source=source, target=target):
                self.reject_unchanged([{'source_path': source, 'target_rel_path': target}])
        (self.root / '_catalog').mkdir()
        (self.root / '_catalog/private.txt').write_text('state')
        result = self.apply([{'source_path': '_catalog/private.txt', 'target_rel_path': 'exposed.txt'}])
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.root / '_catalog/private.txt').read_text(), 'state')

    def test_whole_plan_preflight(self):
        (self.root / 'occupied.txt').write_text('existing target')
        valid = {'source_path': 'source.txt', 'target_rel_path': 'new/source.txt'}
        for second in [{'source_path': 'missing.txt', 'target_rel_path': 'other.txt'},
                       {'source_path': 'occupied.txt', 'target_rel_path': 'new/source.txt'},
                       {'source_path': 'occupied.txt', 'target_rel_path': 'new'},
                       {'source_path': 'occupied.txt', 'target_rel_path': 'source.txt'}]:
            with self.subTest(second=second):
                self.reject_unchanged([valid, second])
        self.reject_unchanged([{'source_path': 'source.txt', 'target_rel_path': 'occupied.txt'}])

    def test_source_overlap_and_nested_target(self):
        (self.root / 'collection').mkdir()
        (self.root / 'collection/item.txt').write_text('item')
        self.reject_unchanged([{'source_path': 'collection', 'target_rel_path': 'new'},
                               {'source_path': 'collection/item.txt', 'target_rel_path': 'other'}])
        self.reject_unchanged([{'source_path': 'collection', 'target_rel_path': 'collection/inside'}])

    def test_symlinks_are_rejected(self):
        (self.root / 'link').symlink_to(self.base, target_is_directory=True)
        self.reject_unchanged([{'source_path': 'source.txt', 'target_rel_path': 'link/new.txt'}])
        self.reject_unchanged([{'source_path': 'link/outside.txt', 'target_rel_path': 'new.txt'}])
        (self.root / 'collection').mkdir()
        (self.root / 'collection/link.txt').symlink_to(self.base / 'outside.txt')
        self.reject_unchanged([{'source_path': 'collection', 'target_rel_path': 'new'}])
        self.reject_unchanged([{'source_path': 'collection', 'archive_path': 'new.zip'}], 'package')

    def test_existing_zip_and_quarantine_are_preserved(self):
        (self.root / 'existing.zip').write_bytes(b'previous archive bytes')
        self.reject_unchanged([{'source_path': 'source.txt', 'archive_path': 'existing.zip'}], 'package')
        (self.root / 'ToDelete').mkdir()
        (self.root / 'ToDelete/source.txt').write_text('quarantined earlier')
        self.reject_unchanged([{'source_path': 'source.txt', 'archive_path': 'new.zip',
                               'move_original_to_quarantine': True, 'quarantine_path': 'ToDelete/source.txt'}], 'package')

    def test_moves_and_recovery_preserve_bytes(self):
        (self.root / 'keep.txt').write_text('already placed')
        before = self.content()
        result = self.apply([{'source_path': 'source.txt', 'target_rel_path': 'Projects/demo/source.txt'},
                             {'source_path': 'keep.txt', 'target_rel_path': 'keep.txt', 'action': 'keep'}])
        self.assertEqual(result.returncode, 0, result.stderr)
        backup = Path(json.loads(result.stdout)['backup_dir'])
        self.assertEqual(json.loads((backup / 'execution_report.json').read_text())['status'], 'complete')
        rollback = self.run_script('apply_actions.py', '--plan-type', 'move', '--plan-file',
                                   str(backup / 'rollback_plan.json'), '--confirm')
        self.assertEqual(rollback.returncode, 0, rollback.stderr)
        self.assertEqual(self.content(), before)

    def test_runtime_failure_preserves_recovery_record(self):
        (self.root / 'second.txt').write_text('second source')
        plan = self.base / 'runtime.json'
        plan.write_text(json.dumps({'items': [{'source_path': 'source.txt', 'target_rel_path': 'new/first.txt'},
                                             {'source_path': 'second.txt', 'target_rel_path': 'new/second.txt'}]}))
        real_move = apply_actions.move_without_overwrite
        def fail_second(source, target):
            if source.name == 'second.txt':
                raise OSError('simulated filesystem failure')
            real_move(source, target)
        with mock.patch.object(sys, 'argv', ['apply', '--root', str(self.root), '--plan-type', 'move',
                                            '--plan-file', str(plan), '--confirm']), \
             mock.patch.object(apply_actions, 'move_without_overwrite', side_effect=fail_second), \
             mock.patch('sys.stdout', new_callable=io.StringIO):
            self.assertEqual(apply_actions.main(), 1)
        reports = list((self.root / '_catalog/backups').glob('*/execution_report.json'))
        self.assertEqual(len(reports), 1)
        report = json.loads(reports[0].read_text())
        self.assertEqual(report['status'], 'failed')
        self.assertEqual(report['operation_count'], 1)
        self.assertTrue((self.root / 'second.txt').exists())
        rollback = json.loads((reports[0].parent / 'rollback_plan.json').read_text())
        self.assertEqual(rollback['items'][0]['source_path'], 'new/first.txt')
        result = self.run_script('apply_actions.py', '--plan-type', 'move', '--plan-file',
                                 str(reports[0].parent / 'rollback_plan.json'), '--confirm')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / 'source.txt').exists())

    def test_packaging_and_original_recovery(self):
        before = (self.root / 'source.txt').read_bytes()
        result = self.apply([{'source_path': 'source.txt', 'archive_path': 'Archives/new.zip',
                             'move_original_to_quarantine': True, 'quarantine_path': 'ToDelete/source.txt'}], 'package')
        self.assertEqual(result.returncode, 0, result.stderr)
        with zipfile.ZipFile(self.root / 'Archives/new.zip') as archive:
            self.assertEqual(archive.read('source.txt'), before)
        self.assertEqual((self.root / 'ToDelete/source.txt').read_bytes(), before)
        backup = Path(json.loads(result.stdout)['backup_dir'])
        recovered = self.run_script('apply_actions.py', '--plan-type', 'move', '--plan-file',
                                    str(backup / 'rollback_plan.json'), '--confirm')
        self.assertEqual(recovered.returncode, 0, recovered.stderr)
        self.assertEqual((self.root / 'source.txt').read_bytes(), before)
        self.assertTrue((self.root / 'Archives/new.zip').exists())

    def test_empty_directory_packaging(self):
        (self.root / 'empty').mkdir()
        result = self.apply([{'source_path': 'empty', 'archive_path': 'empty.zip'}], 'package')
        self.assertEqual(result.returncode, 0, result.stderr)
        with zipfile.ZipFile(self.root / 'empty.zip') as archive:
            self.assertEqual(archive.namelist(), ['empty/'])

    def test_confirmation_required(self):
        result = self.apply([{'source_path': 'source.txt', 'target_rel_path': 'new.txt'}], confirm=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue((self.root / 'source.txt').exists())
        self.assertFalse((self.root / '_catalog').exists())

    def build_plan(self, mappings=None):
        before = self.content()
        result = self.run_script('init_workspace.py')
        self.assertEqual(result.returncode, 0, result.stderr)
        if mappings:
            profile_path = self.root / '_catalog/metadata/profile.json'
            profile = json.loads(profile_path.read_text())
            profile['bucket_names'] = mappings
            profile_path.write_text(json.dumps(profile))
        for script in ['scan_inventory.py', 'build_stats.py', 'find_name_duplicates.py',
                       'find_exact_duplicates.py', 'enrich_semantics.py', 'build_review.py']:
            result = self.run_script(script)
            self.assertEqual(result.returncode, 0, f'{script}: {result.stderr}')
        result = self.run_script('plan_actions.py', '--mode', 'para')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.content(), before)
        plan = json.loads((self.root / '_catalog/metadata/plans/para_plan.json').read_text())
        apply_actions.validate_plan(self.root, plan, 'para')
        return plan

    def test_generated_plan_executes_and_recovers(self):
        (self.root / 'collection').mkdir()
        (self.root / 'collection/reference.txt').write_text('Reusable reference tutorial for Python')
        before = self.content()
        plan = self.build_plan()
        result = self.apply(plan['items'], 'para')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(sorted(self.content().values()), sorted(before.values()))
        backup = Path(json.loads(result.stdout)['backup_dir'])
        recovered = self.run_script('apply_actions.py', '--plan-type', 'move', '--plan-file',
                                    str(backup / 'rollback_plan.json'), '--confirm')
        self.assertEqual(recovered.returncode, 0, recovered.stderr)
        self.assertEqual(self.content(), before)

    def test_numbered_para_containers_remain_in_place(self):
        names = {'01-Projects': 'Current project deliverable and implementation checklist',
                 '02-Areas': 'Health responsibility record', '03-Resources': 'Reference Python tutorial',
                 '04-Archives': 'Completed work report'}
        for name, text in names.items():
            (self.root / name).mkdir()
            (self.root / name / 'note.txt').write_text(text)
        plan = self.build_plan()
        items = {item['source_path']: item for item in plan['items']}
        for name in names:
            self.assertEqual(items[name]['target_rel_path'], name)
            self.assertEqual(items[name]['action'], 'keep')
            self.assertEqual(items[name]['target_bucket'], name.split('-', 1)[1])
        tags = json.loads((self.root / '_catalog/metadata/semantic/file_tags.json').read_text())
        classified = {row['rel_path']: row['dominant_bucket'] for row in tags}
        for name in names:
            self.assertEqual(classified[name + '/note.txt'], name.split('-', 1)[1])
        self.assertFalse(any(item['source_path'].startswith('_catalog') for item in plan['items']))

    def test_custom_nested_mapping_is_respected(self):
        (self.root / 'Work/Current').mkdir(parents=True)
        (self.root / 'Work/Current/note.txt').write_text('Reference tutorial with research notes')
        plan = self.build_plan({'projects': 'Work/Current', 'areas': 'Responsibilities',
                                'resources': 'Library', 'archives': 'Past'})
        item = next(item for item in plan['items'] if item['source_path'] == 'Work/Current')
        self.assertEqual(item['target_bucket'], 'Projects')
        self.assertEqual(item['action'], 'keep')
        profile = json.loads((self.root / '_catalog/metadata/profile.json').read_text())
        self.assertEqual(profile['bucket_names']['unsorted'], 'Library/Unsorted')
        tags = json.loads((self.root / '_catalog/metadata/semantic/file_tags.json').read_text())
        row = next(row for row in tags if row['rel_path'] == 'Work/Current/note.txt')
        self.assertIn('content_differs_from_existing_bucket', row['flags'])

    def test_number_alone_does_not_choose_a_bucket(self):
        self.assertEqual(top_level_context_adjustments('01-Unlabeled/note.txt')[0],
                         top_level_context_adjustments('99-Unlabeled/note.txt')[0])
        (self.root / '01-Unlabeled').mkdir()
        self.assertEqual(default_profile(self.root)['bucket_names']['projects'], 'Projects')


if __name__ == '__main__':
    unittest.main(verbosity=2)
