# 工具即结构化输出 (Tools are structured outputs)

- ID: `ag-tools`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 基础 basic

> 工具只是模型的结构化输出，可无限组合

## 核心主张 (what)

- 工具不需要复杂，其核心就是『LLM 输出的结构化数据，用于触发确定性代码』——工具本质上只是结构化输出。
- 让 LLM『用其中一个工具』，本质上只是让它输出一段我们可以解析成代表这些工具的对象的 JSON，别无玄机。
- 示例：CreateIssue 类携带 intent='create_issue' 与嵌套的 Issue 对象；SearchIssues 携带 intent='search_issues' 与 query、what_youre_looking_for 查询字段。
- 模式三步：①LLM 输出结构化 JSON；②确定性代码执行对应动作（如调用外部 API）；③结果被捕获并喂回上下文。
- 这在 LLM 的『决策』与应用的『行动』之间建立了干净分离：LLM 决定做什么，但你的代码控制怎么做。
- 『LLM 调用了工具』不意味着你必须每次都去执行同一个固定函数——同一意图可以根据业务逻辑走不同实现。
- 把工具调用想成『模型输出一段描述确定性代码该做什么的 JSON』，会解锁大量灵活性，可与 factor 8 配合。
- 原文引用 switch 语句：nextStep.intent=='create_payment_link' → stripe.paymentlinks.create；'wait_for_a_while' → 某种 monadic 处理；else → 兜底。
- 『下一步』不一定原子到『执行纯函数并返回结果』，模型输出的 JSON 可以驱动更复杂、更长的控制流。
- 原文链接了 plain prompting vs tool calling vs JSON mode vs constrained generation 等路线权衡的资源，但声明不展开讨论。

## 为什么 (why)

- 决策与执行解耦：LLM 只输出『意图+参数』的 JSON，具体怎么执行由确定代码决定，行为可预测、可审计。
- 同样的 JSON 意图可以映射到不同实现，随业务变化灵活调整，不锁死工具与函数的严格一一对应，实现可独立演进。
- 为掌控控制流铺路：既然工具是 JSON，你就可以在 JSON 与执行之间插入审批、暂停、重试等逻辑（factor 8）。
- 结构化输出天然可测试：schema 明确、解析稳定，比解析自由文本可靠得多，回归有保障，错误能准确定位到字段。
- 符合『Agent 循环』第一步的标准化产出，后续每一步（执行、回写、再决策）都能被确定性处理，全链路可控。

## 如何实践 (how)

- 用数据类（Python class 或 BAML class）定义每个工具：intent 字段加业务参数，如 CreateIssue 内含 intent 与嵌套的 Issue 对象。
- 让 LLM 基于 schema 输出 JSON，用 BAML 的 type 联合（如 HumanTools \| CalculatorTools）约束可选项，从类型上杜绝未知意图。
- 在确定性代码里按 intent 做 switch/if 分发：命中执行外部 API，未命中走 else 兜底，保证流程不中断。
- 把每次工具调用的结果捕获并追加回上下文（thread.events），供模型决定下一步，形成闭环，执行信息不丢失。
- 模板实现：agent.ts 的 handleNextStep 对 add/subtract/multiply/divide 分别计算并把 tool_response 事件 push 进 thread。
- 用 @description 注解给 BAML 类补充行为约束，例如 ProcessRefund 注明『退款前必须先向经理请求批准』。
- 用 @description 给字段补充说明，例如 DoneForNow.message 注明『写给用户的工作完成说明』。
- 把工具输出与意图组合成联合类型返回（DetermineNextStep -> HumanTools \| CalculatorTools \| CustomerSupportTools），让类型系统承接工具集。

## 案例 (cases)

- CreateIssue / SearchIssues 两个工具类的定义示例，intent 字段加业务参数结构。
- Issue 嵌套对象：title/description/team_id/assignee_id 四个字段的完整定义。
- switch 语句示例：nextStep.intent == 'create_payment_link' → stripe.paymentlinks.create 的执行分支。
- 模板 BAML 工具：AddTool/SubtractTool/MultiplyTool/DivideTool 四个计算器类（intent add/subtract/multiply/divide，a/b 为 int\|float）。
- ProcessRefund 类：intent 'process_refund'，含 order_id/amount/reason，注解要求退款前请求经理批准。
- type CalculatorTools = AddTool \| SubtractTool \| MultiplyTool \| DivideTool 的联合类型定义。
- 模板 agent.ts 的 handleNextStep：按 intent 分发并返回更新后的 thread，供外层循环继续。
- 原文链接资源：boundaryml schema-aligned parsing、Vellum 的 function calling vs structured outputs vs JSON mode、LlamaIndex 对比。

## 反模式/易错点

- 把每个工具与固定函数一一绑定，丧失『同一意图不同实现』的灵活性，业务变化时不得不重构，可维护性差。，属于该因子的基础原则，应在设计中显式落实。
- 让 LLM 直接输出要执行的代码字符串，而不是结构化的『意图+参数』JSON，解析与安全风险陡增，务必拒绝此做法。
- 模型返回未知意图时不设 else 兜底，直接抛错中断，整个 Agent 流程随之失败，应走降级或澄清路径。
- 忽略工具结果、不把执行结果喂回上下文，破坏循环闭环，模型无法基于结果继续决策，决策成了无源之水。，属于该因子的基础原则，应在设计中显式落实。
- 为每个细微动作都定义独立工具，工具爆炸导致 schema 庞大、模型选择困难、维护成本失控，应合并相近意图。
- 把高风险执行逻辑直接交给 LLM 驱动的函数而不做控制流介入，缺少 factor 8 的保护，必须加审批断点。

## 源码索引（实践参考）

- `08-source/agent-content/factor-04-tools-are-structured-outputs.md` — 原文完整内容：工具即结构化输出的三步模式
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/tool_calculator.baml` — 模板计算器工具类：Add/Subtract/Multiply/Divide
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/agent.baml` — 模板工具联合类型与函数签名（HumanTools/CalculatorTools/CustomerSupportTools）
- `08-source/agent-packages/create-12-factor-agent/template/src/agent.ts` — 模板 handleNextStep 按 intent 分发执行的确定性代码

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-nl2tool → ag-tools | 前置依赖 | 工具是自然语言调用的结构化输出 |
| ag-tools → ag-human | 前置依赖 | 联系人类是一类工具调用 |
| ag-tools → ag-control | 前置依赖 | 工具组合受控制流编排 |
| t-deps → ag-tools | 前置依赖 | 显式化落到工具定义 |
| app-deps → ag-tools | 变体 | 依赖清单 ↔ 工具定义 |
| ag-tools → ag-human | 组合 | 工具 + 人类批准 |
| app-backing → ag-tools | 依赖关联 | 工具是 Agent 的外部后端服务 |
| tool-create-agent → ag-tools | 组合 | 模板含 BAML 工具定义（tool_calculator） |
