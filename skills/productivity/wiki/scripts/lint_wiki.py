#!/usr/bin/env python3
"""Inspect Markdown pages and configured navigation without writing files."""
import argparse
from collections import Counter
from datetime import date, datetime
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError:
    print('PyYAML is required; use the project Python environment with PyYAML installed.', file=sys.stderr)
    raise SystemExit(2)


def prose(text):
    """Remove fenced code, inline code and comments before looking for links."""
    lines, fence = [], None
    for line in text.splitlines():
        mark = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if fence:
            if mark and mark[1][0] == fence[0] and len(mark[1]) >= len(fence) and not line[mark.end():].strip():
                fence = None
            lines.append('')
        elif mark:
            fence = mark[1]
            lines.append('')
        else:
            lines.append(line)
    clean = '\n'.join(lines)
    clean = re.sub(r'(`+).*?\1', '', clean, flags=re.S)
    return re.sub(r'<!--.*?-->', '', clean, flags=re.S)


def destination(value):
    value = value.strip()
    if value.startswith('<') and '>' in value:
        return value[1:value.index('>')]
    return re.split(r'\s+(?=[\x22\x27(])', value, maxsplit=1)[0].strip()


def links(body):
    text = prose(body)
    found = [('wiki', m[1].split('|', 1)[0].strip()) for m in re.finditer(r'\[\[([^\]\n]+)\]\]', text)]
    text = re.sub(r'\[\[[^\]\n]+\]\]', '', text)
    definitions = {}
    for m in re.finditer(r'^\s{0,3}\[([^\]\n]+)\]:\s*(.+)$', text, re.M):
        definitions[' '.join(m[1].lower().split())] = destination(m[2])
    text = re.sub(r'^\s{0,3}\[[^\]\n]+\]:.*$', '', text, flags=re.M)
    # Balanced parentheses allow file names such as design(v2).md.
    for m in re.finditer(r'!?\[[^\]\n]*\]\(', text):
        cursor, depth, quoted = m.end(), 1, False
        while cursor < len(text) and depth:
            char = text[cursor]
            if char == '\\':
                cursor += 2
                continue
            if char == '<':
                quoted = True
            elif char == '>':
                quoted = False
            elif not quoted:
                depth += (char == '(') - (char == ')')
            cursor += 1
        if depth == 0:
            found.append(('markdown', destination(text[m.end():cursor - 1])))
    for m in re.finditer(r'!?\[([^\]\n]+)\]\[([^\]\n]*)\]', text):
        key = ' '.join((m[2] or m[1]).lower().split())
        found.append(('markdown', definitions[key]) if key in definitions else ('undefined-reference', key))
    for m in re.finditer(r'(?<![\[])\[([^\[\]\n]+)\](?![\[(])', text):
        key = ' '.join(m[1].lower().split())
        if key in definitions:
            found.append(('markdown', definitions[key]))
    return list(dict.fromkeys(found))


def anchors(body):
    clean = prose(body)
    result = set(re.findall(r'<a\s+[^>]*(?:id|name)=[\x22\x27]([^\x22\x27]+)', clean, flags=re.I))
    counts = Counter()
    for m in re.finditer(r'^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$', clean, re.M):
        heading = m[1]
        explicit = re.search(r'\{#([^} ]+)\}', heading)
        if explicit:
            result.add(explicit[1])
            continue
        heading = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', heading)
        slug = re.sub(r'[^\w\-\s]', '', heading.lower())
        slug = re.sub(r'\s+', '-', slug.strip())
        n = counts[slug]
        counts[slug] += 1
        result.add(slug if not n else slug + '_' + str(n))
        if n:
            result.add(slug + '-' + str(n))
    return result


def load_page(path):
    text = path.read_text(encoding='utf-8')
    match = re.match(r'^---\s*\n(.*?)\n---\s*(?:\n|$)', text, re.S)
    if not match:
        return {}, text
    fm = yaml.safe_load(match[1])
    if fm is None:
        fm = {}
    if not isinstance(fm, dict):
        raise ValueError('Page frontmatter must be a mapping')
    return fm, text[match.end():]


def nav_targets(path, root):
    # Compose nodes only: MkDocs custom tags are not executed or rewritten.
    tree = yaml.compose(path.read_text(encoding='utf-8'), Loader=yaml.SafeLoader)
    if not isinstance(tree, yaml.MappingNode):
        raise ValueError('Site configuration must be a YAML mapping')
    nodes = {key.value: value for key, value in tree.value}
    if 'docs_dir' in nodes:
        node = nodes['docs_dir']
        if node.tag != 'tag:yaml.org,2002:str':
            raise ValueError('Dynamic docs_dir needs explicit project handling')
        if (path.parent / node.value).resolve() != root:
            raise ValueError('Configured docs_dir differs from --root')
    if 'nav' not in nodes:
        raise ValueError('No explicit nav tree; inspect the project navigation method separately')
    found, active = [], set()

    def walk(node):
        if id(node) in active:
            raise ValueError('Recursive navigation alias')
        active.add(id(node))
        if isinstance(node, yaml.SequenceNode):
            for child in node.value:
                walk(child)
        elif isinstance(node, yaml.MappingNode):
            for _, child in node.value:
                walk(child)
        elif node.tag == 'tag:yaml.org,2002:str':
            found.append(node.value)
        else:
            raise ValueError('Unsupported navigation value or custom tag')
        active.remove(id(node))

    walk(nodes['nav'])
    return found


def inspect(args):
    root = args.root.expanduser().resolve()
    report = {key: [] for key in ['errors', 'broken_links', 'navigation', 'missing_sources', 'review_candidates', 'orphans', 'weakly_linked', 'unverified']}
    report['summary'] = {'scanned_pages': 0, 'content_pages': 0, 'external_links_unchecked': 0}
    if not root.is_dir():
        report['errors'].append({'path': str(root), 'detail': 'Page root is not a directory'})
        return report, 2

    def relative(value):
        path = root / value
        if path.is_absolute() and not path.resolve().is_relative_to(root):
            raise ValueError('Page paths must stay within --root: ' + value)
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError('Page paths must stay within --root without symlinks: ' + value)
        return path.resolve().relative_to(root).as_posix()

    home = relative(args.home)
    maintenance = {home, relative(args.log), *map(relative, args.maintenance)}
    topics = set(map(relative, args.topic))
    excluded = [relative(x) for x in args.exclude]
    pages = {}
    for path in sorted(root.rglob('*.md')):
        rel = path.relative_to(root).as_posix()
        if any(part.startswith('.') or part in {'node_modules', '__pycache__'} for part in path.relative_to(root).parts):
            continue
        if any(rel == item or rel.startswith(item.rstrip('/') + '/') for item in excluded):
            continue
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != root):
            report['unverified'].append({'page': rel, 'detail': 'Symlink page not inspected'})
            continue
        try:
            fm, body = load_page(path)
        except (ValueError, yaml.YAMLError, OSError) as exc:
            report['errors'].append({'page': rel, 'detail': str(exc)})
            continue
        role = 'maintenance' if rel in maintenance else ('topic' if rel in topics or fm.get('type') == 'topic' else 'content')
        if role == 'topic':
            topics.add(rel)
        pages[rel] = {'fm': fm, 'body': body, 'role': role}
    report['summary']['scanned_pages'] = len(pages)
    report['summary']['content_pages'] = sum(page['role'] == 'content' for page in pages.values())
    graph = {rel: set() for rel in pages}
    stems = {}
    for rel in pages:
        stems.setdefault(Path(rel).stem, []).append(rel)

    def resolve(source, kind, target):
        item = {'page': source, 'target': target}
        if kind == 'undefined-reference':
            report['broken_links'].append({**item, 'detail': 'Undefined reference label'})
            return None
        if kind == 'wiki' and not args.wikilinks:
            report['unverified'].append({**item, 'detail': 'Wiki-link syntax not enabled for this inspection'})
            return None
        try:
            parts = urlsplit(target)
        except ValueError as exc:
            report['broken_links'].append({**item, 'detail': str(exc)})
            return None
        if parts.scheme or parts.netloc:
            report['summary']['external_links_unchecked'] += 1
            return None
        value, fragment = unquote(parts.path), unquote(parts.fragment)
        if value.startswith('/'):
            report['unverified'].append({**item, 'detail': 'Site-root URL needs renderer-specific resolution'})
            return None
        candidate = root / source if not value else (root / source).parent / value
        choices = [candidate]
        if kind == 'wiki' and value:
            choices += [candidate.with_suffix('.md') if not candidate.suffix else candidate, root / value, root / (value + '.md')]
        if candidate.is_dir():
            choices += [candidate / 'index.md', candidate / 'README.md']
        chosen = next((p for p in choices if p.is_file()), None)
        if chosen is None and kind == 'wiki' and '/' not in value:
            matches = stems.get(Path(value).stem, [])
            if len(matches) > 1:
                report['broken_links'].append({**item, 'detail': 'Ambiguous wiki target', 'candidates': matches})
                return None
            if len(matches) == 1:
                chosen = root / matches[0]
        if chosen is None:
            report['broken_links'].append({**item, 'detail': 'Target does not exist'})
            return None
        if chosen.is_symlink() or not chosen.resolve().is_relative_to(root):
            report['unverified'].append({**item, 'detail': 'Target outside page root or symlink; not inspected'})
            return None
        rel = chosen.resolve().relative_to(root).as_posix()
        if fragment and chosen.suffix == '.md':
            if rel not in pages:
                report['unverified'].append({**item, 'detail': 'Target page excluded or unreadable; anchor not inspected'})
            elif fragment not in anchors(pages[rel]['body']):
                report['broken_links'].append({**item, 'detail': 'Heading or explicit anchor not found; check custom renderer rules if used'})
        return rel

    for rel, page in pages.items():
        for kind, target in links(page['body']):
            resolved = resolve(rel, kind, target)
            if resolved in pages and resolved != rel:
                graph[rel].add(resolved)
        if page['role'] != 'content':
            continue
        sources = page['fm'].get('sources')
        inline_source = any(re.match(r'^https?://', target) for _, target in links(page['body']))
        if not sources and not inline_source:
            report['missing_sources'].append({'page': rel, 'detail': 'No source list or inline web source; review claim type manually'})
        if '<!-- status: 待核验 -->' in page['body']:
            report['review_candidates'].append({'page': rel, 'detail': 'Contains unresolved verification marker'})
        for field, days in [('last_updated', args.review_after_days), ('created', args.draft_after_days if page['fm'].get('status') == '草稿' else None)]:
            if days is None:
                continue
            raw = page['fm'].get(field)
            try:
                value = raw.date() if isinstance(raw, datetime) else (raw if isinstance(raw, date) else date.fromisoformat(str(raw)))
            except (TypeError, ValueError):
                report['review_candidates'].append({'page': rel, 'detail': 'Missing or invalid date for configured review period', 'field': field})
                continue
            age = (args.today - value).days
            if age > days:
                report['review_candidates'].append({'page': rel, 'detail': 'Review period exceeded; not a truth verdict', 'field': field, 'age_days': age})

    entries = {home} & pages.keys()
    if pages and home not in pages:
        report['navigation'].append({'page': home, 'detail': 'Configured home is missing'})
    if args.home_scope != 'none' and home in pages:
        expected = topics if args.home_scope == 'topics' else {rel for rel, p in pages.items() if p['role'] != 'maintenance'}
        for rel in sorted(expected - graph[home]):
            report['navigation'].append({'page': rel, 'detail': 'Missing from configured home scope'})
        if args.home_scope == 'topics':
            for rel in sorted(graph[home] - topics):
                if pages[rel]['role'] == 'content':
                    report['navigation'].append({'page': rel, 'detail': 'Content page listed on topic-only home'})
    if args.nav:
        nav_path = args.nav.expanduser()
        nav_path = (root / nav_path).resolve() if not nav_path.is_absolute() else nav_path.resolve()
        try:
            targets = nav_targets(nav_path, root)
            listed = []
            for target in targets:
                rel = resolve('__site_navigation__.md', 'markdown', target)
                if rel:
                    listed.append(rel)
            for rel, count in Counter(listed).items():
                if count > 1:
                    report['navigation'].append({'page': rel, 'detail': 'Duplicate site navigation entry'})
            needed = {rel for rel, p in pages.items() if p['role'] != 'maintenance'} | ({home} & pages.keys())
            for rel in sorted(needed - set(listed)):
                report['navigation'].append({'page': rel, 'detail': 'Missing from site navigation'})
            entries |= set(listed) & pages.keys()
        except (ValueError, yaml.YAMLError, OSError) as exc:
            report['errors'].append({'path': str(nav_path), 'detail': str(exc)})
    reachable = set(entries)
    pending = list(entries)
    while pending:
        for rel in graph[pending.pop()] - reachable:
            reachable.add(rel)
            pending.append(rel)
    for rel, page in pages.items():
        if page['role'] != 'content':
            continue
        if rel not in reachable:
            report['orphans'].append({'page': rel, 'detail': 'Not reachable from configured entries'})
        elif not any(rel in targets for src, targets in graph.items() if pages[src]['role'] != 'maintenance'):
            report['weakly_linked'].append({'page': rel, 'detail': 'Only home/site entry; no knowledge relationship link'})
    code = 2 if report['errors'] else (1 if report['broken_links'] or report['navigation'] else 0)
    return report, code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True, help='Markdown page directory, not the site project root')
    parser.add_argument('--home', default='index.md', help='Home path relative to --root')
    parser.add_argument('--log', default='log.md', help='Activity log path relative to --root')
    for name in ['topic', 'maintenance', 'exclude']:
        parser.add_argument('--' + name, action='append', default=[], help='Page/directory path relative to --root; repeatable')
    parser.add_argument('--nav', type=Path, help='MkDocs configuration; relative paths resolve from --root')
    parser.add_argument('--home-scope', choices=['none', 'topics', 'all'], default='none')
    parser.add_argument('--wikilinks', action='store_true', help='Check wiki-link syntax when supported by the project')
    parser.add_argument('--review-after-days', type=int)
    parser.add_argument('--draft-after-days', type=int)
    parser.add_argument('--today', type=date.fromisoformat, default=date.today())
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if any(n is not None and n < 0 for n in [args.review_after_days, args.draft_after_days]):
        parser.error('Review periods must be nonnegative')
    try:
        report, code = inspect(args)
    except (ValueError, OSError) as exc:
        report, code = {'errors': [{'detail': str(exc)}]}, 2
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print('Wiki inspection (read-only)')
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
