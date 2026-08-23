# 可观测性与错误可见性 (Observability & Errors)

- ID: `t-observability`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT04 · 可观测性与错误可见性
- 阶段: 高级 advanced

> 运行可见性是传统日志与 Agent 错误压缩的共同目标

## 核心主张 (what)

- App 把日志视为聚合、有序的事件流，而非文件；关注可见性而非存储格式（logs.md）
- Agent 把错误压缩成事件回写上下文窗口，供模型在下一次决策中自愈（factor-09）
- 运行可见性是排障、审计、趋势、告警的共同基础（logs.md）
- Agent 的自愈能力完全依赖错误消息可见：LLM 读错误后修正下一次工具调用（factor-09）
- App 的十二因子应用永不关心输出流的路由或存储（logs.md）
- Agent 的错误通过 format_error 摘要而非原始堆栈进入上下文（factor-09 代码）
- 可观测性从辅助手段变为运行机制：App 事后分析，Agent 实时决策
- 错误重试需设阈值防 spin-out：单工具约 3 次尝试上限（factor-09）

## 为什么 (why)

- 日志提供运行 app 行为的可见性，是生产排障的第一现场（logs.md）
- 事件流可被索引分析系统处理：历史检索、大规模趋势绘图、启发式主动告警（logs.md）
- 自愈：好 LLM 有较高概率读错误消息或堆栈后修正后续调用（factor-09）
- 错误计数阈值是升级到人类或跳出循环的自然触发点（factor-09 代码）
- 过度重试会 spin-out，需靠控制流与上下文工程兜底（factor-09）

## 如何实践 (how)

- App：每个运行进程把事件流无缓冲写入 stdout（logs.md）
- App：环境捕获并汇聚所有流，路由到终目的地；归档目的地对 app 不可见不可配置（logs.md）
- App：Logplex/Fluentd 等开源路由可用，流可送 Splunk/Hadoop/Hive（logs.md）
- Agent：try/except 中把 type:'error'+format_error(e) 追加进 thread.events（factor-09 代码）
- Agent：consecutive_errors 计数，成功即重置，满 3 次 break/重置上下文/升级人类（factor-09 代码）
- Agent：错误与结果同以事件类型入 thread，next_step 决策天然可见全部（factor-09/agent.ts）
- Agent：结合 factor-08 可重构错误表示、移除历史事件、确定性纠偏（factor-09 提及）
- Agent：结合 factor-10 用小而专注的 Agent 从源头防 spin-out（factor-09 收尾）

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| 每个进程无缓冲写 stdout，本地开发在终端前台观察（logs.md） | 错误以事件类型入 thread，LLM 下次决策即可见（factor-09 代码） | App 观测消费者是人类（事后排障/审计）；Agent 观测消费者是 LLM（实时决策输入） |
| staging/prod 由执行环境捕获、汇聚、路由到最终目的地（logs.md） | format_error 提供摘要而非堆栈倾倒，节省上下文（factor-09） | App 事件流是外部化、单向、存档导向；Agent 错误事件是内部化、循环参与、自愈导向 |
| 流可实时 tail、路由到文件或日志索引分析系统（logs.md） | consecutive_errors 限制单工具尝试约 3 次（factor-09 代码） | 可观测性从辅助分析工具升级为 Agent 的运行机制：无错误可见即无自愈 |
| 索引分析支持：定位过去事件、按分钟绘图、自定义阈值主动告警（logs.md） | 阈值后 break 循环、重置上下文片段、或升级人类（factor-09） | App 日志写 stdout 交给环境负责；Agent 错误写回自身上下文由模型消费 |
| 目的地（如 Splunk）对 app 完全不可见、由环境管理（logs.md） | 成功则 errorCounter 归零，保证偶发失败不误触发升级（factor-09） | 差异根源：App 的人类读者在循环外，Agent 的 LLM 读者在循环内 |
| 无固定起点终点的连续流，随运行持续产出（logs.md） | 失败时 Agent 仍可继续运行：durable 属性来自错误可见而非重试无限（factor-09 收益） |  |
| App 自身不写不管理 logfile，杜绝文件锁与轮转负担（logs.md） | 错误表示可被确定性代码重构，不只是原样回填（factor-09 与 factor-08 结合） |  |

## 源码索引（实践参考）

- `08-source/app-content-en/logs.md` — 
- `08-source/agent-content/factor-09-compact-errors.md` — 
- `08-source/agent-content/factor-08-own-your-control-flow.md` — 
- `08-source/agent-content/factor-10-small-focused-agents.md` — 
- `08-source/agent-content/factor-03-own-your-context-window.md` — 

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-logs → t-observability | 前置依赖 | 从日志事件流理解可观测性 |
| t-observability → ag-errors | 前置依赖 | 可观测性落到错误压缩 |
