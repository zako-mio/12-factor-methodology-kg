# 规模化与单元粒度 (Scaling & Granularity)

- ID: `t-scaling`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT08 · 规模化与单元粒度
- 阶段: 高级 advanced

> 进程模型扩展 / 小 Agent 组合，皆是单元化扩展

## 核心主张 (what)

- App 用进程模型横向扩展：share-nothing、可水平分区（concurrency.md）
- Agent 用多个小而专注的 Agent 组合，而非单个巨型 Agent（factor-10）
- App 中进程是 first-class citizen，按工作类型分 process type（concurrency.md）
- Agent 每个小 Agent 聚焦单一领域，3-10 步最多 20 步（factor-10）
- 单元化扩展两种形态：App 靠副本数、Agent 靠能力组合
- 巨型单元难维护：App 单 JVM uberprocess 受限、Agent 长上下文易迷失（concurrency.md/factor-10）
- Agent 是更大确定性系统中的一个构建块（factor-10）
- 规模化是进程编队（formation）与小 Agent 编排（DAG）的共同主题

## 为什么 (why)

- 单个 VM 只能纵向扩展且增长有限，必须能跨多机多进程扩展（concurrency.md）
- 上下文越长 LLM 越易迷失或失去焦点，小步聚焦保性能（factor-10）
- share-nothing 进程使扩容简单可靠，加并发是可靠操作（concurrency.md）
- 小 Agent 带来：上下文可控、责任清晰、可靠性高、易测试、易调试（factor-10 五收益）
- 即便 LLM 变强，小 Agent 仍必要：可渐进扩大范围而保质量（factor-10）

## 如何实践 (how)

- App：按工作类型定义 process type（web/worker），每类型可 0..n 实例（concurrency.md）
- App：进程编队 formation 由类型数组与实例数构成（concurrency.md）
- App：进程不 daemonize 不写 PID 文件，交进程管理器（concurrency.md）
- App：单进程内可用线程/async 复用，但扩展仍靠多进程（concurrency.md）
- Agent：把任务拆给聚焦单领域的小 Agent，控制上下文规模（factor-10）
- Agent：用确定性 DAG 编排小 Agent，追求微代理在确定性 DAG 模式（workshop 2025-07-16）
- Agent：随 LLM 能力增强渐进扩大 agent scope，而非一次做大（factor-10）
- Agent：小 Agent 便于随处触发与独立测试（factor-10/11）

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| PHP 按需子进程、Java 单 uberprocess 是两种极端（concurrency.md） | 小 Agent 聚焦单领域、步数受控，上下文窗口保持小（factor-10） | App 单元是同质进程副本；Agent 单元是异质能力的小 Agent |
| web 进程处理 HTTP 请求、worker 处理后台长任务（concurrency.md） | 责任清晰：每个 Agent 有明确定义的 scope 与目的（factor-10） | App 扩展靠增加副本数（水平分区）；Agent 扩展靠能力组合（DAG 编排） |
| 线程/async（EventMachine/Twisted/Node）可内部复用但非扩展手段（concurrency.md） | 可靠性高：不轻易在复杂工作流中迷失（factor-10） | App 单元由系统进程管理器调度；Agent 单元由确定性编排器调度 |
| 跨多物理机多进程运行，水平分区可行（concurrency.md） | 易测试易调试：可单独验证特定功能（factor-10） | App 规模化面向吞吐；Agent 规模化面向任务复杂度 |
| 进程管理器管理输出流、响应崩溃、处理重启（concurrency.md） | 确定性 DAG 编排多个小 Agent（workshop 2025-07-16 方向） | 差异根源：App 资源瓶颈是计算/内存；Agent 瓶颈是上下文/注意力 |
| systemd/云平台分布式进程管理器/Foreman 承担治理（concurrency.md） | 边界贴近模型能力可创造魔法时刻（factor-10 引 NotebookLM） |  |
| 扩容即增加 process formation 中某类型实例数（concurrency.md） | 渐进扩展：今天拿到结果，明天随上下文可靠而扩大 scope（factor-10） |  |

## 源码索引（实践参考）

- `08-source/app-content-en/concurrency.md` — 
- `08-source/app-content-en/processes.md` — 
- `08-source/agent-content/factor-10-small-focused-agents.md` — 
- `08-source/agent-content/factor-11-trigger-from-anywhere.md` — 
- `08-source/agent-content/factor-12-stateless-reducer.md` — 
- `08-source/agent-workshops/2025-07-16/walkthrough.yaml` — 

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-concurrency → t-scaling | 前置依赖 | 从进程扩展理解规模化 |
| t-scaling → ag-small | 前置依赖 | 规模化落到小 Agent 组合 |
