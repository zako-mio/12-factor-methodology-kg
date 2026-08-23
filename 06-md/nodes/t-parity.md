# 环境一致性 (Environment Parity)

- ID: `t-parity`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT10 · 环境一致性
- 阶段: 高级 advanced

> 开发与生产一致，传统靠环境等价，Agent 靠 prompt 版本化

## 核心主张 (what)

- App 保持开发、预发布、生产环境尽可能相似（dev-prod-parity.md）
- Agent 通过 prompt 版本化与上下文函数化保证可复现（factor-02/03）
- App 三大差距：时间差距、人员差距、工具差距（dev-prod-parity.md）
- Agent 的不一致表现为：本地能跑、上线失控（prompt/上下文漂移）
- 缩小差异是持续交付的前提（dev-prod-parity.md）
- Agent 确定性组件优先、LLM 作库而非框架（workshop/12fa 现代观）
- backing service 差异也是环境漂移源（dev-prod-parity.md/backing-services.md）
- 一致性从同构环境演进到同构行为：App 环境等价、Agent 可回放

## 为什么 (why)

- dev/prod 差异导致「开发能过、生产失败」的经典问题（dev-prod-parity.md）
- 持续部署需要把时间差距缩至小时级（dev-prod-parity.md）
- 工具栈差异（Nginx/SQLite/OS X vs Apache/MySQL/Linux）是隐性故障源（dev-prod-parity.md）
- Agent 侧 prompt 不一致则无法在测试环境复现生产行为（factor-02）
- LLM 是统计性组件，必须版本化其「输入面」才能保证可回放（factor-02/03）

## 如何实践 (how)

- App：把时间差距从周缩到小时：写码后数分钟部署（dev-prod-parity.md）
- App：人员差距缩小：写码者参与部署与观察生产（dev-prod-parity.md）
- App：工具差距缩小：开发与生产堆栈尽可能相似（dev-prod-parity.md）
- App：适配器层让 DB/队列/缓存在多种服务间切换不改代码（dev-prod-parity.md 表）
- Agent：prompt 全控制、可测试、可评测（factor-02）
- Agent：上下文格式自定义与函数化，保证输入可复现（factor-03）
- Agent：BAML 客户端与模型 provider 可切换、生成器版本锁定（clients.baml/generators.baml）
- Agent：确定性组件优先，LLM 决策点最小化（12fa 现代观）

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| 传统部署间隔周级→十二因子小时级（dev-prod-parity.md 表） | prompt 无黑盒抽象，完全掌握指令内容（factor-02） | App 靠环境等价（同构运行环境）；Agent 靠可复现性（版本化可回放） |
| 传统写码者与部署者不同人→十二因子同人（dev-prod-parity.md 表） | 为 prompt 建立测试与评测，类同代码质量门禁（factor-02） | App 关注运行环境一致；Agent 关注推理输入（prompt/上下文）一致 |
| 传统环境发散→十二因子尽可能相似（dev-prod-parity.md 表） | 上下文格式 token 高效且可复现（factor-03） | App 外置的是环境变量值一致；Agent 外置的是指令与上下文一致 |
| ActiveRecord 等适配器适配 MySQL/PostgreSQL/SQLite（dev-prod-parity.md 表） | LLM 作库而非框架：确定性代码控制行为（12fa 现代观/workshop） | 从同构环境演进到同构行为：App 复制环境、Agent 复制决策输入 |
| 容器/虚拟化贴近生产环境，进一步消除工具差异（dev-prod-parity.md 现代实践） | 渐进扩大 agent scope 保质量，避免一次性失控（factor-10） | 差异根源：App 的可变面是运行时配置、Agent 的可变面是模型输入 |
| 本地第三方服务不区分，config 句柄可随时切换（backing-services.md） | BAML 生成客户端版本锁定 0.88.0，杜绝环境间漂移（generators.baml） |  |
| 站点 i18n locales 与 $PORT 环境在本地/生产保持一致（web.rb/Procfile） | 官方现代化方向：可观测性 + Identity 治理生产 Agent（workshop 演进） |  |

## 源码索引（实践参考）

- `08-source/app-content-en/dev-prod-parity.md` — 
- `08-source/app-content-en/backing-services.md` — 
- `08-source/app-content-en/config.md` — 
- `08-source/app-deploy/web.rb` — 
- `08-source/app-deploy/Procfile` — 
- `08-source/agent-content/factor-02-own-your-prompts.md` — 
- `08-source/agent-content/factor-03-own-your-context-window.md` — 
- `08-source/agent-content/factor-10-small-focused-agents.md` — 
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/clients.baml` — 
- `08-source/agent-packages/create-12-factor-agent/template/baml_src/generators.baml` — 

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-dev-prod → t-parity | 前置依赖 | 从环境等价理解一致性 |
| t-parity → ag-prompts | 前置依赖 | 一致性落到 prompt 环境 |
