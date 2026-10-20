#!/usr/bin/env python3
"""Exercise safe installation and file inspection on disposable real files."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def run(script, *args, expected=0):
    result = subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True, text=True)
    assert result.returncode == expected, (result.returncode, result.stdout, result.stderr)
    return result.stdout


def main():
    installer = ROOT / 'scripts/install.py'
    assert not (ROOT / 'skills/in-progress').exists(), 'Removed skill category must stay absent'
    assert not (ROOT / 'docs/in-progress').exists(), 'Removed usage category must stay absent'
    with tempfile.TemporaryDirectory(prefix='personal-skills-check-') as temporary:
        base = Path(temporary)
        admission_copy = base / 'admission-check'
        shutil.copytree(ROOT, admission_copy, ignore=shutil.ignore_patterns('.git', '__pycache__', '.venv', '.DS_Store'))
        approval_catalog = json.loads((admission_copy / 'catalog.json').read_text())
        for source in ['new', 'local-customization', 'upstream-adapted']:
            for release in [True, False]:
                candidate_catalog = json.loads(json.dumps(approval_catalog))
                candidate = next(row for row in candidate_catalog['skills'] if row['name'] == 'ask-skills')
                candidate['source'] = source
                candidate['release'] = release
                candidate.pop('review')
                (admission_copy / 'catalog.json').write_text(json.dumps(candidate_catalog))
                output = run(admission_copy / 'scripts/validate.py', expected=1)
                assert 'ask-skills: explicit user approval' in output, 'Every source type must require approval, even when not released'
                blocked_target = base / ('unapproved-' + source + '-' + str(release))
                run(admission_copy / 'scripts/install.py', '--target', blocked_target, '--skill', 'ask-skills', '--apply', expected=2)
                assert not blocked_target.exists(), 'Unapproved source must not be installed'
                run(admission_copy / 'scripts/sync_catalog.py')
                blocked_manifest = json.loads((admission_copy / '.codex-plugin/plugin.json').read_text())
                assert './skills/productivity/ask-skills' not in blocked_manifest['skills']
        for missing in ['approval_basis', 'audit']:
            incomplete_catalog = json.loads(json.dumps(approval_catalog))
            candidate = next(row for row in incomplete_catalog['skills'] if row['name'] == 'ask-skills')
            candidate['review'].pop(missing)
            (admission_copy / 'catalog.json').write_text(json.dumps(incomplete_catalog))
            output = run(admission_copy / 'scripts/validate.py', expected=1)
            assert 'ask-skills: explicit user approval' in output
            blocked_target = base / ('incomplete-approval-' + missing)
            run(admission_copy / 'scripts/install.py', '--target', blocked_target, '--skill', 'ask-skills', '--apply', expected=2)
            assert not blocked_target.exists()
        target = base / 'installed'
        output = run(installer, '--target', target)
        assert 'Preview only' in output and not target.exists(), 'Preview must not create directories'
        run(installer, '--target', target, '--apply')
        formal = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())['skills']
        assert len(list(target.iterdir())) == len(formal)
        for entry in target.iterdir():
            assert entry.is_symlink() and (entry / 'SKILL.md').is_file()
            assert 'in-progress' not in str(entry.resolve())
        assert (target / 'ask-skills').is_symlink(), 'Explicitly approved ask-skills remains available'
        assert yaml.safe_load((target / 'ask-skills/agents/openai.yaml').read_text())['policy']['allow_implicit_invocation'] is False
        again = run(installer, '--target', target, '--apply')
        assert 'Created 0 links' in again
        conflict = base / 'conflict'
        (conflict / 'read').mkdir(parents=True)
        sentinel = conflict / 'read/keep.txt'
        sentinel.write_text('User-owned content must survive.')
        output = run(installer, '--target', conflict, '--apply', expected=2)
        assert sentinel.read_text() == 'User-owned content must survive.'
        assert sorted(p.name for p in conflict.iterdir()) == ['read'], 'Preflight must prevent partial installation'
        assert 'No changes made' in output
        for legacy_name in ['TangMonk', 'tang-monk']:
            aliases = base / ('aliases-' + legacy_name)
            (aliases / legacy_name).mkdir(parents=True)
            old_reminder = aliases / legacy_name / 'keep.txt'
            old_reminder.write_text('Preserve the old reminder installation.')
            run(installer, '--target', aliases, '--skill', 'remind', '--apply', expected=2)
            assert old_reminder.read_text() == 'Preserve the old reminder installation.'
            assert not (aliases / 'remind').exists()
        reminder_target = base / 'reminder-only'
        run(installer, '--target', reminder_target, '--skill', 'remind', '--apply')
        assert (reminder_target / 'remind').resolve() == ROOT / 'skills/productivity/remind'
        reminder_entry = (reminder_target / 'remind/SKILL.md').read_text()
        assert reminder_entry.startswith('---\nname: remind\n')
        assert '# remind\n' in reminder_entry
        reminder_policy = yaml.safe_load((reminder_target / 'remind/agents/openai.yaml').read_text())['policy']
        assert reminder_policy['allow_implicit_invocation'] is True
        reading_aliases = base / 'reading-aliases'
        (reading_aliases / 'dongnaojin-yeye').mkdir(parents=True)
        old_read = reading_aliases / 'dongnaojin-yeye/keep.txt'
        old_read.write_text('Preserve the old reading installation.')
        run(installer, '--target', reading_aliases, '--skill', 'read', '--apply', expected=2)
        assert old_read.read_text() == 'Preserve the old reading installation.'
        assert not (reading_aliases / 'read').exists()
        para_aliases = base / 'para-aliases'
        (para_aliases / 'konmari').mkdir(parents=True)
        old_para = para_aliases / 'konmari/keep.txt'
        old_para.write_text('Preserve the old PARA installation.')
        run(installer, '--target', para_aliases, '--skill', 'para', '--apply', expected=2)
        assert old_para.read_text() == 'Preserve the old PARA installation.'
        assert not (para_aliases / 'para').exists()
        selected = base / 'selected'
        run(installer, '--target', selected, '--skill', 'teach', '--apply')
        assert (selected / 'teach').resolve() == ROOT / 'skills/productivity/teach'
        for name in ['teach']:
            policy = yaml.safe_load((selected / name / 'agents/openai.yaml').read_text())['policy']
            assert policy['allow_implicit_invocation'] is False, 'Classification must preserve manual invocation'
        for name in ['domain-modeling', 'diagnosing-bugs', 'grilling', 'writing-for-agents']:
            candidate_target = base / ('candidate-' + name)
            run(installer, '--target', candidate_target, '--skill', name, '--apply', expected=2)
            assert not candidate_target.exists(), 'Unapproved candidate must not be installed'
        wiki_aliases = base / 'wiki-aliases'
        (wiki_aliases / 'llm-wiki').mkdir(parents=True)
        old_wiki = wiki_aliases / 'llm-wiki/keep.txt'
        old_wiki.write_text('Preserve the old wiki installation.')
        run(installer, '--target', wiki_aliases, '--skill', 'wiki', '--apply', expected=2)
        assert old_wiki.read_text() == 'Preserve the old wiki installation.'
        assert not (wiki_aliases / 'wiki').exists()
        wiki_target = base / 'wiki-only'
        run(installer, '--target', wiki_target, '--skill', 'wiki', '--apply')
        assert (wiki_target / 'wiki').resolve() == ROOT / 'skills/productivity/wiki'
        wiki_policy = yaml.safe_load((wiki_target / 'wiki/agents/openai.yaml').read_text())['policy']
        assert wiki_policy['allow_implicit_invocation'] is False
        assert not (wiki_target / 'wiki/references/self-test.md').exists()
        writing_aliases = base / 'writing-aliases'
        (writing_aliases / 'writing-master').mkdir(parents=True)
        old_writing = writing_aliases / 'writing-master/keep.txt'
        old_writing.write_text('Preserve the old writing installation and custom styles.')
        output = run(installer, '--target', writing_aliases, '--skill', 'read', '--skill', 'writing-styles', '--apply', expected=2)
        assert 'No changes made' in output
        assert old_writing.read_text() == 'Preserve the old writing installation and custom styles.'
        assert sorted(p.name for p in writing_aliases.iterdir()) == ['writing-master'], 'Legacy conflict must stop the whole batch'
        writing_target = base / 'writing-only'
        run(installer, '--target', writing_target, '--skill', 'writing-styles', '--apply')
        assert (writing_target / 'writing-styles').resolve() == ROOT / 'skills/productivity/writing-styles'
        writing_policy = yaml.safe_load((writing_target / 'writing-styles/agents/openai.yaml').read_text())['policy']
        assert writing_policy['allow_implicit_invocation'] is True
        for style in ['bbs', 'research-analysis']:
            assert (writing_target / 'writing-styles/references/styles' / (style + '.md')).is_file()
        run(installer, '--target', base / 'retired-writing-name', '--skill', 'writing-master', '--apply', expected=2)
        assert not (base / 'retired-writing-name').exists()
        deepcoffee_target = base / 'deepcoffee-only'
        run(installer, '--target', deepcoffee_target, '--skill', 'deepcoffee-dev', '--apply')
        deepcoffee_link = deepcoffee_target / 'deepcoffee-dev'
        assert deepcoffee_link.resolve() == ROOT / 'skills/engineering/deepcoffee-dev'
        deepcoffee_policy = yaml.safe_load((deepcoffee_link / 'agents/openai.yaml').read_text())['policy']
        assert deepcoffee_policy['allow_implicit_invocation'] is False
        for reference in ['delivery', 'deployment', 'maintenance', 'knowledge', 'operating-rules', 'runtime']:
            assert (deepcoffee_link / 'references' / (reference + '.md')).is_file()
        research_target = base / 'research-only'
        run(installer, '--target', research_target, '--skill', 'deep-research', '--apply')
        research_link = research_target / 'deep-research'
        assert research_link.resolve() == ROOT / 'skills/productivity/deep-research'
        assert yaml.safe_load((research_link / 'agents/openai.yaml').read_text())['policy']['allow_implicit_invocation'] is True
        for reference in ['research-method', 'evidence-records', 'reports']:
            assert (research_link / 'references' / (reference + '.md')).is_file()
        record_input = base / 'research-source.json'
        record_input.write_text(json.dumps({'kind': 'source', 'title': 'Test source', 'location': 'materials/source.md', 'retrieved_at': '2026-10-20'}))
        ledger = base / 'research-output/evidence.jsonl'
        recorded = json.loads(run(research_link / 'scripts/records.py', 'add', '--ledger', ledger, '--record', record_input))
        assert recorded['status'] == 'added'
        record_input.write_text(json.dumps({'kind': 'evidence', 'source_id': recorded['id'], 'quote': 'The service never improved latency.', 'locator': 'Section 2'}))
        run(research_link / 'scripts/records.py', 'add', '--ledger', ledger, '--record', record_input)
        assert json.loads(run(research_link / 'scripts/records.py', 'check', '--ledger', ledger)) == {'status': 'valid-records', 'sources': 1, 'excerpts': 1}
        assert 'never improved' in ledger.read_text()
        foreign_research = base / 'foreign-research/deep-research'
        foreign_research.mkdir(parents=True)
        (foreign_research / 'keep.txt').write_text('Keep the existing third-party installation.')
        run(installer, '--target', foreign_research.parent, '--skill', 'deep-research', '--apply', expected=2)
        assert (foreign_research / 'keep.txt').read_text() == 'Keep the existing third-party installation.'
        assert sorted(p.name for p in foreign_research.iterdir()) == ['keep.txt']
        ui_target = base / 'ui-only'
        run(installer, '--target', ui_target, '--skill', 'ui-ux-pro-max', '--apply')
        ui_link = ui_target / 'ui-ux-pro-max'
        assert ui_link.resolve() == ROOT / 'skills/engineering/ui-ux-pro-max'
        assert yaml.safe_load((ui_link / 'agents/openai.yaml').read_text())['policy']['allow_implicit_invocation'] is True
        for reference in ['personal-design', 'reference-search', 'design-records']:
            assert (ui_link / 'references' / (reference + '.md')).is_file()
        proposed_rules = base / 'proposed-design.md'
        proposed_rules.write_text('# Confirmed design rules\nKeep the page task clear.\n')
        design_target = base / 'design-project/rules.md'
        assert 'Preview only' in run(ui_link / 'scripts/save_rules.py', '--input', proposed_rules, '--target', design_target)
        assert not design_target.parent.exists()
        run(ui_link / 'scripts/save_rules.py', '--input', proposed_rules, '--target', design_target, '--apply')
        design_target.write_text('User-edited confirmed rules.\n')
        run(ui_link / 'scripts/save_rules.py', '--input', proposed_rules, '--target', design_target, '--apply', expected=2)
        assert design_target.read_text() == 'User-edited confirmed rules.\n'
        evaluation_target = base / 'evaluation-only'
        run(installer, '--target', evaluation_target, '--skill', 'skill-creator', '--apply')
        evaluation_link = evaluation_target / 'skill-creator'
        assert evaluation_link.resolve() == ROOT / 'skills/engineering/skill-creator'
        assert yaml.safe_load((evaluation_link / 'agents/openai.yaml').read_text())['policy']['allow_implicit_invocation'] is True
        for reference in ['creation', 'task-comparison', 'trigger-evaluation', 'result-records']:
            assert (evaluation_link / 'references' / (reference + '.md')).is_file()
        assert not list(evaluation_link.rglob('*.skill'))
        trigger_cases = base / 'trigger-cases.json'
        trigger_cases.write_text(json.dumps([{'query': 'compare a skill revision', 'should_trigger': True}]))
        planned = json.loads(run(evaluation_link / 'scripts/trigger_eval.py', '--skill-path', evaluation_link, '--cases', trigger_cases))
        assert planned['status'] == 'preview-only' and planned['calls'] == 1
        former_creator = base / 'former-creator/skill-creator'
        former_creator.mkdir(parents=True)
        (former_creator / 'keep.txt').write_text('Preserve the local creator and its evaluation resources.')
        run(installer, '--target', former_creator.parent, '--skill', 'skill-creator', '--apply', expected=2)
        assert (former_creator / 'keep.txt').read_text() == 'Preserve the local creator and its evaluation resources.'
        assert sorted(p.name for p in former_creator.parent.iterdir()) == ['skill-creator']
        support_target = base / 'social-support'
        run(installer, '--target', support_target, '--skill', 'social-feed', '--apply')
        assert (support_target / 'social-feed').resolve() == ROOT / 'skills/productivity/social-feed'
        support_policy = yaml.safe_load((support_target / 'social-feed/agents/openai.yaml').read_text())['policy']
        assert support_policy['allow_implicit_invocation'] is False, 'Moving a reviewed helper must preserve invocation policy'
        workspace = base / 'workspace'
        workspace.mkdir()
        (workspace / 'a').mkdir()
        (workspace / 'b').mkdir()
        (workspace / 'a/same.txt').write_text('Exactly equal sample data.\n')
        (workspace / 'b/same.txt').write_text('Exactly equal sample data.\n')
        (workspace / 'unique.txt').write_text('Different data.\n')
        before = {str(p.relative_to(workspace)): hashlib.sha256(p.read_bytes()).hexdigest() for p in workspace.rglob('*') if p.is_file()}
        scripts = ROOT / 'skills/productivity/para/scripts'
        for name in ['init_workspace.py', 'scan_inventory.py', 'build_stats.py', 'find_exact_duplicates.py', 'build_review.py']:
            run(scripts / name, '--root', workspace)
        groups = json.loads((workspace / '_catalog/metadata/duplicates/exact_groups.json').read_text())
        assert groups['group_count'] == 1
        assert set(groups['items'][0]['paths']) == {'a/same.txt', 'b/same.txt'}
        summary = json.loads((workspace / '_catalog/metadata/stats/summary.json').read_text())
        assert summary['total_files'] == 3, 'Internal _catalog must not count as content'
        for rel, digest in before.items():
            assert hashlib.sha256((workspace / rel).read_bytes()).hexdigest() == digest, 'Inspection modified user content'
        assert sorted(p.name for p in workspace.iterdir()) == ['_catalog', 'a', 'b', 'unique.txt']
    run(ROOT / 'skills/productivity/para/scripts/test_para.py')
    run(ROOT / 'skills/productivity/wiki/scripts/test_wiki.py')
    run(ROOT / 'skills/productivity/deep-research/scripts/test_records.py')
    run(ROOT / 'skills/engineering/ui-ux-pro-max/scripts/test_tools.py')
    run(ROOT / 'skills/engineering/skill-creator/scripts/test_evaluation.py')
    print('Passed: admission checks across all sources, approved manual ask-skills, safe installation and legacy aliases, preserved invocation policies, reviewed references, research/UI preservation, skill-creator preview and existing-creator conflict protection, candidate exclusions, unchanged user files, 14 PARA, 16 wiki, 9 research-record, 9 UI-adapter and 15 evaluation-tool tests.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
