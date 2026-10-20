# 我的 Codex Skills

学习现成系统后，整理自己的能力、共享方法与使用入口。目录分类与文档治理参考 [Matt Pocock 的 skills](https://github.com/mattpocock/skills)。当前只适配 Codex。

来自 OpenAI 官方的技能直接使用官方维护来源，按用户要求跳过个人收录；本仓库聚焦个人技能与必要定制，处理依据见[官方技能处理记录](docs/audit/openai-official-exclusions.md)。

不确定选哪个时，手动使用 `$ask-skills`。需要某项任务时，可以直接使用对应技能；无需每次先经过入口。

## 按场景选技能

以下覆盖已确认保留的 19 个技能、44 个代表场景。待审技能与 Matt 候选继续记录在[分批审查清单](docs/audit/review-checklist.md)，审阅确认后补入此表。brief 已迁到独立定时任务项目。

| 具体场景 | 你可以怎样提出要求 | 用哪个 skill | AI 会怎样协助 | 最终产出 |
| --- | --- | --- | --- | --- |
| 对话中提了几件待办和想法，担心遗漏。 | `$remind` 回顾刚才提到的事项，区分确定要做的事和待考虑想法，提醒我哪些值得跟进。 | [remind](docs/productivity/remind.md) | 依据当前对话和已知状态给出简短提醒，按你的答复确认后续状态。 | 待办与想法的区分、简短提醒及待确认状态。 |
| 读外文文章或专业材料，有些段落和概念不理解。 | `$read` 翻译这篇文章，解释我标出的概念，再和我继续共读。 | [read](docs/productivity/read.md) | 获取实际正文，按指定范围翻译，结合原文回答追问。 | 译文、概念解释和有出处的共读问答。 |
| 共读结束，想把已经讨论清楚的内容留下来。 | `$read` 把刚才讨论的结论整理成阅读笔记，存到我们已约定的位置。 | [read](docs/productivity/read.md) | 收束材料主线、关键解释与未解问题，保留来源并按约定保存。 | 有出处的阅读笔记，以及实际保存位置。 |
| 想系统掌握一门课程、领域或技能，并持续练习。 | `$teach` 我想学会用 Python 整理表格，请先明确学习目标，再安排课程和练习。 | [teach](docs/productivity/teach.md) | 围绕目标选择可信材料，安排适合当前程度的短课与练习，记录学习情况。 | 学习目标、课程与参考资料，以及带反馈的练习。 |
| 已经学过一些内容，希望检验理解并复习。 | `$teach` 根据这些学习材料考考我，等我回答后指出理解漏洞。 | [teach](docs/productivity/teach.md) | 结合目标与已有学习记录出题，对回答给出反馈，再调整复习重点。 | 自测题、反馈和需要复习的知识点。 |
| 资料目录混杂，想按 PARA 整理，但先看看方案。 | `$para` 检查这个目录，保留已有分类名，先给我看 PARA 整理方案。 | [para](docs/productivity/para.md) | 盘点文件，结合当前项目与长期责任分类，列出冲突和不确定归属。 | 可审阅的整理方案、保留项和待确认事项。 |
| 整理方案已确认，希望执行并能核对、恢复。 | `$para` 执行我们刚确认的方案，完成后核对文件完整性。 | [para](docs/productivity/para.md) | 检查路径与目标冲突，按授权移动，核对内容并记录操作。 | 整理后的目录、执行报告与逆向移动方案。 |
| 链接只能读到标题，或需要加载、展开、登录后才有正文。 | `$site-unlocker` 获取这个链接的可读正文，保留来源；如果拿不到，说明卡在哪里。 | [site-unlocker](docs/productivity/site-unlocker.md) | 用可用的读取或浏览器工具处理跳转与加载，需要时使用有效登录状态，并核实实际正文。 | 正文文件与来源链接；无法读取时说明障碍。 |
| 有项目经历或明确观点，想写一篇自然的论坛帖 | `$writing-styles` 按 bbs 把这些材料写成论坛帖，保留我的观点和事实。 | [writing-styles](docs/productivity/writing-styles.md) | 按论坛语气组织已有材料，保留立场和真实细节，并检查基础语言。 | 一篇可以继续修改或使用的论坛草稿。 |
| 已有文章，只想知道哪里需要改 | `$writing-styles` 按 bbs 审阅这篇文章，只列修改建议。 | [writing-styles](docs/productivity/writing-styles.md) | 定位错字、用词与风格问题，给出替换建议，区分必要修正和可选调整。 | 会话中的审稿意见，原文及文件保持。 |
| 研究材料已有，想把分析写得明确简洁 | `$writing-styles` 按 research-analysis 精简这份产品比较，保留证据与来源。 | [writing-styles](docs/productivity/writing-styles.md) | 提出材料支持的结论，删去空话与重复表达，保留关键限定，使用对应领域的比较标准。 | 结论明确、证据可追溯的分析文稿。 |
| 希望直接修改已指定的草稿文件 | `$writing-styles` 按选定文风润色 draft.md，直接修改这个文件，保留事实和立场。 | [writing-styles](docs/productivity/writing-styles.md) | 读取指定稿件，在授权范围内修订和检查语言，核对事实与来源。 | 更新后的草稿文件及简短修改说明。 |
| 刚才的回答没听懂，需要换一种方式讲清楚 | `$wait-what` 我没跟上刚才那段，请补充必要背景，换一种方式讲清楚。 | [wait-what](docs/productivity/wait-what.md) | 沿用当前上下文和已有项目术语，以简明中文重新解释。 | 一段更容易理解、含义准确的中文说明。 |
| 希望从同花顺获取公司的业务与财务资料 | `$akshare-api` 从同花顺获取这家公司的业务介绍和财务指标，保留报告日期与原始字段。 | [akshare-api](docs/misc/akshare-api.md) | 选择对应的同花顺接口，核对股票代码与字段，标明来源、报告期和获取时间。 | 带来源与日期的公司资料和财务数据。 |
| 指定来源，获取几只股票的历史价格 | `$akshare-api` 从新浪获取这些股票最近五个交易日的未复权日线，列明实际日期。 | [akshare-api](docs/misc/akshare-api.md) | 按指定来源调用历史行情，核对代码、日期和复权口径，明确缺失或失败。 | 来源与口径明确的历史日线表。 |
| 明确使用通达信查看沪深股票最新行情 | `$tdx-api` 通过通达信查询这些代码的最新价和涨跌幅，注明日期与获取时间。 | [tdx-api](docs/misc/tdx-api.md) | 按通达信通道读取并核对请求代码，结合有日期的日线确认交易日，说明快照时点和缺失结果。 | 来源和时点明确的行情表。 |
| 需要通达信的历史日线用于比较 | `$tdx-api` 读取这些股票最近五根日线，保留日期，说明是否复权。 | [tdx-api](docs/misc/tdx-api.md) | 读取对应日线，保留实际日期和原始价格口径，说明通达信日线未自动复权。 | 带日期与价格口径说明的历史日线表。 |
| 保存一条视频供稍后观看 | `$yt-dlp-download` 下载这条视频，保存到我指定的目录。 | [yt-dlp-download](docs/misc/yt-dlp-download.md) | 检查媒体及所需工具，保存选定视频，核对文件和音视频流，报告实际位置。 | 可以播放的视频文件与保存路径。 |
| 需要音频，或者已有 M4A 后改要 MP3 | `$yt-dlp-download` 这条链接之前存过 M4A，现在再给我一份 MP3，保留原文件。 | [yt-dlp-download](docs/misc/yt-dlp-download.md) | 按 MP3 目标使用独立目录和下载记录，检查成品格式，并保留已有 M4A。 | 格式正确的 MP3，以及保留的原 M4A。 |
| 查看合集并只保存选定条目 | `$yt-dlp-download` 先列出这个合集，不下载；我选好范围后再保存。 | [yt-dlp-download](docs/misc/yt-dlp-download.md) | 先返回条目清单和可获得的媒体信息，明确选择后仅处理该范围。 | 可供选择的清单，以及后续所选条目的文件。 |
| DeepCoffee 改动完成，需要按已有习惯交付 | `$deepcoffee-dev` 按现有规则完成这次改动的交付，只提交本次相关文件。 | [deepcoffee-dev](docs/engineering/deepcoffee-dev.md) | 沿用交付分流和已有维护安排，选择直接提交或 PR，运行相关检查并报告实际交付结果。 | 提交或 PR、检查结果，以及需要用户验收的页面清单。 |
| 合并后需要发布 DeepCoffee 后端 | `$deepcoffee-dev` 部署本次后端改动，线上由我检查。 | [deepcoffee-dev](docs/engineering/deepcoffee-dev.md) | 解析已确认的本地部署脚本和配置，完成请求的发布动作，按既有分工交接线上验收。 | 实际发布动作结果和具体的用户验收项。 |
| 想确认测试账号将被清理哪些数据 | `$deepcoffee-dev` 只预览这个测试账号的重置范围，不进行任何写入。 | [deepcoffee-dev](docs/engineering/deepcoffee-dev.md) | 使用现有账号工具预览数量与范围，说明保留内容，遵守当前只读要求。 | 目标账号的数据预览和保留清单。 |
| 咖啡资料需要先判断是否值得纳入项目知识库 | `$deepcoffee-dev` 审阅这篇咖啡文章，先给出纳入建议，确认后再重写。 | [deepcoffee-dev](docs/engineering/deepcoffee-dev.md) | 查找已有承载页，区分读者正文、必要模型注释与不纳入材料，按明确阶段处理。 | 具体的新增、修改和不纳入建议清单。 |
| 多份阅读笔记围绕同一主题，想编入长期知识库。 | `$wiki` 把这几份笔记编入指定知识库，先查已有页面，再补充结论与关联。 | [wiki](docs/productivity/wiki.md) | 优先修订已有页，保留证据与冲突，同步受影响的主题入口、导航和日志。 | 更新的知识页、相关入口和变更记录。 |
| 记得以前研究过某个问题，想找回已有结论。 | `$wiki` 在我的知识库查一下这个主题，告诉我已有认识和对应页面。 | [wiki](docs/productivity/wiki.md) | 搜索并阅读相关页面，区分已有结论、推断和知识空白。 | 基于知识库的回答、页面出处及覆盖缺口。 |
| 知识库页面逐渐增多，想检查链接和导航。 | `$wiki` 只读检查这些页面的链接、主题入口和站点导航，先列问题。 | [wiki](docs/productivity/wiki.md) | 按项目约定检查常见链接和导航，结合内容给出复核线索，说明未覆盖部分。 | 断链与导航问题清单、复核建议和检查范围。 |
| 想扫一批 X 首页或微博时间线，而不是阅读单篇文章。 | `$social-feed` 从 X 首页取最近可读的八条动态，保留作者、时间和原帖链接。 | [social-feed](docs/productivity/social-feed.md) | 工具与登录状态可用时读取可见卡片，标记广告或不可读项；失败时说明缺口。 | 结构化动态条目，包含可核实的作者、时间、片段和跳转链接。 |
| 检查指定测试页面的表单交互 | `$agent-browser` 检查这个测试页的表单，填入样例并确认结果。 | [agent-browser](docs/engineering/agent-browser.md) | 使用本次任务自己的会话，读取页面后执行已授权操作，再核对页面实际显示的结果。 | 可复核的交互结果和发现的问题。 |
| 从动态页面提取已显示的数据 | `$agent-browser` 把这个页面显示的商品列表整理成表格，附来源。 | [agent-browser](docs/engineering/agent-browser.md) | 观察页面，按范围展开或翻页，提取实际可见的数据，说明访问或完整性限制。 | 带来源的结构化列表及覆盖范围。 |
| 需要当前集合尚未覆盖的新能力 | `$find-skills` 找找检查电子书排版的现成技能，先比较，暂不安装。 | [find-skills](docs/productivity/find-skills.md) | 搜索外部候选，读取说明，核对来源、依赖和适配性，说明是否与已有能力重合。 | 带来源和依据的候选比较及引入建议。 |
| 想借鉴外部方法改善已有技能 | `$find-skills` 找几个知识库维护技能，与我的 wiki 比较，先不引入。 | [find-skills](docs/productivity/find-skills.md) | 围绕明确的改善目标搜索和对照方法，区分可借鉴内容与需要新增的能力。 | 具体差异、借鉴建议与待确认事项。 |
| 需要围绕问题主动调查，而非只读给定文章 | `$deep-research` 调查这两项技术的适用条件、主要证据和反例，先在对话给结论。 | [deep-research](docs/productivity/deep-research.md) | 检索并阅读原始资料，比较独立证据与实际约束，逐项核对关键断言，解释不确定性。 | 带来源的研究结论、主要取舍与证据缺口。 |
| 需要一份明确格式的独立研究报告 | `$deep-research` 按已约定目录生成 Markdown 报告，附来源和限制，不要其他格式。 | [deep-research](docs/productivity/deep-research.md) | 按既有范围组织报告，核对引用及关键结论，只保存所需文件并报告实际位置。 | 经过内容和引用检查的 Markdown 报告。 |
| 长研究需要保留证据，便于下次继续 | `$deep-research` 把来源和关键摘录保存在已约定的研究目录，列出仍需核对的问题。 | [deep-research](docs/productivity/deep-research.md) | 记录来源、原文位置和摘录，保留反例、当前结论与待解问题；记录检查不替代事实核验。 | 可追溯的研究记录与明确的后续问题。 |
| 检查工具页面的任务和信息层级 | `$ui-ux-pro-max` 审阅这个数据检查页，沿用我的设计习惯，先给布局建议。 | [ui-ux-pro-max](docs/engineering/ui-ux-pro-max.md) | 围绕主要任务、信息层级、动作与结果，结合个人规则和现有项目约束给出修改建议。 | 清晰的页面结构与交互建议。 |
| 为真实平台寻找相关设计和实现参考 | `$ui-ux-pro-max` 这是 React 网页，查查表格选择和状态反馈的参考，保留当前视觉系统。 | [ui-ux-pro-max](docs/engineering/ui-ux-pro-max.md) | 选择可用的实际平台资料，排除异常记录并说明覆盖限制，给出针对当前任务的建议。 | 带适用条件和数据范围的设计参考。 |
| 保存已确认规则，同时保留以前的修改 | `$ui-ux-pro-max` 先比较这份设计建议与已有规则，保留我的修改，再按已确认范围整理。 | [ui-ux-pro-max](docs/engineering/ui-ux-pro-max.md) | 显示差异，保留既有决定和无关内容；新文件可按授权创建，已有文件先准备明确的合并。 | 可复核的差异，以及按范围更新的设计文档。 |
| 把反复使用的方法整理成技能，或改善已有技能 | `$skill-creator` 把这套已使用的方法整理成技能，保持用途清晰，配套说明按需外置。 | [skill-creator](docs/engineering/skill-creator.md) | 从实际任务确定触发条件和完成标准，编写简短入口及必要参考，检查可用性；按本次需要选择验证。 | 可审阅的技能、配套资料和明确的验证结果。 |
| 想知道技能修改是否改善真实任务结果 | `$skill-creator` 比较这个技能的新旧版本，先给出真实用例、评价标准和执行范围。 | [skill-creator](docs/engineering/skill-creator.md) | 定义可比基线与任务结果，记录实际输出和失败，依据匹配样本及证据说明差异。 | 可复核的任务对照、限制和改进建议。 |
| 技能经常误触发或漏触发 | `$skill-creator` 检查这个技能的描述边界，先预览探针，不启动模型调用。 | [skill-creator](docs/engineering/skill-creator.md) | 准备正向与近似反例，预览调用范围，获准执行后区分有效结果、超时和错误，再提出描述修改。 | 触发覆盖说明及有依据的描述建议。 |
| 需要人工比较已有测试输出 | `$skill-creator` 用已有结果生成新的本地评阅页，保留我的旧反馈。 | [skill-creator](docs/engineering/skill-creator.md) | 展示实际输出、判断依据、错误和覆盖范围，提供本地反馈预览，并保留已有文件。 | 可查看和填写反馈的本地评阅页面。 |
| 不确定已有技能里该选哪一个 | `$ask-skills` 我想理解一篇文章并整理阅读笔记，应该用哪个技能？ | [ask-skills](docs/productivity/ask-skills.md) | 从当前路由给出首选、必要备选、选择理由、输入条件和一句可直接使用的请求。 | 明确的技能建议和下一步用法。 |
| 几个技能用途接近，想先确认分工 | `$ask-skills` 比较 read、teach 和 wiki，告诉我当前任务该用哪个，先只推荐。 | [ask-skills](docs/productivity/ask-skills.md) | 结合用户意图及已有选择解释边界，区分已收录能力、外部依赖与候选，保留手动调用要求。 | 针对当前任务的选择依据，不自动启动目标技能。 |

## 当前集合

最初盘点的 32 项原有技能已完成第一轮处理，待审 0 项；Matt 候选放第二批考虑是否引入，ask-skills 单列为体系维护项。当前维护 17 个源码技能（其中 1 项上游适配）及 2 项外部依赖说明；默认发布 17 项。目录按用途分类，审阅和已知问题单独记录。进度见 [分批审查清单](docs/audit/review-checklist.md)，名称与已有安装迁移见 [安装说明](docs/installation.md)。

| 分类 | 作用 | 目录 |
| --- | --- | --- |
| engineering | 工程 | [浏览](skills/engineering/README.md) |
| productivity | 生产力 | [浏览](skills/productivity/README.md) |
| misc | 专用工具 | [浏览](skills/misc/README.md) |
| deprecated | 废弃与迁移 | [浏览](skills/deprecated/README.md) |

## 从这里开始

- [第一轮收尾](docs/audit/first-round-summary.md)：最终集合、处理结论与验证范围。
- [分批审查清单](docs/audit/review-checklist.md)：第一轮原有技能优先，第二批 Matt 候选另列。
- [原有 skills 的技术盘点](docs/audit/existing-skills.md)：来源、改善建议、外部依赖与重复项。
- [Matt 全部 38 项的纳入判断](docs/audit/upstream-skills.md)：在整理自身集合后选择扩展。
- [架构与各目录的作用](docs/architecture.md)：操作入口、使用文档、术语和治理分工。
- [当前目录与文件清单](docs/directory-map.md)：各类技能、外部能力说明与实际文件。
- [安装与调用](docs/installation.md)：按明确清单安装，先预览并检查冲突。
- [验证记录](docs/audit/verification.md)：本次实际验证了什么，以及哪些仍待验证。
- [范围与准入](SCOPE.md)、[词汇表](GLOSSARY.md)、[来源与许可](THIRD_PARTY_NOTICES.md)。

## 默认发布清单

此表只包含已获用户明确确认的技能；对应场景见上表。ask-skills 已获准保留，作为体系维护入口单列，不计入第一轮原有 32 项。

| Skill | 解决什么 | 用法 |
| --- | --- | --- |
| [remind](docs/productivity/remind.md) | 发现待办与想法，提醒并跟进 | `$remind` |
| [read](docs/productivity/read.md) | 阅读、翻译、共读问答与阅读事务 | `$read` |
| [teach](docs/productivity/teach.md) | 围绕目标持续学习课程、领域或技能 | `$teach` |
| [para](docs/productivity/para.md) | 按 PARA 重建用户选定目录 | `$para` |
| [site-unlocker](docs/productivity/site-unlocker.md) | 获取特殊网页的真实正文 | `$site-unlocker` |
| [writing-styles](docs/productivity/writing-styles.md) | 应用和维护多种文风，写作、润色与审稿 | `$writing-styles` |
| [wait-what](docs/productivity/wait-what.md) | 重新解释上一段回答 | `$wait-what` |
| [akshare-api](docs/misc/akshare-api.md) | 获取多来源金融市场数据 | `$akshare-api` |
| [tdx-api](docs/misc/tdx-api.md) | 读取沪深行情与历史数据 | `$tdx-api` |
| [yt-dlp-download](docs/misc/yt-dlp-download.md) | 下载或检查用户指定媒体 | `$yt-dlp-download` |
| [deepcoffee-dev](docs/engineering/deepcoffee-dev.md) | 维护 DeepCoffee 开发、运维与知识流程 | `$deepcoffee-dev` |
| [wiki](docs/productivity/wiki.md) | 维护 Markdown 长期知识、关联与导航 | `$wiki` |
| [social-feed](docs/productivity/social-feed.md) | 读取社交时间线的结构化条目 | `$social-feed` |
| [deep-research](docs/productivity/deep-research.md) | 多来源证据研究 | `$deep-research` |
| [ui-ux-pro-max](docs/engineering/ui-ux-pro-max.md) | 设计资料库与风格建议 | `$ui-ux-pro-max` |
| [skill-creator](docs/engineering/skill-creator.md) | 创建、改进与评测技能 | `$skill-creator` |
| [ask-skills](docs/productivity/ask-skills.md) | 选择合适的 skill | `$ask-skills` |

## 维护

修改 catalog.json 与对应技能后，运行：

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/sync_catalog.py
python3 scripts/validate.py
python3 scripts/smoke_test.py
```

共享方法单独维护；GLOSSARY 只解释术语；docs 帮人选能力；SKILL.md 指导操作；evals 记录场景，验证记录只写实际发生的结果。
