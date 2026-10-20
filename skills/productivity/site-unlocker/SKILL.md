---
name: "site-unlocker"
description: "Use when the user wants to extract readable content from websites that normal fetch/search cannot reliably read, including JavaScript-rendered pages, short-link redirects, login-required pages, X posts/articles, paywalls, click-to-expand pages, or sites that need scrolling or browser interaction before the real content appears. Also use for Chinese requests like “帮我抓正文”, “这个网页要登录”, “这网站特殊处理一下”, “把这个链接内容取出来”, and “先把页面解锁再读”."
---

# Site Unlocker

一个专门负责“先把网页内容真正取出来”的 skill。

它不是总结助手，也不是知识整理助手。它的工作是：

- 进入网页或网站
- 处理跳转、渲染、展开、滚动、登录、会话状态
- 判断是否真的拿到了正文
- 把可读内容保存成干净的 Markdown / text 文件
- 如果拿不到正文，明确停下，不要假装抓到了

后续总结、值不值得读、知识沉淀，交给别的 skill，比如 `read`。

## When To Use

- 用户给了一个链接，但普通抓取只拿到网页外壳、标题或空白页面。
- 页面需要 JavaScript 渲染、点击展开、滚动加载或浏览器交互后才出现正文。
- 页面有短链接跳转，需要先找出最终目标。
- 页面需要登录、OAuth、2FA 或已有会话状态才能读取内容。
- 用户明确说“帮我抓正文”“把这个网站内容弄出来”“这个站得特殊处理一下”。

## When Not To Use

- 普通网页已经能直接拿到正文。
- 用户只是想判断值不值得读、做摘要、做翻译、做出处追溯。
- 用户在做普通搜索，而不是内容提取。

## Primary Goal

把网页从“链接”变成“可读内容”。

成功标准只有两个：

1. 真的拿到了正文或足够长的有效内容
2. 生成了可复用的干净输出文件，并告诉用户保存位置

如果只拿到这些东西，算失败，不算成功抓取：

- 页面标题
- 作者名
- 发布时间
- 短链接跳转结果
- 登录墙
- 错误页
- 空白壳页面
- 极短预览

## Tool Choice

优先顺序：

1. 先尝试最轻量的直接读取方式
2. 需要交互时，优先当前 Codex 提供的浏览器工具，并遵守其会话和登录规则
3. 当前工具不足且已安装 CLI 时，选择 `agent-browser` 或 `playwright`；先确认工具实际存在

一般规则：

- 登录、状态复用、表单交互：优先 `agent-browser`
- 调试复杂页面、看渲染结果、做浏览器快照：优先 `playwright`

## Workflow

1. 识别链接类型
   - 普通网页
   - 短链接
   - 社交平台内容
   - 站内文章页
   - 登录后内容
2. 先拿到最终目标 URL
   - 如果是短链接，先解析跳转链
   - 不要在短链接状态下就开始判断内容
3. 尝试直接读取
   - 如果正文已经能稳定获取，没必要开浏览器
4. 需要浏览器时再进入浏览器
   - 处理渲染
   - 处理展开按钮
   - 处理滚动加载
   - 处理登录流程
5. 判断是否真正拿到正文
   - 正文可见
   - 长度足够
   - 不是错误页或登录墙
   - 不是只有标题和元数据
6. 保存输出
   - 保存正文
   - 保存元数据
   - 如有必要，保存截图
7. 向用户汇报
   - 是否成功
   - 成功时保存到哪里
   - 失败时卡在哪里、下一步需要什么

## Output Rules

默认输出结构：

### 结果

一句话说明抓取成功还是失败。

### 拿到了什么

- 最终 URL
- 页面类型
- 是否拿到正文
- 是否需要登录

### 关键判断

- 为什么这次算成功抓取
- 或为什么这次还不算成功

### 保存位置

如果有成功抓取的输出，明确列出路径。

### 下一步

- 继续交给阅读/总结助手
- 需要用户登录
- 需要用户补更多范围或入口

## Save Rules

只有在**已经拿到正文或足够长的有效内容**时，才允许保存正文文件。

默认输出位置：

- 如果用户已明确提供知识库根目录 `<knowledge-root>`
  - 正文保存到 `<knowledge-root>/03-Resources/articles/_captures/`
- 其他工作区
  - 正文保存到 `output/site-unlocker/`

默认文件内容至少包括：

- 标签
- 原始链接
- 最终链接
- 获取日期
- 获取方式
- 是否需要登录
- 正文内容

推荐字段顺序：

- 获取日期
- 原始链接
- 最终链接
- 标签
- 获取方式
- 是否需要登录

不要写这类过程性字段：

- 当前状态
- 下一步

不要保存这种低价值占位文件：

- 只有标题
- 只有“该页面无法访问”
- 只有跳转地址
- 只有登录提示

除非用户明确说“即使抓不到正文，也先给我记入口”，否则不要写这种占位文件。

## Authentication And State

登录站点时，先阅读 `references/auth-and-state.md`。

核心规则：

- 不在聊天里要求用户贴账号密码
- 可以让用户在浏览器窗口里手动登录
- 可以保存本地认证状态文件，但不要写进仓库
- 成功登录后，优先复用已有状态，而不是每次重登

## Capture Quality Gate

在宣布“抓到了”之前，先阅读 `references/capture-quality.md`。

必须同时满足：

- 能看到正文
- 正文长度足够支撑后续阅读
- 不是壳页面或错误页
- 能说明内容主题是什么

只要有一条不满足，就不能说抓取成功。

## Scope Guardrails

- 默认抓单个链接，不默认全站爬。
- 用户如果说“抓整个网站”，先限定范围、深度、停止条件。
- 不做无限滚动式漫抓。
- 不抓与用户目标无关的导航、评论、推荐流。
- 不把“站点可达”误当成“内容已拿到”。

## Related Skills

- `agent-browser`: 登录、持久会话、交互抓取
- `playwright`: 可视化调试、复杂页面检查
- `read`: 在成功拿到正文之后再交给它判断值不值得读、做总结和沉淀

## Reference Map

- `references/workflow.md`: 常见抓取流程
- `references/auth-and-state.md`: 登录与会话状态处理
- `references/capture-quality.md`: 成功抓取的判断门槛
