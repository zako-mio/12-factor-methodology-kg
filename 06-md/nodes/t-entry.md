# 自含入口与触达 (Self-contained Entry)

- ID: `t-entry`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT07 · 自含入口与触达
- 阶段: 高级 advanced

> 自含导出服务 / 随处触发，皆是不依赖宿主

## 核心主张 (what)

- App 完全自含，通过绑定端口导出 HTTP 服务，不依赖运行时注入 webserver（port-binding.md）
- Agent 从用户所在渠道（slack/email/sms 等）触达与回复（factor-11）
- App 的 webserver 库（Tornado/Thin/Jetty）随依赖声明进入 user space（port-binding.md）
- Agent 支持非人类触发源：事件、cron、故障等外环触发（factor-11 outer loop）
- 入口由应用自定而非宿主注入：App 自含端口、Agent 自含通道
- 端口绑定使一个 app 可成为另一个 app 的 backing service（port-binding.md）
- Agent 外环 Agent 可工作 5-90 分钟，到关键点联系人类（factor-11）
- 自含性保证最大可移植性，不依赖特定宿主环境（intro.md）

## 为什么 (why)

- 自含导出保证 app 可在任何执行环境运行，无需预装特定 web 容器（port-binding.md）
- 不依赖宿主才能保证触达：用户在哪个渠道就到哪里服务（factor-11）
- 多通道让 AI 应用感觉像真实数字同事（factor-11）
- 能快速拉人审批使 Agent 敢用更高赌注的工具（factor-11）
- 入口自主是自包含与可迁移的前提（port-binding.md/intro.md）

## 如何实践 (how)

- App：通过依赖声明引入 webserver 库，绑定端口监听（port-binding.md）
- App：本地访问 http://localhost:5000/，部署由路由层转发（port-binding.md）
- App：Procfile 声明 web: ruby web.rb -p $PORT，端口来自环境（Procfile）
- Agent：server.ts 暴露 POST /api/v1/conversations 作为 HTTP 事件入口（server.ts）
- Agent：cli.ts 提供命令行外层循环作为本地入口（cli.ts）
- Agent：HumanLayer 集成经 createHumanContact 通知 slack/email 等渠道（server.ts）
- Agent：webhook 事件（conversation.created/human_contact.completed）驱动恢复与续跑（server.ts）
- Agent：server 端口由 env PORT \|\| 8000 决定，同样遵循自含绑定（server.ts）

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| PHP 跑 Apache 模块、Java 跑 Tomcat 容器是依赖注入的反例（port-binding.md） | slack/email/sms 等多通道触发与回复（factor-11） | App 入口是单一技术端口（TCP/HTTP）；Agent 入口是多业务渠道（slack/email/sms/webhook） |
| 本地开发 URL http://localhost:5000/ 访问自含服务（port-binding.md） | 非人类源触发：事件、cron、故障、outage 等（factor-11 outer loop） | App 面向服务导出与流量路由；Agent 面向对话触达与事件驱动 |
| 部署时路由层从公网域名转发到端口绑定进程（port-binding.md） | 外环模式：Agent→Human 而非 Human→Agent 的初始化（factor-07 提及 + factor-11） | App 从端口自含扩展自包含；Agent 从随处触发扩展到用户触达 |
| HTTP 非唯一可导出协议：XMPP/Redis 协议同样适用（port-binding.md） | 快速循环人类审批使高赌注工具可用（factor-11） | App 的消费方是另一个程序（routing layer）；Agent 的消费方是用户所在的业务系统 |
| 一个 app 可作另一 app 的 backing service，用 config 句柄消费（port-binding.md） | conversation.created 事件创建新 thread 启动会话（server.ts） | 差异根源：App 服务抽象是端口、Agent 服务抽象是渠道与会话 |
| 绑定发生在 user space 即 app 代码内，与执行环境契约只是端口（port-binding.md） | human_contact.completed 恢复对应 thread 继续 agentLoop（server.ts） |  |
| 12factor.net 自身即经 $PORT 绑定导出的实例（Procfile） | cli.ts 与 server.ts 双入口共享同一 agentLoop 核心（cli.ts/server.ts） |  |

## 源码索引（实践参考）

- `08-source/app-content-en/port-binding.md` — 
- `08-source/app-content-en/backing-services.md` — 
- `08-source/app-content-en/intro.md` — 
- `08-source/app-deploy/Procfile` — 
- `08-source/app-deploy/web.rb` — 
- `08-source/agent-content/factor-11-trigger-from-anywhere.md` — 
- `08-source/agent-content/factor-06-launch-pause-resume.md` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/server.ts` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/cli.ts` — 

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-port → t-entry | 前置依赖 | 从端口绑定理解自含入口 |
| t-entry → ag-trigger | 前置依赖 | 自含入口落到随处触发 |
