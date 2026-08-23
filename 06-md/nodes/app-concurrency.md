# 并发 (Concurrency)

- ID: `app-concurrency`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 进阶 intermediate

> 通过进程模型横向扩展

## 核心主张 (what)

- 任何计算机程序一经运行即由一个或多个进程表示；web 应用进程执行形态多样：PHP 进程作为 Apache 子进程按需启动。
- Java 走另一极端：JVM 提供一个启动时预留大块系统资源（CPU 与内存）的巨型 uberprocess，并发由内部线程管理。
- 上述两种传统形态下，运行中的进程对应用开发者几乎不可见，运维与调试困难，这使并发扩展成为简单可靠的横向操作。
- 十二要素中进程是一等公民，强烈借鉴 unix 运行服务 daemon 的进程模型来组织应用，是十二要素进程模型的核心优势所在。
- 用该模型把每种工作指派给一种进程类型：HTTP 请求由 web 进程处理，长跑后台任务由 worker 进程处理。
- 这不排除单进程内部多路复用：运行时 VM 内的线程，或 EventMachine、Twisted、Node.js 的 async/evented 模型。
- 单个 VM 只能长到一定规模（纵向扩展），应用必须能跨多台物理机的多个进程运行（横向扩展），工作负载多样性因此得到清晰的结构化表达。
- 进程模型在 scale out 时真正发光：share-nothing、可水平分区的特性使增加并发成为简单可靠的操作。
- 进程类型数组及每种类型的进程数合称 process formation，是并发部署的完整描述，运维与开发都能清楚理解并管理进程拓扑。
- 十二要素进程绝不应 daemonize 或写 PID 文件，而应依赖 OS 进程管理器（systemd、云平台分布式进程管理器、开发期 Foreman）管理输出流、响应崩溃并处理用户发起的重启与停机。

## 为什么 (why)

- 进程模型在 scale out（横向扩展）时简单可靠，扩缩容即加减进程数，这使并发扩展成为简单可靠的横向操作。
- 巨型 JVM 单进程模型仅能纵向扩展，受单机资源上限约束，扩展天花板低，是十二要素进程模型的核心优势所在。
- 进程类型清晰表达工作负载多样性，架构边界分明，运维可理解，工作负载多样性因此得到清晰的结构化表达，运维与开发都能清楚理解并管理进程拓扑。

## 如何实践 (how)

- 按工作类型划分 web/worker 等 process type，组成 process formation，明确职责。
- 进程交系统进程管理器管理（systemd、云平台分布式进程管理器、开发期 Foreman），处理崩溃重启与用户发起的重启/停机。
- 单进程内可用线程或 async/evented 模型（EventMachine、Twisted、Node.js）做内部多路复用。
- 扩展时增加进程数量而非单进程能力，实现横向扩展，规避纵向天花板，这使并发扩展成为简单可靠的横向操作。
- 输出流管理、崩溃响应、重启停机全部交给进程管理器负责，应用不亲自打理，是十二要素进程模型的核心优势所在。

## 案例 (cases)

- systemd：Linux 系统进程管理器，管理常驻服务进程与崩溃重启，这使并发扩展成为简单可靠的横向操作。
- Foreman：开发期进程管理器，本地按 Procfile 拉起多个进程类型，是十二要素进程模型的核心优势所在。
- Node.js、EventMachine、Twisted：async/evented 单进程多路复用模型。
- PHP 作为 Apache 子进程按需启动——传统进程形态之一，对开发者不可见，工作负载多样性因此得到清晰的结构化表达。
- JVM 巨型单进程模型——传统形态之二，仅能纵向扩展，有物理上限，运维与开发都能清楚理解并管理进程拓扑。

## 反模式/易错点

- 进程 daemonize 或写 PID 文件——应由进程管理器接管，应用不做后台化，这使并发扩展成为简单可靠的横向操作。
- 单进程巨型模型（巨型 JVM）仅能纵向扩展，扩展天花板受限，是十二要素进程模型的核心优势所在，工作负载多样性因此得到清晰的结构化表达。
- 运行进程对开发者不可见，失去可观测性与管理清晰度，运维与开发都能清楚理解并管理进程拓扑，让扩缩容即增减进程数，简单直接。

## 源码索引（实践参考）

- `08-source/app-content-en/concurrency.md` — VIII. Concurrency 原文：进程一等公民/process type/formation/纵向 vs 横向扩展/daemonize 禁令
- `08-source/app-content-en/processes.md` — share-nothing 可水平分区特性的交叉引用
- `08-source/app-content-en/logs.md` — 进程管理器管理输出流的交叉引用
- `08-source/app-deploy/Procfile` — 实例：web 进程类型声明与启动命令

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-processes → app-concurrency | 前置依赖 | 进程模型是并发的基座 |
| app-concurrency → app-admin | 前置依赖 | 管理进程独立于进程编队 |
| app-concurrency → t-scaling | 前置依赖 | 从进程扩展理解规模化 |
