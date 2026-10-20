#!/usr/bin/env python3
"""Summarize real task records, preserving failures and unknown measurements."""
import argparse
import json
import math
from pathlib import Path
import statistics
import sys


def summarize(data, candidate='candidate', baseline='baseline'):
    if not isinstance(data, dict) or data.get('kind') != 'task-comparison' or not isinstance(data.get('runs'), list) or not data['runs']:
        raise ValueError('expected nonempty task-comparison runs')
    if candidate == baseline:
        raise ValueError('candidate and baseline must differ')
    seen, variants, matched = set(), {}, {}
    for row in data['runs']:
        if not isinstance(row, dict):
            raise ValueError('run must be an object')
        for field in ('case_id', 'variant', 'run_id'):
            if not isinstance(row.get(field), str) or not row[field]:
                raise ValueError(f'{field} must be nonempty text')
        identity = (row['case_id'], row['variant'], row['run_id'])
        if identity in seen:
            raise ValueError('duplicate run identity')
        seen.add(identity)
        if row.get('status') not in ('ok', 'error', 'timeout'):
            raise ValueError('unknown execution status')
        for field in ('seconds', 'tokens'):
            value = row.get(field)
            if value is not None and (type(value) not in (int, float) or not math.isfinite(value) or value < 0):
                raise ValueError(f'{field} must be a measured nonnegative number or omitted')
        group = variants.setdefault(row['variant'], {'completed': 0, 'errors': 0, 'pass_rates': [], 'seconds': [], 'tokens': []})
        if row['status'] != 'ok':
            if not isinstance(row.get('error'), str) or not row['error'].strip():
                raise ValueError('failed execution requires error detail')
            group['errors'] += 1
            continue
        expectations = row.get('expectations')
        if not isinstance(expectations, list) or not expectations:
            raise ValueError('successful execution requires judgments')
        criteria = []
        for item in expectations:
            if not isinstance(item, dict) or type(item.get('passed')) is not bool or not isinstance(item.get('text'), str) or not item['text'].strip() or not isinstance(item.get('evidence'), str) or not item['evidence'].strip():
                raise ValueError('each judgment requires text, Boolean passed, and evidence')
            criteria.append(item['text'])
        if len(set(criteria)) != len(criteria):
            raise ValueError('duplicate judgment criteria')
        rate = sum(e['passed'] for e in expectations) / len(expectations)
        group['completed'] += 1
        group['pass_rates'].append(rate)
        for field in ('seconds', 'tokens'):
            if row.get(field) is not None:
                group[field].append(row[field])
        matched[(row['case_id'], row['run_id'], row['variant'])] = (dict((e['text'], e['passed']) for e in expectations), rate)
    summary = {}
    for variant, group in variants.items():
        summary[variant] = {'completed': group['completed'], 'execution_errors': group['errors'],
                            'pass_rate': statistics.mean(group['pass_rates']) if group['pass_rates'] else None,
                            'mean_seconds': statistics.mean(group['seconds']) if group['seconds'] else None,
                            'seconds_samples': len(group['seconds']),
                            'mean_tokens': statistics.mean(group['tokens']) if group['tokens'] else None,
                            'token_samples': len(group['tokens'])}
    pairs, missing = [], []
    keys = sorted({(r['case_id'], r['run_id']) for r in data['runs'] if r['variant'] in (candidate, baseline)})
    for case, run in keys:
        a, b = matched.get((case, run, candidate)), matched.get((case, run, baseline))
        if a is None or b is None or set(a[0]) != set(b[0]):
            missing.append({'case_id': case, 'run_id': run})
        else:
            pairs.append(a[1] - b[1])
    return {'kind': 'task-summary', 'variants': summary,
            'comparison': {'candidate': candidate, 'baseline': baseline, 'matched_pairs': len(pairs),
                           'unmatched_or_invalid': missing,
                           'paired_pass_rate_delta': statistics.mean(pairs) if pairs else None}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', required=True, type=Path)
    parser.add_argument('--candidate', default='candidate')
    parser.add_argument('--baseline', default='baseline')
    args = parser.parse_args()
    try:
        print(json.dumps(summarize(json.loads(args.results.read_text(encoding='utf-8')), args.candidate, args.baseline), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
