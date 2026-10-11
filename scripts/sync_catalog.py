#!/usr/bin/env python3
"""Generate human navigation and release metadata from the reviewed catalog."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUCKETS = ['engineering', 'productivity', 'misc', 'in-progress', 'deprecated']
TITLES = dict(zip(BUCKETS, ['工程', '生产力', '专用工具', '试用与待改善', '废弃与迁移']))


def outputs():
    catalog = json.loads((ROOT / 'catalog.json').read_text())
    rows = catalog['skills']
    formal = [d for d in rows if d.get('path') and d['category'] not in ['in-progress', 'deprecated']]
    result = {}
    for bucket in BUCKETS:
        selected = [d for d in rows if d['category'] == bucket]
        listing = '| Skill | 用途 | 状态 |\n| --- | --- | --- |\n'
        for d in selected:
            state = '外部依赖' if not d.get('path') else ('手动试用' if bucket == 'in-progress' else '正式')
            listing += f"| [{d['name']}](../../docs/{bucket}/{d['name']}.md) | {d['purpose']} | {state} |\n"
        if not selected:
            listing += '| 暂无技能 | 保留退役与迁移说明 | 未发布 |\n'
        result[f'skills/{bucket}/README.md'] = f'# {TITLES[bucket]}\n\n{listing}\n分类表示用途或成熟度，不代表全部技能都会被默认安装。\n'
    for d in rows:
        state = '外部依赖，继续从上游维护来源获取' if not d.get('path') else ('手动试用，尚未晋升' if d['category'] == 'in-progress' else '正式集合')
        location = f"[操作入口](../../{d['path']}/SKILL.md)" if d.get('path') else d['origin']
        deps = ', '.join(d.get('dependencies', [])) or '以操作入口的当前工具检查为准'
        result[f"docs/{d['category']}/{d['name']}.md"] = f"""# {d['name']}

{d['purpose']}。状态：{state}。

## 为什么保留或调整

{d['reason']}

## 使用例子

> {d['example']}

## 输入与依赖

先明确本次任务范围与需要的输入。依赖：{deps}。已有授权继续适用；缺少事实先检查，缺少用户决定再询问。

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
        state = '外部能力，先确认已安装' if not d.get('path') else ('仅手动试用' if d['category'] == 'in-progress' else '正式能力')
        router += f"| {d['purpose']} | {d['name']} | {state}；{d['done']} |\n"
    result['skills/productivity/ask-skills/references/routes.md'] = router
    readme = '''# 我的 Codex Skills

学习现成系统后，整理自己的能力、共享方法与使用入口。目录分类与文档治理参考 [Matt Pocock 的 skills](https://github.com/mattpocock/skills)。当前只适配 Codex。

不确定选哪个时，手动使用 `$ask-skills`。需要某项任务时，可以直接使用对应技能；无需每次先经过入口。

## 当前集合

'''
    readme += f"审查了 32 个不同现有 skills：13 项本地定制进入源码集合，19 项保留为外部依赖。新增一个推荐入口，并试用四项 Matt 基础方法。当前正式发布 {len(formal)} 项，试用 {sum(d['category'] == 'in-progress' for d in rows)} 项。原安装保持不变。\n\n"
    readme += '| 分类 | 作用 | 目录 |\n| --- | --- | --- |\n'
    for bucket in BUCKETS:
        readme += f'| {bucket} | {TITLES[bucket]} | [浏览](skills/{bucket}/README.md) |\n'
    readme += '''
## 从这里开始

- [现有 skills 的逐项审查](docs/audit/existing-skills.md)：保留、改善、外部依赖与重复项。
- [Matt 全部 38 项的纳入判断](docs/audit/upstream-skills.md)：在整理自身集合后选择扩展。
- [架构与各目录的作用](docs/architecture.md)：操作入口、使用文档、术语和治理分工。
- [安装与调用](docs/installation.md)：只安装正式项，先预览并检查冲突。
- [验证记录](docs/audit/verification.md)：本次实际验证了什么，以及哪些仍待验证。
- [范围与准入](SCOPE.md)、[词汇表](GLOSSARY.md)、[来源与许可](THIRD_PARTY_NOTICES.md)。

## 正式能力

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
        implicit = d['category'] not in ['in-progress', 'deprecated'] and not d.get('manual', False)
        interface = {'display_name': d['name'], 'short_description': ('Codex workflow: ' + d['purpose'] + '; check results')[:64], 'default_prompt': 'Use $' + d['name'] + ' to help with this task: ' + d['example']}
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
