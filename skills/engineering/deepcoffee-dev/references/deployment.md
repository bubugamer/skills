# 部署与验收交接

执行命令前，按 [runtime.md](runtime.md) 解析脚本位置与后端运行环境；以下变量指向已核实的本地文件，不是需要直接照抄的默认路径。

## 能力：deploy（部署到生产）

Codex 负责完成发布动作、必要的本地检查和 CI 检查；所有线上状态、生产环境实际渲染和最终验收都由用户负责。不要访问生产页面验证效果，不要查询 Vercel 或 Cloud Run 的线上部署状态，也不要用 `/v1/health`、revision、traffic 或生产 commit 做上线确认。

职责边界：

- Codex 可以确认代码已提交、已推送、CI 是否通过，以及部署命令是否成功退出。
- Codex 不检查 `$DEEPCOFFEE_PRODUCTION_URL` 的实际页面，不截图生产页面，不读取线上 DOM，也不检查静态资源是否已刷新。
- Codex 不检查 Vercel production deployment、对应 commit、部署 URL 或 dashboard 状态。
- Codex 不检查 Cloud Run revision、traffic、线上版本号或 `/v1/health`。
- 用户负责所有线上状态确认和生产效果验收。

### 流程

1. 确认已在 `main` 并拉到最新：
   ```bash
   git checkout main
   git pull --ff-only
   ```

2. 前端改动推送到 `main` 后，由现有 Vercel 集成自动触发发布。Codex 等待 GitHub CI 通过即可，不再检查 Vercel 或生产站点。

3. 只有任务包含后端改动或用户明确要求部署后端时，才从仓库根运行部署脚本：
   ```bash
   bash "$DEEPCOFFEE_DEPLOY_SCRIPT"
   ```
   如果要更新环境变量，只使用 `--update-env-vars`，不要用 `--set-env-vars`。

4. 最终交接只报告 Codex 实际完成的事项：
   - 提交和分支信息。
   - push / merge 是否成功。
   - CI 是否通过。
   - 如果执行了后端部署脚本，报告命令是否成功完成；不要延伸检查线上状态。
   - 列出需要用户在线上验收的页面、流程和预期变化。

5. 发布用语要准确：
   - 可以说“代码已推送并触发前端发布”或“后端部署命令已成功完成”。
   - 不要说“线上已确认”“生产已验证”或“上线完成”，除非用户主动提供了验收结果。
   - 用户确认线上无误后，可以复述用户的确认结论，不需要再次自行检查。
