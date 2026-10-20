# 原有 skills 技术盘点

审查日期：2026-10-11。33 个本地安装目录，32 个不同名称；find-skills 的两个入口文件字节一致。审查了入口说明、资源结构和脚本依赖，未执行部署、删除、付费 API 或登录抓取。

本页是 AI 的技术盘点及后续处理记录，keep、improve 等盘点建议不表示用户已经逐项审核通过。第一轮原有技能与第二批 Matt 引入评估分别见 [分批审查清单](review-checklist.md)。

## 处理记录与盘点建议

| Skill | 分类 | 处理 | 依据与改进 | Matt 对照 |
| --- | --- | --- | --- | --- |
| remind（原 TangMonk／tang-monk） | productivity | keep | 2026-10-12 收敛为待办与想法提醒；旧工作区规则独立存档，见 [逐项审查](tang-monk-review.md)。 | para、writing-styles；wayfinder、loop-me 仅借鉴边界 |
| brief | 已迁出 | 移到定时任务项目 | 2026-10-13 用户确认退出技能集合；方法与消息源保留，调度尚未实现，见 [迁移说明](../deprecated/brief.md)。 | 定时服务 |
| read（原 dongnaojin-yeye） | productivity | keep | 用户确认阅读助手与阅读秘书定位；与 teach 分开，更名与边界见 [本轮审查](reading-learning-review.md)。 | teach、research |
| para（原 konmari） | productivity | keep | 用户确认 PARA 专用定位并授权更名整改；目录映射、执行边界与恢复记录已用临时样例验证，见 [本轮审查](konmari-review.md)。 | wiki（知识内容）、read（阅读） |
| site-unlocker | productivity | keep | 保留真实正文判定；改为优先当前 Codex 浏览器工具，CLI 作为可用时的后备。 | research 的检索前置层 |
| writing-styles（原 writing-master） | productivity | keep | 2026-10-19 用户确认整改与更名，保留 bbs／research-analysis，多文风与共同规则分离，区分审稿、改写及指定文件编辑；见 [定稿](writing-master-review.md)。 | writing-fragments、writing-shape、writing-beats |
| wait-what | productivity | keep | 2026-10-20 用户确认审阅通过；恢复 Matt 英文正文，末尾仅加 Reply in Chinese.，保持手动调用。见 [定稿](wait-what-review.md)。 | read、teach、writing-styles |
| akshare-api | misc | keep | 用户确认独立保留；多来源取数与按需函数检索保持，参数及安装恢复问题列为改进项，见 [确认](akshare-api-review.md)。 | 与 tdx-api 在沪深行情部分重合，其他覆盖互补 |
| tdx-api | misc | keep | 用户确认与 AKShare 分别保留，通达信来源独立；入口和脚本保持，验证范围见 [确认](tdx-api-review.md)。 | 与 akshare-api 行情部分重合，按来源分工 |
| yt-dlp-download | misc | keep | 用户确认并完成整改；精简入口、命令外置，按用户范围与目标格式下载，合成媒体实际验证通过，见 [定稿](yt-dlp-download-review.md)。 | site-unlocker、transcribe 各负责不同媒体处理任务 |
| deepcoffee-dev | engineering | keep | 用户确认整理完成并审阅通过，规则保留在 skill，纳入默认清单且保持手动调用。脚本仍为现有本地运行依赖，见 [确认记录](deepcoffee-dev-review.md)。 | skill 内的交付、维护与知识方法 |
| wiki（原 llm-wiki） | productivity | keep | 2026-10-16 用户认可改造、移除自测；独立工作区约定、六类模板与只读链接／导航检查已落地，见 [本轮审查](llm-wiki-review.md)。 | teach（学习与自测） |
| social-feed | productivity | keep | 脚本硬编码寻找旧的 Playwright 安装路径，且需要登录状态；不把未验证的登录抓取包装成通用可用。 | research 的信息获取层 |
| agent-browser | engineering | 已确认外部保留 | Vercel Labs 第三方浏览器工具，沿用当前 CLI 配套说明，不复制源码；已知限制见 [审阅](agent-browser-review.md)。 | 当前浏览器工具、site-unlocker |
| find-skills | productivity | 已确认外部保留 | 外部发现工具，与 ask-skills 的已有能力推荐分工；候选仍逐项确认，两处安装当前不处理。见 [确认](find-skills-review.md)。 | ask-skills |
| deep-research | productivity | 已确认保留并整改 | 方法参考第三方，已为 Codex 独立重写；精简入口、三篇参考和记录工具，不纳入上游评分器，见 [定稿](deep-research-review.md)。 | read、wiki、writing-styles；Matt research 仍为候选 |
| ui-ux-pro-max | engineering | 已确认保留并整改 | 个人偏好留在 skill；仓库新增短入口及数据／平台、保存适配，外部引擎和资料不复制，见 [定稿](ui-ux-pro-max-review.md)。 | 项目设计系统；Matt prototype 仍为候选 |
| skill-creator | engineering | 已确认保留并整改 | 用户最终确认创建与评测同属一个入口；仓库独立重写入口、四篇参考及工具，修正失败统计，排除旧打包器与嵌套包；见 [定稿](skill-creator-review.md)。 | 系统同名能力留待统一迁移；Matt writing-for-agents 仍为候选 |
| cloudflare-deploy | 官方能力，不收录 | 按用户规则跳过 | 来源登记为 OpenAI 官方，入口与原盘点一致；移出个人集合，本机安装保持。见 [处理记录](openai-official-exclusions.md)。 | 不重复维护官方实现 |
| gh-address-comments | 官方能力，不收录 | 按用户规则跳过 | 来源登记为 OpenAI 官方，入口与原盘点一致；移出个人集合，本机安装保持。见 [处理记录](openai-official-exclusions.md)。 | 不重复维护官方实现 |
| gh-fix-ci | 官方能力，不收录 | 按用户规则跳过 | 来源登记为 OpenAI 官方，入口与原盘点一致；移出个人集合，本机安装保持。见 [处理记录](openai-official-exclusions.md)。 | 不重复维护官方实现 |
| imagegen | 官方能力，不收录 | 沿用官方 | 用户确认审阅通过，通用功能由官方维护，不纳入个人集合；仅保留 [确认记录](imagegen-review.md)，本机安装暂不处理。 | screenshot、可视化工具（产出不同） |
| jupyter-notebook | 官方能力，不收录 | 按用户规则跳过 | 来源登记为 OpenAI 官方，入口与原盘点一致；移出个人集合，本机安装保持。见 [处理记录](openai-official-exclusions.md)。 | 不重复维护官方实现 |
| openai-docs | 官方能力，不收录 | 按用户规则跳过 | 来源登记为 OpenAI 官方，入口与原盘点一致；移出个人集合，本机安装保持。见 [处理记录](openai-official-exclusions.md)。 | 不重复维护官方实现 |
| pdf | 官方能力，不收录 | 沿用官方 | 用户确认直接沿用官方，不纳入个人集合；保留 [确认记录](pdf-review.md)，本机安装暂不处理。 | read（内容理解与阅读笔记） |
| playwright | 官方能力，不收录 | 按用户规则跳过 | 来源登记为 OpenAI 官方，入口与原盘点一致；移出个人集合，本机安装保持。见 [处理记录](openai-official-exclusions.md)。 | 不重复维护官方实现 |
| playwright-interactive | 官方能力，不收录 | 按用户规则跳过 | 来源登记为 OpenAI 官方，入口与原盘点一致；移出个人集合，本机安装保持。见 [处理记录](openai-official-exclusions.md)。 | 不重复维护官方实现 |
| screenshot | 官方能力，不收录 | 按用户规则跳过 | 来源登记为 OpenAI 官方，入口与原盘点一致；移出个人集合，本机安装保持。见 [处理记录](openai-official-exclusions.md)。 | 不重复维护官方实现 |
| security-best-practices | 官方能力，不收录 | 按用户规则跳过 | 来源登记为 OpenAI 官方，入口与原盘点一致；移出个人集合，本机安装保持。见 [处理记录](openai-official-exclusions.md)。 | 不重复维护官方实现 |
| security-threat-model | 官方能力，不收录 | 按用户规则跳过 | 来源登记为 OpenAI 官方，入口与原盘点一致；移出个人集合，本机安装保持。见 [处理记录](openai-official-exclusions.md)。 | 不重复维护官方实现 |
| transcribe | 官方能力，不收录 | 按用户规则跳过 | 来源登记为 OpenAI 官方，入口与原盘点一致；移出个人集合，本机安装保持。见 [处理记录](openai-official-exclusions.md)。 | 不重复维护官方实现 |
| vercel-deploy | 官方能力，不收录 | 按用户规则跳过 | 来源登记为 OpenAI 官方，入口与原盘点一致；移出个人集合，本机安装保持。见 [处理记录](openai-official-exclusions.md)。 | 不重复维护官方实现 |

## 迁移边界

最初纳入了 13 项个人定制，brief 现已迁出；当前源码与发布数量以 catalog 和 README 为准。原有 19 项外部能力中，14 项 OpenAI 官方技能按用户规则跳过并退出个人 catalog；其余 5 项按第一轮逐项处理，其中 deep-research、ui-ux-pro-max 与 skill-creator 已获批准并为 Codex 重写或适配，另 2 项仍作外部登记；不复制整个第三方项目。保留的外部依赖按任务归类并有使用页。keep 表示值得继续使用，不代表本次已经完成该 skill 的线上行为验证。

除已授权迁移外，原安装保持不变。提醒技能已从 TangMonk／tang-monk 更名 remind；原入口完整备份，旧名继续用于安装冲突检查，避免双份发现。重复 find-skills、旧版系统同名能力和不适合当前宿主的说明列为迁移事项，未经迁移不会删除现有安装。

## 已确认的缺口

- 原 llm-wiki 的检查和首页生成问题已在 2026-10-16 改造中处理：新版 wiki 使用只读检查，旧覆盖首页生成器退出；真实公开构建仍由各知识库项目验证。
- social-feed：pwcli_path 固定拼接 legacy 安装路径，未提供路径或宿主适配参数。
- deepcoffee-dev：已按用户确认恢复完整规则与六篇参考，三个现有脚本尚未打包进公开仓库，实际操作仍需解析其本地位置与后端环境。
- deep-research：原第三方入口的宿主与保存假设已通过仓库重写处理；来源和摘录记录工具不判断内容真假，真实研究质量仍需具体任务核验。
- skill-creator：仓库已将创建与评测合在同一入口，修正故障统计并排除夹带旧包；本机旧版保持，真实模型效果尚未评估。同名安装选择留待统一迁移。

## 先改善什么

1. 统一入口、简报、阅读与知识库之间的责任边界；本版已将普通阅读默认改为会话交付。
2. llm-wiki 的双层导航与私有页构建验证。
3. social-feed 的工具定位、登录失败与公开时间线验证。
4. deepcoffee-dev 保持一个技能入口，专属交付、维护与知识规则按需放在技能自身的 references，运行依赖据实记录。
5. deep-research 的证据机制保留，移除宿主专用假设和强制多格式报告。

2026-10-15 分类与优先级纠正：取消 in-progress 目录，已知问题在本页和使用页保留。第一轮仅审原有 32 项，当前已确认处理 6 项、待审 26 项；Matt 候选第二批再考虑引入。social-feed 已确认保持现状并归 productivity；deepcoffee-dev、llm-wiki 只迁移用途目录，仍待第一轮内容审阅。

2026-10-16 wiki 用户确认后完成更名与改造，移除自测，保持手动调用并列入默认清单；第一轮已处理 7 项、待审 25 项。此前各日期盘点保留为历史记录，当前状态以分批清单为准。

2026-10-19 writing-styles 用户确认并完成整改与更名；第一轮已处理 8 项、待审 24 项。前述日期的盘点保留为历史记录。

2026-10-20 第一轮已全部确认处理：原有 17 项保留、brief 迁出 1 项、OpenAI 官方跳过 14 项，共 32 项。teach 为提前确认的新增能力，保留集合共 18 项；ask-skills 另列体系维护，Matt 36 项候选留待第二批。

2026-10-20 后续确认：用户明确批准体系新增的 ask-skills 加入，当前已确认保留 19 项；该入口不属于原有 32 项，第一轮计数保持。原先提前纳入的遗漏及统一准入检查见 [确认记录](ask-skills-review.md)。
