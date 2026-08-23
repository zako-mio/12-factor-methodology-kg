# 掌控上下文窗口 (Own your context window)

- ID: `ag-context`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 进阶 intermediate

> 对上下文进行工程化管理（上下文工程）

## 核心主张 (what)

- 你不需要拘泥于标准消息格式来向 LLM 传递上下文：『任何时刻，你给 LLM 的输入本质上就是：到目前为止发生了什么，下一步是什么』。
- 一切都是上下文工程。LLM 是『把输入变成输出的无状态函数』，要得到最好的输出，就必须给它最好的输入。
- 好的上下文包括：给模型的 prompt 与指令、检索到的文档或外部数据（如 RAG）、过去状态/工具调用/结果等历史、记忆、结构化输出指令。
- 原文声明不讨论 temperature/top_p/frequency_penalty/presence_penalty 等采样参数，也不讨论训练模型或微调——本指南聚焦纯上下文构造。
- 标准消息格式是 role=system/user/assistant/tool 的数组，assistant 消息里带 tool_calls（id/name/arguments），tool 消息用 tool_call_id 回传结果。
- 替代方案：自建针对你用例优化的上下文格式，把自定义对象打包/展开进一个或多个 user/system/assistant/tool 消息中。
- 原文示例把整个上下文窗口放进一条 user 消息：用 <slack_message>、<list_git_tags>、<list_git_tags_result> 等 XML 标签表达事件流。
- 你可以完全控制『存什么 vs 传给 LLM 什么』：实验不同的上下文结构会带来明显的质量提升，这是上下文工程的核心杠杆。
- 上下文窗口是你与 LLM 的主接口，掌控其结构能大幅提升 Agent 性能；原文给出信息密度对比图证明同语义可更少 token。
- 发布约两月后『context engineering』流行：原文引用 Karpathy、Tobi 讨论与 @lenadroid 的 Context Engineering Cheat Sheet 佐证。

## 为什么 (why)

- 信息密度：以最大化 LLM 理解的方式组织信息，相同语义用更少 token 表达，注意力更集中、理解更准。
- 错误处理：以有助于 LLM 恢复的格式包含错误信息，错误和失败调用解决后应主动从上下文窗口隐藏，防止历史失败干扰。
- 安全性：严格控制什么信息进入 LLM，过滤敏感数据，防止密码、密钥等意外泄露给模型，泄露面可收敛到最小。
- 灵活性：随着你对用例理解的深入，可以随时调整上下文格式，不必被框架锁死，结构迭代也无需迁移任何系统。
- Token 效率：为 token 效率与 LLM 理解力双重优化上下文格式，长上下文成本与质量双收益。
- LLM 是无状态函数，只有把『最佳输入』喂给它才能得到『最佳输出』，而这完全取决于你的上下文构造能力。
- 上下文工程在 2025 年中成为热门概念，社区（Karpathy 等）与工具链都验证了这一方向的正确性。

## 如何实践 (how)

- 定义 Thread/Event 模型：Thread.events 为事件列表，Event 有 type（list_git_tags、deploy_backend、error 等 Literal 联合类型）与 data。
- 实现 event_to_prompt(event)：把事件渲染为 <type>\n数据\n</type> 的 XML 风格字符串，对象数据用 stringifyToYaml 嵌入。
- 实现 thread_to_prompt(thread)：用 \n\n 把各事件渲染串接成最终喂给 LLM 的上下文窗口。
- 上下文演进演示：初始 <slack_message> 追加 <list_git_tags> 与 <list_git_tags_result>，出错加 <error>，再追加 <request_more_information> 与 <human_response>。
- 用 determine_next_step(thread_to_prompt(thread)) 把自建上下文喂给 LLM，获取下一步意图（如 get_workflow_status 与 workflow_name）。
- 把『What's the next step?』显式写进 prompt 模板，虽然模型可能从工具 schema 推断，但显式声明总是无坏处。
- 把错误信息以 XML 标签结构化进上下文，同时考虑在解决后从窗口移除，避免失败历史污染后续推理，这本身就是格式实验。
- 实验性地决定『存什么 vs 传什么』，用信息密度对比（同语义更少 token）验证格式收益，再推广到全部事件类型。
- 工具模板参考 create-12-factor-agent/template/src/agent.ts：serializeForLLM/serializeOneEvent 把事件序列化为 <intent>k: v</intent> 格式。

## 案例 (cases)

- 标准消息格式示例：system+user+assistant(tool_calls: list_git_tags)+tool 消息返回 v1.2.3/v1.2.2/v1.2.1 的 tags 数组。
- 单条 user 消息打包全部上下文的 <slack_message>…</slack_message> 方案，XML 风格事件流。
- Python Thread/Event 类代码：Event.type 为 Literal["list_git_tags",…,"error"] 联合类型定义。
- event_to_prompt 的 f"<{event.type}>\n{data}\n</{event.type}>" 渲染逻辑与 stringifyToYaml 数据序列化。
- 错误后恢复的上下文示例：<error> error running deploy_backend: Failed to connect to deployment service </error>。
- 模板实现：agent.ts 的 serializeOneEvent 输出 <multiply>\na: 3\nb: 4\n</multiply> 这类 XML 风格事件。
- @lenadroid 的 Context Engineering Cheat Sheet（2025-07），原文配图引用作为社区资源。
- Karpathy 与 Tobi（Vercel CEO）关于上下文工程的推文截图，发布于 2025 年中。

## 反模式/易错点

- 无条件沿用标准 messages 数组格式，从不针对用例优化结构，白白浪费 token 与注意力，应至少做一次格式对比实验。
- 把未解决的错误事件长期留在上下文里，模型反复看到失败历史，严重影响后续决策质量，错误解决后应立即隐藏。
- 用调采样参数（temperature/top_p 等）来弥补上下文构造不足，而不是去优化输入本身，治标不治本。
- 把敏感数据（密码上下文、session id 等）不加过滤直接塞进上下文，造成泄密风险，机密应留在外部存储。
- 只堆砌『发生了什么』而不显式声明『下一步是什么』，模型只能靠猜，决策稳定性差，务必把引导句写进模板。
- 把工具结果以大段 JSON 原文塞入而不做压缩/结构化，token 效率与可读性双输，应按事件语义重新组织。
- 上下文越长越不管理，违反『隐藏已解决错误、修剪无关节』的纪律，为错误空转埋下隐患，要主动修剪历史、定期压缩。

## 源码索引（实践参考）

- `08-source/agent-content/factor-03-own-your-context-window.md` — 原文完整内容：上下文工程、标准 vs 自定义格式、Thread/Event 代码
- `08-source/agent-packages/create-12-factor-agent/template/src/agent.ts` — 模板实现：serializeForLLM/serializeOneEvent 的 XML 序列化
- `08-source/agent-workshops/2025-05/walkthrough.md` — workshop Chapter 7 定制上下文窗口：JSON pretty-print 到 XML 序列化

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-prompts → ag-context | 前置依赖 | 拥有 prompt 才能掌控上下文 |
| ag-context → ag-errors | 前置依赖 | 错误压缩是上下文工程应用 |
| ag-context → ag-errors | 组合 | 上下文 + 错误压缩 |
