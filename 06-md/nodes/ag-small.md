# 小而专注的 Agent (Small, focused agents)

- ID: `ag-small`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 高级 advanced

> 用多个小 Agent 而非一个巨型 Agent 解决问题

## 核心主张 (what)

- 与其构建想包办一切的单体 Agent，不如构建小而专注、一件事做到位的 Agent——Agent 只是更大的、基本确定性系统中的构件。
- 关键洞见在于 LLM 的局限：任务越大越复杂，步骤越多，上下文就越长；随着上下文增长，LLM 更容易迷失或失去焦点。
- 把 Agent 保持在特定领域、3-10 步（最多 20 步）的规模，就能让上下文窗口可控、LLM 性能保持高位。
- 核心原则是『随着上下文增长，LLM 更容易迷失或失去焦点』，这是把 Agent 控制在小规模的根本理由。
- 收益：可控的上下文（小窗口=更好性能）、清晰的职责（每 Agent 范围明确）、更高的可靠性（复杂流程中不易迷路）、更易测试、更易调试。
- 关于『如果 LLM 变聪明了呢』：即使模型能处理 100+ 步工作流，答案依然是『要』——该做法让你今天就能交付成果，同时为将来逐步扩展范围做准备。
- 这就像重构大型确定性代码库：有意识地拆分与逐步扩展是保持质量的关键，重构经验可平移复用。，属于该因子的基础原则，应在设计中显式落实。
- 原文引用 NotebookLM 团队的话：『最神奇的 AI 构建时刻，总是发生在我极度贴近模型能力边界的时候』。
- 不管边界在哪里，只要你能稳定地找到它并做对，就能构建出魔法般的体验；可以建立很多护城河，但它们都需要工程严谨性。
- brief-history 补充：长上下文问题让多数构建者把『工具调用循环』推到一边——超过 10-20 轮就成一团乱，90% 正确率也远不够交付给客户。

## 为什么 (why)

- 上下文可控：小上下文窗口意味着更好的 LLM 性能与更低的失败率，输出质量有保障，成本也更低。，属于该因子的基础原则，应在设计中显式落实。
- 职责清晰：每个 Agent 有明确定义的范围与目的，系统整体易推理、易演进，边界一目了然。，属于该因子的基础原则，应在设计中显式落实。
- 更可靠：在复杂工作流中不易迷失，错误不易在长链条里传播放大，单点失败影响面小。，属于该因子的基础原则，应在设计中显式落实。
- 更易测试/调试：单 Agent 功能边界小，测试用例与问题定位都简单直接，验证成本大幅降低。，属于该因子的基础原则，应在设计中显式落实。
- 防止错误空转：短上下文里错误不累积，是 factor 9 防 spin-out 的头号手段，自愈更有效。
- 即便模型更强，小 Agent 方式保证今天可交付，同时为未来扩范围留好结构，与重构大代码库同理。，属于该因子的基础原则，应在设计中显式落实。

## 如何实践 (how)

- 把任务按领域拆成多个小 Agent，每个只管一件事，由确定性 DAG 编排（micro-agent DAG 模式）。
- 限制每 Agent 的步骤规模在 3-10 步，硬上限 20 步，超出就继续拆分，规模纪律明确。，属于该因子的基础原则，应在设计中显式落实。
- 隔离任务与上下文：让 LLM 只关注一个小的 5-10 步工作流（如 deploybot 的做法）。
- 用确定性代码处理结构化流程，只在『解析人类反馈、提出更新行动方案』等关键点引入 LLM，物尽其用。，属于该因子的基础原则，应在设计中显式落实。
- 配合 factor 7 把人类反馈翻译成工作流步骤，避免在长上下文里错误循环，反馈落地更稳。，属于该因子的基础原则，应在设计中显式落实。
- 保持循环三件套（prompt/switch/context 累积）在每个小 Agent 内小而齐整，职责单一。
- 随着模型上下文可靠性提升，再逐步扩大 Agent 范围（agent-scope-grow 动画），而非一步到位。
- reducer 视角收束：每个小 Agent 就是一个 reducer，输入历史事件输出下一步，职责单一便于推理。

## 案例 (cases)

- 原文 5 条收益清单：Manageable Context / Clear Responsibilities / Better Reliability / Easier Testing / Improved Debugging。
- NotebookLM 团队名言：紧贴模型能力边界的时刻最神奇（引用 swyx 的 substack 文章）。
- deploybot 实例（got-agents/agents repo）：确定性代码部署 staging、跑 e2e、把『deploy SHA 4af9ec0 to production』交给 Agent。
- deploybot 收束：『We isolate tasks and contexts as much as possible to keep the LLM focused on a small, 5-10 step workflow』。
- agent-scope-grow GIF（1a5-agent-scope-grow.gif）演示 Agent 范围随能力提升渐进扩展。
- brief-history 的 micro-agent DAG 图与『10-20 轮后一团乱』的行业观察。
- chainlit 的 support/chatbot 演示（更多经典案例），作为社区佐证小 Agent 模式的有效性。
- 『Even as models support longer context windows, you'll ALWAYS get better results with a small, focused prompt and context』的论断。

## 反模式/易错点

- 构建什么都能做的单体 Agent，上下文随任务膨胀到失控，迷失与失败成为常态，务必拆分。，属于该因子的基础原则，应在设计中显式落实。
- 在上下文不可靠时激进扩大 Agent 范围，质量崩坏而不可逆，扩大必须基于验证过的可靠性。，属于该因子的基础原则，应在设计中显式落实。
- 让单个 Agent 跑 100+ 步的长链条，迷失与错误累积成为常态，超长任务应切分为 DAG。，属于该因子的基础原则，应在设计中显式落实。
- 不在确定性 DAG 中编排小 Agent，而是让一个 Agent 全流程自行其事，失控风险高，编排是骨架。
- 忽略『贴近模型能力边界』的质量纪律，为了炫技而超规模设计，能力与边界失衡必然失败。，属于该因子的基础原则，应在设计中显式落实。
- 把小 Agent 的上下文与任务混在一起共享，违背隔离原则，隔离才能保住各 Agent 的聚焦。，属于该因子的基础原则，应在设计中显式落实。

## 源码索引（实践参考）

- `08-source/agent-content/factor-10-small-focused-agents.md` — 原文完整内容：小而专注的 Agent、收益、LLM 变聪明了怎么办
- `08-source/agent-content/brief-history-of-software.md` — 背景：长上下文问题、micro-agent DAG、deploybot 实例
- `08-source/agent-content/factor-09-compact-errors.md` — 关联：防错误空转的头号手段是小而专注的 Agent

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-reducer → ag-small | 前置依赖 | 无状态 reducer 使小 Agent 可行 |
| ag-small → ag-trigger | 前置依赖 | 小 Agent 便于随处触发 |
| t-scaling → ag-small | 前置依赖 | 规模化落到小 Agent 组合 |
