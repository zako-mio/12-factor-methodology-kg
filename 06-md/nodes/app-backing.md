# 后端服务 (Backing services)

- ID: `app-backing`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 基础 basic

> 后端服务作为附加资源，可随时替换连接

## 核心主张 (what)

- backing service 是应用网络消费的任何服务
- 本地与第三方不做区分，经 config 句柄访问
- deploy 可随意挂摘资源不改代码

## 为什么 (why)

- 本地与托管服务可互换
- 资源与 deploy 松散耦合
- 故障时可拆旧挂新

## 如何实践 (how)

- 视为 attached resources
- 换服务仅改资源句柄

## 案例 (cases)

- Amazon RDS、Postmark、S3

## 反模式/易错点

- 代码区分本地与第三方
- 与 deploy 强耦合

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-backing → app-config | 前置依赖 | 后端服务句柄存于配置 |
| app-deps → app-backing | 组合 | 依赖声明 + 后端资源 |
| app-backing → ag-tools | 依赖关联 | 工具是 Agent 的外部后端服务 |
