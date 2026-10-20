#!/usr/bin/env python3
"""Preview design-rule differences; create new files without replacing edits."""
import argparse
import difflib
from pathlib import Path
import sys


def save(source, target, apply=False):
    proposed = source.read_text(encoding='utf-8')
    if target.is_symlink():
        raise ValueError('target must not be a symlink')
    existing = target.read_text(encoding='utf-8') if target.exists() else ''
    diff = ''.join(difflib.unified_diff(existing.splitlines(True), proposed.splitlines(True),
                                       fromfile=str(target), tofile='proposed'))
    if not apply:
        return 'Preview only; no files changed.\n' + diff
    if target.exists():
        raise ValueError('Existing file preserved; merge the reviewed differences explicitly.\n' + diff)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(proposed)
    return 'Created: ' + str(target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--target', required=True, type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        print(save(args.input, args.target, args.apply))
        return 0
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
