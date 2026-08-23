# 构建·发布·运行 (Build, release, run)

- ID: `app-build-run`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 进阶 intermediate

> 严格分离构建、发布、运行三阶段

## 核心主张 (what)

- codebase 经三阶段转变为非开发 deploy：build 阶段把代码仓库转换为可执行 bundle，按部署进程指定的提交版本拉取 vendored 依赖并编译二进制与资源。
- release 阶段把 build 与 deploy 当前 config 组合，产出同时包含 build 与 config、可立即在运行环境执行的 release。
- run 阶段（runtime）在运行环境中启动一组应用进程，针对选定的 release 运行，是应用真正服务的阶段。
- 十二要素应用严格分离 build、release、run 三阶段：例如运行时不可能改动代码，因为改动无法传播回 build 阶段。
- 部署工具通常提供发布管理能力，最显著的是回滚到先前 release，保障发布安全，这保证了发布过程的可追溯与可回滚。
- 每个 release 应有唯一 ID，如时间戳 2011-04-06-20:32:17 或递增数字 v100，便于定位与回退。
- release 是只追加的账本：创建后不可变更，任何变更都必须产生新 release，保证账本可信。
- build 由开发者在新代码部署时发起；run 可自动发生（服务器重启、崩溃进程被进程管理器重启），故 run 阶段应保持最少活动部件。
- build 阶段可以更复杂，因为错误总是发生在前台驱动部署的开发者面前，可及时处理与修正，使运行期行为与构建产物严格一致，杜绝热改隐患。

## 为什么 (why)

- 运行时改动无法传播回 build，严格分离保证运行期行为与构建产物一致，杜绝热改隐患，这保证了发布过程的可追溯与可回滚。
- release 含 build+config 且不可变，使回滚成为选择先前 release 的简单操作，发布安全。
- run 阶段最小化活动部件：运行问题会在无开发者到场的深夜自动重启时爆发，越简单越健壮，使运行期行为与构建产物严格一致，杜绝热改隐患。

## 如何实践 (how)

- 把代码转换（build）、组合 config（release）、启动进程（run）严格分离为独立阶段，各司其职。
- 用部署工具的 release 管理能力做回滚，例如 Capistrano 的 rollback 命令。
- Capistrano 在 releases 子目录存放各版本，当前 release 是指向当前版本目录的 symlink，rollback 命令可快速回退。
- 每个 release 打唯一 ID（时间戳或递增数字），保证可精确引用，这保证了发布过程的可追溯与可回滚。
- release 只追加、创建后不可变，任何变更新建 release，保持账本完整，使运行期行为与构建产物严格一致，杜绝热改隐患。
- build 由开发者驱动可复杂；run 自动发生应保持最少活动部件，降低自动场景风险，是十二要素发布可靠性设计的核心机制。

## 案例 (cases)

- Capistrano：releases 子目录 + 当前版本 symlink + rollback 命令，快速回退到先前版本。
- release ID 示例：时间戳 2011-04-06-20:32:17 或递增数字 v100，两种格式均可采用。
- 服务器重启、崩溃进程被进程管理器重启等 run 阶段自动执行场景，常发生在深夜无开发者在场时，这保证了发布过程的可追溯与可回滚。
- 发布新代码时开发者驱动 build 阶段，把提交固定到部署进程指定的版本上，使运行期行为与构建产物严格一致，杜绝热改隐患。

## 反模式/易错点

- 运行时修改代码——改动无法传播回 build 阶段，运行态与构建产物脱节，这保证了发布过程的可追溯与可回滚。
- 变更既有 release——release 是不可变、只追加的账本，任何修改破坏可追溯性，使运行期行为与构建产物严格一致，杜绝热改隐患。
- run 阶段引入过多活动部件，放大深夜无人时的故障风险，降低可靠性，是十二要素发布可靠性设计的核心机制。
- 把 build 与 release 混为一体，无法独立回滚配置或复用构建产物，发布管理因此简单、安全、可控。

## 源码索引（实践参考）

- `08-source/app-content-en/build-release-run.md` — V. Build, release, run 原文：三阶段定义/回滚/release 不可变/run 最小化
- `08-source/app-content-en/codebase.md` — build 的输入 codebase 定义
- `08-source/app-content-en/config.md` — release 与 config 组合的交叉引用
- `08-source/app-content-en/processes.md` — run 阶段启动进程的交叉引用

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-deps → app-build-run | 前置依赖 | 依赖在构建阶段声明 |
| app-codebase → app-build-run | 前置依赖 | 代码库是构建的输入 |
| app-build-run → t-control | 前置依赖 | 从三阶段分离理解控制流 |
| app-build-run → ag-control | 变体 | 阶段分离 ↔ 控制流所有权 |
| tool-app-site → app-build-run | 依赖关联 | Procfile 三阶段部署实践 |
