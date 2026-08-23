# 开发/线上等价 (Dev/prod parity)

- ID: `app-dev-prod`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 进阶 intermediate

> 保持开发、预发布、生产环境尽可能相似

## 核心主张 (what)

- 缩小时间/人员/工具三大差距
- 支持持续部署
- 各 deploy 用同类型同版本服务

## 为什么 (why)

- 服务差异致微不兼容，生产失败
- 摩擦抑制持续部署，成本极高

## 如何实践 (how)

- 包装系统易装现代服务
- Docker/Vagrant 贴近生产
- adapters 不能掩盖差异

## 案例 (cases)

- Chef、Puppet、Docker、Vagrant

## 反模式/易错点

- 本地轻量生产重量
- adapters 掩盖差异

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-config → app-dev-prod | 前置依赖 | 配置差异是环境漂移主因 |
| app-dev-prod → t-parity | 前置依赖 | 从环境等价理解一致性 |
