# 后端服务 (Backing services)

- ID: `app-backing`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 基础 basic

> 后端服务作为附加资源，可随时替换连接

## 核心主张 (what)

- backing service 是应用在正常运行过程中经网络消费的任何服务，示例包括数据存储（MySQL、CouchDB）、消息/队列系统（RabbitMQ、Beanstalkd）。
- backing service 还包括出站邮件 SMTP 服务（如 Postfix）与缓存系统（如 Memcached），都是应用运行依赖的网络服务。
- 除本地托管服务外，应用还常使用第三方托管服务：Postmark（SMTP）、New Relic/Loggly（指标收集）、Amazon S3（二进制资产）、Twitter/Google Maps/Last.fm（API 消费服务）。
- 数据库等 backing service 传统上由部署应用运行时的同一批系统管理员管理，运维归属一致。
- 十二要素应用的代码对本地与第三方服务不做区分：对应用而言都是 attached resources，经 config 中的 URL 或其他定位符/凭据访问。
- deploy 可在不改代码的情况下把本地 MySQL 换成第三方托管的 Amazon RDS，或把本地 SMTP 换成 Postmark，仅需修改 config 中的资源句柄。
- 每个不同的 backing service 是一个资源：例如一个 MySQL 数据库是一个资源，应用层分片用的两个 MySQL 数据库算两个不同资源。
- 资源可随意挂到或摘离 deploy：数据库因硬件故障表现异常时，管理员可启动一台从近期备份恢复的新数据库服务器，摘旧挂新，全程无需代码变更。

## 为什么 (why)

- 本地与托管服务对应用可互换，基础设施选型与代码完全解耦，选型自由度高，这正是 backing service 与代码解耦的核心体现。
- 资源与 deploy 松散耦合，实现 attached resources 的语义，挂摘清晰，资源更换因此成为纯运维操作，与代码无关。
- 故障时可拆旧挂新，运维灵活且无需代码变更，恢复速度快，保证应用可随时切换基础设施而不影响业务逻辑，是十二要素松散耦合与可移植性的重要支撑。
- 多资源建模（如分片数据库）与部署拓扑清晰对应，边界分明易管理，使故障恢复与扩容都能在不改代码的前提下完成。

## 如何实践 (how)

- 把数据库、队列、缓存等一切网络消费服务一律视为 attached resources 处理，统一对待。
- 经 config 中的资源句柄（URL/凭据）访问全部 backing service，不硬编码访问方式。
- 换服务只需改 config 中的资源句柄，不改应用代码，即可完成替换，这正是 backing service 与代码解耦的核心体现。
- 挂摘资源作为部署层操作，与代码演进完全解耦，运维动作独立，资源更换因此成为纯运维操作，与代码无关，保证应用可随时切换基础设施而不影响业务逻辑。

## 案例 (cases)

- 本地 MySQL 换成第三方 Amazon RDS，不改代码只改资源句柄，即完成托管迁移，这正是 backing service 与代码解耦的核心体现。
- 本地 SMTP 换成第三方 Postmark 服务，仅换 config 句柄，代码零改动，资源更换因此成为纯运维操作，与代码无关。
- 数据库硬件故障：启动新库（从备份恢复）→摘旧库→挂新库，全程无代码变更，仅运维操作，保证应用可随时切换基础设施而不影响业务逻辑。
- 应用层分片的两个 MySQL 数据库算两个不同资源，各自独立挂摘管理，是十二要素松散耦合与可移植性的重要支撑。
- New Relic/Loggly（指标收集）、Amazon S3（二进制资产）、Twitter/Google Maps/Last.fm（消费型 API 服务）等第三方典型。

## 反模式/易错点

- 代码中区分本地服务与第三方服务，破坏互换性，迁移需改代码，这正是 backing service 与代码解耦的核心体现。
- backing service 与特定 deploy 强耦合，无法挂摘，故障恢复困难，资源更换因此成为纯运维操作，与代码无关。
- 资源句柄硬编码在代码而非 config，换服务需改代码并重新部署，保证应用可随时切换基础设施而不影响业务逻辑。
- 把不同用途的 backing service 混为一个资源管理，拓扑无法清晰表达，是十二要素松散耦合与可移植性的重要支撑。

## 源码索引（实践参考）

- `08-source/app-content-en/backing-services.md` — IV. Backing services 原文：定义/本地与第三方不分/资源建模/挂摘无代码变更
- `08-source/app-content-en/config.md` — 资源句柄经 config 存储的交叉引用
- `08-source/app-content-en/dev-prod-parity.md` — backing service 在开发/生产一致性中的角色
- `08-source/app-content-en/port-binding.md` — 端口绑定服务可成为另一 app 的 backing service

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-backing → app-config | 前置依赖 | 后端服务句柄存于配置 |
| app-deps → app-backing | 组合 | 依赖声明 + 后端资源 |
| app-backing → ag-tools | 依赖关联 | 工具是 Agent 的外部后端服务 |
