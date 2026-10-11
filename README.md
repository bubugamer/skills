# 我的 Codex Skills

学习现成系统后，整理自己的能力、共享方法与使用入口。目录分类与文档治理参考 [Matt Pocock 的 skills](https://github.com/mattpocock/skills)。当前只适配 Codex。

不确定选哪个时，手动使用 `$ask-skills`。需要某项任务时，可以直接使用对应技能；无需每次先经过入口。

## 当前集合

审查了 32 个不同现有 skills：13 项本地定制进入源码集合，19 项保留为外部依赖。新增一个推荐入口，并试用四项 Matt 基础方法。当前正式发布 11 项，试用 7 项。原安装保持不变。

| 分类 | 作用 | 目录 |
| --- | --- | --- |
| engineering | 工程 | [浏览](skills/engineering/README.md) |
| productivity | 生产力 | [浏览](skills/productivity/README.md) |
| misc | 专用工具 | [浏览](skills/misc/README.md) |
| in-progress | 试用与待改善 | [浏览](skills/in-progress/README.md) |
| deprecated | 废弃与迁移 | [浏览](skills/deprecated/README.md) |

## 从这里开始

- [现有 skills 的逐项审查](docs/audit/existing-skills.md)：保留、改善、外部依赖与重复项。
- [Matt 全部 38 项的纳入判断](docs/audit/upstream-skills.md)：在整理自身集合后选择扩展。
- [架构与各目录的作用](docs/architecture.md)：操作入口、使用文档、术语和治理分工。
- [安装与调用](docs/installation.md)：只安装正式项，先预览并检查冲突。
- [验证记录](docs/audit/verification.md)：本次实际验证了什么，以及哪些仍待验证。
- [范围与准入](SCOPE.md)、[词汇表](GLOSSARY.md)、[来源与许可](THIRD_PARTY_NOTICES.md)。

## 正式能力

| Skill | 解决什么 | 用法 |
| --- | --- | --- |
| [tang-monk](docs/productivity/tang-monk.md) | 管理想法、探索和每日重点 | `$tang-monk` |
| [brief](docs/productivity/brief.md) | 筛选指定来源并生成简报 | `$brief` |
| [dongnaojin-yeye](docs/productivity/dongnaojin-yeye.md) | 阅读、翻译、出处追溯和笔记 | `$dongnaojin-yeye` |
| [konmari](docs/productivity/konmari.md) | 检查文件结构与整理方案 | `$konmari` |
| [site-unlocker](docs/productivity/site-unlocker.md) | 获取特殊网页的真实正文 | `$site-unlocker` |
| [writing-master](docs/productivity/writing-master.md) | 按命名风格写作和审稿 | `$writing-master` |
| [wait-what](docs/productivity/wait-what.md) | 重新解释上一段回答 | `$wait-what` |
| [akshare-api](docs/misc/akshare-api.md) | 获取多来源金融市场数据 | `$akshare-api` |
| [tdx-api](docs/misc/tdx-api.md) | 读取沪深行情与历史数据 | `$tdx-api` |
| [yt-dlp-download](docs/misc/yt-dlp-download.md) | 下载或检查用户指定媒体 | `$yt-dlp-download` |
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
