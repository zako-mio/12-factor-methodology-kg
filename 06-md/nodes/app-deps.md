# 依赖 (Dependencies)

- ID: `app-deps`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 基础 basic

> 显式声明并隔离依赖，绝不依赖系统级隐式包

## 核心主张 (what)

- 清单完整精确声明全部依赖
- 隔离工具杜绝隐式依赖泄漏
- 开发生产统一使用

## 为什么 (why)

- 显式声明简化环境搭建，一条命令跑通
- 系统工具存在与版本无法保证

## 如何实践 (how)

- 声明与隔离同时使用
- Bundler/Pip+Virtualenv 等
- 确定性 build command

## 案例 (cases)

- Bundler、Pip、Autoconf、Leiningen

## 反模式/易错点

- 只声明不隔离或反之
- 依赖隐式系统工具
- 依赖系统级 site packages

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-deps → app-build-run | 前置依赖 | 依赖在构建阶段声明 |
| app-deps → t-deps | 前置依赖 | 从依赖声明理解显式化 |
| app-deps → ag-tools | 变体 | 依赖清单 ↔ 工具定义 |
| app-deps → app-backing | 组合 | 依赖声明 + 后端资源 |
