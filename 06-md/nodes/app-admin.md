# 管理进程 (Admin processes)

- ID: `app-admin`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 进阶 intermediate

> 管理/维护任务作为一次性进程运行

## 核心主张 (what)

- process formation 是应用运行时做常规业务（如处理 web 请求）的进程数组；开发者还常想对应用做一次性管理/维护任务。
- 一次性任务例子：数据库迁移，Django 用 manage.py migrate、Rails 用 rake db:migrate。
- 一次性任务例子：运行 console（REPL shell）执行任意代码或对实时数据库检查模型；多数语言无参运行解释器即得 REPL（python、perl），或独立命令（Ruby 的 irb、Rails 的 rails console）。
- 一次性任务例子：运行提交进应用 repo 的一次性脚本，如 php scripts/fix_bad_records.php 修复坏数据。
- 一次性 admin 进程应在与常规长跑进程相同的环境中运行，针对某个 release 运行，这保证管理操作与线上环境完全一致。
- admin 进程使用与该 release 任何进程相同的 codebase 与 config，保证操作的是线上同款数据环境。
- admin 代码必须随应用代码一起发布，以避免同步问题，保证版本一致，是数据迁移与修复类操作安全性的前提。
- 所有进程类型应使用相同的依赖隔离技术：Ruby web 进程用 bundle exec thin start，则数据库迁移用 bundle exec rake db:migrate。
- Python 用 Virtualenv 的应用，Tornado webserver 与 manage.py admin 进程都应使用 vendored 的 bin/python。
- 十二要素强烈偏好开箱即提供 REPL shell、且便于运行一次性脚本的语言，减少开发摩擦，管理任务因此可重复、可预期、可审计。
- 本地 deploy：开发者在应用检出目录内用直接 shell 命令调用一次性 admin 进程，简单直接。
- 生产 deploy：开发者可用 ssh 或该 deploy 执行环境提供的远程命令执行机制运行此类进程。

## 为什么 (why)

- 一次性任务（迁移/REPL/脚本）需生产同环境才能正确操作线上数据，环境不符必出错，这保证管理操作与线上环境完全一致。
- admin 代码随应用发布避免同步问题，版本永远一致，是数据迁移与修复类操作安全性的前提，管理任务因此可重复、可预期、可审计。
- 依赖隔离一致保证 admin 进程与长跑进程环境完全一致，行为可预期，避免管理脚本与线上环境脱节造成事故。

## 如何实践 (how)

- 数据库迁移、REPL console、一次性修复脚本都作为一次性进程运行，与长跑进程同级，这保证管理操作与线上环境完全一致。
- admin 进程针对 release 运行，使用与长跑进程相同的 codebase 与 config。
- admin 代码随应用代码一起发布，杜绝版本漂移，是数据迁移与修复类操作安全性的前提，管理任务因此可重复、可预期、可审计。
- 所有进程类型用相同依赖隔离技术（bundle exec、vendored bin/python），环境一致。
- 本地用 shell 直接命令，生产用 ssh 或远程执行机制，按环境选择通道，避免管理脚本与线上环境脱节造成事故。

## 案例 (cases)

- manage.py migrate（Django）数据库迁移，管理任务典型，这保证管理操作与线上环境完全一致。
- rake db:migrate（Rails）数据库迁移，同属管理任务，是数据迁移与修复类操作安全性的前提。
- REPL：python、perl 无参运行；irb（Ruby）、rails console（Rails）独立命令。
- php scripts/fix_bad_records.php：提交进 repo 的一次性脚本，修复线上数据。
- bundle exec rake db:migrate 与 bundle exec thin start 同源依赖隔离，环境一致。
- Virtualenv 应用的 vendored bin/python 同时运行 Tornado 与 manage.py，统一解释器。

## 反模式/易错点

- admin 代码与应用代码分离，导致同步问题，版本漂移，这保证管理操作与线上环境完全一致，是数据迁移与修复类操作安全性的前提。
- admin 进程的依赖隔离与长跑进程不一致，环境行为不可预期，管理任务因此可重复、可预期、可审计，避免管理脚本与线上环境脱节造成事故。
- 在非生产同环境下运行一次性管理任务操作线上数据，操作危险，让一次性任务与常规进程共享同一套环境与依赖。

## 源码索引（实践参考）

- `08-source/app-content-en/admin-processes.md` — XII. Admin processes 原文：迁移/REPL/一次性脚本/同环境同 release/依赖隔离一致/本地 shell 生产 ssh
- `08-source/app-content-en/concurrency.md` — process formation 概念来源
- `08-source/app-content-en/build-release-run.md` — admin 进程针对 release 运行的交叉引用
- `08-source/app-content-en/dependencies.md` — 依赖隔离技术在 admin 进程的应用

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-concurrency → app-admin | 前置依赖 | 管理进程独立于进程编队 |
| app-admin → t-human | 前置依赖 | 从管理进程理解人机边界 |
