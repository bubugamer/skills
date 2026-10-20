# 工作区约定

首次接入知识库，或材料位置、页面规则、站点命令不明确时读本篇。约定属于知识库项目；skill 提供识别方法和填写参考。

## 找到操作范围

先读取用户选定项目的说明、入口页、相关页面与现有配置，确认：

- 项目根与知识页目录；两者可能不同。
- 原始资料、阅读笔记和附件的位置，以及本次可写范围。作为证据使用的原始资料保持原样。
- 首页、主题入口、站点导航与活动日志的位置及各自职责。
- 页面类型、属性、状态、证据标注、链接语法与发布约定。
- 本地站点的启动方式、运行目录、地址、依赖与停止方式；仅在操作站点时读取这些设置。

从已有文件能确定的信息直接沿用；只对影响本次操作的未决事项提问。纯查询无需先补全一份配置。已有约定缺项时，先采用本次需要的最小补充，不批量改造旧页面。

所有相对路径都应注明基准。来源目录可以位于知识库外，读取来源不扩大本次写入范围。执行工具前确认其 `--root` 指向项目根还是页面目录。

## 项目说明示例

下方是可放入知识库已有项目说明的示例，文件名由项目决定。它不是要求用户事先手填的表单。使用过程中可以根据现有文件整理；需要新建或修改项目说明时，沿用本次授权。

```yaml
# 示例：路径均相对用户选定的知识库项目根；按真实项目调整。
pages_root: docs
source_roots: [materials]
home: docs/index.md
topic_pages: [docs/topics/overview.md]
activity_log: docs/log.md
navigation:
  kind: mkdocs
  config: mkdocs.yml
  home_scope: topic-pages
  site_scope: configured-pages
page_conventions:
  content_fields: [title, created, last_updated, status, tags, sources]
  topic_type: topic
  statuses: [草稿, 已看过, 已确认]
  link_style: markdown
  visibility: project-defined
site:
  working_directory: .
  start_command: bash serve.sh
  url: http://127.0.0.1:8000
  readiness: http-response
  stop: recorded-process-or-project-service
```

示例中的 `docs`、`materials`、`serve.sh` 与地址不是 skill 默认值，也不表示文件或服务已经存在。没有站点的纯 Markdown 知识库可省略站点设置。属性和导航行为见 [页面约定](page-conventions.md) 与 [导航说明](navigation.md)。

## 通用规则与个人设置

- 通用规则：先查已有知识、保留证据、区分状态、维护链接与记录变更。
- 项目设置：个人 PARA 路径、首页和日志文件名、主题树、MkDocs 配置、可见性处理、启动脚本、端口和运行环境。
- 运行信息：本次启动的进程、实际地址与日志留在本地操作记录；登录状态、密钥和虚拟环境不打包进 skill。

沿用发布约定时，检查实际构建流程如何解释 `visibility`、缺省值和导航排除。仅有属性名不能证明页面已经受到过滤。
