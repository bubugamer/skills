# 用途分类与显式发布清单

状态：采用；初始日期：2026-10-11；当前修订：2026-10-20。

技能按 engineering、productivity、misc 三种用途归类，deprecated 留迁移说明。用户要求取消 in-progress，已知问题和用户审阅状态在文档与 catalog 中记录，不设试用目录或统一晋升门槛。

插件和默认安装使用 catalog 生成的显式技能列表，不扫描整个树。用途目录、审阅状态、发布范围和调用方式各自独立；移动位置不代替用户确认，也不自动启用原本被排除的待审项。deepcoffee-dev 已于 2026-10-20 获用户确认审阅通过，纳入默认清单并保持手动调用；social-feed 已确认保留，wiki 已于 2026-10-16 获准整改更名，二者归 productivity 并进入默认清单。`release: false` 只记录具体技能已有的发布排除，不建立新的试用制度。

第一轮只审原有 32 项；Matt 候选第二批评估是否引入，体系新增入口单列。未确认的第三方候选不进入源码、catalog、安装或发布清单；teach 已明确获准，wait-what 是原有安装。

metadata 与使用文档由 catalog.json 生成，维护源数据后运行 scripts/sync_catalog.py。结构检查和实际行为验证分别记录。当前只服务 Codex，AGENTS.md 是实际规则入口。
