# Matt 写作技能纳入

日期：2026-10-21。用户明确表示「matt关于writing的skill也算是审核通过了，也纳入到我的项目里面吧」。本次指向此前已完整比较并列举场景的四项：writing-fragments、writing-shape、writing-beats、writing-for-agents。它们先获得本次确认，再进入当前源码、catalog 和默认清单；不据此扩大其他候选的纳入范围。

## 版本与来源

采用先前审阅的固定提交 `49dd158d1076134a641b33efb035946536778336`，避免把新的未读版本当作已审核内容。GitHub API 获取四个入口、上游界面配置、配套 SKILL-MECHANICS.md 与根目录 MIT 许可；四个入口和配套说明的原始 SHA-256 均与 [此前比较](writing-master-matt-comparison.md) 记录一致。

| 技能 | 用途 | 当前目录 | 调用方式 | 固定上游 |
| --- | --- | --- | --- | --- |
| writing-fragments | 访谈并记录素材片段 | productivity | 手动 | [原文](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/in-progress/writing-fragments) |
| writing-shape | 从固定素材逐块组织文章 | productivity | 手动 | [原文](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/in-progress/writing-shape) |
| writing-beats | 逐次选择叙述方向共同写作 | productivity | 手动 | [原文](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/in-progress/writing-beats) |
| writing-for-agents | AI 指令文档的表达与组织 | productivity | 正常自动选择，也可手动指定 | [原文](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/productivity/writing-for-agents) |

上游的 in-progress 只是来源位置；本仓库仅按用途分类，不建立试用目录。每项目录保留 MIT 许可、原作者版权及来源指纹，不冒称原创或上游未修改发行版。

## 五列适配记录

| 内容 | 取舍 | 原因 | 位置 | 使用影响 |
| --- | --- | --- | --- | --- |
| 英文 description 与正文 | 全文保留 | 用户偏好沿用原版方法，中文回复不要求翻译技能文本 | 四项 SKILL.md | 正文唯一新增为末尾 Reply in Chinese. |
| 旧宿主手动调用标记 | 映射到 Codex 配置 | 保留上游调用选择，同时使用当前宿主支持的设置 | agents/openai.yaml | 前三项手动，writing-for-agents 自动选择 |
| 上游界面名称与简介 | 保留 | 来源已有适合的展示文案 | catalog 的 interface 及生成配置 | 默认提示补齐，已有集合的界面配置不变 |
| SKILL-MECHANICS.md | 保留主体，调整调用与路由段 | 原文把旧宿主调用字段及 description 可见性当作通用机制；不能直接用来指导 Codex | writing-for-agents 配套文件 | 保留 name/description，用 policy 配置调用；路由只推荐；原文与改后指纹均可核对 |
| 素材与文章工作方式 | 保留原版 | 文件化访谈及逐步共写是这些入口的实际用途 | 各入口及中文使用页 | 素材／稿件路径由用户指定，保存前读取现状；阶段选择不自动串联全部流程 |
| 个人 writing-styles | 独立保留 | 个人文风与写作阶段分工不同 | 原有文风入口和参考 | bbs／research-analysis 不被替换，也不自动附加到每项阶段技能 |

## 使用与计数

每项补充两条使用场景和三条行为场景定义，README 与对应使用页合计增加八条场景。ask-skills 推荐表同步，原先将 writing-shape 当作未纳入候选的场景改为当前事实；仅推荐和手动调用约定保持。

当前已确认保留 23 项，包含 21 项仓库源码与 2 项外部说明，默认清单 21 项，公开场景 52 条。第一轮原有 32 项仍全部处理完毕、待审 0 项。第二批原 36 项候选本次纳入 4 项，剩余 32 项；提前引入 teach、原有 wait-what 和体系新增 ask-skills 不重复计数。

## 验证范围

逐项核对原文、英文正文差异、许可、配套引用、Codex 调用配置和隔离安装；实际检查结果集中在 [验证记录](verification.md)。结构和安装检查不代表已经实测写作质量或自动触发效果。没有额外模型评测、代理任务，也没有同步或替换本机现有安装。
