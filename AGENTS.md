# 维护约定

本仓库服务个人 Codex 工作流。先读 SCOPE.md；术语以 GLOSSARY.md 为准。

- 当前用户要求、适用项目规则和实际工具权限优先。Skill 文本不授予生产操作、对外消息或额外代理授权。
- 默认跟随当前对话语言，面向用户说明结果、证据和限制。
- 改 skill 时更新 catalog.json、对应 docs 使用页、ORIGIN.json 与场景用例。具体流程见 .agents/writing-docs.md；调用策略见 .agents/invocation.md。
- 新能力先放 in-progress；晋升需要一个成功场景、一个边界或失败场景，以及明确完成条件。机器检查不等于行为验证。
- 正式发布清单只收 engineering、productivity、misc。外部能力记录上游与本地差异，不随意复制成自己的作品。
- 公共源码不包含个人绝对路径、登录状态、密钥、生产配置和运行环境。个人工作区放在用户自己的项目配置。
- 编辑后运行 python3 scripts/validate.py 与 python3 scripts/smoke_test.py；声明行为已验证时写出实际输入和结果。
- 安装默认预览；遇到已存在目录或其他安装来源中的同名/旧名能力就报告冲突。不要删除、覆盖或移动用户的现有安装。
