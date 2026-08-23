# 12 Factor 方法论合并知识图谱 · AI 友好索引

版本 1.0.0 | 38 节点 | 61 边 | 16 组

## 节点总表

| ID | 名称 | 类型 | 来源 | 阶段 | 分组 | 定义 |
|---|---|---|---|---|---|---|
| app-codebase | 代码库 | 方法原则 | App 体系 | 基础 basic | GA | 一个代码库，多环境部署，版本控制跟踪一切 |
| app-deps | 依赖 | 方法原则 | App 体系 | 基础 basic | GA | 显式声明并隔离依赖，绝不依赖系统级隐式包 |
| app-config | 配置 | 方法原则 | App 体系 | 基础 basic | GA | 配置存于环境变量，与代码严格分离 |
| app-backing | 后端服务 | 方法原则 | App 体系 | 基础 basic | GA | 后端服务作为附加资源，可随时替换连接 |
| app-build-run | 构建·发布·运行 | 方法原则 | App 体系 | 进阶 intermediate | GA | 严格分离构建、发布、运行三阶段 |
| app-processes | 进程 | 方法原则 | App 体系 | 基础 basic | GA | 以一个或多个无状态进程执行应用 |
| app-port | 端口绑定 | 方法原则 | App 体系 | 基础 basic | GA | 通过端口绑定自含导出服务，不依赖注入的 Web 服务器 |
| app-concurrency | 并发 | 方法原则 | App 体系 | 进阶 intermediate | GA | 通过进程模型横向扩展 |
| app-disposability | 可处置性 | 方法原则 | App 体系 | 进阶 intermediate | GA | 快速启动与优雅终止，最大化鲁棒性 |
| app-dev-prod | 开发/线上等价 | 方法原则 | App 体系 | 进阶 intermediate | GA | 保持开发、预发布、生产环境尽可能相似 |
| app-logs | 日志 | 方法原则 | App 体系 | 进阶 intermediate | GA | 将日志视为事件流，不关心存储格式 |
| app-admin | 管理进程 | 方法原则 | App 体系 | 进阶 intermediate | GA | 管理/维护任务作为一次性进程运行 |
| ag-nl2tool | 自然语言→工具调用 | 方法原则 | Agent 体系 | 基础 basic | GB | LLM 将自然语言转换为结构化工具调用对象 |
| ag-prompts | 掌控你的 Prompt | 方法原则 | Agent 体系 | 基础 basic | GB | 像管理代码一样版本化、测试、部署 prompt |
| ag-context | 掌控上下文窗口 | 方法原则 | Agent 体系 | 进阶 intermediate | GB | 对上下文进行工程化管理（上下文工程） |
| ag-tools | 工具即结构化输出 | 方法原则 | Agent 体系 | 基础 basic | GB | 工具只是模型的结构化输出，可无限组合 |
| ag-state | 统一执行/业务状态 | 方法原则 | Agent 体系 | 进阶 intermediate | GB | 将执行状态与业务状态统一为单一事实源 |
| ag-pause | 启动/暂停/恢复 | 方法原则 | Agent 体系 | 进阶 intermediate | GB | 用简单 API 管理 Agent 生命周期 |
| ag-human | 工具调用联系人类 | 方法原则 | Agent 体系 | 进阶 intermediate | GB | 把人类接入作为一类工具调用，主动寻求批准 |
| ag-control | 掌控控制流 | 方法原则 | Agent 体系 | 进阶 intermediate | GB | 控制流由代码决定，LLM 只做决策点 |
| ag-errors | 压缩错误进上下文 | 方法原则 | Agent 体系 | 进阶 intermediate | GB | 把错误摘要压缩回上下文窗口供模型反思 |
| ag-small | 小而专注的 Agent | 方法原则 | Agent 体系 | 高级 advanced | GB | 用多个小 Agent 而非一个巨型 Agent 解决问题 |
| ag-trigger | 随处触发 | 方法原则 | Agent 体系 | 高级 advanced | GB | 从任何触发源唤起 Agent，触达用户所在之处 |
| ag-reducer | 无状态 Reducer | 方法原则 | Agent 体系 | 高级 advanced | GB | 将 Agent 建模为无状态 reducer（state, event）→ state |
| t-stateless | 无状态性 | 桥接主题 | 桥接 | 高级 advanced | GT01 | 无状态是传统应用与 Agent 共有的可靠运行基石 |
| t-disposable | 生命周期与可处置性 | 桥接主题 | 桥接 | 高级 advanced | GT02 | 进程可快速启停，Agent 可暂停恢复，本质同源 |
| t-config | 配置与可变性外置 | 桥接主题 | 桥接 | 高级 advanced | GT03 | 可变部分（环境变量 / prompt）外置于代码之外 |
| t-observability | 可观测性与错误可见性 | 桥接主题 | 桥接 | 高级 advanced | GT04 | 运行可见性是传统日志与 Agent 错误压缩的共同目标 |
| t-deps | 依赖与工具显式化 | 桥接主题 | 桥接 | 高级 advanced | GT05 | 显式声明依赖 / 工具，不隐式依赖环境 |
| t-control | 控制流与阶段治理 | 桥接主题 | 桥接 | 高级 advanced | GT06 | 确定性控制流 / 阶段分离保证可预测交付 |
| t-entry | 自含入口与触达 | 桥接主题 | 桥接 | 高级 advanced | GT07 | 自含导出服务 / 随处触发，皆是不依赖宿主 |
| t-scaling | 规模化与单元粒度 | 桥接主题 | 桥接 | 高级 advanced | GT08 | 进程模型扩展 / 小 Agent 组合，皆是单元化扩展 |
| t-human | 人为交互边界 | 桥接主题 | 桥接 | 高级 advanced | GT09 | 一次性管理任务 / 人类批准，皆是人机协作边界 |
| t-parity | 环境一致性 | 桥接主题 | 桥接 | 高级 advanced | GT10 | 开发与生产一致，传统靠环境等价，Agent 靠 prompt 版本化 |
| tool-create-agent | create-12-factor-agent 脚手架 | 工具 | 工具 | 进阶 intermediate | G-TOOLS | 官方 CLI 脚手架，一键生成符合 12 要素的 Agent 项目骨架 |
| tool-walkthroughgen | Walkthroughgen 教程生成器 | 工具 | 工具 | 进阶 intermediate | G-TOOLS | 从 YAML 配置生成分步教程/文档与工作目录，跟踪增量 diff |
| tool-workshops | 官方工作坊材料 | 工具 | 工具 | 高级 advanced | G-TOOLS | 2025 年两次官方工作坊（TS/Python 双版本）的演练材料与样例 |
| tool-app-site | 12factor.net 站点源码 | 工具 | 工具 | 基础 basic | G-TOOLS | 官方文档站自身即 Jekyll 应用，是 App 原则的参考实现 |
