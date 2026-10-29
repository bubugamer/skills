# Matt 全部 skills 的纳入判断

先审查自己的 32 项，再基于真实缺口判断。 本页记录候选审查建议，只有用户逐项确认的技能才可纳入集合。参考提交：49dd158d1076134a641b33efb035946536778336（1.3.1）。总共 38 项：27 个工程/生产力正式入口、4 个 misc、7 个试用；作者插件只发布前 27 项。

当前已采用 7 项（含原有 wait-what、teach、四项写作技能及 grilling），剩余候选 31 项。grilling 采用 2026-10-29 核对的 59db609eb1e18aaf59b63284d0e52255aff0c63c 版本，其他条目枚举仍沿用初始快照。本页保留用途盘点与候选建议；哪些已逐项讨论、哪些已获用户确认，统一见 [合并审查清单](review-checklist.md)。借鉴设计原则与用户完成技能审核分别记录。

| 作者分类 | Skill | 决定 | 为什么 |
| --- | --- | --- | --- |
| engineering | [ask-matt](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/ask-matt) | 借鉴 | 已改成覆盖自己的全部类别的 ask-skills；不保留只列作者工程入口的路由。 |
| engineering | [code-review](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/code-review) | 优先后续 | 区分工程质量和是否满足需求，有明显价值；原版并行审阅者策略需按当前授权适配。 |
| engineering | [codebase-design](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/codebase-design) | 优先后续 | 共享模块与接口设计语言，适合补齐工程方法；需结合真实项目验证。 |
| engineering | [diagnosing-bugs](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/diagnosing-bugs) | 候选，待用户逐项审核 | 候选用途是复现故障并验证修复；待用户逐项审阅其用途、边界与现有能力重合。 |
| engineering | [domain-modeling](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/domain-modeling) | 候选，待用户逐项审核 | 候选用途是统一业务术语、词汇表与重要决策记录；待用户逐项审阅后决定是否纳入。 |
| engineering | [grill-with-docs](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/grill-with-docs) | 后续组合 | 很短的组合入口，依赖 grilling 与 domain-modeling；先验证底层方法，再决定是否需要独立按钮。 |
| engineering | [implement](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/implement) | 后续组合 | 主要组合 tdd 与 code-review；避免重复已有项目交付流程，先把方法验收完成。 |
| engineering | [implement-spec](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/implement-spec) | 暂缓 | 依赖任务图、隔离工作区、多代理和集成策略；先把单次实现流程跑稳，需要时再授权并行。 |
| engineering | [improve-codebase-architecture](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/improve-codebase-architecture) | 后续适配 | 适合真实架构痛点的候选比较；先建立 codebase-design 与可衡量问题，而非默认全库审查。 |
| engineering | [pr](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/pr) | 借鉴现有 | 可以加强 gh-address-comments、项目交付中的问题与结果描述；暂不再建同职责入口。 |
| engineering | [prototype](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/prototype) | 借鉴现有 | 与 ui-ux-pro-max、浏览器工具互补；优先借用逻辑和界面分支、可丢弃原型的验证方式。 |
| engineering | [research](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/research) | 借鉴现有 | 比 deep-research 轻，适合采用一次问题、原始来源、明确产物的设计；保留个人阅读和研究入口。 |
| engineering | [retro](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/retro) | 优先后续 | 将反复故障转成自动检查与规则，适合维护 skill 体系；需以实际任务失败为输入。 |
| engineering | [setup-matt-pocock-skills](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/setup-matt-pocock-skills) | 后续适配 | 项目配置有价值；改成自己的工作区与交付配置，不默认创建作者的 tracker 标签。 |
| engineering | [tdd](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/tdd) | 优先后续 | 行为与公共边界测试有价值；按实际变化选检查，不强制为可逆低影响改动写镜像测试。 |
| engineering | [to-spec](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/to-spec) | 优先后续 | 自己的工程体系缺少从已讨论结论生成需求说明的能力；要加入用户用例与验收，保存位置服从项目。 |
| engineering | [to-tickets](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/to-tickets) | 优先后续 | 端到端小任务与依赖关系有价值；先确定任务载体，区分总说明与真正可执行任务状态。 |
| engineering | [triage](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/triage) | 后续适配 | 适合 GitHub issue/PR 处理；现有 gh skills 只覆盖局部，需先定个人分类与就绪标准。 |
| engineering | [wayfinder](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/wayfinder) | 借鉴现有 | 2026-10-12 对照提醒版 tang-monk：借鉴产出与范围边界；复杂决策地图属于独立能力，不并入提醒入口。 |
| engineering | [wizard](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/wizard) | 后续适配 | 人工登录或控制台设置可形成有停止条件的流程；有真实人工瓶颈时再纳入。 |
| in-progress | [chief-of-staff](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/in-progress/chief-of-staff) | 暂缓 | 实验型长期协调入口范围很大，涉及 Codex 会话调度；不纳入本轮提醒能力收敛。 |
| in-progress | [claude-handoff](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/in-progress/claude-handoff) | 暂缓 | 依赖 Claude CLI，Codex 可使用自身交接能力。 |
| in-progress | [loop-me](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/in-progress/loop-me) | 借鉴现有 | 2026-10-12 对照提醒版 tang-monk：借鉴单一用途和简短入口；重复流程的设计另行评估，不并入提醒入口。 |
| in-progress | [setup-ts-deep-modules](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/in-progress/setup-ts-deep-modules) | 按需纳入 | 只针对 TypeScript 模块边界；有明确项目结构时再验证 dependency-cruiser 规则。 |
| in-progress | [writing-beats](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/in-progress/writing-beats) | 已确认纳入 productivity | 2026-10-21 用户明确批准；逐次选择叙述动作共写，保留原英文及 MIT，按 Codex 映射调用设置。见 [纳入记录](writing-skills-adoption.md)。 |
| in-progress | [writing-fragments](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/in-progress/writing-fragments) | 已确认纳入 productivity | 2026-10-21 用户明确批准；素材探索与片段记录，保留原英文及 MIT，按 Codex 映射调用设置。见 [纳入记录](writing-skills-adoption.md)。 |
| in-progress | [writing-shape](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/in-progress/writing-shape) | 已确认纳入 productivity | 2026-10-21 用户明确批准；从已有素材逐块成文，保留原英文及 MIT，按 Codex 映射调用设置。见 [纳入记录](writing-skills-adoption.md)。 |
| misc | [git-guardrails-claude-code](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/misc/git-guardrails-claude-code) | 暂缓 | Claude PreToolUse hook，当前只用 Codex，不能直接采用。 |
| misc | [migrate-to-shoehorn](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/misc/migrate-to-shoehorn) | 暂缓 | 仅 TypeScript 测试数据迁移；当前没有对应迁移需求。 |
| misc | [scaffold-exercises](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/misc/scaffold-exercises) | 暂缓 | 依赖作者课程结构与 ai-hero-cli，不是通用个人工作流。 |
| misc | [setup-pre-commit](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/misc/setup-pre-commit) | 按需纳入 | 针对有明确 lint/typecheck 工具链的项目使用；本仓库已有提交后检查，不默认添加 JS 工具链。 |
| productivity | [grill-me](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/productivity/grill-me) | 后续组合 | 只是 grilling 的手动入口；grilling 已获准并可直接手动指定；本包装入口仍未确认纳入。 |
| productivity | [grilling](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/productivity/grilling) | 已确认纳入并安装 | 2026-10-29 用户明确批准；保留分轮访谈原文，仅适配代理授权并追加中文回复，见 [记录](grilling-review.md)。 |
| productivity | [handoff](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/productivity/handoff) | 优先后续 | 任务切换时小型交接有价值；要使用当前 Codex 会话/工作区能力，不默认开启新会话。 |
| productivity | [teach](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/productivity/teach) | 已按用途正式纳入，手动调用 | 2026-10-13 用户确认与 read 独立；恢复完整英文教学正文，仅适配 Codex 调用记号与手动调用设置，中文使用说明单独维护。 |
| productivity | [to-questionnaire](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/productivity/to-questionnaire) | 按需纳入 | 给第三方的问卷和给用户自己的追问不同；有明确对象与信息缺口时再增设。 |
| productivity | [wait-what](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/productivity/wait-what) | 已改善现有 | 原有集合，第一轮已确认保留；仓库按用户要求保留英文说明，正文仅追加 Reply in Chinese.，保留 MIT、出处与 Codex 手动配置。见 [审阅](wait-what-review.md)；不计入第二批候选。 |
| productivity | [writing-for-agents](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/productivity/writing-for-agents) | 已确认纳入 productivity | 2026-10-21 用户明确批准；AI 指令文档的表达与组织，保留原英文及 MIT，按 Codex 映射调用设置。见 [纳入记录](writing-skills-adoption.md)。 |

## 本轮与后续顺序

先按用户既定顺序审阅原有技能，再逐项讨论外部候选，由用户明确确认后纳入。teach 已获逐项确认，当前保留完整英文版本。domain-modeling、diagnosing-bugs、grilling、writing-for-agents 曾被提前导入，2026-10-14 已纠正撤回，仅保留候选链接。2026-10-21 用户明确批准 writing-for-agents 及 writing-fragments、writing-shape、writing-beats 纳入；之前撤回记录保留为历史，不再将 writing-for-agents 视为当前候选。其他纳入建议仍只表示待讨论提案，不构成用户批准。

入选条件是自身缺口与可验证收益，不是作者数量更多。类似能力优先借鉴和改善，避免同一任务有多个互相争夺的入口。

2026-10-29 用户明确批准仅将 grilling 纳入项目及本地，先前撤回记录保留为历史；grill-me、grill-with-docs、domain-modeling、wayfinder 均不随之引入。
