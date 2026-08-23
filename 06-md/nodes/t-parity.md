# 环境一致性 (Environment Parity)

- ID: `t-parity`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT10 · 环境一致性
- 阶段: 高级 advanced

> 开发与生产一致，传统靠环境等价，Agent 靠 prompt 版本化

## 核心主张 (what)

- 开发生产一致，传统靠环境等价
- Agent 靠 prompt 版本化
- 缩小差异才能持续交付

## 为什么 (why)

- dev/prod 差异致「开发能过生产失败」
- Agent 侧不一致则「本地能跑上线失控」

## 如何实践 (how)

- App 缩小三大差距
- Agent 确定性组件优先
- 官方现代化：可观测性+Identity

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| 三大差距最小化 | prompt/上下文构建函数化 | App 靠环境等价（同构环境） |
| 各 deploy 同类型同版本服务 | 确定性组件优先 | Agent 靠可复现性（版本化可回放） |
| 容器虚拟贴近生产 | LLM 作库而非框架 | 从同构环境演进到同构行为 |

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-dev-prod → t-parity | 前置依赖 | 从环境等价理解一致性 |
| t-parity → ag-prompts | 前置依赖 | 一致性落到 prompt 环境 |
