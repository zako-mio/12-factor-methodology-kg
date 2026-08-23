# 控制流与阶段治理 (Control Flow & Stages)

- ID: `t-control`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT06 · 控制流与阶段治理
- 阶段: 高级 advanced

> 确定性控制流 / 阶段分离保证可预测交付

## 核心主张 (what)

- 确定性控制流/阶段分离保证可预测交付
- App 分离 build/release/run
- Agent 代码控循环，LLM 只选路

## 为什么 (why)

- 阶段分离支持不可变发布回滚
- 确定性控制流可中断可审计

## 如何实践 (how)

- App release 只追加回滚
- Agent while-loop+intent 分支

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| 三阶段严格分离 | 自建控制流 LLM 决策点 | App 是部署管线纵向流程 |
| release 不可变只追加 | 选择与执行间可中断 | Agent 是运行循环横向迭代 |
| run 最少活动部件 | async break、sync continue | 前者治理交付后者治理行为 |

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-build-run → t-control | 前置依赖 | 从三阶段分离理解控制流 |
| t-control → ag-control | 前置依赖 | 控制流治理落到 Agent 编排 |
