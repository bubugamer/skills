# Codex 技能入口与调用

SKILL.md 必须有 name 和 description；description 用任务意图区分邻近能力，避免只罗列同义词。

自动或手动可用：agents/openai.yaml 中 policy.allow_implicit_invocation 为 true（或使用默认策略）。仅手动：设为 false。手动项仍保留描述，作为用户选择时的说明。

本集合试用项统一仅手动；正式项是否允许自动选择由 catalog.json 的 manual 属性决定。不要用 Claude 的 frontmatter 字段推测当前 Codex 行为。

当前有技能调用工具时按其文档使用；没有时读取已发现技能入口和必要参考，不编造 Skill 工具。路由入口只推荐能力，不批量安装或隐式触发手动技能。
