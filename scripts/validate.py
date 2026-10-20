#!/usr/bin/env python3
"""Check names, references, metadata, origins and explicit release selection."""
import ast
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml
from sync_catalog import ROOT, outputs, is_released, is_adopted, BUCKETS


def main():
    errors = []
    catalog = json.loads((ROOT / 'catalog.json').read_text())
    rows = catalog['skills']
    names = [d['name'] for d in rows]
    if len(names) != len(set(names)):
        errors.append('Duplicate catalog names')
    for retired in [ROOT / 'skills/in-progress', ROOT / 'docs/in-progress']:
        if retired.exists():
            errors.append('Removed category must not be recreated: ' + str(retired.relative_to(ROOT)))
    actual = {str(p.parent.relative_to(ROOT)) for p in ROOT.glob('skills/*/*/SKILL.md')}
    managed = {d['path'] for d in rows if d.get('path')}
    if actual != managed:
        errors.append('Catalog/source mismatch: ' + str(actual ^ managed))
    for d in rows:
        if d['category'] not in BUCKETS:
            errors.append(d['name'] + ': invalid purpose category')
        if 'release' in d and not isinstance(d['release'], bool):
            errors.append(d['name'] + ': release setting must be boolean')
        if d['source'] == 'upstream-adapted' and d.get('review', {}).get('admission_status') != 'user-approved':
            errors.append(d['name'] + ': upstream admission is not user-approved')
        scenarios = d.get('usage_scenarios', [])
        if is_adopted(d) and not scenarios:
            errors.append(d['name'] + ': adopted skill needs usage scenarios')
        if scenarios and not is_adopted(d):
            errors.append(d['name'] + ': public usage scenarios require confirmed adoption')
        if not isinstance(scenarios, list):
            errors.append(d['name'] + ': usage_scenarios must be a list')
        elif any(not isinstance(case, dict) or set(case) != {'situation', 'prompt', 'assistance', 'result'} or any(not isinstance(value, str) or not value.strip() for value in case.values()) for case in scenarios):
            errors.append(d['name'] + ': each usage scenario needs situation, prompt, assistance and result')
        if not d.get('path'):
            continue
        folder = ROOT / d['path']
        text = (folder / 'SKILL.md').read_text()
        match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
        if not match:
            errors.append(d['name'] + ': missing frontmatter')
            continue
        fm = yaml.safe_load(match[1])
        if fm.get('name') != d['name'] or folder.name != d['name'] or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', d['name']) or len(d['name']) > 64:
            errors.append(d['name'] + ': invalid name')
        desc = fm.get('description')
        if not isinstance(desc, str) or not desc.strip() or len(desc) > 1024:
            errors.append(d['name'] + ': invalid description')
        meta = yaml.safe_load((folder / 'agents/openai.yaml').read_text())
        expected = not d.get('manual', False)
        if meta.get('policy', {}).get('allow_implicit_invocation') != expected:
            errors.append(d['name'] + ': inconsistent invocation policy')
        ui = meta['interface']
        if not 25 <= len(ui['short_description']) <= 64 or '$' + d['name'] not in ui['default_prompt']:
            errors.append(d['name'] + ': invalid UI metadata')
        origin = json.loads((folder / 'ORIGIN.json').read_text())
        if origin['source'] != d['source'] or origin['origin'] != d['origin']:
            errors.append(d['name'] + ': inconsistent origin')
        if (d['source'] == 'upstream-adapted' or d['name'] == 'wait-what') and not (folder / 'LICENSE.txt').exists():
            errors.append(d['name'] + ': missing upstream license')
        cases = json.loads((folder / 'evals/evals.json').read_text())
        if cases['skill_name'] != d['name'] or not cases['evals']:
            errors.append(d['name'] + ': missing evaluation cases')
        for dep in d.get('dependencies', []):
            if dep not in names:
                errors.append(d['name'] + ': unknown dependency ' + dep)
    plugin = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
    expected_paths = {'./' + d['path'] for d in rows if is_released(d)}
    if len(plugin['skills']) != len(expected_paths) or set(plugin['skills']) != expected_paths or plugin['version'] != catalog['version']:
        errors.append('Release manifest differs from formal catalog')
    market = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
    if market['plugins'][0]['name'] != plugin['name'] or market['plugins'][0]['source']['path'] != './':
        errors.append('Marketplace does not point at collection')
    if errors:
        print('\n'.join(errors))
        return 1
    for rel, text in outputs().items():
        path = ROOT / rel
        if not path.is_file() or path.read_text() != text:
            errors.append('Stale generated output: ' + rel)
    for path in ROOT.rglob('*'):
        if not path.is_file() or any(x in {'.git', '__pycache__', '.venv', '_catalog'} for x in path.relative_to(ROOT).parts):
            continue
        if path.name in {'.DS_Store', 'auth.json'} or path.name.endswith('.auth-state.json') or path.name.startswith('.env'):
            errors.append('Local runtime/state file: ' + str(path.relative_to(ROOT)))
        if path.suffix not in {'.md', '.py', '.json', '.yaml', '.yml', '.txt', '.sh'}:
            continue
        text = path.read_text()
        if re.search(r'/Users/[A-Za-z0-9_-]+/', text):
            errors.append('Personal absolute path: ' + str(path.relative_to(ROOT)))
        if re.search(r'(?:sk-(?:proj-)?[A-Za-z0-9_-]{25,}|gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----)', text):
            errors.append('Credential-like value: ' + str(path.relative_to(ROOT)))
        if path.suffix == '.py':
            try:
                ast.parse(text, filename=str(path))
            except SyntaxError as exc:
                errors.append(str(exc))
        if path.suffix == '.md':
            # Example paths inside fenced templates refer to the future user's project.
            prose = re.sub(r'^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$', '', text, flags=re.M | re.S)
            for target in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)', prose):
                target = unquote(target.split('#')[0].split(' "')[0])
                if not target or re.match(r'[a-z]+:', target) or '<' in target or '`' in target:
                    continue
                resolved = path.parent / target
                if not resolved.exists():
                    errors.append(str(path.relative_to(ROOT)) + ': missing link ' + target)
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'Validated {len(rows)} catalog entries, {len(managed)} managed skills, {len(expected_paths)} release entries.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
