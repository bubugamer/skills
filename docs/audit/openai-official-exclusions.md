# OpenAI 官方技能处理记录

日期：2026-10-20。用户明确要求「来自openai官方的，你就给我直接跳过吧，也不需要放到项目仓库了」。本轮按来源批量执行，无需再逐项等待确认。

## 本轮直接跳过：12 项

以下来源均已登记为 OpenAI 官方 skills，且当前本机入口 SHA-256 与原盘点快照一致。仅核对来源和入口版本，不声称完成逐项内容审阅、功能验证或线上上游同步。

| 技能 | 登记来源 | 原快照及当前入口 SHA-256 |
| --- | --- | --- |
| `cloudflare-deploy` | [OpenAI 官方来源](https://github.com/openai/skills/tree/main/skills/.curated/cloudflare-deploy) | `d7632537cf19be17cf33d2c696b9d9c2ea3ee51026030e9b203d5b9255e75b15` |
| `gh-address-comments` | [OpenAI 官方来源](https://github.com/openai/skills/tree/main/skills/.curated/gh-address-comments) | `77389eefd3fb6584210668ca8e43f4b8de87e7722ddd953474bc9e24cdfaaedd` |
| `gh-fix-ci` | [OpenAI 官方来源](https://github.com/openai/skills/tree/main/skills/.curated/gh-fix-ci) | `7b326b4a2f0f5f85122144628ec02077e48841e0e0e82efce88b3415bcfb7c26` |
| `jupyter-notebook` | [OpenAI 官方来源](https://github.com/openai/skills/tree/main/skills/.curated/jupyter-notebook) | `62f102e8554b25716dccef0ffab4572d4e3eaf05ccc76562d33a065bc9c521fb` |
| `openai-docs` | [OpenAI 官方来源](https://github.com/openai/skills/tree/main/skills/.curated/openai-docs) | `100099568ce8887ccd961aad2aa824a6d6054d4e5e697625815cc6e1b30d54a7` |
| `playwright` | [OpenAI 官方来源](https://github.com/openai/skills/tree/main/skills/.curated/playwright) | `0ffaabcc8e0990627c4725f18bf1c7955534a796c1c199e872909de2013ce6a8` |
| `playwright-interactive` | [OpenAI 官方来源](https://github.com/openai/skills/tree/main/skills/.curated/playwright-interactive) | `f6c1155d923e6ae3ccc12abfef2266f119f8e9546df2ddeee1f5eb369845a0a1` |
| `screenshot` | [OpenAI 官方来源](https://github.com/openai/skills/tree/main/skills/.curated/screenshot) | `081935a6a163277537d46365f49d6b4a3cb40b4748347e7e88759c5927fa8cf5` |
| `security-best-practices` | [OpenAI 官方来源](https://github.com/openai/skills/tree/main/skills/.curated/security-best-practices) | `7b3dae1ffc5434d890f3c65c8f552af52d0307fab3b35dec13013c9ca3844c4f` |
| `security-threat-model` | [OpenAI 官方来源](https://github.com/openai/skills/tree/main/skills/.curated/security-threat-model) | `1283c0dd62a8104d9edda4583569b5d8510b4ddaa45120687c999250fd96bad2` |
| `transcribe` | [OpenAI 官方来源](https://github.com/openai/skills/tree/main/skills/.curated/transcribe) | `f530021da9f377362ee4214e0bc689cbb5404640d2eb88ee272d51d61f530a09` |
| `vercel-deploy` | [OpenAI 官方来源](https://github.com/openai/skills/tree/main/skills/.curated/vercel-deploy) | `f1f3fa3ff57f87f8f32d77ed635b63416f200a1f976a8a8d3e23d12b30df3ae4` |

## 先前已确认的官方项目

- [imagegen](imagegen-review.md)：先前已确认沿用官方、不收录。
- [pdf](pdf-review.md)：先前已确认沿用官方、不收录。

两项与本轮 12 项合计 14 项，全部不在个人 catalog、用途使用页、生成推荐、安装或发布集合中。仅保留必要的处理依据，不保存官方实现副本。

## 批量跳过时剩余的六项

deepcoffee-dev、agent-browser、find-skills、deep-research、ui-ux-pro-max、skill-creator。其中 skill-creator 登记为本地评测定制，初始来源未核实；系统存在官方同名入口不证明这个本地版本来自 OpenAI，不能据此误跳过。其他第三方项目也不因产品名称或使用 OpenAI API 就归为官方。

## 执行范围

移出 catalog 的条目及独立使用页，重新生成分类导航和推荐；14 个现有个人源码与 13 项默认发布范围保持。本机安装、认证状态、项目环境及其他仓库保持。未执行部署、生产清理、浏览器操作、录音转写或付费 API 请求。

本轮批量跳过完成时，个人 catalog 19 项：14 个源码技能与 5 项其他外部能力说明。已审阅保留 12 项；第一轮已处理 26 项、待审 6 项；Matt 第二批 36 项及 ask-skills 维护项单列。

官方技能不收录不等于其工具不再需要。site-unlocker 的浏览器或 Playwright 后备要求、social-feed 对现有 playwright_cli.sh 的依赖继续在输入条件中说明；social-feed 固定路径问题保持，未改脚本、登录或安装。catalog 的集合内依赖不再指向已移除的官方条目。
