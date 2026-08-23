# 自然语言→工具调用 (NL to Tool Calls)

- ID: `ag-nl2tool`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 基础 basic

> LLM 将自然语言转换为结构化工具调用对象

## 核心主张 (what)

- Agent 构建中最常见也最强大的模式，就是把用户的自然语言请求翻译成结构化的工具调用对象，让 LLM 既能推理任务又能驱动系统真正执行动作。
- 原子化应用时，它只是把一句话如『能否给 Terri 创建一笔 750 美元的付款链接，赞助二月的 AI Tinkerers 聚会』翻译成一个描述 Stripe API 调用的结构化 JSON 对象。
- 结构化对象包含 function.name 与 function.parameters，例如 name=create_payment_link，parameters 内含 amount=750、customer、product、price、quantity、memo 等字段。
- 真正的 Agent 在构造 payload 前需要先查询系统：列客户、列商品、列价格，把正确的 ID 填进参数，而不是凭空猜测 ID 值。
- 翻译完成后由确定性代码接手：LLM 只负责『下一步做什么』的决策，工具 payload 的执行交给普通程序逻辑，完全不依赖模型随机性。
- 原文给出 Python 示例：llm.determineNextStep(自然语言) 返回 nextStep 对象，再按 nextStep.function 走 if/elif 分支分发执行。
- 若模型返回了系统不认识的功能名，代码必须落入 else 分支做兜底处理，例如记录日志或向用户请求澄清，而不是直接崩溃。
- 原文明确说明：这一步刻意跳过『拿到结果后再循环、最终回给用户』的闭环，把循环留到后面其他因子（如 factor 3/8）再补全。
- 演示中真实返回形如『已成功为 Terri 创建 750 美元付款链接，链接见 buy.stripe.com/test_1234567890』，说明该模式最终仍要闭环交付。
- 该模式是后面所有因子的地基：工具即结构化输出、掌控上下文、掌控控制流都从这一个原子翻译步骤展开而来。

## 为什么 (why)

- 这是把 LLM 的『自然语言理解』与系统的『确定性执行』连接起来的最直接方式，几乎所有 Agent 应用都离不开它。
- 结构化输出让后续处理可以依赖完全确定的代码：一旦拿到对象，if/else 分发、参数校验、执行都不再需要模型参与，行为可预测。
- 相比让模型自由发挥文本，结构化输出把决策空间显式化，降低了解析失败和幻觉参数混入真实执行环节的风险。
- 先查询再构造 payload 的做法让参数中的 customer/product/price 等 ID 来自真实数据源，而不是模型猜测，正确性大幅提升。
- 原文强调这是『最常见』的模式，意味着工程上高度成熟，围绕它可以积累大量可复用工具、schema 与最佳实践模板。

## 如何实践 (how)

- 先定义清晰的工具/函数名与参数 schema，例如 create_payment_link 及其 amount、customer、product、price、quantity、memo 字段。
- 把自然语言请求原样交给 LLM，通过 prompt 或 BAML 这类工具约束其输出为预定义的结构化对象，而非自由文本。
- LLM 返回 nextStep 后，代码按 function/intent 字段用 switch 或 if/elif 分发，命中则执行真实 API（如 stripe.paymentlinks.create）。
- 真实 Agent 在翻译前先查询系统：调用 list_customers、list_products、list_prices 等把 ID 集齐，再填充 payload 参数。
- 也可以把需要的 ID 直接放进 prompt 或上下文窗口里（原文指出这与『先查询再构造』本质上是同一回事，见 factor 3）。
- 对未知 function 设置 else 兜底分支，避免模型输出未定义工具时程序崩溃或静默失败，至少记录并请求澄清。
- 把工具结果追加回上下文，让 Agent 可以基于结果继续决策，直到模型输出 done 类意图才结束循环。
- 将『翻译』与『执行』分离为两个独立阶段，便于单独为翻译逻辑做测试、评估与回滚，而不牵连执行链路，也能只替换模型输出解析层而保持工具执行代码不动。

## 案例 (cases)

- 原文示例：把『创建 750 美元付款链接』翻译为 create_payment_link 结构化对象，内含完整的 Stripe 参数。
- 真实 Agent 参考：github.com/dexhorthy/mailcrew（附演示视频），会先列出客户、商品、价格再构建 payload。
- Stripe API 的 create_payment_link 调用示例，参数含 cust_128934ddasf9 这类真实 customer ID。
- Python 代码片段 llm.determineNextStep 接收自然语言并返回 nextStep 结构化对象供分发。
- 演示返回值：『I've successfully created a payment link for $750 to Terri… https://buy.stripe.com/test_1234567890』。
- if nextStep.function=='create_payment_link' → stripe.paymentlinks.create(nextStep.parameters) 的确定性分发代码。
- mailcrew 项目被原文点名作为『真实会查 ID 的 Agent』，印证先查询后构造 payload 的工程实践。

## 反模式/易错点

- 把 ID 硬编码进参数而不做真实查询，模型给出的 customer/product/price ID 很可能不存在或与真实数据对不上号。
- 模型返回未知工具时没有 else 兜底，直接抛异常导致整个流程中断，用户得不到任何反馈，正确做法是落入 else 做降级或澄清。
- 只做『翻译』不做循环闭环，拿到工具结果后不继续推理，Agent 退化为一次性的单步函数调用，无法完成多步任务。
- 依赖模型以非结构化文本表达工具调用，再靠脆弱解析去还原参数，极易因格式漂移而解析失败，应改用受约束的结构化输出。
- 把大量系统状态硬塞进一次 prompt 让模型『记住』，而不是通过结构化查询或上下文按需提供，浪费 token 且易错。
- 忽略工具结果，不把执行结果喂回上下文，模型后续决策失去依据，整个循环名存实亡，必须把结果作为事件回写。

## 源码索引（实践参考）

- `08-source/agent-content/factor-01-natural-language-to-tool-calls.md` — 原文完整内容：自然语言到工具调用的原子翻译模式
- `08-source/agent-content/brief-history-of-software.md` — 软件史背景：Agent 循环三步论（LLM 定步骤→确定性执行→结果回上下文）
- `08-source/agent-content/factor-04-tools-are-structured-outputs.md` — 承上启下：工具本质就是结构化输出

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-nl2tool → ag-tools | 前置依赖 | 工具是自然语言调用的结构化输出 |
| ag-nl2tool → ag-control | 前置依赖 | 工具调用需要确定性控制流 |
| tool-create-agent → ag-nl2tool | 组合 | 脚手架内建自然语言→工具调用模板 |
