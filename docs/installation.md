# 安装与调用

这个仓库是源码与维护入口。现有安装保持不变，正式发布清单不包括 in-progress、deprecated 或外部依赖。不要同时用插件和本地链接安装同一批技能。

## 本地源码方式

在仓库根目录先检查与预览：

```bash
python3 scripts/validate.py
python3 scripts/install.py
```

预览不会创建目录。存在 `.agents/skills`、legacy `.codex/skills` 的同名技能或 TangMonk 旧名时，报告冲突并停止整批安装。脚本没有强制覆盖选项；先制定备份与迁移方案。

可以只选没有冲突的正式技能：

```bash
python3 scripts/install.py --skill ask-skills
python3 scripts/install.py --skill ask-skills --apply
```

链接创建后，按 Codex 当前提示刷新或开始新会话，再手动输入 `$ask-skills`。试用项需明确选择并先阅读使用页，不通过本脚本默认安装。

## Codex 插件方式

仓库提供 `.codex-plugin/plugin.json` 兼容格式与 `.agents/plugins/marketplace.json`。官方仍支持此兼容格式，采用明确路径列表来避免把试用目录包含进去。公开 GitHub 发布后可以添加目录源：

```bash
codex plugin marketplace add bubugamer/skills --ref main
codex plugin add bubugamer-skills@bubugamer
```

已有同名的独立安装时，先完成迁移，再安装插件。不要把命令示例当作已在用户环境执行过的证明。插件是否被当前桌面会话加载、以及每项能力的实际行为需要分别检查。

## 外部能力

外部依赖已有独立使用页和上游链接。优先当前 Codex 系统或插件提供的能力，避免同名重复安装。需要 CLI 时现场检查工具、权限和认证状态；登录状态与 API 密钥只放本地。

出处：[Codex 技能与工作区范围](https://learn.chatgpt.com/docs/build-skills)、[官方插件封装与 marketplace](https://developers.openai.com/plugins/build/plugins)。
