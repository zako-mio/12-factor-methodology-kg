# 开发/线上等价 (Dev/prod parity)

- ID: `app-dev-prod`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 进阶 intermediate

> 保持开发、预发布、生产环境尽可能相似

## 核心主张 (what)

- 历史上开发（开发者对本地 deploy 实时编辑）与生产（最终用户访问的运行 deploy）之间存在三大差距：时间、人员、工具。
- 时间差距：开发者编写的代码要数天、数周甚至数月才进入生产，反馈周期长，这大幅降低了环境差异引发的线上故障概率。
- 人员差距：开发者写代码、运维工程师负责部署，责任割裂，是持续部署得以长期坚持的基础条件，开发与生产的栈一致让问题更早暴露、更快修复。
- 工具差距：开发者可能使用 Nginx、SQLite、OS X 的栈，而生产使用 Apache、MySQL、Linux，栈不一致。
- 十二要素应用通过保持开发与生产差距小来设计支持持续部署，追求敏捷发布，减少因环境特化导致的隐性不兼容。
- 缩小时间差距：开发者写完代码几小时甚至几分钟后即可部署上线，反馈即时，让测试结论对生产行为更有参考价值。
- 缩小人员差距：编写代码的开发者密切参与部署并观察其生产行为，责任闭环，从源头消除大多数生产环境才出现的问题。
- 缩小工具差距：开发与生产环境尽可能相似，栈一致降低差异风险，责任闭环使部署与观察都由同一批人完成，为高频发布提供了充分的环境一致性保障。
- backing service 是 dev/prod parity 的重要领域；许多语言提供简化访问的库与适配器，如 ActiveRecord 适配 MySQL/PostgreSQL/SQLite。
- Celery（Python/Django 队列库）适配 RabbitMQ/Beanstalkd/Redis；ActiveSupport::Cache 适配 Memory/文件系统/Memcached。
- 传统应用部署间隔数周、代码作者与部署者不同、开发与生产环境分歧；十二要素为小时级部署、同一批人、环境尽可能相似。
- 开发者有时偏爱本地用轻量 backing service、生产用更严肃健壮的：本地 SQLite + 生产 PostgreSQL，或开发期进程内存缓存 + 生产 Memcached。
- 十二要素开发者抵制开发与生产用不同 backing service 的诱惑，即使适配器理论上抽象掉了差异。
- backing service 差异滋生微小不兼容，使开发/预发布通过测试的代码在生产失败；此类摩擦抑制持续部署，生命周期内聚合成本极高。
- 现代 backing service（Memcached、PostgreSQL、RabbitMQ）经 Homebrew、apt-get 等现代打包系统不难安装运行。
- 声明式配置工具 Chef/Puppet + 轻量虚拟环境 Docker/Vagrant 可运行贴近生产的本地环境，成本远低于 dev/prod parity 与持续部署的收益。
- 适配器仍有用（移植到新 backing service 相对无痛），但所有 deploy 应使用每个 backing service 的同类型同版本。

## 为什么 (why)

- backing service 差异滋生微小不兼容，使通过测试的代码在生产失败，打击信心，这大幅降低了环境差异引发的线上故障概率。
- 摩擦抑制持续部署，应用生命周期内聚合成本极高，长期代价巨大，是持续部署得以长期坚持的基础条件，开发与生产的栈一致让问题更早暴露、更快修复。
- 缩小时间/人员/工具三大差距是持续部署得以成立的前提，缺一不可，减少因环境特化导致的隐性不兼容，让测试结论对生产行为更有参考价值。

## 如何实践 (how)

- 用现代打包系统（Homebrew/apt-get）在本地安装与生产相同的服务，栈一致，这大幅降低了环境差异引发的线上故障概率。
- 用 Chef/Puppet 声明式配置 + Docker/Vagrant 轻量虚拟环境贴近生产，环境近似。
- 不用适配器掩盖 backing service 差异；所有 deploy 用同类型同版本，杜绝微不兼容。
- 把部署间隔从周缩短到小时/分钟级，加速反馈闭环，是持续部署得以长期坚持的基础条件，开发与生产的栈一致让问题更早暴露、更快修复。
- 让写代码的开发者参与部署与生产行为观察，责任闭环，减少因环境特化导致的隐性不兼容，让测试结论对生产行为更有参考价值。

## 案例 (cases)

- 本地 SQLite + 生产 PostgreSQL——应抵制的诱惑，微不兼容风险高，这大幅降低了环境差异引发的线上故障概率。
- 开发期进程内存缓存 + 生产 Memcached——应抵制的诱惑，行为差异大，是持续部署得以长期坚持的基础条件。
- ActiveRecord 适配 MySQL/PostgreSQL/SQLite；Celery 适配 RabbitMQ/Beanstalkd/Redis；ActiveSupport::Cache 适配 Memory/文件系统/Memcached。
- Homebrew、apt-get 安装现代 backing service，本地轻松贴近生产，开发与生产的栈一致让问题更早暴露、更快修复。
- Chef、Puppet + Docker、Vagrant 贴近生产环境，声明式可复现，减少因环境特化导致的隐性不兼容。
- 传统 vs 十二要素对比：部署间隔 周/小时、作者与部署者 不同人/同一人、环境 分歧/尽可能相似。

## 反模式/易错点

- 本地轻量、生产重量级 backing service（SQLite vs PostgreSQL）组合，行为不一致。
- 依赖 adapters 抽象掩盖 backing service 差异，微不兼容潜伏，这大幅降低了环境差异引发的线上故障概率。
- 三大差距放任扩大，抑制持续部署并抬高生命周期成本，是持续部署得以长期坚持的基础条件，开发与生产的栈一致让问题更早暴露、更快修复。

## 源码索引（实践参考）

- `08-source/app-content-en/dev-prod-parity.md` — X. Dev/prod parity 原文：三大差距/对比表/适配器差异/现代服务可安装/Chef/Puppet/Docker/Vagrant
- `08-source/app-content-en/backing-services.md` — backing service 类型的交叉引用
- `08-source/app-deploy/Readme.md` — 实例：bundle install + heroku local:start 本地跑生产同款 Ruby 栈
- `08-source/app-deploy/Gemfile` — 生产同款依赖声明，支撑本地/生产一致

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-config → app-dev-prod | 前置依赖 | 配置差异是环境漂移主因 |
| app-dev-prod → t-parity | 前置依赖 | 从环境等价理解一致性 |
