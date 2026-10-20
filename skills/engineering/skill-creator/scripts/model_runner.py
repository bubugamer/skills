#!/usr/bin/env python3
"""Optional Codex trigger probe. No model call occurs on import."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import uuid
import yaml


def read_skill(path):
    content = (path / 'SKILL.md').read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---(?:\n|$)', content, re.S)
    if not match:
        raise ValueError('missing skill frontmatter')
    data = yaml.safe_load(match[1])
    if not isinstance(data, dict):
        raise ValueError('frontmatter must be an object')
    name, description = data.get('name'), data.get('description')
    if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError('invalid skill name')
    if not isinstance(description, str) or not description.strip():
        raise ValueError('missing skill description')
    return name, description


def probe(query, name, description, timeout, model=None):
    if shutil.which('codex') is None:
        raise RuntimeError('Codex CLI is unavailable')
    marker = '__SKILL_CREATOR_' + uuid.uuid4().hex + '__'
    with tempfile.TemporaryDirectory(prefix='skill-creator-probe-') as folder:
        root = Path(folder)
        skill = root / '.agents/skills' / name
        skill.mkdir(parents=True)
        frontmatter = yaml.safe_dump({'name': name, 'description': description}, allow_unicode=True, sort_keys=False)
        (skill / 'SKILL.md').write_text('---\n' + frontmatter + '---\n\nThis is a trigger probe. If you read it, reply with exactly ' + marker + '. Do not run other tools.\n', encoding='utf-8')
        output = root / 'last-message.txt'
        command = ['codex', 'exec', '--skip-git-repo-check', '--ephemeral', '--color', 'never',
                   '--sandbox', 'read-only', '-C', str(root), '-o', str(output)]
        if model:
            command.extend(['--model', model])
        command.append('-')
        result = subprocess.run(command, input=query, text=True, capture_output=True, timeout=timeout)
        if result.returncode:
            raise RuntimeError(f'Codex exited {result.returncode}: {(result.stderr or result.stdout).strip()}')
        final = output.read_text(encoding='utf-8').strip() if output.exists() else ''
        if not final:
            raise RuntimeError('Codex returned no final response')
        return marker in final
