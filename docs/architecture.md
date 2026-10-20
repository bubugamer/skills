# 体系架构与参考系统

参考快照：Matt Pocock skills 1.3.1，提交 49dd158d1076134a641b33efb035946536778336。原项目有 38 个技能，正式 engineering 20、productivity 7、misc 4，试用 7，deprecated 当前为空。作者插件只发布工程与生产力 27 项；misc 在仓库保留但没有纳入其插件。我们的正式集合包含专用工具，因此把自己的 misc 纳入明确发布清单。

本仓库按 engineering、productivity、misc 三种用途归类，deprecated 留迁移说明；取消 in-progress。已知问题、用户审阅状态、默认发布设置与调用方式分别维护。第一轮只审阅原有 32 项，Matt 尚未引入的技能作为第二批扩展候选。

## 目录的作用

| 位置 | 谁读、解决什么 |
| --- | --- |
| README.md | 用户入口、正式列表、文档导航。由 catalog.json 生成。 |
| AGENTS.md | 维护本仓库的规则；当前只用 Codex，不增加重复的 CLAUDE.md。 |
| GLOSSARY.md | 定义体系术语，不收执行计划和技术决策。 |
| SCOPE.md | 收录边界、分类依据与退出说明。 |
| CHANGELOG.md | 说明每版实际变化。 |
| catalog.json | 记录分类、选择理由、来源、例子、依赖与调用策略。 |
| skills/用途分类/名称/SKILL.md | AI 操作入口。 |
| 每个技能的 agents/openai.yaml | Codex 展示信息与手动/自动策略。 |
| 每个技能的 references/ | 按条件读取的细节与模板说明。 |
| 每个技能的 scripts/、assets/ | 可执行工具和产物素材，按需存在。 |
| 每个技能的 evals/ | 场景输入与预期；不伪装成已执行结果。 |
| 每个技能的 ORIGIN.json | 原始入口指纹、来源日期和公开版本的改动。 |
| docs/用途分类/ | 给人看的用途、依赖、例子、完成条件与限制。 |
| docs/audit/ | 第一轮原有集合审查、第二批上游引入评估和真实验证记录。 |
| docs/directory-map.md | 当前用途目录与完整文件清单。 |
| docs/agents/ | 工作区配置示例；个人路径与生产配置留在用户项目。 |
| .agents/ | 调用、文档编写、重要维护决策和插件目录清单。 |
| .codex-plugin/ | 默认发布的明确技能清单，不扫描整个树。 |
| .out-of-scope/ | 暂缓原因，避免相同提案反复进入集合。 |
| scripts/ | 生成目录、检查一致性、受控安装和真实样例检查。 |
| .github/workflows/ | 每次提交检查结构与安全安装行为。 |

## 从作者结构取用的原则

1. 共享方法与任务入口分开。read、teach、写作等各自对应任务目的；social-feed、site-unlocker 是可共享的辅助能力。brief 的方法和消息源迁入独立定时任务项目，当前不创建调度。
2. 文档职责分开。使用页、术语、来源、权衡、版本与用例各有承载位置。
3. 路由只帮人选择。ask-skills 对照本集合，覆盖内容、生活与数据任务；不套用只覆盖工程的 ask-matt 名单。
4. 分类与调用策略分别维护。发布清单读取 catalog 的具体发布设置，目录移动不自动批准待审项；手动或自动选择由各技能的调用设置决定。
5. 完成条件是可观察的结果。用例描述要求；执行记录只写实测结果，避免把格式检查当作技能效果验证。

## 没有直接复制的部分

作者的链接脚本会同时写多个工具目录，并可能删除已有同名目录；本版改为预览与冲突阻断。作者的 issue tracker、标签和团队并行实施流程依赖项目配置，不作为默认个人流程。作者个人的英语风格、频繁追问和 Claude 专用工具名也不进入全局规则。

作者有 changesets、版本同步脚本与发布工作流。初版只有一个发布包、没有 npm 依赖，先采用 catalog 版本与一致性检查；需要多维护者或自动发布时再增加 changesets。避免建立没有实际用途的文件。

官方 Codex 机制与作者参考分别见 [Codex 技能文档](https://learn.chatgpt.com/docs/build-skills)、[插件封装文档](https://developers.openai.com/plugins/build/plugins)、[参考源码](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336)。
