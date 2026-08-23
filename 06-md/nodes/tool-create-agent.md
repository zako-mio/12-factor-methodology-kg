# create-12-factor-agent 脚手架 (create-12-factor-agent)

- ID: `tool-create-agent`
- 类型: 工具
- 来源: 工具
- 分组: G-TOOLS · 辅助工具集
- 阶段: 进阶 intermediate

> 官方 CLI 脚手架，一键生成符合 12 要素的 Agent 项目骨架

## 核心主张 (what)

- 基于 template/ 目录的一键脚手架，生成 12-factor agent 的 TS 项目骨架（package.json/tsconfig/.gitignore 齐备）
- src/ 六个核心模块：cli.ts 命令行外层循环、agent.ts 线程与 agentLoop、state.ts 文件系统线程存储、server.ts Express 事件入口、a2h.ts 人类审批 A2H API 类型、index.ts 入口
- baml_src/ 提供 BAML 工具定义：agent.baml 的 DetermineNextStep 意图枚举（HumanTools/CalculatorTools/CustomerSupportTools union）、tool_calculator.baml 四则工具、clients.baml 多 LLM 客户端、generators.baml TS 生成器
- 依赖锁定 @boundaryml/baml、humanlayer、express、zod、tsx、typescript，开箱即跑
- Thread 事件流 + serializeForLLM 把事件序列化为 XML 喂给 BAML（agent.ts）
- agentLoop 用 while(true) 按 intent 分派工具或返回 thread 转人类（agent.ts）
- FileSystemThreadStore 实现 ThreadStore 接口（create/get/update），JSON+可读文本双落盘 .threads 目录（state.ts）
- server.ts 暴露 POST /api/v1/conversations，处理 conversation.created / human_contact.completed / function_call.completed 三类事件（server.ts）

## 为什么 (why)

- 手工搭建 12-factor agent 需处理 BAML 初始化、humanlayer 审批集成、线程状态持久化等大量样板，脚手架固化官方工作坊验证过的骨架
- 六模块职责分离：状态/审批/入口/循环各自独立，不被塞进单一 agent.ts
- ThreadStore 接口抽象使状态存储可按需替换 redis/sqlite/postgres（state.ts 注释）
- 内置 divide 意图强制人类审批的完整链路演示，含 CLI 与 HTTP 双入口（cli.ts/server.ts）
- 让开发者专注扩展自己的工具与业务逻辑，而非重复配置
- BAML 生成客户端由 generators.baml 版本锁定，保证声明与实现同步

## 如何实践 (how)

- 运行脚手架把 template/ 目录复制进目标项目，改名后即可启动
- 扩展工具三步：tool_calculator.baml 加 intent 类 → agent.baml 的 union 类型加入 → handleNextStep 加 switch 分支（agent.baml/agent.ts）
- 改 clients.baml 的 provider 行切换模型提供商（openai/anthropic），baml-cli generate 重新生成客户端（clients.baml）
- 状态可替换：FileSystemThreadStore 按 ThreadStore 接口换成 redis/sqlite/postgres（state.ts）
- CLI 外层循环 cliOuterLoop：create thread → agentLoop → store.update → askHumanCLI 审批（cli.ts）
- server 外层循环 outerLoop：读事件 → reload/新建 thread → handleNextStep/推响应 → innerLoop → createHumanContact/createFunctionCall（server.ts）
- 人类审批双路径：CLI 走 approveCLI 本地交互；server 走 HumanLayer createFunctionCall 异步审批回程（cli.ts/server.ts）
- 修改 agent.baml 的 prompt 后需重跑 baml-cli generate，保证客户端与源码同步（generators.baml）

## 案例 (cases)

- 官方 2025-05-17 工作坊从裸仓库逐步手工构建出同名骨架，final/ 与 template/ 六模块完全对应（agent/state/server/cli/a2h/index）
- 模板内置 divide 意图强制人类审批分支：cli.ts 中 Enter 批准、server.ts 中 function_call.completed 事件回程执行（cli.ts/server.ts）
- 客户支持场景：agent.baml 内置 ProcessRefund 工具并强制 request_approval_from_manager 前置（agent.baml）
- 2025-05 与 2025-05-17 两份 workshop 的 walkthrough/ 每章快照即模板的逐步演进史

## 反模式/易错点

- 改 src 代码却不重跑 baml-cli generate，导致生成的 BAML 客户端与源码不同步（generators.baml 版本锁定失效）
- 跳过 a2h/state 模块，把人类审批与状态持久化全塞进 agent.ts，使循环逻辑不可维护
- 把模板当黑盒整体复制后原地修改，未按 ThreadStore 接口抽象状态存储，后续难替换
- 只在 CLI 入口验证，不测 server.ts 的 webhook 回程恢复路径，长任务审批链断裂
- 直接在模板业务上改却不维护 thread_id 回程状态，导致 server.ts 404 Thread not found（server.ts notFound）

## 源码索引（实践参考）

- `08-source/agent-packages/create-12-factor-agent/template/src/agent.ts` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/cli.ts` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/state.ts` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/server.ts` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/a2h.ts` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/index.ts` — 
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/agent.baml` — 
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/tool_calculator.baml` — 
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/clients.baml` — 
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/generators.baml` — 
- `08-source/agent-packages/create-12-factor-agent/template/package.json` — 

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| tool-create-agent → ag-nl2tool | 组合 | 脚手架内建自然语言→工具调用模板 |
| tool-create-agent → ag-tools | 组合 | 模板含 BAML 工具定义（tool_calculator） |
| tool-create-agent → ag-human | 组合 | 模板含 a2h.ts 人类批准机制 |
| tool-create-agent → ag-reducer | 组合 | 模板含 state.ts 无状态 reducer |
