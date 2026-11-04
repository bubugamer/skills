# 第一轮收尾

日期：2026-10-20。原有 32 项均已确认处理，第一轮待审为 0。处理结论与逐项依据集中在 [分批审查清单](review-checklist.md)；审阅通过表示确认用途、去留和整改，不表示全部线上行为都已验证。

## 最终集合

| 类型 | 数量 | 内容 |
| --- | --- | --- |
| engineering 已确认保留 | 5 | deepcoffee-dev、ui-ux-pro-max、skill-creator、plan-eng-review；agent-browser 为外部使用说明 |
| productivity 已确认保留 | 18 | remind、read、para、site-unlocker、social-feed、wiki、writing-styles、wait-what、teach、deep-research、ask-skills、writing-fragments、writing-shape、writing-beats、writing-for-agents、grilling、handoff；find-skills 为外部使用说明 |
| misc 已确认保留 | 3 | akshare-api、tdx-api、yt-dlp-download |
| 原有技能迁出 | 1 | brief：方法和消息源已移到独立定时任务项目，尚未创建调度 |
| 官方能力跳过 | 14 | 按用户要求直接沿用 OpenAI 官方来源，不纳入个人库；[逐项名单](openai-official-exclusions.md) |
| 第一轮待审 | 0 | 无 |

原有保留 17 项 + brief 迁出 1 项 + 官方跳过 14 项 = 原有 32 项。teach 是提前确认引入的能力，ask-skills 随后获用户明确批准加入，2026-10-21 四项 Matt 写作技能获准纳入，2026-10-29 再纳入 grilling，另有 2026-11-02 用户批准的 gstack plan-eng-review，2026-11-04 再纳入 Matt handoff，当前已确认保留共 26 项。

当前 catalog 共 26 项：24 项有仓库入口，2 项只登记外部能力。24 项入口中含已获准的体系维护入口 ask-skills。README 和使用页收录 26 项已确认技能的 59 个代表场景，场景定义不冒称已执行评测。

## 最终决定

skill-creator 按用户最终要求将创建、改进与评测合在同一入口，不建立独立评测技能。短入口按任务选择四篇参考；新工具修正错误／超时的统计，保留未知测量及可核对的任务对照，评阅页保留已有文件与反馈。没有复制旧打包器、无关技能包或系统技能。

已取消 in-progress。正式技能按用途归 engineering、productivity、misc，状态、调用方式、已知问题及发布范围分别记录。第一轮收尾时只整理与发布仓库；2026-10-21 用户随后明确授权本地接入，现已完成 21 项链接安装、旧版归档与系统同名入口选择。见 [安装说明](../installation.md)。

## 核对与限制

具体输入、检查结果及覆盖范围见 [验证记录](verification.md)。文件、安装保护和脚本检查不能证明实际模型效果；合成评阅样例用于核对页面与反馈交互，不是能力提升证据。真实登录抓取、完整行情链路、生产操作和独立模型效果未纳入本次收尾验证，已有问题继续保留在对应使用页。

## 按需查阅

Matt 第二批原有 36 项候选，已纳入四项写作技能、grilling 和 handoff。剩余 30 项暂停批量审阅，留作按需检索资料，其中 4 项做过相邻方法比较。ask-skills 单列为体系维护。见 [审查清单](review-checklist.md) 和 [技能来源资料库](../../skills/productivity/ask-skills/references/skill-sources.md)。

公开仓库：[bubugamer/skills](https://github.com/bubugamer/skills)。

2026-10-29 用户批准 grilling 项目与本地均安装，当前已接入 22 项仓库技能；该次增量安装和最小适配见 [记录](grilling-review.md)，第一轮原有数量保持。

2026-11-02 gstack plan-eng-review 经用户明确批准后单列外部扩展，不改变第一轮或 Matt 第二批计数；当前接入 23 项仓库入口。见 [纳入记录](plan-eng-review-adoption.md)。
