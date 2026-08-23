# 配置与可变性外置 (Config Externalization)

- ID: `t-config`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT03 · 配置与可变性外置
- 阶段: 高级 advanced

> 可变部分（环境变量 / prompt）外置于代码之外

## 核心主张 (what)

- App 的 config 是随 deploy 变化的一切：数据库/缓存句柄、外部服务凭据、每部署特有值（config.md）
- App 要求 config 与代码严格分离，代码常量式 config 明确违规（config.md）
- Agent 不把 prompt 工程外包给框架，prompt 应作为一等代码受控（factor-02）
- Agent 的 prompt 是应用逻辑与 LLM 之间的主接口，是 Agent 的配置面（factor-02）
- 可变部分外置是版本化、回滚、审计的前提：App 外置运行时值，Agent 外置指令策略
- App 试金石：代码库能否随时开源而不泄露任何凭据（config.md）
- Agent 侧同样要求：prompt 可版本化、可回滚、可测试（factor-02）
- config 随部署变化而代码不变；prompt 随策略演进而逻辑不变
- 内层可变点也需显式化：App 的 routes/模块连接留代码，Agent 的推理步骤留 prompt

## 为什么 (why)

- 代码内常量 config 违反十二因子：config 跨部署差异大而代码不（config.md）
- config 文件（如 config/database.yml）比常量好但仍易误提交、散落各处、格式语言相关（config.md）
- 按环境名分组导致组合爆炸，部署越增多越脆弱（config.md）
- 框架黑盒 prompt 难以调优或逆向工程出精确 token 序列（factor-02）
- 外包 prompt 意味着丢失对指令、测试、迭代、透明度的控制（factor-02 五收益的反面）

## 如何实践 (how)

- App：config 全入环境变量，语言与 OS 无关的标准机制（config.md）
- App：env vars 是正交的粒度控件，每个 deploy 独立管理而非按环境分组（config.md）
- App：内部应用配置（routes/bean wiring）留代码，不混入 env（config.md）
- Agent：用 BAML 定义 DetermineNextStep 函数与 prompt 模板，prompt 即函数签名的一部分（factor-02/agent.baml）
- Agent：baml_src/clients.baml 改 provider 行切换模型，接口保持稳定（clients.baml）
- Agent：上下文构建函数化（thread_to_prompt），格式自定义可控（factor-03）
- Agent：BAML 生成器版本锁定（0.88.0），prompt 变更后 baml-cli generate 重新生成客户端（generators.baml）
- 两侧共法：把一切随环境/策略变化的内容移出核心逻辑，保留在可版本化的外置位置

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| config 包含 DB/Memcached 句柄、S3/Twitter 凭据、每部署 canonical hostname（config.md） | prompt 是 Agent 与应用逻辑的主接口，全控制才能精确送入模型（factor-02） | App 外置的是运行时值（句柄/凭据/每部署数据）；Agent 外置的是指令与策略（prompt） |
| 试金石：开源不泄凭据即视为 config 外置彻底（config.md） | 为 prompt 建测试与评测，像对待任何代码一样（factor-02） | App 外置物是纯数据，由环境注入；Agent 外置物本身是代码，可测试可回滚 |
| 拒绝 config/database.yml 式未入版本库配置：易误提交、散落、格式不一（config.md） | 基于真实表现快速迭代 prompt，无需改应用逻辑（factor-02） | 差异根源：App 配置决定连接哪，Agent 配置决定怎么做 |
| 拒绝 Java System Properties 等语言特定配置机制（config.md） | 透明性：确切知道 Agent 在执行什么指令（factor-02） | App 靠 ENV 正交管理；Agent 靠 prompt 版本化管理 |
| 拒绝 development/test/production 命名分组，避免 joes-staging 式爆炸（config.md） | 可对非标准角色用法的 API 做 role hacking（factor-02） | Agent 的配置面更接近「行为契约」而非「参数表」，因此需要代码级治理 |
| Rails config/routes.rb 等内部配置正确留在代码内（config.md） | BAML prompt 模板与生成客户端同步版本，避免漂移（generators.baml） |  |
| 官方站点 PASSWORD/FORCE_SSL 均从 ENV 读取注入（web.rb） | 上下文格式自定义（XML 打包进单 user 消息）实现 token 高效（factor-03） |  |

## 源码索引（实践参考）

- `08-source/app-content-en/config.md` — 
- `08-source/app-content-en/backing-services.md` — 
- `08-source/app-deploy/web.rb` — 
- `08-source/agent-content/factor-02-own-your-prompts.md` — 
- `08-source/agent-content/factor-03-own-your-context-window.md` — 
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/agent.baml` — 
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/clients.baml` — 
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/generators.baml` — 

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-config → t-config | 前置依赖 | 从环境配置理解可变性外置 |
| t-config → ag-prompts | 前置依赖 | 可变性外置落到 prompt 管理 |
