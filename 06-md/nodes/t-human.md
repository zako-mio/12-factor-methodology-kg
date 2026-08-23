# 人为交互边界 (Human Interaction Boundary)

- ID: `t-human`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT09 · 人为交互边界
- 阶段: 高级 advanced

> 一次性管理任务 / 人类批准，皆是人机协作边界

## 核心主张 (what)

- App 的管理/维护任务作为一次性进程运行，与常规进程同环境（admin-processes.md）
- Agent 把人类接入建模成一类工具调用，主动寻求批准（factor-07）
- App 管理进程包括数据库迁移、REPL 控制台、一次性脚本（admin-processes.md）
- Agent 的 RequestHumanInput 工具带 question/context/options（urgency/format/choices）（factor-07 代码）
- 高赌注动作需人把关：App 运维操作、Agent 审批前不执行（factor-08/07）
- 人机协作不打断主路径：App admin 独立进程、Agent 异步 break 等响应（factor-07 durable）
- Agent 人类响应经 webhook 恢复 thread 续跑（factor-07/server.ts）
- 人从操作者变决策者：两侧边界的角色迁移

## 为什么 (why)

- 迁移/REPL/修复脚本是应用运维刚需，需在一致环境下运行（admin-processes.md）
- admin 进程用与常规进程相同的代码库和 config，避免同步问题（admin-processes.md）
- 人类联系工具化让 LLM 以结构化方式请求输入与审批（factor-07）
- 可协调多个不同人类的结构化输入（factor-07）
- 与暂停恢复结合形成持久、可靠、可检视的多人工作流（factor-07 收益 5）

## 如何实践 (how)

- App：manage.py migrate / rake db:migrate 运行迁移（admin-processes.md）
- App：python/perl 无参解释器或 irb/rails console 开 REPL（admin-processes.md）
- App：一次性脚本入 repo（php scripts/fix_bad_records.php）同环境执行（admin-processes.md）
- Agent：定义 RequestHumanInput 工具，LLM 输出结构化请求（factor-07 代码）
- Agent：request_human_input 分支保存 thread 状态并 notify_human 后 break（factor-07 代码）
- Agent：webhook 带 thread_id 恢复，加载状态追加响应继续决策（factor-07/server.ts）
- Agent：divide 意图在 cli.ts 请求 Enter 审批、在 server.ts 经 HumanLayer function_call 审批（cli.ts/server.ts）
- Agent：function_call.completed 中 approved 才执行工具，否则写入拒绝反馈（server.ts）

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| Django manage.py migrate、Rails rake db:migrate（admin-processes.md） | 人类联系工具化：RequestHumanInput 声明 urgency/format/choices（factor-07） | App 侧人是运维执行者（运行迁移/脚本）；Agent 侧人是自动决策节点（批准/提供信息） |
| REPL 检查活库模型：python/irb/rails console（admin-processes.md） | save_state + notify_human + return 打断循环，等响应回带 thread ID（factor-07 代码） | App 管理任务手动触发一次性运行；Agent 审批自动等待循环内工具 |
| 一次性修复脚本提交进应用 repo（admin-processes.md） | webhook 收到 response_from_human 事件加载 thread 续跑（factor-07/server.ts） | App admin 进程独立于 process formation；Agent 审批是循环内的工具调用 |
| admin 代码随应用发布，避免同步问题（admin-processes.md） | 内层/外层循环支持 Agent→Human 初始化（外环 agent）（factor-07） | App 人机边界在部署管线外；Agent 人机边界在推理循环内 |
| 全部进程类型用同一依赖隔离技术（bundle exec rake db:migrate）（admin-processes.md） | 多人类输入协调：通过结构化事件跟踪不同来源（factor-07） | 差异根源：App 人类执行事后维护、Agent 人类参与事前决策 |
| 本地直接 shell 命令、生产用 ssh/远程执行机制（admin-processes.md） | 多 Agent 扩展：同一抽象支持 Agent→Agent 请求响应（factor-07） |  |
| 偏好自带 REPL 且易跑一次性脚本的语言（admin-processes.md） | server.ts 的 divide 分支：createFunctionCall 提交审批、回程执行/拒绝（server.ts） |  |
|  | cli.ts 的 askHumanCLI：Enter 批准、带反馈取消（cli.ts） |  |

## 源码索引（实践参考）

- `08-source/app-content-en/admin-processes.md` — 
- `08-source/app-content-en/dependencies.md` — 
- `08-source/agent-content/factor-07-contact-humans-with-tools.md` — 
- `08-source/agent-content/factor-06-launch-pause-resume.md` — 
- `08-source/agent-content/factor-08-own-your-control-flow.md` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/cli.ts` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/server.ts` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/a2h.ts` — 

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-admin → t-human | 前置依赖 | 从管理进程理解人机边界 |
| t-human → ag-human | 前置依赖 | 人机边界落到人类批准 |
