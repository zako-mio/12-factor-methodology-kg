# 掌控控制流 (Own your control flow)

- ID: `ag-control`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 进阶 intermediate

> 控制流由代码决定，LLM 只做决策点

## 核心主张 (what)

- 自建控制结构，工具选择与执行间可中断
- 某些工具调用是跳出循环的理由
- 可融入缓存/LLM-judge/限速等

## 为什么 (why)

- 无该粒度被迫三选一：sleep/低风险/yolo
- 自建才能支持自然工作流

## 如何实践 (how)

- while True 按 intent 分支
- async break、sync continue

## 案例 (cases)

- handle_next_step 三分支

## 反模式/易错点

- while...sleep 内存等待
- 限制低风险调用
- 无复核的 yolo

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-nl2tool → ag-control | 前置依赖 | 工具调用需要确定性控制流 |
| ag-tools → ag-control | 前置依赖 | 工具组合受控制流编排 |
| ag-control → ag-reducer | 前置依赖 | 确定性控制流保障 reducer 语义 |
| t-control → ag-control | 前置依赖 | 控制流治理落到 Agent 编排 |
| app-build-run → ag-control | 变体 | 阶段分离 ↔ 控制流所有权 |
