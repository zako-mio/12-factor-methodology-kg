# 依赖与工具显式化 (Dependency & Tool Explicitness)

- ID: `t-deps`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT05 · 依赖与工具显式化
- 阶段: 高级 advanced

> 显式声明依赖 / 工具，不隐式依赖环境

## 核心主张 (what)

- App 显式声明并隔离全部依赖，绝不依赖系统级隐式包存在（dependencies.md）
- Agent 把工具建模为 LLM 的结构化输出，触发确定性代码执行（factor-04）
- App 声明清单 + 隔离工具必须同时使用，仅其一不满足十二因子（dependencies.md）
- Agent 的工具即 intent schema：LLM 输出 JSON 描述确定性代码该做什么（factor-04）
- 隐式依赖无法保证存在与版本兼容，这是两侧共同的显式化动机（dependencies.md）
- 工具决策（LLM）与工具执行（代码）分离，使工具可组合可测试（factor-04）
- App shell out 系统工具需 vendored 而非假设存在（dependencies.md）
- Agent 的 BAML 工具类（Add/Subtract/Multiply/Divide）即声明式的工具清单（tool_calculator.baml）

## 为什么 (why)

- 系统级 site packages 等隐式依赖的存在与版本无法保证（dependencies.md）
- ImageMagick/curl 等系统工具未来系统可能不存在或不兼容（dependencies.md）
- 显式声明简化新开发者搭建：仅需语言运行时+依赖管理器即可确定性 build（dependencies.md）
- Agent 侧把工具当结构化输出解锁无限组合与可测试性（factor-04）
- 决策与执行分离让 LLM 决定做什么、代码控制怎么做，避免工具被误执行（factor-04）

## 如何实践 (how)

- App：Bundler 用 Gemfile manifest 声明 + bundle exec 隔离（dependencies.md）
- App：Python 用 Pip 声明 + Virtualenv 隔离，两步分开（dependencies.md）
- App：C 用 Autoconf 声明 + 静态链接隔离（dependencies.md）
- Agent：tool_calculator.baml 定义四则工具类，带 intent 常量与参数类型（tool_calculator.baml）
- Agent：agent.baml 用 union 类型 CalculatorTools 聚合工具，作为 DetermineNextStep 返回类型（agent.baml）
- Agent：handleNextStep 用 switch(intent) 分派到确定性执行，结果 push 回 thread（agent.ts）
- Agent：生成客户端 baml_client 由 BAML 编译器产出，与 baml_src 声明同步（agent.ts import + generators.baml）
- Agent：未知 intent 分支有兜底 else，不默认放行（factor-01/04 代码）

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| Gemfile manifest 完整精确声明依赖，bundle exec 保证隐式不泄漏（dependencies.md） | 工具是带 schema 的 intent 类，LLM 输出即工具调用对象（tool_calculator.baml） | App 显式化对象是库与包（代码依赖）；Agent 显式化对象是行为能力与副作用（工具调用） |
| Pip（声明）+ Virtualenv（隔离）双工具模式（dependencies.md） | divide 等高风险工具被 agentLoop 返回 thread 而非直接执行，强制审批（agent.ts） | App 用 manifest+bundler 隔离运行时；Agent 用 schema+生成客户端契约化决策面 |
| 确定性 build command：bundle install / lein deps（dependencies.md） | 工具类以 union 组合进单一返回类型，天然可扩展（agent.baml） | Agent 的工具声明还隐含授权边界：工具即权限，需额外关注安全 |
| 不 shell out ImageMagick/curl，需要则 vendored 进 app（dependencies.md） | switch(intent) 是确定性执行面，工具行为不随 LLM 波动（agent.ts handleNextStep） | App 依赖在构建期解析；Agent 工具在运行循环中按 intent 实时分派 |
| 开发与生产统一应用同一份显式依赖规范（dependencies.md） | 工具结果作为事件回填上下文，支撑下一轮决策（factor-04 pattern + agent.ts） | 差异根源：App 依赖静态引入、Agent 工具动态选择，后者需结合控制流治理 |
| 依赖声明让新开发者一条命令跑通（dependencies.md） | BAML 生成客户端版本由 generators.baml 锁定，避免声明与实现漂移（generators.baml） |  |
| 系统级包只在运行时隐式可用即违规（dependencies.md） | 工具即行为能力的声明：新增能力=新增 intent 类+执行分支（agent.baml + agent.ts） |  |

## 源码索引（实践参考）

- `08-source/app-content-en/dependencies.md` — 
- `08-source/agent-content/factor-04-tools-are-structured-outputs.md` — 
- `08-source/agent-content/factor-01-natural-language-to-tool-calls.md` — 
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/tool_calculator.baml` — 
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/agent.baml` — 
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/generators.baml` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/agent.ts` — 

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-deps → t-deps | 前置依赖 | 从依赖声明理解显式化 |
| t-deps → ag-tools | 前置依赖 | 显式化落到工具定义 |
