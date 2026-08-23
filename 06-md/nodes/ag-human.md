# 工具调用联系人类 (Contact humans with tools)

- ID: `ag-human`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 进阶 intermediate

> 把人类接入作为一类工具调用，主动寻求批准

## 核心主张 (what)

- LLM API 默认依赖一个高风险的『首个 token』选择：返回纯文本，还是返回结构化数据，赌注全押在这一枚 token 上。
- 第一个 token 就背负重担：weather in tokyo 场景下是 'the'，fetch_weather 场景是标记 JSON 开头的特殊 token（如 \|JSON>）。
- 更好的做法：让 LLM 永远输出 JSON，用 request_human_input、done_for_now 这类意图（而非 check_weather 类工具）声明想联系人类。
- 你可能不会因此获得性能提升，但应该保持实验自由——去尝试奇怪的方式以获得最好的结果，不被惯例和框架束缚。
- 把『请求人类输入』建模成工具调用：class RequestHumanInput 含 intent/question/context/options，options 设 urgency、format 与 choices。
- 命中 request_human_input 时：追加 human_input_requested 事件、save_state、notify_human，然后 break 等人回复。
- 回复经 webhook 回来：POST /webhook 里 load_state(thread_id)、push response_from_human，再跑 determine_next_step 继续。
- 配合 factor 3 的 XML 上下文，对话窗口形如 <slack_message> 后接 <request_human_input>、<human_response>、<deploy_backend> 事件。
- 这支持外循环（outer loop）：控制流与上下文初始化是 Agent→Human 而非 Human→Agent，例如由 cron 或事件启动。

## 为什么 (why)

- 清晰指令：为不同类型的人类接触定义工具，LLM 能给出更具体的请求，包括问题、上下文与选项格式，交互更精准。
- 内外循环：支持 chatGPT 式聊天界面之外的 Agent→Human 工作流，Agent 可以由 cron 或事件主动发起。
- 多人类接入：通过结构化事件轻松跟踪和协调不同人类的输入，谁批准谁拒绝一目了然，权责清晰、全程可追溯。
- 多 Agent：简单抽象可轻松扩展为 Agent→Agent 的请求/响应模式，扩展开销极低，复用同一套事件机制。
- 持久化：配合 factor 6（Launch/Pause/Resume），能构建持久、可靠、可内省的多人在线工作流。
- 首 token 抉择的赌注太大，把『是否联系人类』从 token 层的隐式选择提升为显式的结构化意图更稳妥。
- 外循环 Agent 是『agent 像数字同事』体验的基础，详见 theouterloop 博客与 factor 11。

## 如何实践 (how)

- 在 BAML 里定义人类工具类：ClarificationRequest（intent request_more_information + message）、DoneForNow 与 RequestApprovalFromManager（含 message）。
- 用 Options 对象给人类请求加交互规格：urgency、format（free_text/yes_no/multiple_choice）、choices，指导呈现方式。
- Agent 循环命中 request_human_input：push human_input_requested 事件、save_state、notify_human、break 等待人类回复。
- 提供 /webhook 端点接收人类回复：解析出 thread_id，load_state，push response_from_human 事件。
- 恢复循环：determine_next_step(thread_to_prompt(thread)) → handle_next_step → 决定继续还是再次等待。
- 用 awaitingHumanResponse() 判断 thread 是否卡在等人，避免对不需要人类参与的线程发出请求。
- 模板 a2h.ts 定义 A2H 协议：Message 带 apiVersion 'proto.a2h.dev/v1alpha1'、kind 'Message'、spec 内含 agentMessage/response_schema/channel_id 与 status。
- 用 Zod schema（如 ApprovalSchema {approved, comment}）定义人类响应结构，approval 与 human request 复用 Message 类型。

## 案例 (cases)

- RequestHumanInput 类：intent/question/context/options(urgency/format/choices) 的完整字段定义。
- webhook 处理代码：@app.post('/webhook') 里 load thread、push response_from_human、重新 determine_next_step。
- XML 上下文演进：<request_human_input>（question: 是否部署 v1.2.3 到生产，urgency high, format yes_no）后接 <human_response>（approved true）。
- 模板 BAML：ClarificationRequest、DoneForNow、RequestApprovalFromManager、ProcessRefund（含必须批准注解）组成 HumanTools 联合。
- 模板 src/a2h.ts：ApprovalSchema（approved/comment）、Message 协议、NewConversation（user_message/channel_id/agent_name）。
- workshop Chapter 5：CLI 里 askHuman 用 readline 收集回复；Chapter 11 改为 email 审批（divide 走 fetchHumanApproval）。
- 外循环参考：theouterloop.substack.com 关于 OpenAI realtime API 是朝外循环的一步；另有 deploybot 真实对话截图佐证。

## 反模式/易错点

- 依赖模型在首个 token 上做『文本 vs 结构化』的隐式赌博，而不是用结构化意图显式声明是否联系人类。
- 只支持 chatGPT 式聊天界面，Agent 永远由人类发起，无法被 cron/事件启动并主动找人。
- 把人类请求与普通工具混在同一 schema，无法区分『执行动作』与『联系人类』两类分支，控制流无从下手。
- 人类回复没有结构化事件记录（谁、何时、批准与否），审计与多人类协调无从谈起，必须落为结构化事件以可追溯。
- 同步阻塞等待人类回复（while...sleep 轮询），而不是 save 状态加 break 加 webhook 恢复。
- 请求人类时丢失 thread_id 引用，webhook 回来无法定位线程，恢复失败，须把 thread_id 塞进 spec.state 回程定位。

## 源码索引（实践参考）

- `08-source/agent-content/factor-07-contact-humans-with-tools.md` — 原文完整内容：人类交互建模为工具调用、webhook 收回复、5 条收益
- `08-source/agent-packages/create-12-factor-agent/template/src/a2h.ts` — 模板 A2H 协议：Message/ApprovalSchema/HumanRequest/NewConversation
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/agent.baml` — 模板 HumanTools：ClarificationRequest/RequestApprovalFromManager/ProcessRefund
- `08-source/agent-workshops/2025-05/walkthrough.md` — workshop Chapter 5 CLI 人机交互、Chapter 11 email 审批、Chapter 12 webhook

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-tools → ag-human | 前置依赖 | 联系人类是一类工具调用 |
| t-human → ag-human | 前置依赖 | 人机边界落到人类批准 |
| ag-tools → ag-human | 组合 | 工具 + 人类批准 |
| tool-create-agent → ag-human | 组合 | 模板含 a2h.ts 人类批准机制 |
