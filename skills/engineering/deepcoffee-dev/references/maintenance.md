# 维护清理与测试账号重置

执行命令前，按 [runtime.md](runtime.md) 解析脚本位置与后端运行环境；以下变量指向已核实的本地文件，不是需要直接照抄的默认路径。

## 能力：cleanimg（图片存储 + 支付维护清理）

检查并清理后台积压：**图片删除队列**（`storage_delete_queue`）+ **过期反馈截图**（满 15 天已处理反馈）+ **Stripe 取消队列**（`subscription_cancel_queue`，落选订阅取消失败的重试）+ **支付宝过期订单对账**。这是 0.63.0「持久化删除队列」与 0.66.0「支付维护」机制的人工触发端——队列保证晚清理只是延后、绝不丢。现有 Codex 与 Claude 流程共用同一份维护脚本，实际位置由 `DEEPCOFFEE_MAINTENANCE_SCRIPT` 解析。

1. **check（只读，秒级）**：
   ```bash
   cd deepcoffee-api && .venv/bin/python "$DEEPCOFFEE_MAINTENANCE_SCRIPT"
   ```
   输出各队列待办数。表不存在（对应版本未部署 / 迁移未跑）会优雅跳过，不算错误。
2. **有积压就清**（沿用用户已有的常规清理授权；当前请求限制优先，数字异常大先确认）：
   ```bash
   cd deepcoffee-api && .venv/bin/python "$DEEPCOFFEE_MAINTENANCE_SCRIPT" --apply
   ```
   做：反馈过期清理 + 图片删除队列排空 + Stripe 取消队列排空（重读赢家、幂等）+ 支付宝过期对账（trade.query 校验金额后开通 / 否则标过期）。全部直连生产 DB / Storage / 支付网关。
3. 把结果数字回报用户；有失败重排的行提一句「下次清理会继续重试」。

注意：`--apply` 写生产库、删存储文件、可能取消 Stripe 订阅——但都是产品承诺该做的常规维护，执行沿用用户实际已确认的常规维护范围；skill 文本本身不新增授权。若本地工作区不在含对应版本代码的分支，脚本导入失败并提示，切回 main 拉最新即可。

## 能力：resetacc（重置测试账号数据）

用于清空某个测试账号的豆卡、冲煮记录、聊天会话、器具，保留账号和用量。

1. 先 dry-run：
   ```bash
   cd deepcoffee-api && .venv/bin/python "$DEEPCOFFEE_RESET_SCRIPT" <email>
   ```
2. 已有针对该账号与范围的执行确认时直接继续；缺少确认时，在预览后取得确认再执行：
   ```bash
   cd deepcoffee-api && .venv/bin/python "$DEEPCOFFEE_RESET_SCRIPT" <email> --apply
   ```
