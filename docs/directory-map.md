# 目录与文件清单

整理日期：2026-10-21。当前 21 个技能源码，按用途归 engineering 3 项、productivity 15 项、misc 3 项；另有 agent-browser、find-skills 两项外部说明。已确认保留 23 项，原有第一轮 32 项全部处理完毕、待审 0。Matt 第二批本次获准纳入四项写作技能，剩余候选 32 项；ask-skills 仍单列体系维护。见 [写作技能纳入](audit/writing-skills-adoption.md) 与 [第一轮收尾](audit/first-round-summary.md)。

## 整理记录（历史）

2026-10-16 用户确认 wiki 改造并移除自测；wiki 正式替代 llm-wiki，源码数量不变。原入口与参考保存在审查快照目录。

2026-10-19 用户确认个人文风方案，writing-master 正式更名 writing-styles，保留两种可扩展文风；源码总数不变，第一轮已处理 8 项。2026-10-20 wait-what 用户确认通过，第一轮已处理 9 项、待审 23 项；同日用户确认 akshare-api、tdx-api 分别保留，已处理 11 项、待审 21 项；原有改进项继续记录，未修改两者入口或脚本。

2026-10-20 用户确认 yt-dlp-download 改造，精简入口并增加命令参考；已处理 12 项、待审 20 项，已确认保留 12 项。imagegen 随后获用户确认直接沿用官方，不再作为个人集合条目，现第一轮已处理 13 项、待审 19 项；本机安装暂不处理。

2026-10-20 用户确认 pdf 沿用官方、不纳入个人集合；原使用页与生成推荐已移出。第一轮已处理 14 项、待审 18 项，已审阅保留仍为 12 项。screenshot 开始初审，保留方式待用户确认。

2026-10-20 用户要求 OpenAI 官方技能直接跳过、不纳入个人库。剩余 12 项官方外部说明与使用页已批量移出，连同此前 imagegen、pdf 合计 14 项；处理依据见 [官方技能记录](audit/openai-official-exclusions.md)。第一轮已处理 26 项、待审 6 项，个人源码及发布范围保持。本机安装不变。

2026-10-20 用户明确 deepcoffee-dev 的专属规则是在使用 skill 中形成的，应继续保存在 skill。仓库已恢复六类能力及六篇配套说明，撤回迁入项目的建议；三个脚本、现有安装及默认发布范围未改，第一轮计数保持。

2026-10-20 用户确认 deepcoffee-dev 审阅结束，纳入默认清单并保持手动调用；本机安装暂不处理。已确认保留 13 项，第一轮已处理 27 项、待审 5 项。agent-browser 开始审阅，尚未获得纳入确认。

2026-10-20 用户确认 agent-browser 作为 engineering 外部工具保留，不复制源码、不进入发布清单；已确认保留 14 项，第一轮已处理 28 项、待审 4 项。find-skills 开始审阅，已核对来源与一次只读搜索，去留待用户确认。源码 14 项、外部说明 5 项、默认发布 14 项不变。

2026-10-20 用户确认 find-skills 作为 productivity 外部发现工具保留，沿用上游；已确认保留 15 项，第一轮已处理 29 项、待审 3 项。deep-research 开始审阅，已核对来源、现有测试与证据校验反例，方案待用户确认。源码 14 项、外部说明 5 项、默认发布 14 项保持。

2026-10-20 用户确认 deep-research 保留并整改，方法参考第三方，由 Codex 独立重写为短英文入口、三篇参考和轻量记录工具，纳入默认清单并维持正常自动选择。本机旧安装不变。已确认保留 16 项，第一轮已处理 30 项、待审 2 项；源码 15 项、外部说明 4 项、默认发布 15 项。ui-ux-pro-max 开始审阅，去留与整改待用户确认。

2026-10-20 用户确认 ui-ux-pro-max 保留及整改，个人规则、Codex 入口和适配工具纳入 engineering；外部资料及引擎不复制，本机安装不变。已确认保留 17 项，第一轮已处理 31 项、待审 1 项；源码和默认清单各 16 项，外部说明 3 项。skill-creator 开始审阅，拆分评测能力的建议待用户确认。

## 技能分类

| 目录 | 本仓库技能源码 | 只记录使用说明的外部能力 |
| --- | --- | --- |
| engineering | deepcoffee-dev、ui-ux-pro-max、skill-creator | agent-browser |
| productivity | remind、read、teach、para、site-unlocker、social-feed、wiki、writing-styles、wait-what、ask-skills、deep-research、writing-fragments、writing-shape、writing-beats、writing-for-agents | find-skills |
| misc | akshare-api、tdx-api、yt-dlp-download | 暂无 |
| deprecated | 暂无 | 暂无 |

domain-modeling、diagnosing-bugs、grilling 未获用户逐项确认，已撤回。三项仅在 [上游候选审查](audit/upstream-skills.md) 中保留链接，不计入当前集合。teach 已获明确确认，继续保留；wait-what 是原有技能。

已取消 in-progress 目录。deepcoffee-dev 已按用户确认恢复六类能力与配套规则，三个现有脚本仍为本地运行依赖，现已审阅通过；social-feed 的工具定位和登录处理仍有已知问题。wiki 已获用户确认，完成更名与只读检查工具改造；真实站点与公开过滤仍由知识库项目验证。当前默认发布 21 项，四项 Matt 写作技能已获准纳入；skill-creator 已按用户最终决定保留创建、维护与评测的一体入口；ui-ux-pro-max 已确认个人适配入口并纳入清单，外部运行依赖单独配置；deepcoffee-dev 已获用户确认并纳入清单，保持手动调用；deep-research 重写后纳入默认清单，正常自动选择。

## 文件职责

| 位置或文件 | 作用 |
| --- | --- |
| README.md | 总入口与正式技能导航。 |
| AGENTS.md、SCOPE.md | 维护规则、范围与分类依据。 |
| GLOSSARY.md | 统一术语。 |
| catalog.json | 当前技能名称、分类、来源、用途与调用设置。 |
| CHANGELOG.md、THIRD_PARTY_NOTICES.md | 变更与第三方出处。 |
| requirements-dev.txt、.gitignore | 检查工具依赖和忽略规则。 |
| skills/ | 技能本体，按 engineering、productivity、misc 用途归类；deprecated 保留迁移说明。 |
| docs/engineering、productivity、misc | 给人看的使用说明；外部能力也在这里记录。 |
| docs/deprecated/brief.md | brief 迁出技能集合的历史说明。 |
| docs/productivity/brief.md、dongnaojin-yeye.md、konmari.md、tang-monk.md、writing-master.md | 保留旧链接的迁移提示页。 |
| docs/audit/ | 审查判断、用户场景与实际验证记录。 |
| docs/agents/ | 工作区配置示例。 |
| .agents/ | 调用、文档维护与重要选择的说明。 |
| .codex-plugin/ | 正式发布技能清单。 |
| scripts/ | 生成导航、校验和安全安装检查。 |
| .github/workflows/ | 提交后的自动检查。 |
| .out-of-scope/ | 已暂缓事项与原因。 |

技能文件的共同部分是 SKILL.md、ORIGIN.json、agents/openai.yaml 和 evals/evals.json；模板、参考资料、脚本、素材与许可证按该技能实际需要保留。完整名称见下方树。

## 完整文件树

以下为本次整理后的文件快照，省略 Git 内部数据和本地缓存。审查快照不属于可安装技能。

```text
skills/（仓库根目录）
├── .agents/
│   ├── adr/
│   │   ├── 0001-personal-and-external.md
│   │   └── 0002-promoted-only-release.md
│   ├── plugins/
│   │   └── marketplace.json
│   ├── invocation.md
│   └── writing-docs.md
├── .codex-plugin/
│   └── plugin.json
├── .github/
│   └── workflows/
│       └── validate.yml
├── .out-of-scope/
│   └── README.md
├── docs/
│   ├── agents/
│   │   └── skill-workspace.example.md
│   ├── audit/
│   │   ├── llm-wiki-original/
│   │   │   ├── references/
│   │   │   │   ├── lint-rules.md
│   │   │   │   ├── page-templates.md
│   │   │   │   └── scaling.md
│   │   │   └── SKILL.md
│   │   ├── agent-browser-review.md
│   │   ├── akshare-api-review.md
│   │   ├── ask-skills-review.md
│   │   ├── brief-review.md
│   │   ├── deep-research-review.md
│   │   ├── deepcoffee-dev-review.md
│   │   ├── existing-skills.md
│   │   ├── find-skills-review.md
│   │   ├── first-round-summary.md
│   │   ├── imagegen-review.md
│   │   ├── konmari-review.md
│   │   ├── llm-wiki-review.md
│   │   ├── openai-official-exclusions.md
│   │   ├── pdf-review.md
│   │   ├── reading-learning-review.md
│   │   ├── review-checklist.md
│   │   ├── scenarios.md
│   │   ├── screenshot-review.md
│   │   ├── skill-creator-review.md
│   │   ├── tang-monk-legacy-workspace.md
│   │   ├── tang-monk-review.md
│   │   ├── tdx-api-review.md
│   │   ├── ui-ux-pro-max-review.md
│   │   ├── upstream-skills.md
│   │   ├── verification.md
│   │   ├── wait-what-review.md
│   │   ├── wiki-comparison.md
│   │   ├── wiki-workspace-legacy.md
│   │   ├── writing-master-matt-comparison.md
│   │   ├── writing-master-review.md
│   │   ├── writing-skills-adoption.md
│   │   └── yt-dlp-download-review.md
│   ├── deprecated/
│   │   └── brief.md
│   ├── engineering/
│   │   ├── agent-browser.md
│   │   ├── deepcoffee-dev.md
│   │   ├── skill-creator.md
│   │   └── ui-ux-pro-max.md
│   ├── misc/
│   │   ├── akshare-api.md
│   │   ├── tdx-api.md
│   │   └── yt-dlp-download.md
│   ├── productivity/
│   │   ├── ask-skills.md
│   │   ├── brief.md
│   │   ├── deep-research.md
│   │   ├── dongnaojin-yeye.md
│   │   ├── find-skills.md
│   │   ├── konmari.md
│   │   ├── llm-wiki.md
│   │   ├── para.md
│   │   ├── read.md
│   │   ├── remind.md
│   │   ├── site-unlocker.md
│   │   ├── social-feed.md
│   │   ├── tang-monk.md
│   │   ├── teach.md
│   │   ├── wait-what.md
│   │   ├── wiki.md
│   │   ├── writing-beats.md
│   │   ├── writing-for-agents.md
│   │   ├── writing-fragments.md
│   │   ├── writing-master.md
│   │   ├── writing-shape.md
│   │   └── writing-styles.md
│   ├── architecture.md
│   ├── directory-map.md
│   └── installation.md
├── scripts/
│   ├── install.py
│   ├── smoke_test.py
│   ├── sync_catalog.py
│   └── validate.py
├── skills/
│   ├── deprecated/
│   │   └── README.md
│   ├── engineering/
│   │   ├── deepcoffee-dev/
│   │   │   ├── agents/
│   │   │   │   └── openai.yaml
│   │   │   ├── evals/
│   │   │   │   └── evals.json
│   │   │   ├── references/
│   │   │   │   ├── delivery.md
│   │   │   │   ├── deployment.md
│   │   │   │   ├── knowledge.md
│   │   │   │   ├── maintenance.md
│   │   │   │   ├── operating-rules.md
│   │   │   │   └── runtime.md
│   │   │   ├── ORIGIN.json
│   │   │   └── SKILL.md
│   │   ├── skill-creator/
│   │   │   ├── agents/
│   │   │   │   └── openai.yaml
│   │   │   ├── evals/
│   │   │   │   └── evals.json
│   │   │   ├── references/
│   │   │   │   ├── creation.md
│   │   │   │   ├── result-records.md
│   │   │   │   ├── task-comparison.md
│   │   │   │   └── trigger-evaluation.md
│   │   │   ├── scripts/
│   │   │   │   ├── model_runner.py
│   │   │   │   ├── review_report.py
│   │   │   │   ├── task_results.py
│   │   │   │   ├── test_evaluation.py
│   │   │   │   └── trigger_eval.py
│   │   │   ├── ORIGIN.json
│   │   │   ├── requirements.txt
│   │   │   └── SKILL.md
│   │   ├── ui-ux-pro-max/
│   │   │   ├── agents/
│   │   │   │   └── openai.yaml
│   │   │   ├── evals/
│   │   │   │   └── evals.json
│   │   │   ├── references/
│   │   │   │   ├── design-records.md
│   │   │   │   ├── personal-design.md
│   │   │   │   └── reference-search.md
│   │   │   ├── scripts/
│   │   │   │   ├── save_rules.py
│   │   │   │   ├── search_references.py
│   │   │   │   └── test_tools.py
│   │   │   ├── ORIGIN.json
│   │   │   └── SKILL.md
│   │   └── README.md
│   ├── misc/
│   │   ├── akshare-api/
│   │   │   ├── agents/
│   │   │   │   └── openai.yaml
│   │   │   ├── evals/
│   │   │   │   └── evals.json
│   │   │   ├── references/
│   │   │   │   └── function-routing.md
│   │   │   ├── scripts/
│   │   │   │   ├── akshare
│   │   │   │   ├── akshare_api.py
│   │   │   │   └── test_akshare_api.py
│   │   │   ├── ORIGIN.json
│   │   │   ├── requirements.txt
│   │   │   └── SKILL.md
│   │   ├── tdx-api/
│   │   │   ├── agents/
│   │   │   │   └── openai.yaml
│   │   │   ├── evals/
│   │   │   │   └── evals.json
│   │   │   ├── references/
│   │   │   │   └── pytdx-interface.md
│   │   │   ├── scripts/
│   │   │   │   ├── tdx
│   │   │   │   ├── tdx_api.py
│   │   │   │   └── test_tdx_api.py
│   │   │   ├── ORIGIN.json
│   │   │   ├── requirements.txt
│   │   │   └── SKILL.md
│   │   ├── yt-dlp-download/
│   │   │   ├── agents/
│   │   │   │   └── openai.yaml
│   │   │   ├── evals/
│   │   │   │   └── evals.json
│   │   │   ├── references/
│   │   │   │   └── commands.md
│   │   │   ├── ORIGIN.json
│   │   │   └── SKILL.md
│   │   └── README.md
│   └── productivity/
│       ├── ask-skills/
│       │   ├── agents/
│       │   │   └── openai.yaml
│       │   ├── evals/
│       │   │   └── evals.json
│       │   ├── references/
│       │   │   └── routes.md
│       │   ├── ORIGIN.json
│       │   └── SKILL.md
│       ├── deep-research/
│       │   ├── agents/
│       │   │   └── openai.yaml
│       │   ├── evals/
│       │   │   └── evals.json
│       │   ├── references/
│       │   │   ├── evidence-records.md
│       │   │   ├── reports.md
│       │   │   └── research-method.md
│       │   ├── scripts/
│       │   │   ├── records.py
│       │   │   └── test_records.py
│       │   ├── ORIGIN.json
│       │   └── SKILL.md
│       ├── para/
│       │   ├── agents/
│       │   │   └── openai.yaml
│       │   ├── assets/
│       │   │   └── review-desk/
│       │   │       ├── app.js
│       │   │       ├── index.html
│       │   │       └── style.css
│       │   ├── evals/
│       │   │   └── evals.json
│       │   ├── references/
│       │   │   ├── junk-rules.md
│       │   │   ├── metadata-schema.md
│       │   │   ├── organization-profiles.md
│       │   │   ├── para-rebuild.md
│       │   │   └── workflow.md
│       │   ├── scripts/
│       │   │   ├── __init__.py
│       │   │   ├── apply_actions.py
│       │   │   ├── build_review.py
│       │   │   ├── build_stats.py
│       │   │   ├── build_workspace_index.py
│       │   │   ├── build_workspace_tree.py
│       │   │   ├── enrich_semantics.py
│       │   │   ├── find_exact_duplicates.py
│       │   │   ├── find_name_duplicates.py
│       │   │   ├── init_workspace.py
│       │   │   ├── plan_actions.py
│       │   │   ├── scan_inventory.py
│       │   │   ├── serve_review_desk.py
│       │   │   ├── test_para.py
│       │   │   └── workspace_lib.py
│       │   ├── ORIGIN.json
│       │   └── SKILL.md
│       ├── read/
│       │   ├── agents/
│       │   │   └── openai.yaml
│       │   ├── evals/
│       │   │   └── evals.json
│       │   ├── references/
│       │   │   ├── note-templates.md
│       │   │   ├── routing-rules.md
│       │   │   └── source-evaluation.md
│       │   ├── ORIGIN.json
│       │   └── SKILL.md
│       ├── remind/
│       │   ├── agents/
│       │   │   └── openai.yaml
│       │   ├── evals/
│       │   │   └── evals.json
│       │   ├── ORIGIN.json
│       │   └── SKILL.md
│       ├── site-unlocker/
│       │   ├── agents/
│       │   │   └── openai.yaml
│       │   ├── evals/
│       │   │   └── evals.json
│       │   ├── references/
│       │   │   ├── auth-and-state.md
│       │   │   ├── capture-quality.md
│       │   │   └── workflow.md
│       │   ├── ORIGIN.json
│       │   └── SKILL.md
│       ├── social-feed/
│       │   ├── agents/
│       │   │   └── openai.yaml
│       │   ├── evals/
│       │   │   └── evals.json
│       │   ├── references/
│       │   │   └── auth-setup.md
│       │   ├── scripts/
│       │   │   └── fetch_social_feed.py
│       │   ├── ORIGIN.json
│       │   └── SKILL.md
│       ├── teach/
│       │   ├── agents/
│       │   │   └── openai.yaml
│       │   ├── evals/
│       │   │   └── evals.json
│       │   ├── LEARNING-RECORD-FORMAT.md
│       │   ├── LICENSE.txt
│       │   ├── MISSION-FORMAT.md
│       │   ├── ORIGIN.json
│       │   ├── RESOURCES-FORMAT.md
│       │   └── SKILL.md
│       ├── wait-what/
│       │   ├── agents/
│       │   │   └── openai.yaml
│       │   ├── evals/
│       │   │   └── evals.json
│       │   ├── LICENSE.txt
│       │   ├── ORIGIN.json
│       │   └── SKILL.md
│       ├── wiki/
│       │   ├── agents/
│       │   │   └── openai.yaml
│       │   ├── evals/
│       │   │   └── evals.json
│       │   ├── references/
│       │   │   ├── health-check.md
│       │   │   ├── navigation.md
│       │   │   ├── page-conventions.md
│       │   │   ├── page-templates.md
│       │   │   ├── site-operations.md
│       │   │   └── workspace-profile.md
│       │   ├── scripts/
│       │   │   ├── lint_wiki.py
│       │   │   └── test_wiki.py
│       │   ├── ORIGIN.json
│       │   └── SKILL.md
│       ├── writing-beats/
│       │   ├── agents/
│       │   │   └── openai.yaml
│       │   ├── evals/
│       │   │   └── evals.json
│       │   ├── LICENSE.txt
│       │   ├── ORIGIN.json
│       │   └── SKILL.md
│       ├── writing-for-agents/
│       │   ├── agents/
│       │   │   └── openai.yaml
│       │   ├── evals/
│       │   │   └── evals.json
│       │   ├── LICENSE.txt
│       │   ├── ORIGIN.json
│       │   ├── SKILL-MECHANICS.md
│       │   └── SKILL.md
│       ├── writing-fragments/
│       │   ├── agents/
│       │   │   └── openai.yaml
│       │   ├── evals/
│       │   │   └── evals.json
│       │   ├── LICENSE.txt
│       │   ├── ORIGIN.json
│       │   └── SKILL.md
│       ├── writing-shape/
│       │   ├── agents/
│       │   │   └── openai.yaml
│       │   ├── evals/
│       │   │   └── evals.json
│       │   ├── LICENSE.txt
│       │   ├── ORIGIN.json
│       │   └── SKILL.md
│       ├── writing-styles/
│       │   ├── agents/
│       │   │   └── openai.yaml
│       │   ├── evals/
│       │   │   └── evals.json
│       │   ├── references/
│       │   │   └── styles/
│       │   │       ├── bbs.md
│       │   │       └── research-analysis.md
│       │   ├── ORIGIN.json
│       │   └── SKILL.md
│       └── README.md
├── .gitignore
├── AGENTS.md
├── catalog.json
├── CHANGELOG.md
├── GLOSSARY.md
├── README.md
├── requirements-dev.txt
├── SCOPE.md
└── THIRD_PARTY_NOTICES.md
```
