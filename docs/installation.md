# 安装与调用

截至 2026-10-29，已接入 22 项仓库技能；本次按用户明确批准，仅追加 grilling。完整调用名为 `$bubugamer-skills:grilling`，保留正常自动选择；实际本地发现已核对，其他安装及用户配置保持。

2026-10-21 用户明确要求安装本地版本，本次已完成统一接入：21 个已确认的仓库技能安装到 `~/.agents/skills`，以链接读取仓库源码；agent-browser、find-skills 两项外部能力沿用原安装。11 个旧目录和 5 个旧链接完整归档后退出原发现位置，运行依赖单独保留。下方按日期的此前迁移与暂缓约定保留为历史，不作为当前未安装状态。

这个仓库是源码与维护入口。除用户明确授权的名称或退出迁移外，现有安装保持不变。默认发布清单不包括 deprecated、外部依赖或明确设置 release: false 的条目。不要同时用插件和本地链接安装同一批技能。

## 本地源码方式

在仓库根目录先检查与预览：

```bash
python3 scripts/validate.py
python3 scripts/install.py
```

预览不会创建目录。存在 `.agents/skills`、legacy `.codex/skills` 的同名技能、TangMonk、dongnaojin-yeye、konmari、llm-wiki 或 writing-master 旧名时，报告冲突并停止整批安装。脚本没有强制覆盖选项；先制定备份与迁移方案。

可以只选没有冲突的正式技能：

```bash
python3 scripts/install.py --skill ask-skills
python3 scripts/install.py --skill ask-skills --apply
```

本次 Codex 实际发现名称为 `bubugamer-skills:<技能名>`，例如 `$bubugamer-skills:ask-skills`、`$bubugamer-skills:writing-fragments`。在选择器中可搜索短名称。用户配置增加运行绑定并关闭系统同名 skill-creator 入口后，需要重启 Codex 刷新配置；系统文件保留。目录按用途归类，调用方式及已知问题继续按使用页维护。

## Codex 插件方式

仓库提供 `.codex-plugin/plugin.json` 兼容格式与 `.agents/plugins/marketplace.json`。官方仍支持此兼容格式，采用明确路径列表维护默认发布范围，不通过目录位置推断用户审阅状态。公开 GitHub 发布后可以添加目录源：

```bash
codex plugin marketplace add bubugamer/skills --ref main
codex plugin add bubugamer-skills@bubugamer
```

已有同名的独立安装时，先完成迁移，再安装插件。不要把命令示例当作已在用户环境执行过的证明。插件是否被当前桌面会话加载、以及每项能力的实际行为需要分别检查。

## 外部能力

外部依赖已有独立使用页和上游链接。优先当前 Codex 系统或插件提供的能力，避免同名重复安装。需要 CLI 时现场检查工具、权限和认证状态；登录状态与 API 密钥只放本地。

出处：[Codex 技能与工作区范围](https://learn.chatgpt.com/docs/build-skills)、[官方插件封装与 marketplace](https://developers.openai.com/plugins/build/plugins)。

## 2026-10-13 已授权的迁移

用户确认动脑筋爷爷更名为 read、teach 独立加入体系，以及 brief 退出技能集合。源码入口和安装别名同步维护；旧内容保留备份，不覆盖用户的其他安装。teach 当时作为手动试用引入，当前分类见下方 2026-10-14 更新。

本地 read 已按用户授权更名，个人工作区与原笔记约定暂时保留，目录模型最后统一整理；公开源码不包含个人路径。teach 通过独立链接读取仓库源码，保持手动调用。其他安装仅同步相关旧名称引用，抓取与知识维护方法未重写。

brief 的仓库版与本地旧安装迁入用户的独立定时任务项目归档；该迁移只保存方法与消息源，不创建调度。完整范围见 [本轮审查](audit/reading-learning-review.md)。

## 2026-10-14 分类整理

取消「新能力先试用」要求后，已由用户逐项审阅确认的 teach 进入 productivity，保持原有手动调用方式。本地已有的 teach 链接随目录移动更新，其余现有安装保留原样。

同日纠正提前导入：domain-modeling、diagnosing-bugs、grilling、writing-for-agents 未获用户逐项确认，已从当前源码、catalog、推荐、安装与发布清单撤回，仅在上游候选审查文档保留链接。取消试用要求只调整已获准技能的分类。

2026-10-14 曾因已知问题保留三个 in-progress 项；2026-10-15 按用户要求取消该目录，当前分类见下方更新和 [文件清单](directory-map.md)。

## 2026-10-15 para 更名整改

用户授权 konmari 的 PARA 收敛与更名。原安装和整改前源码完整备份在本机 skill-archive；旧 konmari 安装退出可发现目录后，以 para 链接到本仓库正式源码。安装器继续识别 konmari 旧名冲突，不自行覆盖旧安装。

PARA 更名当时仅同步其他既有技能中的相关名称引用；提醒技能后续的 remind 更名见下节。真实资料目录未执行 PARA 重建；验证使用自动清理的临时样例。当前对话的技能列表可能仍保留打开时的旧快照，重新加载技能后使用 `$para`。

## 2026-10-15 remind 更名

用户要求将 tang-monk 统一更名 remind。正式源码和本地入口采用 remind；原本机 TangMonk 安装与更名前提醒版源码完整备份在 skill-archive。个人任务目录不随技能更名迁移。

安装器检查 TangMonk 和 tang-monk 两个旧名，存在任一个就报告冲突并停止，不覆盖既有内容。本次有明确更名授权，备份后将原安装退出发现目录，再将 remind 链接到正式源码。其他既有安装只同步必要引用。

通过 `$remind` 使用。若当前会话仍显示打开时的旧技能列表，重新加载技能后即可看到新名称。

## 2026-10-15 取消 in-progress，原有技能优先审阅

移除 skills/in-progress 与 docs/in-progress。deepcoffee-dev 归 engineering；llm-wiki、social-feed 归 productivity，技能正文、脚本和手动调用方式保持。三项在本机都是独立安装，本次源码目录变化无需改写这些个人安装。

social-feed 已获保留确认，进入用途目录和默认发布清单。deepcoffee-dev、llm-wiki 尚待第一轮内容审阅，用 release: false 继续记录此前已有的默认发布排除，避免目录移动同时启用它们。既有个人安装保留。公开集合的完整默认清单以 catalog 和插件配置为准。

第一轮仅原有 32 项；2026-10-16 wiki 通过后，当前待审 25 项；Matt 其他候选第二批评估是否引入，ask-skills 单列体系维护，不合并为一个待审数。

## 2026-10-16 wiki 更名整改

用户确认 llm-wiki 改为 wiki，移除知识库自测，其余方案认可。正式入口为 `$wiki`，归 productivity，保持手动调用并纳入默认清单。自测使用 teach；知识库自身的目录与站点设置另行维护。

原源码、草案和本机旧安装先完整备份，再按本次授权将旧安装退出发现目录，以 wiki 链接读取正式源码。安装器识别 llm-wiki 旧名冲突，不替用户覆盖或迁移其他安装。当前对话的技能列表可能仍是启动时快照，重新加载后使用新名称。真实知识页、个人项目配置与服务不随本次改造变更。


## 2026-10-19 writing-styles 更名

用户确认多文风方案并授权实施。writing-master 已更名 writing-styles，归 productivity，继续允许自动选择，保留 bbs 与 research-analysis 两种文风。

改前源码和本机原安装完整备份并核对文件指纹后，原安装退出发现目录，新入口链接到正式源码。安装器识别 writing-master 旧名冲突；普通安装仍不覆盖或迁移已有目录。其他既有安装、用户稿件与 Matt 候选不随本次更名变更。当前会话的技能列表可能保留启动时名称，重新加载后按新名称使用。


## 2026-10-20 deepcoffee-dev 审阅通过

用户确认本轮整理完成，deepcoffee-dev 进入默认安装与发布清单，保持手动调用。专属规则继续随 skill 及六篇参考维护，三个原脚本仍为现有本地运行依赖。本次只更新仓库发布设置与隔离安装检查，本机安装按既有决定留待统一处理。

## 2026-10-20 第一轮收尾

原有 32 项均已确认处理，仓库版本已整理；本机旧安装尚未统一迁移。skill-creator 按用户最终要求同时负责创建、维护与评测，普通安装仍检测已有同名目录并停止；系统同名入口的实际选择也须在后续迁移时核对。不要把当前源码发布视为已更换本机能力。

skill-creator 的离线辅助工具需 Python 3 和 PyYAML（见技能内 requirements.txt）；只有明确执行实时触发探针时才需可用 Codex CLI 及相应模型调用。预览、任务汇总与本地评阅页生成不启动模型调用。

## 2026-10-21 Matt 写作技能纳入

用户明确批准 writing-fragments、writing-shape、writing-beats、writing-for-agents 纳入，四项均归 productivity 并进入默认清单。前三项保持手动调用，writing-for-agents 正常自动选择；中文使用场景见各自使用页。固定版本、许可与必要适配见 [纳入记录](audit/writing-skills-adoption.md)。只发布仓库版本，不同步本机安装；现有同名能力仍按安装器规则报告冲突，不覆盖。此前 writing-for-agents 撤回记录保留为历史。


## 2026-10-21 已授权统一安装

本次授权来自用户在审阅完成后明确提出「将这些 skill 安装到本地」，并沿用先前仓库为主、旧版随后退出的决定。普通 install.py 仍不覆盖或移动冲突项；这次是先记录具体迁移计划、固化指纹和配置备份，再按已授权范围归档旧入口，之后调用普通安装器创建链接。

实际结果：21 个链接、11 个旧目录与 5 个旧链接归档；两项外部能力保留，其他官方能力及用户工作区不变。实际重复安装创建 0 个新链接。Codex skills/list 返回全部 21 项启用并指向仓库、0 个加载错误，系统同名 skill-creator 入口为禁用；文件未删除。不能将源码链接已存在代替实际发现验证。

本地运行环境和配置不进入公开源码。保留两套行情 Python 环境并通过依赖及帮助检查；UI 数据库另存运行目录并通过列表与 UX 查询；三个现有 DeepCoffee 脚本只绑定位置，没有执行项目操作。个人完整计划、改前配置、指纹和恢复说明留在本机 skill-archive；公开记录见 [安装验证](audit/verification.md)。

官方依据：[本地发现、链接和启停配置](https://learn.chatgpt.com/docs/build-skills)。实际安装与发现结果优先于通用命令示例。

## 2026-10-29 追加 grilling

用户明确批准项目与本地均安装，仅将 grilling 纳入 productivity 并用正常安装器追加链接。首次预览无冲突，创建 1 个链接；再次执行创建 0 个。独立 Codex skills/list 在技能仓库和用户主目录两处均返回全部 22 项仓库技能启用、0 个加载错误，新增名称为 bubugamer-skills:grilling。用户配置指纹保持，没有替换旧安装或一并安装其他访谈入口。来源及适配见 [纳入记录](audit/grilling-review.md)，个人路径与实际发现记录仅留在本机。
