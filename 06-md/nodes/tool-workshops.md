# 官方工作坊材料 (Official Workshops)

- ID: `tool-workshops`
- 类型: 工具
- 来源: 工具
- 分组: G-TOOLS · 辅助工具集
- 阶段: 高级 advanced

> 2025 年两次官方工作坊（TS/Python 双版本）的演练材料与样例

## 核心主张 (what)

- 两次官方工作坊均以 walkthrough.yaml 为唯一源，主题都是「从裸仓库逐章构建 12-factor agent」
- 2025-05-17 TS 版：cleanup + Chapter 0-11 + Chapter XX（HumanLayer Webhook），从 Hello World 一路到 email 审批与 webhook 集成（walkthrough.yaml）
- 2025-07-16 Python 版：8 章（hello-world→context-window），targets 为 ipynb 输出 Jupyter notebook，面向 Google Colab
- 两种形态：walkthroughgen 的 markdown+folders（TS）vs walkthroughgen_py 的 notebook（Python）
- 章节递进覆盖：工具定义→工具循环→BAML 测试→人类工具→状态管理→人类审批→webhook（walkthrough.yaml sections）
- 2025-05 目录含完整 13 节 sections（00-hello-world…12-humanlayer-webhook）+ final 工程
- final/ 工程即完整六模块骨架（src/agent.ts、cli.ts、state.ts、server.ts、index.ts + baml_src 四文件）
- 每章一个可运行检查点，快照文件经 walkthroughgen 自动生成章节 README

## 为什么 (why)

- 把抽象方法论变成可跟随的动手路径，每章一个可运行检查点，降低入门门槛
- TS/Python 双语言 + CLI/notebook 双形态，验证方法论跨技术栈可复现
- 从零构建比只看成品更内化：读者亲手经历每个文件变更
- 工作坊产物即 create-12-factor-agent 模板的验证来源，两者互为证明
- 2025-07-16 终点明确指向「微代理在确定性 DAG」模式，衔接方法论未来方向

## 如何实践 (how)

- 以 walkthrough.yaml 声明章节与步骤（file/dir/command/results），walkthrough/ 目录存每章快照
- TS 版生成 by-section 工作目录与 final 工程，每个增量命令标注 incremental 只用于目录构建（walkthrough.yaml targets）
- Python 版由 walkthroughgen_py 转 notebook，注入 baml-cli generate 与 Colab secrets（OpenAI key）辅助单元（walkthroughgen_py.py）
- 章节递进：0 hello-world → 1 CLI+agent loop → 2 calculator tools → 3 tool loop → 4 BAML tests → 5 human tools → 6 customize prompt → 7 context window → 8 API endpoints → 9 state → 10-11 human approval → XX webhook（walkthrough.yaml）
- 每章 walkthrough 快照经 walkthroughgen 生成 README，读者按 diff/cp 步骤逐节构建（sections/*/README.md）
- notebook 环境教训固化为 CLAUDE.md 实现要点：无 async、无 sys.argv、全局命名空间、IN_COLAB 检测（CLAUDE.md）

## 案例 (cases)

- 2025-05-17 TS 版 13 节从空目录构建出含 email/webhook 审批的完整 agent（build/sections + build/final）
- 2025-07-16 Python 版 8 节 + Colab 环境，workshop_final.ipynb 输出验证（2025-07-16/）
- 2025-05 与 2025-05-17 为同一内容的两份版本目录，sections 逐章对应
- 章节 README 与 template/src 六模块完全对应，工作坊即脚手架的逐步说明

## 反模式/易错点

- 跳章节不跑前序步骤，导致后续文件变更缺少依赖上下文、diff 对不上
- 把工作坊当演示 PPT 而非动手构建，跳过 walkthrough 快照文件手敲内容
- 忽略 cleanup 节残留旧文件，使后续生成的 final 工程混入脏状态
- 只看 final 工程而不看增量 diff，丧失对每步变更动因的理解
- 在 notebook 环境误用 async/await 或 sys.argv，违背 CLAUDE.md 固化的约束（无 async、无 sys.argv）

## 源码索引（实践参考）

- `08-source/agent-workshops/2025-05-17/walkthrough.yaml` — 
- `08-source/agent-workshops/2025-05-17/sections/00-hello-world/README.md` — 
- `08-source/agent-workshops/2025-05-17/sections/01-cli-and-agent/README.md` — 
- `08-source/agent-workshops/2025-05-17/sections/03-tool-loop/README.md` — 
- `08-source/agent-workshops/2025-05/walkthrough.yaml` — 
- `08-source/agent-workshops/2025-05/final/src/agent.ts` — 
- `08-source/agent-workshops/2025-05/final/baml_src/agent.baml` — 
- `08-source/agent-workshops/2025-07-16/walkthrough.yaml` — 
- `08-source/agent-workshops/2025-07-16/walkthroughgen_py.py` — 
- `08-source/agent-workshops/2025-07-16/CLAUDE.md` — 

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| tool-walkthroughgen → tool-workshops | 前置依赖 | 工作坊由 walkthroughgen 生成 |
| tool-workshops → ag-prompts | 组合 | 工作坊演练 prompt 管理与工具编排 |
