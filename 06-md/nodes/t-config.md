# 配置与可变性外置 (Config Externalization)

- ID: `t-config`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT03 · 配置与可变性外置
- 阶段: 高级 advanced

> 可变部分（环境变量 / prompt）外置于代码之外

## 核心主张 (what)

- 可变部分外置：config 入 env，prompt 作代码
- 变更不触及核心逻辑
- 外置是版本化/回滚/审计前提

## 为什么 (why)

- 配置随部署变化而代码不变
- prompt 是 Agent 的配置面

## 如何实践 (how)

- App 用 env vars 按 deploy 管理
- Agent 把 prompt 版本化测试回滚

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| 配置全入 env vars | prompt 版本化可回滚 | App 外置的是运行时值 |
| 开源不泄凭据试金石 | 不被框架外包 | Agent 外置的是指令与策略 |
| 拒绝 config 文件与分组 | 上下文构建函数化 | Agent 的外置物本身是代码 |

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-config → t-config | 前置依赖 | 从环境配置理解可变性外置 |
| t-config → ag-prompts | 前置依赖 | 可变性外置落到 prompt 管理 |
