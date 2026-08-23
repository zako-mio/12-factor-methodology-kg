# 依赖 (Dependencies)

- ID: `app-deps`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 基础 basic

> 显式声明并隔离依赖，绝不依赖系统级隐式包

## 核心主张 (what)

- 多数编程语言提供打包系统分发支持库，如 Perl 的 CPAN、Ruby 的 Rubygems；经打包系统安装的库可装到系统全局（site packages）或限定到应用目录（vendoring/bundling）。
- 十二要素应用绝不依赖系统级包的隐式存在：通过依赖声明清单完整且精确地声明全部依赖及其版本约束，这使构建在任何环境都能可复现、结果确定。
- 执行时使用依赖隔离工具，确保没有隐式依赖从周围系统泄漏进应用运行环境，是十二要素保证开发与生产一致的关键手段。
- 完整显式的依赖规格对生产与开发环境统一应用，保证两处依赖完全一致、行为可复现，环境搭建因此只需少量前置条件即可一步到位。
- Ruby 的 Bundler 提供 Gemfile 清单格式作依赖声明，bundle exec 作隔离；声明与隔离两步骤常是两个独立工具。
- Python 中 Pip 负责声明、Virtualenv 负责隔离；C 用 Autoconf 声明、用静态链接提供隔离能力。
- 无论何种工具链，依赖声明与隔离必须同时使用，只用一个不足以满足十二要素的要求，从根本上杜绝隐式依赖在不同机器上的行为差异。

## 为什么 (why)

- 显式声明简化新开发者上手：检出代码后只需语言运行时与依赖管理器两个前置条件，即可搭建全部运行所需环境。
- 通过确定性构建命令即可搭好一切，如 bundle install、lein deps，减少环境搭建的试错成本与手工步骤。
- 系统工具的隐式存在无法保证：ImageMagick、curl 等可能在某些运行系统缺失，或版本与应用不兼容导致运行失败。
- 隔离机制杜绝隐式依赖从系统泄漏，保证运行环境纯净可复现，避免开发环境过得了而生产环境崩溃，这使构建在任何环境都能可复现、结果确定。

## 如何实践 (how)

- 用依赖清单（Gemfile、requirements.txt 等）完整精确声明全部依赖及版本约束，不遗漏任何传递依赖。
- 用隔离工具运行应用：bundle exec、virtualenv、静态链接等，阻止系统包泄漏进应用环境。
- 开发与生产统一使用同一套显式依赖规格，杜绝两处依赖漂移，这使构建在任何环境都能可复现、结果确定，是十二要素保证开发与生产一致的关键手段。
- 新开发者前置条件收敛为语言运行时 + 依赖管理器两个，一条构建命令即可跑通，环境搭建因此只需少量前置条件即可一步到位。
- 确定性构建命令：Ruby/Bundler 用 bundle install，Clojure/Leiningen 用 lein deps。
- 若应用需要 shell out 到系统工具（如 ImageMagick），应把该工具 vendored 进应用而非依赖系统安装。

## 案例 (cases)

- Bundler：Ruby 依赖声明（Gemfile）与隔离（bundle exec）的一体化工具，业界典范实现。
- Pip：Python 依赖声明工具；Virtualenv：Python 依赖隔离工具，两者配套使用。
- Autoconf：C 依赖声明；静态链接可提供 C 依赖隔离，弥补声明之外的空缺，这使构建在任何环境都能可复现、结果确定。
- Leiningen：Clojure 依赖工具，lein deps 为确定性构建命令，一条命令解决依赖。
- CPAN：Perl 打包系统；Rubygems：Ruby 打包系统，是打包分发的经典基础设施，是十二要素保证开发与生产一致的关键手段。

## 反模式/易错点

- 只声明不隔离，或只隔离不声明——声明与隔离必须成对使用，缺一不可，这使构建在任何环境都能可复现、结果确定。
- 依赖系统级 site packages 的隐式存在，环境一变即挂，无法保证可复现，是十二要素保证开发与生产一致的关键手段。
- shell out 到 ImageMagick、curl 等系统工具而不 vendoring，跨系统版本无法保证。
- 依赖声明不全或版本不精确，导致构建不可复现、跨环境行为漂移，排查困难，环境搭建因此只需少量前置条件即可一步到位。

## 源码索引（实践参考）

- `08-source/app-content-en/dependencies.md` — II. Dependencies 原文：声明/隔离两步骤、Gemfile/bundle exec、build command、系统工具 vendoring
- `08-source/app-content-en/admin-processes.md` — 依赖隔离一致性在 admin 进程的应用（bundle exec rake db:migrate 等）
- `08-source/app-deploy/Gemfile` — 12factor 站点自身 Gemfile 示例：sinatra/thin/maruku/i18n 等依赖声明
- `08-source/app-deploy/Readme.md` — 实例：bundle install 作本地运行前置步骤

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-deps → app-build-run | 前置依赖 | 依赖在构建阶段声明 |
| app-deps → t-deps | 前置依赖 | 从依赖声明理解显式化 |
| app-deps → ag-tools | 变体 | 依赖清单 ↔ 工具定义 |
| app-deps → app-backing | 组合 | 依赖声明 + 后端资源 |
