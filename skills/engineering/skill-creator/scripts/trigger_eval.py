#!/usr/bin/env python3
"""Preview or run explicitly authorized trigger probes; errors never pass."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import yaml
from model_runner import probe, read_skill


def validate(cases, runs, threshold, timeout):
    if not isinstance(cases, list) or not cases:
        raise ValueError('cases must be a nonempty array')
    seen = set()
    for item in cases:
        if not isinstance(item, dict) or not isinstance(item.get('query'), str) or not item['query'].strip() or type(item.get('should_trigger')) is not bool:
            raise ValueError('each case requires a query and Boolean should_trigger')
        if item['query'] in seen:
            raise ValueError('duplicate query')
        seen.add(item['query'])
    if type(runs) is not int or runs < 1 or timeout <= 0 or not 0 < threshold <= 1:
        raise ValueError('invalid runs, timeout, or threshold')


def evaluate(cases, name, description, runs=1, threshold=0.5, timeout=30, model=None, runner=probe):
    validate(cases, runs, threshold, timeout)
    results = []
    for case in cases:
        attempts, errors, valid = [], [], []
        for index in range(runs):
            try:
                triggered = runner(case['query'], name, description, timeout, model)
                if type(triggered) is not bool:
                    raise ValueError('probe did not return a Boolean result')
                valid.append(triggered)
                attempts.append({'run': index + 1, 'status': 'ok', 'triggered': triggered})
            except Exception as exc:
                status = 'timeout' if isinstance(exc, (subprocess.TimeoutExpired, TimeoutError)) else 'error'
                error = {'run': index + 1, 'status': status, 'error': str(exc)}
                attempts.append(error)
                errors.append(error)
        rate = sum(valid) / len(valid) if valid else None
        passed = None if errors else (rate >= threshold if case['should_trigger'] else rate < threshold)
        results.append({**case, 'attempts': attempts, 'valid_runs': len(valid), 'error_runs': len(errors),
                        'trigger_rate': rate, 'pass': passed, 'status': 'incomplete' if errors else 'complete'})
    return {'kind': 'trigger-probe', 'skill_name': name, 'description': description, 'results': results,
            'summary': {'total': len(results), 'completed': sum(r['status'] == 'complete' for r in results),
                        'incomplete': sum(r['status'] == 'incomplete' for r in results),
                        'passed': sum(r['pass'] is True for r in results),
                        'failed': sum(r['pass'] is False for r in results),
                        'execution_errors': sum(r['error_runs'] for r in results)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill-path', required=True, type=Path)
    parser.add_argument('--cases', required=True, type=Path)
    parser.add_argument('--runs', type=int, default=1)
    parser.add_argument('--threshold', type=float, default=0.5)
    parser.add_argument('--timeout', type=float, default=30)
    parser.add_argument('--model')
    parser.add_argument('--description')
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        cases = json.loads(args.cases.read_text(encoding='utf-8'))
        validate(cases, args.runs, args.threshold, args.timeout)
        name, description = read_skill(args.skill_path)
        if not args.execute:
            print(json.dumps({'status': 'preview-only', 'skill_name': name, 'calls': len(cases) * args.runs,
                              'timeout_per_call': args.timeout, 'model': args.model or 'user-configured'}, ensure_ascii=False))
            return 0
        if args.output and (args.output.exists() or args.output.is_symlink()):
            raise ValueError('output already exists; choose a new result file')
        result = evaluate(cases, name, args.description or description, args.runs, args.threshold, args.timeout, args.model)
        text = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open('x', encoding='utf-8') as stream:
                stream.write(text + '\n')
        print(text)
        return 2 if result['summary']['execution_errors'] else 0
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        print(str(exc), file=sys.stderr)
        return 2



if __name__ == '__main__':
    raise SystemExit(main())
