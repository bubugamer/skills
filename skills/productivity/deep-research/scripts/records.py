#!/usr/bin/env python3
"""Optional source/excerpt ledger. Validates records, never factual support."""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import sys


def require_text(record, key):
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{key} must be nonempty text')
    return value


def identity(record):
    kind = record.get('kind')
    if kind == 'source':
        allowed = {'kind', 'title', 'location', 'retrieved_at', 'id'}
        require_text(record, 'title')
        location = require_text(record, 'location')
        stamp = require_text(record, 'retrieved_at')
        if date.fromisoformat(stamp).isoformat() != stamp:
            raise ValueError('retrieved_at must be YYYY-MM-DD')
        parts = [kind, location]
    elif kind == 'evidence':
        allowed = {'kind', 'source_id', 'quote', 'locator', 'note', 'id'}
        parts = [kind, *(require_text(record, k) for k in ('source_id', 'quote', 'locator'))]
        if 'note' in record and not isinstance(record['note'], str):
            raise ValueError('note must be text')
    else:
        raise ValueError('kind must be source or evidence')
    if set(record) - allowed:
        raise ValueError('unknown fields: ' + ', '.join(sorted(set(record) - allowed)))
    digest = hashlib.sha256(json.dumps(parts, ensure_ascii=False).encode()).hexdigest()
    return kind + '-' + digest[:24]


def load(path):
    if path.is_symlink():
        raise ValueError('ledger must not be a symlink')
    sources, records = set(), {}
    if not path.exists():
        return records
    for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError('record must be an object')
            key = identity(record)
            if record.get('id') != key or key in records:
                raise ValueError('incorrect or duplicate id')
            if record['kind'] == 'source':
                sources.add(key)
            elif record['source_id'] not in sources:
                raise ValueError('evidence references an unregistered source')
            records[key] = record
        except (ValueError, TypeError) as exc:
            raise ValueError(f'line {number}: {exc}') from exc
    return records


def add(path, record):
    if not isinstance(record, dict):
        raise ValueError('record must be an object')
    key = identity(record)
    if 'id' in record and record['id'] != key:
        raise ValueError('supplied id does not match record identity')
    records = load(path)
    if key in records:
        return {'status': 'duplicate', 'id': key}
    if record['kind'] == 'evidence':
        source = records.get(record['source_id'], {})
        if source.get('kind') != 'source':
            raise ValueError('evidence references an unregistered source')
    output = {**record, 'id': key}
    # Single writer: validate first, then append without rewriting prior records.
    prefix = ''
    if path.exists() and path.stat().st_size:
        with path.open('rb') as existing:
            existing.seek(-1, 2)
            if existing.read(1) != b'\n':
                prefix = '\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as stream:
        stream.write(prefix + json.dumps(output, ensure_ascii=False) + '\n')
    return {'status': 'added', 'id': key}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    add_parser = sub.add_parser('add')
    add_parser.add_argument('--ledger', required=True, type=Path)
    add_parser.add_argument('--record', required=True, type=Path)
    check_parser = sub.add_parser('check')
    check_parser.add_argument('--ledger', required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'add':
            result = add(args.ledger, json.loads(args.record.read_text(encoding='utf-8')))
        else:
            if not args.ledger.is_file():
                raise ValueError('ledger does not exist')
            records = load(args.ledger)
            result = {'status': 'valid-records', 'sources': sum(r['kind'] == 'source' for r in records.values()),
                      'excerpts': sum(r['kind'] == 'evidence' for r in records.values())}
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
