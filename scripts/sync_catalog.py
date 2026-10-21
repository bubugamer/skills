#!/usr/bin/env python3
"""Generate human navigation and release metadata from the reviewed catalog."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUCKETS = ['engineering', 'productivity', 'misc', 'deprecated']
TITLES = dict(zip(BUCKETS, ['工程', '生产力', '专用工具', '废弃与迁移']))


def is_released(row):
    return bool(row.get('path')) and row['category'] in ['engineering', 'productivity', 'misc'] and row.get('release', True) and is_adopted(row)


def is_adopted(row):
    review = row.get('review', {})
    return review.get('admission_status') == 'user-approved' and all(
        isinstance(review.get(key), str) and review[key].strip()
        for key in ['approval_basis', 'audit']
    )


def usage_table(rows, link_usage_pages=False):
    def cell(value):
        return value.replace('|', '\\|').replace('\n', '<br>')

    table = '| 具体场景 | 你可以怎样提出要求 | 用哪个 skill | AI 会怎样协助 | 最终产出 |\n| --- | --- | --- | --- | --- |\n'
    for row in rows:
        skill = f"[{row['name']}](docs/{row['category']}/{row['name']}.md)" if link_usage_pages else f"`${row['name']}`"
        for case in row.get('usage_scenarios', []):
            command = '$' + row['name']
            prompt = case['prompt']
            if prompt.startswith(command):
                prompt = f'`{command}`' + prompt[len(command):]
            values = [case['situation'], prompt, skill, case['assistance'], case['result']]
            table += '| ' + ' | '.join(cell(value) for value in values) + ' |\n'
    return table


def outputs():
    catalog = json.loads((ROOT / 'catalog.json').read_text())
    rows = catalog['skills']
    formal = [d for d in rows if is_released(d)]
    adopted = [d for d in rows if is_adopted(d) and d.get('usage_scenarios')]
    result = {}
    for bucket in BUCKETS:
        selected = [d for d in rows if d['category'] == bucket]
        listing = '| Skill | 用途 | 状态 |\n| --- | --- | --- |\n'
        for d in selected:
            state = '外部依赖' if not d.get('path') else ('默认发布' if is_released(d) else '未默认发布')
            listing += f"| [{d['name']}](../../docs/{bucket}/{d['name']}.md) | {d['purpose']} | {state} |\n"
        if not selected:
            listing += '| 暂无技能 | 保留退役与迁移说明 | 未发布 |\n'
        result[f'skills/{bucket}/README.md'] = f'# {TITLES[bucket]}\n\n{listing}\n按用途归类；用户审阅状态、已知问题和默认发布设置分别记录，目录存在不表示已经审阅通过。\n'
    for d in rows:
        state = '外部依赖，继续从上游维护来源获取' if not d.get('path') else ('已收录，列入默认发布清单' if is_released(d) else '已收录，尚未列入默认发布清单')
        location = f"[操作入口](../../{d['path']}/SKILL.md)" if d.get('path') else d['origin']
        deps = ', '.join(d.get('dependencies', [])) or '以操作入口的当前工具检查为准'
        inputs = d.get('inputs', '先明确本次任务范围与需要的输入')
        role_note = {'support': '角色：辅助技能。', 'task-entry': '角色：任务入口。'}.get(d.get('role'), '')
        usage = '## 使用场景\n\n' + usage_table([d]) if is_adopted(d) and d.get('usage_scenarios') else f"## 使用例子\n\n> {d['example']}\n"
        result[f"docs/{d['category']}/{d['name']}.md"] = f"""# {d['name']}

{d['purpose']}。状态：{state}。{role_note}

## 为什么保留或调整

{d['reason']}
{chr(10) + d['release_reason'] + chr(10) if d.get('release_reason') else ''}

{usage.rstrip()}

## 输入与依赖

{inputs}。依赖：{deps}。已有授权继续适用；缺少事实先检查，缺少用户决定再询问。

## 怎样算完成

{d['done']}

## 与相邻能力的关系

对照：{d['compare']}。按本次目的选择；名称相似不代表输出相同。

## 来源与验证范围

{location}

本页用于选择与验收；具体步骤以操作入口和当前工具文档为准。实际执行记录见 [首版验证](../audit/verification.md)。尚未执行的场景见入口的 evals，用例存在不等于已经通过。
"""
    router = '# 能力路由\n\n| 任务目的 | 首选 | 条件与边界 |\n| --- | --- | --- |\n'
    for d in rows:
        if d['name'] == 'ask-skills':
            continue
        state = '外部能力，先确认已安装' if not d.get('path') else ('当前集合，结合使用页检查已知限制' if is_released(d) else '尚待第一轮审阅，未默认发布；先检查安装与使用页限制')
        if d.get('path') and d.get('manual', False):
            state += '；手动选择'
        router += f"| {d['purpose']} | {d['name']} | {state}；{d['done']} |\n"
    result['skills/productivity/ask-skills/references/routes.md'] = router
    readme = '''# 我的 Codex Skills

学习现成系统后，整理自己的能力、共享方法与使用入口。目录分类与文档治理参考 [Matt Pocock 的 skills](https://github.com/mattpocock/skills)。当前只适配 Codex。

来自 OpenAI 官方的技能直接使用官方维护来源，按用户要求跳过个人收录；本仓库聚焦个人技能与必要定制，处理依据见[官方技能处理记录](docs/audit/openai-official-exclusions.md)。

不确定选哪个时，手动使用 `$ask-skills`。需要某项任务时，可以直接使用对应技能；无需每次先经过入口。

'''
    readme += '## 按场景选技能\n\n'
    scenario_count = sum(len(d['usage_scenarios']) for d in adopted)
    readme += f'以下覆盖已确认保留的 {len(adopted)} 个技能、{scenario_count} 个代表场景。待审技能与 Matt 候选继续记录在[分批审查清单](docs/audit/review-checklist.md)，审阅确认后补入此表。brief 已迁到独立定时任务项目。\n\n'
    readme += usage_table(adopted, link_usage_pages=True) + '\n## 当前集合\n\n'
    managed = [d for d in rows if d.get('path')]
    external = [d for d in rows if not d.get('path')]
    upstream = sum(d.get('source') == 'upstream-adapted' for d in managed)
    readme += f"最初盘点的 32 项原有技能已完成第一轮处理，待审 0 项；Matt 候选放第二批考虑是否引入，ask-skills 单列为体系维护项。当前维护 {len(managed)} 个源码技能（其中 {upstream} 项上游适配）及 {len(external)} 项外部依赖说明；默认发布 {len(formal)} 项。目录按用途分类，审阅和已知问题单独记录。进度见 [分批审查清单](docs/audit/review-checklist.md)，名称与已有安装迁移见 [安装说明](docs/installation.md)。\n\n"
    readme += '| 分类 | 作用 | 目录 |\n| --- | --- | --- |\n'
    for bucket in BUCKETS:
        readme += f'| {bucket} | {TITLES[bucket]} | [浏览](skills/{bucket}/README.md) |\n'
    readme += '''
## 从这里开始

- [第一轮收尾](docs/audit/first-round-summary.md)：最终集合、处理结论与验证范围。
- [分批审查清单](docs/audit/review-checklist.md)：第一轮原有技能优先，第二批 Matt 候选另列。
- [原有 skills 的技术盘点](docs/audit/existing-skills.md)：来源、改善建议、外部依赖与重复项。
- [Matt 全部 38 项的纳入判断](docs/audit/upstream-skills.md)：在整理自身集合后选择扩展。
- [架构与各目录的作用](docs/architecture.md)：操作入口、使用文档、术语和治理分工。
- [当前目录与文件清单](docs/directory-map.md)：各类技能、外部能力说明与实际文件。
- [安装与调用](docs/installation.md)：按明确清单安装，先预览并检查冲突。
- [验证记录](docs/audit/verification.md)：本次实际验证了什么，以及哪些仍待验证。
- [范围与准入](SCOPE.md)、[词汇表](GLOSSARY.md)、[来源与许可](THIRD_PARTY_NOTICES.md)。

## 默认发布清单

此表只包含已获用户明确确认的技能；对应场景见上表。ask-skills 已获准保留，作为体系维护入口单列，不计入第一轮原有 32 项。

| Skill | 解决什么 | 用法 |
| --- | --- | --- |
'''
    for d in formal:
        readme += f"| [{d['name']}](docs/{d['category']}/{d['name']}.md) | {d['purpose']} | `${d['name']}` |\n"
    readme += '''
## 维护

修改 catalog.json 与对应技能后，运行：

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/sync_catalog.py
python3 scripts/validate.py
python3 scripts/smoke_test.py
```

共享方法单独维护；GLOSSARY 只解释术语；docs 帮人选能力；SKILL.md 指导操作；evals 记录场景，验证记录只写实际发生的结果。
'''
    result['README.md'] = readme
    plugin = {'name': 'bubugamer-skills', 'version': catalog['version'], 'description': 'Personal Codex workflows for reading, writing, organization and data.', 'author': {'name': 'bubugamer'}, 'repository': 'https://github.com/bubugamer/skills', 'skills': ['./' + d['path'] for d in formal]}
    result['.codex-plugin/plugin.json'] = json.dumps(plugin, ensure_ascii=False, indent=2) + '\n'
    for d in rows:
        if not d.get('path'):
            continue
        implicit = not d.get('manual', False)
        interface = {'display_name': d['name'], 'short_description': ('Codex workflow: ' + d['purpose'] + '; check results')[:64], 'default_prompt': 'Use $' + d['name'] + ' to help with this task: ' + d['example']}
        interface.update(d.get('interface', {}))
        result[d['path'] + '/agents/openai.yaml'] = 'interface:\n' + ''.join('  ' + k + ': ' + json.dumps(v, ensure_ascii=False) + '\n' for k, v in interface.items()) + 'policy:\n  allow_implicit_invocation: ' + str(implicit).lower() + '\n'
    return {p: s.rstrip() + '\n' for p, s in result.items()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    for name, content in outputs().items():
        path = ROOT / name
        if args.check:
            if not path.is_file() or path.read_text() != content:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    if stale:
        print('Catalog outputs need regeneration: ' + ', '.join(stale))
        return 1
    print('Catalog outputs are consistent.' if args.check else 'Catalog navigation and metadata generated.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
