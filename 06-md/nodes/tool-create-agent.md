# create-12-factor-agent 脚手架 (create-12-factor-agent)

- ID: `tool-create-agent`
- 类型: 工具
- 来源: 工具
- 分组: G-TOOLS · 辅助工具集
- 阶段: 进阶 intermediate

> 官方 CLI 脚手架，一键生成符合 12 要素的 Agent 项目骨架

## 核心主张 (what)

- 基于 template 目录的一键脚手架，生成 12-factor agent 的 TS 项目骨架（package.json、tsconfig、.gitignore 齐备）
- src/ 下六个核心模块：cli.ts 命令行外层循环、agent.ts 线程与 agentLoop、state.ts 文件系统线程存储、server.ts Express 事件入口、a2h.ts 人类审批 A2H API 类型、index.ts 入口
- baml_src/ 提供 BAML 工具定义：agent.baml 的 DetermineNextStep 意图枚举、tool_calculator.baml 加减乘除四则工具、clients.baml 多 LLM 客户端、generators.baml
- 依赖锁定 @boundaryml/baml、humanlayer、express、zod、tsx、typescript，开箱即跑

## 为什么 (why)

- 手工搭建 12-factor agent 需处理 BAML 初始化、humanlayer 审批集成、线程状态持久化等大量样板，脚手架把官方工作坊验证过的骨架固化
- 让开发者专注扩展自己的工具与业务逻辑，而非重复配置

## 如何实践 (how)

- 运行脚手架把 template 目录复制进目标项目，改名后即可启动
- 基于 Thread 的 serializeForLLM 把事件流序列化喂给 BAML，agentLoop 按意图分派工具或转人类
- 修改 agent.baml 的 client 行切换模型提供商（openai/anthropic/baseten 等），baml-cli generate 重新生成客户端
- 状态可替换：FileSystemThreadStore 按 ThreadStore 接口可换成 redis/sqlite/postgres

## 案例 (cases)

- 官方 2025-05-17 工作坊从裸仓库逐步手工构建出同名骨架（hello-world→cli-and-agent→calculator-tools→humanlayer-webhook）
- 模板内置 divide 意图强制人类审批的分支示例，演示 a2h 审批接入点

## 反模式/易错点

- 改 src 代码却不重跑 baml-cli generate，导致生成的 BAML 客户端与源码不同步
- 跳过 a2h/state 模块把人类审批与状态持久化全塞进 agent.ts，使循环逻辑不可维护
- 把模板当黑盒整体复制后原地修改，未按 ThreadStore 接口抽象状态存储

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| tool-create-agent → ag-nl2tool | 组合 | 脚手架内建自然语言→工具调用模板 |
| tool-create-agent → ag-tools | 组合 | 模板含 BAML 工具定义（tool_calculator） |
| tool-create-agent → ag-human | 组合 | 模板含 a2h.ts 人类批准机制 |
| tool-create-agent → ag-reducer | 组合 | 模板含 state.ts 无状态 reducer |
