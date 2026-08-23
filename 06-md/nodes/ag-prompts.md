# 掌控你的 Prompt (Own your prompts)

- ID: `ag-prompts`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 基础 basic

> 像管理代码一样版本化、测试、部署 prompt

## 核心主张 (what)

- 不要把 prompt 工程外包给框架，这是本因子最核心的一句话：prompt 必须由你亲自掌控，而不是交给黑盒。
- 框架常提供『黑盒』式抽象，如 agent = Agent(role=…, goal=…, personality=…, tools=[…]) 加 task = Task(instructions=…) 后 agent.run(task)。
- 黑盒方式适合快速起步，能借用顶级 prompt 工程经验，但往往难以调优，也无法逆向工程出『到底把哪些 token 送进了模型』。
- 替代方案：把 prompt 当作一等公民代码对待，用带类型签名的函数表达，例如 Rust 风格函数声明返回 DoneForNow \| ListGitTags 等联合类型。
- 原文用 BAML 生成 prompt：在模板里用 {{ _.role("system") }} / {{ _.role("user") }} 组织角色与内容，通过类型签名约束输出。
- 签名看起来『有点怪』的部分会在 factor 4（工具即结构化输出）得到解释——函数返回的联合类型就是工具集合。
- prompt 是应用逻辑与 LLM 之间的主接口，谁掌控 prompt，谁就掌控了 Agent 行为的最终决定权与可调性。
- 原文引用 Hamel 的博客，强调『这是远非新颖的建议』，即掌控 prompt 早已是被反复验证的工程常识。
- prompt 内容直接决定模型能调用哪些工具、按什么顺序思考、何时请求人类介入，是所有后续因子落实的落点。

## 为什么 (why)

- 全权掌控：你可以写出 Agent 精确需要的指令，没有黑盒抽象遮挡任何一层，改动即可生效无需等框架。
- 可测试与评估：为 prompt 建测试和 evals，就像为普通代码建测试一样，每次改动都能被回归验证。
- 可迭代：基于真实线上表现快速修改 prompt 内容，而不必等待框架发版或逆向黑盒定位问题，试错成本极低。
- 透明性：永远清楚 Agent 正在依据哪些指令工作，便于审计、排查与向利益相关方解释行为，合规与排障都有据可依。
- 角色利用：可以利用支持 user/assistant 角色非标准用法的 API，例如现已废弃的 OpenAI『completions』非 chat 口味，乃至所谓 gaslighting 技巧。
- 你不知道什么 prompt 最好，但你想要能尝试一切的灵活性——只有真正拥有 prompt 才能做到这一点。
- 原文 BAML 示例把部署 Agent 的系统提示写成完整段落：职责、先查环境（staging vs production）、再验 tag、再查系统状态。

## 如何实践 (how)

- 放弃框架的 Agent/Task 黑盒，直接用 BAML 或任意模板工具手写 prompt，甚至用纯字符串模板拼接也完全可以。
- 为 prompt 声明强类型函数签名：输入是 thread 字符串，输出是语义明确的意图联合类型（DoneForNow/ListGitTags/DeployBackend…）。
- 在 system 段写清楚角色与行为准则：例如『You are a helpful assistant that manages deployments…』并列出安全部署最佳实践。
- 在 user 段注入动态内容 {{ thread }}，末尾固定询问『What should the next step be?』引导模型输出下一步意图。
- 在 prompt 中显式列出可用工具（deploy_backend、deploy_frontend、check_deployment_status），并说明敏感操作要 request_approval。
- 引导模型先想后做：先查部署状态、验证 tag 存在、需要时请求批准、先上 staging 再上生产、最后监控部署进度。
- 像写代码一样为 prompt 建立版本管理与测试套件，把每次迭代纳入回归，保证既有行为不被无意破坏。
- 利用非标准角色 API 的能力做试验（如角色反转/gaslighting 技术），保持实验自由，寻找更好的行为空间。
- 用 BAML 的测试语法（test 块 + @@assert）固化关键行为，例如断言意图、断言参数，防止后续改动破坏已通过路径。

## 案例 (cases)

- 黑盒反例：Agent(role, goal, personality, tools) + Task(instructions, expected_output) + agent.run(task) 三段式框架用法。
- BAML 正向示例：DetermineNextStep 函数用类型签名加 prompt #" … "# 模板组织 system/user 角色与内容。
- 具体系统提示文本：管理 frontend/backend 部署的助理、按最佳实践安全部署、部署前检查环境/标签/系统状态。
- 工具列举示例：deploy_backend、deploy_frontend、check_deployment_status，敏感部署要求 request_approval 获得人工验证。
- 思考顺序清单：先查部署状态 → 验证 tag 存在 → 需要时请求批准 → 先上 staging 再上生产 → 监控部署进度。
- 类型签名联合类型：DoneForNow \| ListGitTags \| DeployBackend \| DeployFrontend \| RequestMoreInformation 五选一。
- 外部佐证：hamel.dev/blog/posts/prompt 关于掌控 prompt 的论述，原文以配图形式引用。
- 原文观点：『I don't know what's the best prompt, but I know you want the flexibility to be able to try EVERYTHING.』
- 原文提及的非标准 API 例子：现已废弃的 OpenAI non-chat completions API，以及 model gaslighting 技术。

## 反模式/易错点

- 完全依赖黑盒 Agent/Task 抽象，出了问题无法定位是框架哪一层把 prompt 改坏或篡改了指令。
- 把 prompt 工程彻底外包给框架，丧失对『送入模型的精确 token』的控制，调优无从下手，行为也不可审计。
- 对 prompt 不建测试不建 evals，任何改动的风险都不可评估，线上出问题只能靠肉眼试错，回归无从谈起。
- 在 prompt 中重复堆砌长指令而没有结构化组织，浪费 token 且降低模型的遵循度，应精简并按角色分层。
- 不区分 system 与 user 角色内容，把动态 thread 与固定指令混在一起，破坏可复用性与可维护性。
- 直接复用框架默认 prompt 而从不审视其中是否含有与业务不符、甚至有害的指令，必须逐句核对后再上线。
- 忽略角色 API 的能力差异，白白放弃非标准角色用法能带来的行为红利与实验空间，应把角色能力纳入选型。

## 源码索引（实践参考）

- `08-source/agent-content/factor-02-own-your-prompts.md` — 原文完整内容：掌控 prompt、BAML 示例、五项收益
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/agent.baml` — 模板真实 BAML：DetermineNextStep 函数、ClarificationRequest/DoneForNow 等类与测试块
- `08-source/agent-workshops/2025-05/walkthrough.md` — workshop Chapter 6 定制 prompt 加入推理步骤；Chapter 4 为 prompt 添加 @@assert 测试

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-prompts → ag-context | 前置依赖 | 拥有 prompt 才能掌控上下文 |
| t-config → ag-prompts | 前置依赖 | 可变性外置落到 prompt 管理 |
| t-parity → ag-prompts | 前置依赖 | 一致性落到 prompt 环境 |
| app-config → ag-prompts | 变体 | 环境配置 ↔ prompt 管理 |
| app-codebase → ag-prompts | 依赖关联 | prompt 应像代码库一样管理 |
| tool-workshops → ag-prompts | 组合 | 工作坊演练 prompt 管理与工具编排 |
