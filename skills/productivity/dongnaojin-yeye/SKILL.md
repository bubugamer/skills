---
name: dongnaojin-yeye
description: Read, summarize, translate, explain background, judge whether supplied material is worth reading, or trace its original source. Save reading entries or notes when the user asks to save, collect, or record them. Do not use for general life logging or task priorities.
---

# 动脑筋爷爷

围绕用户给出的材料完成阅读、解释与出处判断。

1. 区分这次意图：阅读价值判断、摘要、翻译、背景、出处追溯、保存入口或稳定笔记。
2. 获取足以支撑回答的正文。普通网页直接读；遇到渲染、跳转或登录障碍时参考 site-unlocker；PDF、文档、音频使用当前可用的相应工具。
3. 登录墙、标题和极短预览不算已读正文。拿不到有效内容时明确报告，保留已知来源信息，不编造摘要或阅读价值。
4. 在会话里交付结果。阅读价值判断使用「现在读 / 先收藏 / 可跳过」，给出与用户目标有关的理由。出处判断分清已验证事实、推断与未验证部分；按需读取 references/source-evaluation.md。
5. 用户要求「保存 / 收藏 / 记下来 / 沉淀」时，先确定目标知识库，按 references/routing-rules.md 选择位置，再按 references/note-templates.md 保存。用户的持续授权适用于已指定工作区。普通总结、翻译和讨论本身不启动写入。
6. 多轮共读按收束后的结论单元记录。保留旧结论和来源；收到明确编辑要求时才改原文。报告实际写入的位置。

## 工作区与写入边界

`<knowledge-root>` 是用户指定的知识库根目录。优先读当前项目的 docs/agents/skill-workspace.md；没有配置时，只在真正需要保存而目标不明时询问。不要猜测个人目录，不把占位符当成真实路径。

- 只判断值不值得读：会话回答；若同时要求收藏，更新阅读队列，不顺带创建伴随笔记。
- 已进入摘要或共读：会话回答；若同时要求保存，记录已收束的结论。
- 尚未获取正文：不创建空笔记；用户明确要求先记入口时，可保存一个标明未读取的链接。
- 学习或调研计划：按明确计划请求处理，普通解释不新建项目。
- 稳定知识整理：已有笔记需要编译、交叉链接或知识库查询时，选择 llm-wiki；该能力在本集合仍是试用项。
- 通用优先级与任务状态：选择 tang-monk；文件结构：选择 konmari。

## 完成条件

实际读到的内容能支持结论；引用能回到原始来源；没有把推断写成事实；写入范围与本次要求一致。
