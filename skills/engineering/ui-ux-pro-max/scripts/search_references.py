#!/usr/bin/env python3
"""Search external UI/UX data through its own engine using validated tables."""
import argparse
import csv
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import tempfile


def load_runtime(root):
    root = root.expanduser().resolve()
    source = root / 'scripts/core.py'
    if not source.is_file() or not (root / 'data').is_dir():
        raise ValueError('runtime requires scripts/core.py and data/')
    spec = importlib.util.spec_from_file_location('_selected_uiux_core', source)
    module = importlib.util.module_from_spec(spec)
    before = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = before
    if not all(hasattr(module, name) for name in ('CSV_CONFIG', 'STACK_CONFIG', 'search', 'search_stack', '_STACK_COLS')):
        raise ValueError('incompatible upstream search interface')
    return root, module


def clean_table(path, required):
    with path.open(newline='', encoding='utf-8-sig') as stream:
        rows = list(csv.reader(stream))
    if not rows or not rows[0] or len(set(rows[0])) != len(rows[0]) or any(not h for h in rows[0]):
        raise ValueError('missing or duplicate CSV headers')
    header = rows[0]
    if not set(required).issubset(header):
        raise ValueError('table is missing required search columns')
    clean, skipped = [], []
    for index, row in enumerate(rows[1:], 1):
        if not row:
            continue
        reason = None
        if len(row) != len(header):
            reason = 'field count mismatch'
        elif any('\x00' in value or re.search(r'[\r\n]\s*\d+,', value) for value in row):
            reason = 'invalid content or embedded CSV record'
        if reason:
            skipped.append({'record': index, 'reason': reason})
        else:
            clean.append(row)
    if not clean:
        raise ValueError('no usable data remains in this table')
    return header, clean, skipped


def inventory(root, module):
    data = root / 'data'
    stacks = {p.stem: {'file': str(p.relative_to(data))} for p in sorted((data / 'stacks').glob('*.csv'))}
    domains = {key: value for key, value in module.CSV_CONFIG.items() if (data / value['file']).is_file()}
    return domains, stacks


def search(root, query, domain=None, stack=None, limit=3):
    root, module = load_runtime(root)
    domains, stacks = inventory(root, module)
    if not query or not query.strip():
        raise ValueError('query must be nonempty')
    if limit < 1:
        raise ValueError('limit must be positive')
    if stack:
        if stack not in stacks:
            raise ValueError('stack is unavailable; choose from: ' + ', '.join(stacks))
        config, required = stacks[stack], module._STACK_COLS['search_cols']
    else:
        domain = domain or 'ux'
        if domain not in domains:
            raise ValueError('domain is unavailable; choose from: ' + ', '.join(domains))
        config, required = domains[domain], domains[domain]['search_cols']
    relative = Path(config['file'])
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('table must use a simple relative runtime path')
    data = (root / 'data').resolve()
    source = (data / relative).resolve()
    if data not in source.parents:
        raise ValueError('table must remain inside the runtime data directory')
    header, rows, skipped = clean_table(source, required)
    with tempfile.TemporaryDirectory(prefix='uiux-table-') as temp:
        module.DATA_DIR = Path(temp)
        target = module.DATA_DIR / config['file']
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.writer(stream)
            writer.writerow(header)
            writer.writerows(rows)
        if stack:
            module.STACK_CONFIG = stacks
            module.AVAILABLE_STACKS = list(stacks)
            result = module.search_stack(query, stack, limit)
        else:
            result = module.search(query, domain, limit)
    if not isinstance(result, dict) or 'error' in result:
        raise ValueError(str(result.get('error', 'unexpected search output')) if isinstance(result, dict) else 'unexpected search output')
    result['data_quality'] = {'usable_records': len(rows), 'skipped_records': skipped,
                              'coverage': 'partial; malformed records excluded' if skipped else 'no structural exclusions'}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?')
    parser.add_argument('--runtime', type=Path, default=os.environ.get('UI_UX_PRO_MAX_RUNTIME'))
    select = parser.add_mutually_exclusive_group()
    select.add_argument('--domain')
    select.add_argument('--stack')
    parser.add_argument('--limit', type=int, default=3)
    parser.add_argument('--list', action='store_true')
    args = parser.parse_args()
    try:
        if not args.runtime:
            raise ValueError('select --runtime or set UI_UX_PRO_MAX_RUNTIME')
        if args.list:
            root, module = load_runtime(args.runtime)
            domains, stacks = inventory(root, module)
            result = {'domains': list(domains), 'stacks': list(stacks)}
        else:
            result = search(args.runtime, args.query, args.domain, args.stack, args.limit)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, csv.Error, ImportError, AttributeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
