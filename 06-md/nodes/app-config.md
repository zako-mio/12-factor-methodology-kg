# 配置 (Config)

- ID: `app-config`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 基础 basic

> 配置存于环境变量，与代码严格分离

## 核心主张 (what)

- config 是随 deploy 变化的一切：句柄、凭据、特有值
- 配置存于环境变量，与代码严格分离
- env vars 正交，按 deploy 独立管理

## 为什么 (why)

- config 随部署变化而代码不变
- 代码内常量/配置文件易泄露且脆弱
- 按环境分组随部署增多组合爆炸

## 如何实践 (how)

- 全部 config 入 env vars
- 每 deploy 独立管理
- 试金石：开源不泄凭据

## 案例 (cases)

- env vars 优于 Java System Properties

## 反模式/易错点

- config 作为代码常量
- 用 config 文件
- 按环境名分组

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-backing → app-config | 前置依赖 | 后端服务句柄存于配置 |
| app-config → app-dev-prod | 前置依赖 | 配置差异是环境漂移主因 |
| app-config → t-config | 前置依赖 | 从环境配置理解可变性外置 |
| app-config → ag-prompts | 变体 | 环境配置 ↔ prompt 管理 |
