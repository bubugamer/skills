# Codex 调用策略

每个技能保持 name 与 description。agents/openai.yaml 控制手动或自动选择；试用项统一 allow_implicit_invocation: false，正式项按 catalog.json 的 manual 属性生成。

按当前工具的技能机制加载入口，不假设存在 Skill 工具。路由仅推荐。缺少外部能力时说明依赖，不自动安装多个工具。用户已明确选择任务时，不必先经过路由。

安装只选择一个入口：正式 plugin 或受控本地链接；同名技能与 TangMonk/tang-monk 旧名视为冲突。当前 legacy .codex 与 .agents 安装仍可能共存，按实际路径核查。
