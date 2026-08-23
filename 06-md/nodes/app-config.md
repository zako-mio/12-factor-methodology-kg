# 配置 (Config)

- ID: `app-config`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 基础 basic

> 配置存于环境变量，与代码严格分离

## 核心主张 (what)

- 应用的 config 是随 deploy 变化的一切（staging、生产、开发者环境等），包括数据库、Memcached 等 backing service 的资源句柄。
- config 还包括外部服务凭据，如 Amazon S3 或 Twitter 的凭据，以及按 deploy 特有的值，如该 deploy 的规范主机名。
- 把 config 作为代码常量存储是十二要素违规，要求 config 与代码严格分离：config 跨 deploy 差异大而代码不差异。
- 试金石：无论何时都可把 codebase 开源而不泄露任何凭据，即说明 config 已正确从代码中抽出。
- config 定义不包括内部应用配置，如 Rails 的 config/routes.rb 或 Spring 的模块连接方式；此类不随 deploy 变化，宜留在代码中。
- 不用版本控制跟踪的配置文件（如 Rails 的 config/database.yml）比代码常量进步，但仍固有弱点：易误检入 repo、散落各处格式各异难以统观。
- 配置文件格式往往语言或框架相关（如 Java System Properties），缺乏跨环境通用性，迁移成本高。
- 十二要素应用把 config 存于环境变量（env vars）：跨 deploy 易改且无需改代码、几乎不会误检入 repo、语言与 OS 无关。
- env vars 是细粒度控件，彼此完全正交，绝不按环境名分组，而是每个 deploy 独立管理自身配置。

## 为什么 (why)

- config 随部署变化而代码不变，混在一起会使不同部署无法复用同一份代码，部署即需改代码，这使配置变更与代码演进彻底解耦，部署灵活。
- 代码内常量使凭据入库，泄露风险高且部署迁移困难，安全性无法保证，从根本上避免凭据等敏感信息随代码泄露。
- 配置文件易误提交、散落各处且格式语言相关，难以统一管理，越管越乱，保证同一份代码能在任意 deploy 上运行而不需改动。
- 按环境名分组（development/test/production）无法随规模扩展：deploy 变多需新环境名，开发者私名环境（joes-staging）导致配置组合爆炸与管理脆弱。
- env vars 是语言与 OS 无关的标准，优于 Java System Properties 等专有机制，跨栈通用。

## 如何实践 (how)

- 把全部 config（资源句柄、凭据、per-deploy 值）放入环境变量，严格与代码分离，这使配置变更与代码演进彻底解耦，部署灵活。
- 每个 deploy 独立管理自身 env vars，不按环境名分组，保持配置正交，从根本上避免凭据等敏感信息随代码泄露。
- 用开源试金石检验：能否随时开源 codebase 而不泄露任何凭据，作为验收标准，保证同一份代码能在任意 deploy 上运行而不需改动。
- 内部应用配置（路由、模块连接）保留在代码中，不误入 env，区分两类配置，配置管理因此可随应用规模自然扩展。
- config 变更作为独立于代码变更的部署维度单独管理，可独立调整与回滚，是十二要素可移植性与安全性的核心保障。

## 案例 (cases)

- env vars 优于 Java System Properties：语言/OS 无关的通用标准，跨栈一致。
- config/database.yml 不入库是相对常量的改进，但仍可能误提交、散落，是过渡方案，这使配置变更与代码演进彻底解耦，部署灵活。
- Rails 的 config/routes.rb 属内部配置，不随 deploy 变化，留在代码中是正确做法。
- development/test/production 环境分组在出现 staging、qa、joes-staging 等新名时暴露扩展性问题。

## 反模式/易错点

- 把 config 存为代码常量（硬编码凭据）——凭据随代码入库，泄露风险极高，这使配置变更与代码演进彻底解耦，部署灵活。
- 用不入库的 config 文件管理配置——易误提交、散落、格式语言相关，难统一管理，从根本上避免凭据等敏感信息随代码泄露。
- 按环境名分组管理配置——组合爆炸、管理脆弱，无法随 deploy 数量扩展，保证同一份代码能在任意 deploy 上运行而不需改动。
- 把内部应用配置与随 deploy 变化的 config 混为一谈，边界混乱难以维护，配置管理因此可随应用规模自然扩展。

## 源码索引（实践参考）

- `08-source/app-content-en/config.md` — III. Config 原文：config 定义/开源试金石/配置文件弱点/env vars 正交性与分组反模式
- `08-source/app-content-en/backing-services.md` — 资源句柄作为 config 组成部分的交叉引用
- `08-source/app-deploy/web.rb` — 实例：ENV['FORCE_SSL']/ENV['PASSWORD'] 直接读取环境变量控制行为

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-backing → app-config | 前置依赖 | 后端服务句柄存于配置 |
| app-config → app-dev-prod | 前置依赖 | 配置差异是环境漂移主因 |
| app-config → t-config | 前置依赖 | 从环境配置理解可变性外置 |
| app-config → ag-prompts | 变体 | 环境配置 ↔ prompt 管理 |
