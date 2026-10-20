#!/usr/bin/env python3
"""Offline evaluation invariants; no live Codex or model calls."""
import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import model_runner
import trigger_eval
from task_results import summarize
from review_report import render

CASES = [{'query': 'make a reusable workflow', 'should_trigger': True},
         {'query': 'answer a simple question', 'should_trigger': False}]


def run_row(variant='candidate', passed=True, **extra):
    return {'case_id': 'one', 'variant': variant, 'run_id': '1', 'status': 'ok',
            'prompt': 'The actual task', 'output': 'The actual output',
            'expectations': [{'text': 'Requested outcome', 'passed': passed, 'evidence': 'Inspected result'}], **extra}


class EvalTests(unittest.TestCase):
    def test_process_errors_never_pass_negative_cases(self):
        def broken(*args):
            raise RuntimeError('synthetic process failure')
        result = trigger_eval.evaluate(CASES, 'probe', 'description', runner=broken)
        self.assertEqual(result['summary'], {'total': 2, 'completed': 0, 'incomplete': 2, 'passed': 0, 'failed': 0, 'execution_errors': 2})
        self.assertTrue(all(row['pass'] is None and row['trigger_rate'] is None for row in result['results']))

    def test_mixed_runs_use_valid_denominator_but_remain_incomplete(self):
        answers = iter([True, RuntimeError('failed')])
        def runner(*args):
            answer = next(answers)
            if isinstance(answer, Exception):
                raise answer
            return answer
        row = trigger_eval.evaluate(CASES[:1], 'probe', 'description', runs=2, runner=runner)['results'][0]
        self.assertEqual(row['trigger_rate'], 1.0)
        self.assertEqual(row['valid_runs'], 1)
        self.assertEqual(row['error_runs'], 1)
        self.assertIsNone(row['pass'])

    def test_timeout_is_explicit(self):
        def timeout(*args):
            raise subprocess.TimeoutExpired('synthetic', 1)
        row = trigger_eval.evaluate(CASES[:1], 'probe', 'description', runner=timeout)['results'][0]
        self.assertEqual(row['attempts'][0]['status'], 'timeout')
        self.assertIsNone(row['pass'])

    def test_valid_positive_and_negative_results(self):
        result = trigger_eval.evaluate(CASES, 'probe', 'description', runner=lambda query, *args: query == CASES[0]['query'])
        self.assertEqual(result['summary']['passed'], 2)
        self.assertEqual(result['summary']['execution_errors'], 0)

    def test_invalid_cases_fail_before_any_run(self):
        runner = unittest.mock.Mock()
        for cases in ([], CASES + CASES[:1], [{'query': 'x', 'should_trigger': 'false'}]):
            with self.subTest(cases=cases), self.assertRaises(ValueError):
                trigger_eval.evaluate(cases, 'probe', 'description', runner=runner)
        runner.assert_not_called()

    def test_non_boolean_probe_is_an_error(self):
        row = trigger_eval.evaluate(CASES[:1], 'probe', 'description', runner=lambda *args: None)['results'][0]
        self.assertIsNone(row['pass'])
        self.assertEqual(row['error_runs'], 1)

    def test_preview_creates_no_result_or_model_process(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'SKILL.md').write_text('---\nname: probe\ndescription: Useful probe\n---\n')
            cases = root / 'cases.json'
            cases.write_text(json.dumps(CASES))
            output = root / 'output.json'
            result = subprocess.run([sys.executable, str(HERE / 'trigger_eval.py'), '--skill-path', str(root), '--cases', str(cases), '--runs', '2', '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['calls'], 4)
            self.assertEqual(json.loads(result.stdout)['status'], 'preview-only')
            self.assertFalse(output.exists())

    def test_probe_sandbox_project_path_and_empty_output(self):
        captured = {}
        def fake(command, **kwargs):
            root = Path(command[command.index('-C') + 1])
            captured['root'] = root
            captured['command'] = command
            text = (root / '.agents/skills/probe/SKILL.md').read_text()
            marker = re.search(r'__SKILL_CREATOR_[a-f0-9]+__', text).group()
            Path(command[command.index('-o') + 1]).write_text(marker)
            return subprocess.CompletedProcess(command, 0, '', '')
        with patch('model_runner.shutil.which', return_value='codex'), patch('model_runner.subprocess.run', side_effect=fake):
            self.assertTrue(model_runner.probe('query', 'probe', 'description', 2))
        command = captured['command']
        self.assertEqual(command[command.index('--sandbox') + 1], 'read-only')
        self.assertIn('--ephemeral', command)
        self.assertNotIn('--model', command)
        self.assertFalse(captured['root'].exists())
        with patch('model_runner.shutil.which', return_value='codex'), patch('model_runner.subprocess.run', return_value=subprocess.CompletedProcess([], 0, '', '')):
            with self.assertRaisesRegex(RuntimeError, 'no final response'):
                model_runner.probe('query', 'probe', 'description', 2)

    def test_failed_task_and_unknown_measurements_remain_unknown(self):
        data = {'kind': 'task-comparison', 'runs': [run_row(), {'case_id': 'one', 'variant': 'baseline', 'run_id': '1', 'status': 'timeout', 'error': 'Timed out'}]}
        result = summarize(data)
        self.assertEqual(result['variants']['baseline']['execution_errors'], 1)
        self.assertIsNone(result['variants']['baseline']['pass_rate'])
        self.assertIsNone(result['variants']['candidate']['mean_tokens'])
        self.assertIsNone(result['comparison']['paired_pass_rate_delta'])

    def test_comparison_matches_successful_pairs_and_criteria(self):
        data = {'kind': 'task-comparison', 'runs': [run_row(), run_row('baseline', False)]}
        result = summarize(data)
        self.assertEqual(result['comparison']['matched_pairs'], 1)
        self.assertEqual(result['comparison']['paired_pass_rate_delta'], 1.0)
        data['runs'][1]['expectations'][0]['text'] = 'Different criterion'
        self.assertIsNone(summarize(data)['comparison']['paired_pass_rate_delta'])

    def test_missing_judgments_duplicates_and_invalid_metrics_rejected(self):
        for rows in ([run_row(), run_row()], [run_row(expectations=[])], [run_row(tokens=float('nan'))]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                summarize({'kind': 'task-comparison', 'runs': rows})

    def test_measurements_are_actual_samples(self):
        result = summarize({'kind': 'task-comparison', 'runs': [run_row(seconds=2.5, tokens=12), run_row('baseline')]})
        self.assertEqual(result['variants']['candidate']['mean_tokens'], 12)
        self.assertEqual(result['variants']['candidate']['seconds_samples'], 1)
        self.assertEqual(result['variants']['baseline']['token_samples'], 0)

    def test_report_escapes_output_and_shows_failure(self):
        data = {'kind': 'task-comparison', 'runs': [run_row(output='</pre><script>bad()</script>'), {'case_id': 'one', 'variant': 'baseline', 'run_id': '1', 'status': 'error', 'error': 'Execution failed'}]}
        document = render(data)
        self.assertNotIn('<script>bad()', document)
        self.assertIn('&lt;script&gt;bad()', document)
        self.assertIn('Execution failed', document)
        self.assertIn('generate-feedback', document)

    def test_incomplete_trigger_cannot_be_reviewed_as_passed(self):
        data = {'kind': 'trigger-probe', 'results': [{'query': 'q', 'status': 'incomplete', 'pass': True}]}
        with self.assertRaises(ValueError):
            render(data)

    def test_review_cli_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            records = root / 'results.json'
            records.write_text(json.dumps({'kind': 'task-comparison', 'runs': [run_row(), run_row('baseline', False)]}))
            output = root / 'review.html'
            command = [sys.executable, str(HERE / 'review_report.py'), '--results', str(records), '--output', str(output)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            output.write_text('User feedback must remain')
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
            self.assertEqual(output.read_text(), 'User feedback must remain')


if __name__ == '__main__':
    unittest.main()
