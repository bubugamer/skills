# 现有 skills 审查

审查日期：2026-10-11。33 个本地安装目录，32 个不同名称；find-skills 的两个入口文件字节一致。审查了入口说明、资源结构和脚本依赖，未执行部署、删除、付费 API 或登录抓取。

## 决定

| Skill | 分类 | 处理 | 依据与改进 | Matt 对照 |
| --- | --- | --- | --- | --- |
| TangMonk | productivity | keep | 保留执行状态与内容分类分离的设计；原 TangMonk 规范为小写名称，并保留迁移说明。 | wayfinder、loop-me |
| brief | productivity | keep | 保留来源范围、去重和短输出；浏览器抓取能力是条件依赖，缺失时明确报告。 | research |
| dongnaojin-yeye | productivity | keep | 保留内容获取门槛与结论收束规则；修正默认自动落库，摘要和讨论先在会话完成。 | teach、research |
| konmari | productivity | keep | 保留内部目录隔离、重复检测与可回退计划；先验证脚本，再讨论重构算法。 | improve-codebase-architecture（仅方法相似） |
| site-unlocker | productivity | keep | 保留真实正文判定；改为优先当前 Codex 浏览器工具，CLI 作为可用时的后备。 | research 的检索前置层 |
| writing-master | productivity | keep | 保留风格文件与共同规则分离；只做建议的审稿和明确要求改文件的编辑区分清楚。 | writing-fragments、writing-shape、writing-beats |
| wait-what | productivity | keep | 本地版本与 Matt 原文一致，明确记录出处；改成跟随当前语言，默认中文。 | wait-what |
| akshare-api | misc | keep | 保留来源标注、日期验证和空结果处理；只收源码与固定依赖，不收运行环境。 | 无直接同类；属于专用工具 |
| tdx-api | misc | keep | 与 AKShare 保持来源边界；保留空实时结果失败规则和明确服务器优先级。 | 无直接同类；与 akshare-api 互补 |
| yt-dlp-download | misc | keep | 保留单条默认、集合范围选择和防覆盖；输出位置改为当前用户 Downloads。 | 无直接同类；属于专用工具 |
| deepcoffee-dev | in-progress | improve | 一个入口混合提交、部署、生产清理和知识库；引用集合外脚本。公开版本先保留边界与改善计划，项目内部流程留在本地。 | pr、implement、retro、domain-modeling |
| llm-wiki | in-progress | improve | rebuild_index.py 仍按全页目录重建 index，未同步修改 mkdocs.yml；说明声称 lint 支持 --dry-run，而脚本未定义。 | domain-modeling、teach |
| social-feed | in-progress | improve | 脚本硬编码寻找旧的 Playwright 安装路径，且需要登录状态；不把未验证的登录抓取包装成通用可用。 | research 的信息获取层 |
| agent-browser | engineering | keep | CLI、浏览器和认证状态；allowed-tools 是其他宿主的提示，不构成 Codex 工具授权。 | playwright、site-unlocker |
| find-skills | productivity | keep | 两个安装目录的 SKILL.md 完全相同；只保留一个来源，先确认 Codex 内置发现能力是否已覆盖。 | ask-skills |
| deep-research | productivity | improve | 当前定制仍含 Claude Task/WebSearch 和 ~/.claude 输出假设；默认强制 HTML/PDF、多目录产物，与会话优先原则冲突。先统一工具与输出契约。 | research、writing-master |
| ui-ux-pro-max | engineering | improve | 本地增加了个人设计偏好，但 description 仍只有一句模糊介绍。应把偏好与可更新的第三方资料库分开，并补充触发范围。 | prototype |
| skill-creator | engineering | prefer-builtin | 本地评测版已经使用 codex exec，不能误称为 Claude 脚本。与系统 skill-creator 职责重叠，且夹带另一个 .skill 包；日常创建优先系统版，复杂评测按需使用本地版。 | writing-for-agents |
| cloudflare-deploy | engineering | keep | Wrangler 登录与指定产品；本地说明的 sandbox 升权语法必须服从当前工具权限。 | wizard |
| gh-address-comments | engineering | keep | gh 登录；已有明确处理范围时无需重复询问所有意见。 | code-review、pr |
| gh-fix-ci | engineering | keep | 仅覆盖 GitHub Actions；计划审批应结合当前用户授权。 | diagnosing-bugs |
| imagegen | misc | keep | 与系统 imagegen 同名；优先当前原生工具，CLI 是显式 API 工作流，需密钥。 | prototype（输出形态不同） |
| jupyter-notebook | engineering | keep | 脚手架只需 Python；运行代码另需 notebook 环境。 | scaffold-exercises（用途不同） |
| openai-docs | engineering | keep | 与系统同名；优先系统新版，不因旧说明反复安装 MCP。 | research |
| pdf | misc | keep | 与插件能力重叠；选一个维护来源，文本读取不能替代版面验证。 | 无直接同类 |
| playwright | engineering | keep | Node/npm 与浏览器；不与 agent-browser 同时建立重复会话。 | prototype 的 UI 验证 |
| playwright-interactive | engineering | keep | 本地说明要求 js_repl 和配置变更；当前宿主工具名称须现场核对，不能照搬。 | prototype |
| screenshot | misc | keep | 屏幕录制权限；优先对应应用工具的截图能力。 | 无直接同类 |
| security-best-practices | engineering | keep | 仅明确安全请求；当前资料覆盖 Python、JS/TS、Go。 | code-review（专项补充） |
| security-threat-model | engineering | keep | 仓库证据和环境范围；与普通架构概述分开。 | codebase-design（专项补充） |
| transcribe | misc | keep | OpenAI API 密钥与音频输入；现成原生能力可优先。 | 无直接同类 |
| vercel-deploy | engineering | keep | 默认预览；生产需用户已授权；不要将部署命令成功说成页面验收通过。 | pr、wizard |

## 迁移边界

本仓库维护 13 项个人定制的公开版本；另外 19 项作为外部依赖记录，不复制整个第三方项目。外部依赖也属于体系，按任务归类并有使用页。keep 表示值得继续使用，不代表本次已经完成该 skill 的线上行为验证。

原安装仍保持不变。TangMonk 在源集合改为 tang-monk；激活时应检查旧名称，避免双份发现。重复 find-skills、旧版系统同名能力和不适合当前宿主的说明列为迁移事项，未经迁移不会删除现有安装。

## 已确认的缺口

- llm-wiki：说明称 lint 有 --dry-run，实际 argparse 没有此项；rebuild_index 生成全页 index，未写 MkDocs 导航。
- social-feed：pwcli_path 固定拼接 legacy 安装路径，未提供路径或宿主适配参数。
- deepcoffee-dev：源目录仅 SKILL.md，实际操作依赖集合外脚本；公开版本先降为边界适配说明。
- deep-research：原 README 指向 Claude 来源；定制引用 Task、WebSearch，输出与保存流程需要 Codex 适配。
- skill-creator：本地 run_eval.py 与 improve_description.py 已使用 codex exec；系统版和评测版应区分职责，夹带 .skill 包不属于该 skill 源码。

## 先改善什么

1. 统一入口、简报、阅读与知识库之间的责任边界；本版已将普通阅读默认改为会话交付。
2. llm-wiki 的双层导航与私有页构建验证。
3. social-feed 的工具定位、登录失败与公开时间线验证。
4. deepcoffee-dev 分离交付、发布、维护与知识库能力。
5. deep-research 的证据机制保留，移除宿主专用假设和强制多格式报告。
