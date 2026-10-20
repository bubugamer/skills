# 分批技能审查清单

更新日期：2026-10-20。**第一轮原有技能已全部确认处理。** Matt 的其他技能放在第二批，届时重点判断是否值得引入。

2026-10-20 范围补充：当前以仓库版本为审阅与整改对象；本机旧安装统一处理留待全部技能梳理完成后进行，见 [范围约定](../../SCOPE.md)。

## 当前优先级与进度

| 顺序 | 范围 | 当前进度 | 后续处理 |
| --- | --- | --- | --- |
| 第一轮：当前重点 | 原有 32 个不同技能 | 已确认处理 32 项，待审 0 项 | 本轮收尾完成；已知限制继续记录，安装迁移另行处理。 |
| 第二批：稍后扩展 | Matt 尚未引入的 36 个候选 | 尚未启动整批引入评估；其中 6 项只做过方法比较 | 原有集合审完后，再判断是否值得引入。 |
| 体系维护：单列 | ask-skills | 用户已明确批准加入，保持手动推荐入口 | 不计入原有技能的第一轮待审数量。 |

teach 已经用户明确确认引入，单独保留，不算第一轮原有技能。wait-what 原本就在本地集合，也来自 Matt，归第一轮审阅，第二批不重复列入。

## 已审阅并保留在用途目录：19 项

| Skill | 当前目录 | 来源或角色 |
| --- | --- | --- |
| `remind` | productivity | 原有技能；待办、承诺和想法提醒。 |
| `read` | productivity | 原有技能；阅读、翻译、问答与笔记。 |
| `para` | productivity | 原有技能；按 PARA 重建选定目录。 |
| `site-unlocker` | productivity | 原有辅助技能；特殊网页正文获取。 |
| `social-feed` | productivity | 原有辅助技能；社交时间线获取，用户确认保持现状。 |
| `wiki` | productivity | 原有 llm-wiki；长期知识维护，用户确认移除自测。 |
| `writing-styles` | productivity | 原 writing-master；多文风应用、润色与审稿。 |
| `wait-what` | productivity | 原有 Matt 技能；用简明中文重讲未理解的回答，保留手动入口。 |
| `teach` | productivity | Matt 已确认引入；独立系统学习与自测入口。 |
| `akshare-api` | misc | 原有技能；AKShare 多来源数据访问，保留已知改进项。 |
| `tdx-api` | misc | 原有技能；通达信沪深行情与历史数据。 |
| `yt-dlp-download` | misc | 原有技能；视频、音频与选定合集下载，直接调用 CLI。 |
| `deepcoffee-dev` | engineering | 原有技能；专属开发、运维与知识规则留在 skill 内，手动调用。 |
| `agent-browser` | engineering（外部工具说明） | Vercel Labs 浏览器操作能力；沿用上游，不复制第三方源码。 |
| `find-skills` | productivity（外部工具说明） | Vercel Labs 外部技能发现；搜索后逐项审核候选。 |
| `deep-research` | productivity | 方法参考第三方；已批准 Codex 重写，取证与交叉核对，报告和记录按需。 |
| `ui-ux-pro-max` | engineering | 个人设计规则与 Codex 适配入口；第三方资料和引擎仍外置。 |
| `skill-creator` | engineering | 创建、维护与评测统一入口；按需比较任务、检查触发和评阅结果。 |
| `ask-skills` | productivity | 体系新增入口；用户明确批准加入，手动推荐已有技能，不执行任务。 |

其他已确认处理：

- **brief**：迁到定时任务项目，方法与消息源已保存，调度尚未实现。
- **OpenAI 官方 14 项**：imagegen、pdf 已先前确认沿用官方；本轮另按用户规则直接跳过 `cloudflare-deploy`、`gh-address-comments`、`gh-fix-ci`、`jupyter-notebook`、`openai-docs`、`playwright`、`playwright-interactive`、`screenshot`、`security-best-practices`、`security-threat-model`、`transcribe`、`vercel-deploy`。全部不纳入个人集合，仅保留 [处理依据](openai-official-exclusions.md)，本机安装暂不处理。

第一轮已确认处理 32 项：原有保留 17 项、brief 迁出 1 项、官方跳过 14 项。提前确认的 teach 和体系新增 ask-skills 不计入原有 32 项，因此个人集合已审阅保留共 19 项，其中 agent-browser 和 find-skills 仅登记外部工具，不包含可发布源码。批量跳过依据用户授权与来源，不表示已完成这些技能的逐项内容审阅或行为验证。

## 第一轮已确认处理：32 项

| Skill | 来源 | 本轮结论 | 确认记录 |
| --- | --- | --- | --- |
| `remind`（原 TangMonk／tang-monk） | 你的原有集合 | 已确认提醒助手定位及收敛后的说明；2026-10-15 按用户要求更名 remind，保留为正式技能。 | [定稿记录](tang-monk-review.md) |
| `brief` | 你的原有集合 | 已确认新闻摘要用途，随后决定退出技能集合；资料已迁到定时任务项目，调度尚未实现。 | [用途审查](brief-review.md)、[迁出决定](../deprecated/brief.md) |
| `social-feed` | 你的原有集合 | 已审阅来源、用途、与 brief 的关系；用户确认保持现状，作为辅助技能。已知问题保留在使用说明中，目录归 productivity。 | [辅助关联确认](brief-review.md)、[保持现状记录](reading-learning-review.md) |
| `site-unlocker` | 你的原有集合 | 已审阅来源、用途与独立场景；用户确认保持现状，作为辅助技能。 | [辅助关联确认](brief-review.md)、[保持现状记录](reading-learning-review.md) |
| `read`（原 dongnaojin-yeye／动脑筋爷爷） | 你的原有集合 | 原动脑筋爷爷（dongnaojin-yeye）；已确认阅读助手与阅读秘书定位、命名、与 teach 的边界及说明精简。 | [阅读助手确认](reading-learning-review.md) |
| `para`（原 konmari） | 你的原有集合 | 用户确认 PARA 专用重建、整改与更名；查看入口、配套说明及操作流程后，明确审阅通过，保留 productivity 正式目录。实际验证范围见审查记录。 | [本轮审查](konmari-review.md) |
| `wiki`（原 llm-wiki） | 你的原有集合 | 2026-10-16 用户认可其余改造方案，明确移除自测；完成更名、六篇配套参考与只读检查工具，保留手动调用，纳入默认清单。 | [本轮审查](llm-wiki-review.md)、[五列取舍对照](wiki-comparison.md) |
| `writing-styles`（原 writing-master） | 你的原有集合 | 2026-10-19 用户确认个人文风层方案，完成复数更名、共同规则精简、两种文风整理及九条场景定义；安装先备份后迁移，保持自动选择设置。 | [本轮审查](writing-master-review.md)、[使用页](../productivity/writing-styles.md) |
| `wait-what` | 你的原有集合（来自 Matt） | 2026-10-20 用户确认保留 Matt 英文原文、末尾仅加 Reply in Chinese.；修改后接受结果并继续下一项。保留 Codex 手动调用，本机安装暂不处理。 | [定稿记录](wait-what-review.md)、[使用页](../productivity/wait-what.md) |
| `akshare-api` | 你的原有集合 | 用户确认与通达信入口分别保留；AKShare 按所用接口标注真实来源。参数类型、安装恢复等已知问题保留为改进项，本轮未修复。 | [保留决定](akshare-api-review.md)、[使用页](../misc/akshare-api.md) |
| `tdx-api` | 你的原有集合 | 用户直接确认独立保留，按通达信通道使用。此次确认去留，未新增脚本或真实行情验证；入口及安装保持。 | [保留决定](tdx-api-review.md)、[使用页](../misc/tdx-api.md) |
| `yt-dlp-download` | 你的原有集合 | 2026-10-20 用户确认按建议整改；精简英文入口与命令外置，保留目录偏好，完善合集范围、按格式下载及已有文件核对。本地合成媒体配方验证通过，本机安装暂不处理。 | [定稿记录](yt-dlp-download-review.md)、[使用页](../misc/yt-dlp-download.md) |
| `imagegen` | 你的原有集合（OpenAI 官方） | 2026-10-20 用户表示官方技能直接通过，并确认无需纳入个人项目库；沿用官方能力，移出 catalog、用途使用页与生成推荐。保留审阅依据，不复制源码，不修改本机安装。 | [确认记录](imagegen-review.md) |
| `pdf` | 你的原有集合（OpenAI 官方） | 用户在审阅建议后表示「好的，那就继续吧」，确认沿用官方、不纳入个人集合。移出 catalog、使用页与生成推荐，保留审查结论，本机安装暂不处理。 | [确认记录](pdf-review.md) |
| `cloudflare-deploy` | 你的原有集合（OpenAI 官方） | 按用户明确规则直接跳过，不纳入个人集合；来源登记及入口指纹已核对，本机安装保持。 | [批量处理记录](openai-official-exclusions.md) |
| `gh-address-comments` | 你的原有集合（OpenAI 官方） | 按用户明确规则直接跳过，不纳入个人集合；来源登记及入口指纹已核对，本机安装保持。 | [批量处理记录](openai-official-exclusions.md) |
| `gh-fix-ci` | 你的原有集合（OpenAI 官方） | 按用户明确规则直接跳过，不纳入个人集合；来源登记及入口指纹已核对，本机安装保持。 | [批量处理记录](openai-official-exclusions.md) |
| `jupyter-notebook` | 你的原有集合（OpenAI 官方） | 按用户明确规则直接跳过，不纳入个人集合；来源登记及入口指纹已核对，本机安装保持。 | [批量处理记录](openai-official-exclusions.md) |
| `openai-docs` | 你的原有集合（OpenAI 官方） | 按用户明确规则直接跳过，不纳入个人集合；来源登记及入口指纹已核对，本机安装保持。 | [批量处理记录](openai-official-exclusions.md) |
| `playwright` | 你的原有集合（OpenAI 官方） | 按用户明确规则直接跳过，不纳入个人集合；来源登记及入口指纹已核对，本机安装保持。 | [批量处理记录](openai-official-exclusions.md) |
| `playwright-interactive` | 你的原有集合（OpenAI 官方） | 按用户明确规则直接跳过，不纳入个人集合；来源登记及入口指纹已核对，本机安装保持。 | [批量处理记录](openai-official-exclusions.md) |
| `screenshot` | 你的原有集合（OpenAI 官方） | 按用户明确规则直接跳过，不纳入个人集合；来源登记及入口指纹已核对，本机安装保持。 | [批量处理记录](openai-official-exclusions.md) |
| `security-best-practices` | 你的原有集合（OpenAI 官方） | 按用户明确规则直接跳过，不纳入个人集合；来源登记及入口指纹已核对，本机安装保持。 | [批量处理记录](openai-official-exclusions.md) |
| `security-threat-model` | 你的原有集合（OpenAI 官方） | 按用户明确规则直接跳过，不纳入个人集合；来源登记及入口指纹已核对，本机安装保持。 | [批量处理记录](openai-official-exclusions.md) |
| `transcribe` | 你的原有集合（OpenAI 官方） | 按用户明确规则直接跳过，不纳入个人集合；来源登记及入口指纹已核对，本机安装保持。 | [批量处理记录](openai-official-exclusions.md) |
| `vercel-deploy` | 你的原有集合（OpenAI 官方） | 按用户明确规则直接跳过，不纳入个人集合；来源登记及入口指纹已核对，本机安装保持。 | [批量处理记录](openai-official-exclusions.md) |
| `deepcoffee-dev` | 你的原有集合 | 用户确认规则保留于 skill，整理完成后确认本项结束并继续下一项；已审阅保留，纳入默认清单并保持手动调用。本机安装暂不处理。 | [确认记录](deepcoffee-dev-review.md)、[使用页](../engineering/deepcoffee-dev.md) |
| `agent-browser` | 你的原有集合（Vercel Labs） | 用户确认作为外部工具保留，归 engineering；不复制第三方源码，已知 profile 限制继续记录，本机安装暂不处理。 | [确认记录](agent-browser-review.md)、[使用页](../engineering/agent-browser.md) |
| `find-skills` | 你的原有集合（Vercel Labs） | 用户确认作为 productivity 外部发现工具保留，沿用上游；候选仍需逐项审阅确认，不复制源码或处理本机重复安装。 | [确认记录](find-skills-review.md)、[使用页](../productivity/find-skills.md) |
| `deep-research` | 你的原有集合（第三方方法，Codex 重写） | 用户明确批准保留与整改；完成英文短入口、三篇参考、轻量记录工具及九项测试，纳入默认清单，本机安装留待统一处理。 | [定稿记录](deep-research-review.md)、[使用页](../productivity/deep-research.md) |
| `ui-ux-pro-max` | 你的原有集合（第三方工具，个人规则与 Codex 适配） | 用户批准保留与整改；短入口、三篇参考、数据／平台适配和保留已有规则的保存工具已完成。本机安装不变。 | [定稿记录](ui-ux-pro-max-review.md)、[使用页](../engineering/ui-ux-pro-max.md) |
| `skill-creator` | 你的原有集合（Anthropic 方法及本地 Codex 改写） | 用户最终确认创建、维护与评测放在同一入口；短英文入口、四篇参考及工具完成整改，纳入默认清单，本机安装不变。 | [定稿记录](skill-creator-review.md)、[使用页](../engineering/skill-creator.md) |

## 第一轮待审：0 项

无。原有 32 项均已确认处理；保留、迁出与官方跳过分别列明，不把批量来源确认视作逐项行为验证。

## 已提前确认的 Matt 引入：teach

| Skill | 来源 | 本轮结论 | 确认记录 |
| --- | --- | --- | --- |
| `teach` | Matt 候选／已确认引入 | 已读原版并讨论用途，用户明确同意纳入；已按要求恢复完整英文正文，独立、手动调用。 | [独立纳入与英文恢复](reading-learning-review.md) |

## 第二批 Matt 候选：36 项

此处是之后的扩展候选，不合并进第一轮的 1 项待审。参考快照为提交 49dd158d1076134a641b33efb035946536778336，原作者共 38 项；扣除已引入的 teach 与归第一轮的 wait-what 后，余下 36 项。作者原有分类只表示上游位置，不作为本仓库的目录规则。

### 已做过相邻方法比较：6 项

这些讨论不表示已决定引入。

| Skill | 来源 | 已涉及的内容 | 查看 |
| --- | --- | --- | --- |
| `wayfinder` | Matt 候选 | 只与 remind 比较用途和边界；尚未决定是否独立纳入。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/wayfinder) |
| `loop-me` | Matt 候选 | 只与 remind 比较用途和边界；尚未决定是否独立纳入。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/in-progress/loop-me) |
| `writing-for-agents` | Matt 候选 | 已核对原文与 SKILL-MECHANICS，比较引用条件、按需加载、去重与拆分原则；仅借鉴，未确认导入。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/productivity/writing-for-agents) |
| `writing-fragments` | Matt 候选 | 已读原文：素材探索与片段记录，可补足个人写作助手前期方法；未确认导入。 [对照](writing-master-matt-comparison.md) | [上游](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/in-progress/writing-fragments/SKILL.md) |
| `writing-shape` | Matt 候选 | 已读原文：文章主张、读者基础、开头与逐块成文；建议借鉴方法，未确认导入。 [对照](writing-master-matt-comparison.md) | [上游](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/in-progress/writing-shape/SKILL.md) |
| `writing-beats` | Matt 候选 | 已读原文：按叙述动作选择下一方向，一个动作可跨多段；可选共写方式，未确认导入。 [对照](writing-master-matt-comparison.md) | [上游](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/in-progress/writing-beats/SKILL.md) |

### 其余扩展候选：30 项

| Skill | 作者分类 | 当前状态或备注 | 查看上游 |
| --- | --- | --- | --- |
| `ask-matt` | engineering | 曾作为体系路由设计参考；尚未逐项审核该技能本身。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/ask-matt) |
| `code-review` | engineering | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/code-review) |
| `codebase-design` | engineering | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/codebase-design) |
| `diagnosing-bugs` | engineering | 已核实来自 Matt，提前导入已撤回；来源核实不算用途与内容审核。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/diagnosing-bugs) |
| `domain-modeling` | engineering | 已核实来自 Matt，提前导入已撤回；来源核实不算用途与内容审核。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/domain-modeling) |
| `grill-with-docs` | engineering | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/grill-with-docs) |
| `implement` | engineering | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/implement) |
| `implement-spec` | engineering | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/implement-spec) |
| `improve-codebase-architecture` | engineering | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/improve-codebase-architecture) |
| `pr` | engineering | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/pr) |
| `prototype` | engineering | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/prototype) |
| `research` | engineering | 曾用作 brief 编写参考；AI 查阅资料不算用户逐项审阅。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/research) |
| `retro` | engineering | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/retro) |
| `setup-matt-pocock-skills` | engineering | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/setup-matt-pocock-skills) |
| `tdd` | engineering | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/tdd) |
| `to-spec` | engineering | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/to-spec) |
| `to-tickets` | engineering | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/to-tickets) |
| `triage` | engineering | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/triage) |
| `wizard` | engineering | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/wizard) |
| `chief-of-staff` | in-progress | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/in-progress/chief-of-staff) |
| `claude-handoff` | in-progress | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/in-progress/claude-handoff) |
| `setup-ts-deep-modules` | in-progress | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/in-progress/setup-ts-deep-modules) |
| `git-guardrails-claude-code` | misc | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/misc/git-guardrails-claude-code) |
| `migrate-to-shoehorn` | misc | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/misc/migrate-to-shoehorn) |
| `scaffold-exercises` | misc | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/misc/scaffold-exercises) |
| `setup-pre-commit` | misc | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/misc/setup-pre-commit) |
| `grill-me` | productivity | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/productivity/grill-me) |
| `grilling` | productivity | 提前导入已撤回，保留候选链接，等待逐项审阅。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/productivity/grilling) |
| `handoff` | productivity | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/productivity/handoff) |
| `to-questionnaire` | productivity | 候选，未完成用户逐项审核；先前纳入／暂缓建议仅作盘点参考。 | [上游](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/productivity/to-questionnaire) |

## 体系维护项：ask-skills

用户明确表示「ask-skills可以加入」，已确认保留，归 productivity，保持手动调用、仅推荐而不安装或执行任务。此前未获确认便进入源码和发布的遗漏已记录，统一准入检查不再区分来源或维护角色。不属于原有 32 项，不改变第一轮计数。见 [确认记录](ask-skills-review.md) 与 [当前说明](../../skills/productivity/ask-skills/SKILL.md)。

## 目录与审查状态

取消本仓库的 in-progress 目录。技能按用途归 engineering、productivity 或 misc；已知问题、实际验证范围与审阅状态写在使用页和审查记录，不再用目录名表达。social-feed、wiki 已审阅保留并归 productivity；deepcoffee-dev 已审阅保留在 engineering，保持手动调用并纳入默认清单。

目录迁移不代替内容审阅。deepcoffee-dev 已获用户确认并纳入默认清单；wiki 已获用户确认整改与更名，纳入默认清单并保持手动调用。其他既有安装不受本次更名影响。

## 每次审阅通过后的更新约定

继续更新本文件，并在回复中列出已审阅保留的技能及目录、brief 等其他明确处理，以及**第一轮原有技能的全部待审名称**。Matt 候选只列第二批进度和链接，按用户要求再展开；ask-skills 单列为体系维护项。原有 32 项、第二批候选与新增入口不再合并成一个待审总数。更名或已计数技能完成整改不重复计数。

OpenAI 官方项目按用户明确要求直接跳过，不逐项等待确认；其他第一轮项目继续审阅，再推进第二批引入评估。用户可以随时指定其他顺序。新第三方技能须逐项审阅并明确确认后才纳入，这份清单本身不导入任何候选。
