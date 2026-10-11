# 发布只收正式清单

状态：采用；日期：2026-10-11。

选择 Codex 兼容 manifest 的显式技能路径列表。通用扫描整个 skills 树可能把 in-progress 与 deprecated 一起发现，因此默认安装与插件只加载三个正式目录。

metadata 与文档由 catalog.json 生成，维护源数据后执行 scripts/sync_catalog.py。结构检查和行为验证分别记录；试用方法即使文本已适配也不自动晋升。

当前只服务 Codex，AGENTS.md 是真实文件；不增设 CLAUDE.md 或跨工具破坏式链接脚本。Codex 支持此兼容布局，来源见 docs/installation.md。
