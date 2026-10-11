#!/usr/bin/env python3
"""Preview or create Codex skill links without replacing existing installations."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, default=Path.home() / '.agents/skills')
    parser.add_argument('--skill', action='append', help='Select one formal skill; may be repeated')
    parser.add_argument('--apply', action='store_true', help='Create links after the full conflict check')
    args = parser.parse_args()
    target = args.target.expanduser().resolve()
    if target == ROOT or ROOT in target.parents:
        parser.error('Install outside the collection source tree.')
    catalog = json.loads((ROOT / 'catalog.json').read_text())['skills']
    available = {d['name']: d for d in catalog if d.get('path') and d['category'] not in ['in-progress', 'deprecated']}
    names = args.skill or list(available)
    unknown = set(names) - set(available)
    if unknown:
        parser.error('Not a formal skill: ' + ', '.join(sorted(unknown)))
    names = list(dict.fromkeys(names))
    defaults = [Path.home() / '.agents/skills', Path.home() / '.codex/skills']
    peers = defaults if target in [p.resolve() for p in defaults] else [target]
    conflicts, pending = [], []
    for name in names:
        d = available[name]
        source = (ROOT / d['path']).resolve()
        if ROOT not in source.parents or not (source / 'SKILL.md').is_file():
            parser.error('Invalid source for ' + name)
        aliases = [name] + ([d['original']] if d.get('original') else [])
        for peer in peers:
            for alias in aliases:
                existing = peer / alias
                if existing.exists() or existing.is_symlink():
                    same_link = existing == target / name and existing.is_symlink() and existing.resolve() == source
                    if not same_link:
                        conflicts.append(str(existing))
        dest = target / name
        if not (dest.is_symlink() and dest.resolve() == source):
            pending.append((source, dest))
    if conflicts:
        print('No changes made. Existing installations conflict:')
        for path in conflicts:
            print(path)
        return 2
    if not args.apply:
        print('Preview only; no files changed.')
        for source, dest in pending:
            print(f'{dest} -> {source}')
        return 0
    created = []
    try:
        target.mkdir(parents=True, exist_ok=True)
        for source, dest in pending:
            dest.symlink_to(source, target_is_directory=True)
            created.append(dest)
    except OSError as exc:
        for path in reversed(created):
            if path.is_symlink() and path.resolve() in [source for source, _ in pending]:
                path.unlink()
        print('Link creation failed; links created in this run rolled back: ' + str(exc))
        return 1
    print(f'Created {len(created)} links; existing matching links left in place.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
