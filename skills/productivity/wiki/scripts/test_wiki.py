#!/usr/bin/env python3
"""File-based regressions for wiki inspection; never touch a personal wiki."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('lint_wiki.py')


class WikiChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='wiki-check-')
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.root = self.project / 'docs'
        self.root.mkdir()

    def write(self, path, text):
        dest = self.root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text)
        return dest

    def content(self, body='', extra=''):
        return '---\ntitle: Guide\ncreated: 2020-01-01\nlast_updated: 2020-01-01\nstatus: 草稿\nsources:\n  - https://example.org/source\n' + extra + '---\n' + body

    def run_check(self, *args, expected=0):
        before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in self.project.rglob('*') if p.is_file()}
        result = subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root), '--json', *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        after = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in self.project.rglob('*') if p.is_file()}
        self.assertEqual(before, after, 'Inspection changed project files')
        return report

    def test_empty_json(self):
        report = self.run_check()
        self.assertEqual(report['summary']['scanned_pages'], 0)
        self.assertEqual(report['broken_links'], [])

    def test_markdown_and_wiki_missing(self):
        self.write('index.md', '[Guide](guide.md)')
        self.write('guide.md', self.content('[missing](missing.md)\n[[also-missing|alias]]'))
        report = self.run_check('--wikilinks', expected=1)
        self.assertEqual({x['target'] for x in report['broken_links']}, {'missing.md', 'also-missing'})

    def test_yaml_and_roles(self):
        self.write('index.md', '[Topic](topic.md)')
        self.write('topic.md', '---\ntype: topic\n---\n[Guide](guide.md)')
        self.write('guide.md', self.content())
        self.write('log.md', '# Activity log')
        report = self.run_check('--home-scope', 'topics')
        self.assertEqual(report['missing_sources'], [])
        self.assertEqual(report['summary']['content_pages'], 1)
        self.assertEqual(report['orphans'], [])

    def test_full_navigation_and_custom_yaml_tags(self):
        self.test_yaml_and_roles()
        config = self.project / 'mkdocs.yml'
        config.write_text('docs_dir: docs\ntheme:\n  custom: !!python/name:unused.symbol\nnav:\n  - Home: index.md\n  - Topic:\n      - Overview: topic.md\n      - Guide: guide.md\n')
        before = config.read_bytes()
        report = self.run_check('--nav', '../mkdocs.yml', '--home-scope', 'topics')
        self.assertEqual(report['navigation'], [])
        self.assertEqual(config.read_bytes(), before)

    def test_nested_home_and_exact_navigation_paths(self):
        self.write('portal/home.md', '[Topic](../topic.md)')
        self.write('topic.md', '---\ntype: topic\n---\n[A](a/guide.md)\n[B](b/guide.md)')
        self.write('a/guide.md', self.content())
        self.write('b/guide.md', self.content())
        (self.project / 'mkdocs.yml').write_text('docs_dir: docs\nnav:\n  - Home: portal/home.md\n  - Topic: topic.md\n  - A: a/guide.md\n')
        report = self.run_check('--home', 'portal/home.md', '--nav', '../mkdocs.yml', expected=1)
        self.assertEqual([x['page'] for x in report['navigation']], ['b/guide.md'])

    def test_heading_and_reference_links(self):
        self.write('index.md', '[Guide][g]\n[g]: <guide.md#定义> "title"\n[bad](guide.md#missing)')
        self.write('guide.md', self.content('# 定义\n'))
        report = self.run_check(expected=1)
        self.assertEqual(len(report['broken_links']), 1)
        self.assertIn('#missing', report['broken_links'][0]['target'])

    def test_alias_and_ambiguous_wiki_links(self):
        self.write('index.md', '[[guide|Alias]]\n[[a/guide#机制|Specific]]')
        self.write('a/guide.md', self.content('# 机制'))
        self.write('b/guide.md', self.content())
        report = self.run_check('--wikilinks', expected=1)
        self.assertEqual(len(report['broken_links']), 1)
        self.assertEqual(len(report['broken_links'][0]['candidates']), 2)

    def test_code_and_comments_not_links(self):
        self.write('index.md', '[Guide](guide.md)\n```md\n[missing](missing.md)\n```\n`[[missing2]]`\n<!-- [x](missing3.md) -->')
        self.write('guide.md', self.content())
        report = self.run_check('--wikilinks')
        self.assertEqual(report['broken_links'], [])

    def test_parentheses_and_encoded_path(self):
        self.write('index.md', '[v2](design(v2).md)\n[space](space%20name.md)\n![asset](image.png)')
        self.write('design(v2).md', self.content())
        self.write('space name.md', self.content())
        self.write('image.png', 'representative asset')
        self.assertEqual(self.run_check()['broken_links'], [])

    def test_configured_dates_are_review_only(self):
        self.write('index.md', '[Guide](guide.md)')
        self.write('guide.md', self.content())
        self.assertEqual(self.run_check()['review_candidates'], [])
        report = self.run_check('--today', '2026-10-16', '--review-after-days', '180', '--draft-after-days', '30')
        self.assertEqual(len(report['review_candidates']), 2)
        self.assertTrue(all(x['age_days'] > 30 for x in report['review_candidates']))

    def test_unreachable_and_weakly_linked_separate(self):
        self.write('index.md', '[Guide](guide.md)')
        self.write('guide.md', self.content())
        self.write('lonely.md', self.content())
        report = self.run_check()
        self.assertEqual([x['page'] for x in report['orphans']], ['lonely.md'])
        self.assertEqual([x['page'] for x in report['weakly_linked']], ['guide.md'])

    def test_site_config_missing_target_and_duplicate(self):
        self.write('index.md', '[Guide](guide.md)')
        self.write('guide.md', self.content())
        (self.project / 'mkdocs.yml').write_text('nav:\n  - Home: index.md\n  - Guide: guide.md\n  - Again: guide.md\n  - Missing: missing.md\n')
        report = self.run_check('--nav', '../mkdocs.yml', expected=1)
        self.assertEqual(report['broken_links'][0]['target'], 'missing.md')
        self.assertEqual(report['navigation'][0]['page'], 'guide.md')

    def test_invalid_frontmatter_and_config_json(self):
        self.write('index.md', 'Home')
        self.write('bad.md', '---\nsources: [broken\n---\nText')
        report = self.run_check(expected=2)
        self.assertEqual(report['errors'][0]['page'], 'bad.md')
        (self.root / 'bad.md').unlink()
        (self.project / 'mkdocs.yml').write_text('nav: [invalid')
        report = self.run_check('--nav', '../mkdocs.yml', expected=2)
        self.assertEqual(len(report['errors']), 1)

    def test_scope_and_symlink(self):
        self.write('index.md', 'Home')
        external = self.project / 'outside.md'
        external.write_text('[not-scanned](missing.md)')
        (self.root / 'linked.md').symlink_to(external)
        report = self.run_check()
        self.assertEqual(report['summary']['scanned_pages'], 1)
        self.assertEqual(len(report['unverified']), 1)
        report = self.run_check('--home', '../outside.md', expected=2)
        self.assertTrue(report['errors'])

    def test_exclusions_and_unknown_wiki_syntax(self):
        self.write('index.md', '[[guide]]')
        self.write('guide.md', self.content())
        self.write('archive/old.md', '[missing](missing.md)')
        report = self.run_check('--exclude', 'archive')
        self.assertEqual(report['summary']['scanned_pages'], 2)
        self.assertEqual(len(report['unverified']), 1)

    def test_plain_home_without_mkdocs(self):
        self.write('index.md', '[Guide](guide.md)')
        self.write('guide.md', self.content('<!-- status: 待核验 -->\nPending check.'))
        report = self.run_check()
        self.assertEqual(report['navigation'], [])
        self.assertEqual(len(report['review_candidates']), 1)


if __name__ == '__main__':
    unittest.main()
