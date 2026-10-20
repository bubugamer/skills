# 交付与 PR

## 默认交付模式（直接 main 与 PR 分流）

DeepCoffee 当前按单人主程节奏处理改动：低风险改动可以直接提交到 `main`，中高风险改动才走分支 + PR。不要机械地每次都开 PR，也不要为了省步骤把高风险改动直接推到 `main`。

### 低风险：直接 main

适用场景：

- 文案、README、CHANGELOG、纯样式小修、单页面低风险 UI 调整。
- 明确的小 bug 修复，影响范围窄，容易用本地检查或线上页面确认。
- 不涉及账号、支付、权限、数据库、AI 行为、核心数据流或大面积页面改版。

流程：

1. 确认在 `main` 且拉到最新：
   ```bash
   git checkout main
   git pull --ff-only
   ```

2. 查看并限制改动范围：
   ```bash
   git status --short --branch
   git diff --stat
   ```
   只 stage 本任务相关文件，不提交无关脏文件。

3. 做与改动匹配的轻量验证：
   - 前端 TypeScript 改动优先跑：
     ```bash
     cd frontend && npx tsc --noEmit
     ```
   - 视觉小修能本地看就本地看；线上页面、生产渲染和线上状态统一交给用户检查，Codex 不检查。
   - 后端小修跑相关单测，不跑无关大范围测试。

4. 直接提交并推送 `main`：
   ```bash
   git add <相关文件>
   git commit -m "<简短说明>"
   git push origin main
   ```

5. 如果改动会触发前端 Vercel 或后端生产发布，按 `deploy` 规则触发发布并交给用户验收。不要检查线上状态，也不要把 `git push` 直接说成“上线完成”；应准确表述为“已推送并触发发布”。

### 中高风险：分支 + PR

适用场景：

- 后端行为、数据库迁移、账号、登录、权限、支付、订阅、用量、数据清理。
- AI prompt、解析链路、推荐逻辑、实体归一、知识库检索或模型上下文机制。
- 多页面前端改版、跨端适配、大面积重构、依赖升级。
- 用户明确说「提 PR」「开 PR」「合 PR」「ship」或要求先走审查。

流程使用下面的 `ship`。PR 合并后必须删除远端分支，避免仓库长期堆积历史分支。

## 能力：ship（分支 + PR + 合并到 main）

把中高风险改动或用户明确要求走审查的改动，通过 GitHub PR 流水线合并回 `main`。**不自动部署生产**；生产部署另走 `deploy`。

### 触发

- 用户说「提 PR」「开 PR」「合 PR」「合并到 main」「ship」。
- 用户只说「提交到 GitHub」「推上去」时，先按默认交付模式判断风险；低风险直接 `main`，中高风险走 `ship`。
- 用户说「完成后上线」时，先 `ship`，合并成功后再 `deploy`。

### 流程

1. 查看改动范围：
   ```bash
   git status --short --branch
   git diff --stat
   ```
   不要提交无关文件。尤其不要碰未跟踪的 `deepcoffee-api/migrations/manual_bug2_cleanup.sql`，除非用户明确点名。

2. 只做必要的轻量验证：
   - 默认依赖 GitHub / Vercel 流水线，不跑完整本地测试。
   - 后端改动可跑相关单测：
     ```bash
     deepcoffee-api/.venv/bin/pytest deepcoffee-api/tests/test_xxx.py -q
     ```
   - 前端 TypeScript 改动可跑：
     ```bash
     cd frontend && npx tsc --noEmit
     ```
   - 线上页面、生产渲染和部署状态由用户统一检查；Codex 只需明确列出需要用户验收的页面和预期变化。

3. 创建或沿用分支：
   - 若在 `main`，新建 `codex/<short-topic>`。
   - 若已在合适 feature 分支，沿用。

4. 只 stage 本任务相关文件并提交：
   ```bash
   git add <相关文件>
   git commit -m "<简短说明>"
   ```

5. 推送并开 PR：
   ```bash
   git push -u origin HEAD
   gh pr create --base main --head "$(git branch --show-current)" --title "<PR 标题>" --body-file "$deepcoffee_pr_body_file"
   ```
   先把 PR 说明写入临时文件，并将实际文件路径传给 `deepcoffee_pr_body_file`。内容包含：改了什么、验证了什么、需要用户在线上检查什么。

6. 等待 CI：
   ```bash
   gh pr checks --watch
   ```
   CI 失败先修，不要合并。

7. 合并：
   ```bash
   branch="$(git branch --show-current)"
   gh pr merge --merge
   git checkout main
   git pull --ff-only
   git push origin --delete "$branch"
   ```
   默认 merge commit，保持当前仓库历史习惯。合并后删除远端分支；如果删除失败，最终汇报中说明。
