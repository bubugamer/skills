#!/usr/bin/env python3
"""Check the pinned gstack runtime or run one supplied shell block in its environment."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

SKILL = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = Path.home() / '.codex/skill-runtimes/plan-eng-review.json'


def verify(config, spec):
    root = Path(config['runtime_root']).expanduser().resolve(strict=True)
    state = Path(config['state_root']).expanduser().resolve()
    bun = Path(config['bun_path']).expanduser().resolve(strict=True)
    if state == root or root in state.parents:
        raise ValueError('Keep mutable state outside the pinned upstream checkout.')
    commit = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True, stderr=subprocess.PIPE).strip()
    if commit != spec['upstream_commit']:
        raise ValueError('Upstream revision differs from the approved snapshot.')
    for relative in spec['required_files']:
        path = (root / relative).resolve(strict=True)
        if root not in path.parents or not path.is_file():
            raise ValueError('Missing or external runtime file: ' + relative)
    for relative, expected in spec['normalized_sha256'].items():
        path = (root / relative).resolve(strict=True)
        if root not in path.parents:
            raise ValueError('Document escapes runtime: ' + relative)
        normalized = path.read_text()
        aliases = {str(root), str(Path(config['runtime_root']).expanduser())}
        for alias in sorted(aliases, key=len, reverse=True):
            normalized = normalized.replace(alias, '<GSTACK_RUNTIME>')
        if hashlib.sha256(normalized.encode()).hexdigest() != expected:
            raise ValueError('Pinned document changed: ' + relative)
    version = subprocess.check_output([str(bun), '--version'], text=True, stderr=subprocess.PIPE).strip()
    if version != spec['bun_version']:
        raise ValueError('Expected Bun ' + spec['bun_version'] + '; found ' + version)
    return {
        'status': 'ready', 'upstream_commit': commit, 'bun_version': version,
        'runtime_root': str(root), 'state_root': str(state), 'bun_path': str(bun),
        'entrypoint': str(root / spec['entrypoint']),
        'preamble': str(root / spec['preamble']),
    }


def environment(info):
    env = os.environ.copy()
    env.update({
        'PATH': str(Path(info['bun_path']).parent) + os.pathsep + env.get('PATH', ''),
        'GSTACK_ROOT': info['runtime_root'], 'GSTACK_INSTALL_DIR': info['runtime_root'],
        'GSTACK_DIR': info['runtime_root'], 'GSTACK_BIN': str(Path(info['runtime_root']) / 'bin'),
        'GSTACK_HOME': info['state_root'], 'GSTACK_STATE_ROOT': info['state_root'],
        'GSTACK_ACTIVE_HOST': 'codex',
    })
    return env


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'shell'])
    parser.add_argument('--config', type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args()
    try:
        config = json.loads(args.config.expanduser().read_text())
        spec = json.loads((SKILL / 'references/runtime-spec.json').read_text())
        info = verify(config, spec)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print('Runtime unavailable: ' + str(exc) + '. See references/runtime.md.', file=sys.stderr)
        return 2
    if args.command == 'check':
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 0
    block = sys.stdin.read()
    if not block.strip():
        parser.error('shell requires a shell block on standard input')
    return subprocess.run(['bash'], input=block, text=True, env=environment(info)).returncode


if __name__ == '__main__':
    raise SystemExit(main())
