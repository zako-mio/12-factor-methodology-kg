# 控制流与阶段治理 (Control Flow & Stages)

- ID: `t-control`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT06 · 控制流与阶段治理
- 阶段: 高级 advanced

> 确定性控制流 / 阶段分离保证可预测交付

## 核心主张 (what)

- App 严格分离 build/release/run 三阶段，运行时不可能改代码（build-release-run.md）
- Agent 控制流由确定性代码决定，LLM 只在决策点选路（factor-08）
- App 的 release 是不可变只追加账本，创建后不可变更（build-release-run.md）
- Agent 的 while-loop 中 async 步骤 break 等待、sync 步骤 continue 回环（factor-08）
- 阶段分离/控制流治理共同目标：可预测、可回滚、可审计的交付
- App 每 release 有唯一 ID（时间戳或递增号），变更即新建（build-release-run.md）
- Agent 可在工具选择与执行之间插入审批等确定性中断（factor-08）
- 确定性控制流是 reducer 语义、暂停恢复、错误压缩的前提（factor-08/09/12）

## 为什么 (why)

- 运行期改代码无法传播回 build，严格分离杜绝运行时漂移（build-release-run.md）
- release 不可变保证回滚能力：Capistrano releases 目录 + rollback 命令（build-release-run.md）
- run 阶段尽量少活动部件，避免无人在场时夜间故障（build-release-run.md）
- 确定性控制流让中断/审批/审计成为可能（factor-08）
- 自定义控制结构（总结/缓存/LLM-as-judge/限流/sleep）针对场景裁剪（factor-08）
- 可中断可恢复创造更自然的对话与工作流（factor-08）

## 如何实践 (how)

- App：build 把代码库转换为可执行 bundle（拉依赖、编译资产）（build-release-run.md）
- App：release=build+config，带唯一 ID，只追加不回写（build-release-run.md）
- App：run 用所选 release 启动一组进程（build-release-run.md）
- Agent：agentLoop while(true) 反复调用 DetermineNextStep 决策（agent.ts）
- Agent：request_clarification/create_issue 类 async 步骤 break 等 webhook（factor-08 代码）
- Agent：fetch_open_issues 类 sync 步骤 continue 带结果回环（factor-08 代码）
- Agent：done_for_now 返回 thread 结束循环，交由外层决定（agent.ts）
- Agent：switch(intent) 全覆盖 + else 兜底，控制流确定性（agent.ts/factor-01）

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| build 阶段取指定 commit，拉取 vendored 依赖并编译二进制与资产（build-release-run.md） | 自建控制结构可自由裁剪到用例：总结/缓存/judge/限流/睡眠（factor-08） | App 是部署管线的纵向流程（build→release→run）；Agent 是运行循环的横向迭代（决策→执行→反馈） |
| release 阶段把 build 与 deploy 当前 config 组合（build-release-run.md） | request_clarification：模型要更多信息时 break 循环等人类（factor-08 代码） | 前者治理「交付物怎么产生」；后者治理「行为怎么演进」 |
| release 带时间戳/递增号唯一 ID，创建后不可变更（build-release-run.md） | fetch_open_issues：同步执行把结果 append 进上下文继续（factor-08 代码） | App 阶段分离面向不可变发布与回滚；Agent 循环面向可中断交互与审批 |
| Capistrano 用 releases 子目录 + symlink 管理当前版本，rollback 即回切（build-release-run.md） | create_issue：高赌注操作 break 等人类审批（factor-08 代码） | App 的控制点是每个发布周期；Agent 的控制点是每次循环迭代 |
| run 可由服务器重启/进程管理器崩溃重启自动触发（build-release-run.md） | agentLoop 由代码完全掌控迭代，模型仅产出 intent（agent.ts） | 差异根源：App 交付物是一次性产物、Agent 行为是持续运行过程 |
| run 阶段保持最少活动部件，build 可复杂因为总有人在现场（build-release-run.md） | 中断与恢复组合出自然的多轮交互与工作流（factor-08） |  |
| 站点 Procfile 声明 web 进程即 run 阶段的入口定义（Procfile） | 与错误压缩结合：确定性重构错误表示防 spin-out（factor-09） |  |

## 源码索引（实践参考）

- `08-source/app-content-en/build-release-run.md` — 
- `08-source/app-content-en/codebase.md` — 
- `08-source/app-content-en/config.md` — 
- `08-source/app-deploy/Procfile` — 
- `08-source/agent-content/factor-08-own-your-control-flow.md` — 
- `08-source/agent-content/factor-09-compact-errors.md` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/agent.ts` — 

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-build-run → t-control | 前置依赖 | 从三阶段分离理解控制流 |
| t-control → ag-control | 前置依赖 | 控制流治理落到 Agent 编排 |
