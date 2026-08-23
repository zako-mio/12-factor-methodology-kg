# Walkthroughgen 教程生成器 (Walkthroughgen)

- ID: `tool-walkthroughgen`
- 类型: 工具
- 来源: 工具
- 分组: G-TOOLS · 辅助工具集
- 阶段: 进阶 intermediate

> 从 YAML 配置生成分步教程/文档与工作目录，跟踪增量 diff

## 核心主张 (what)

- 从单个 walkthrough.yaml 生成教程、README、文档的 CLI 工具，命令为 walkthroughgen generate <yaml>（src/cli.ts）
- 多 targets：markdown 输出（含 diff 代码块、可折叠段落、语法高亮）、folders 逐节工作目录（by-section + final 最终工程）、ipynb（Python 版扩展出 notebook）
- 增量变更：以虚拟文件状态跟踪每节文件，同一文件被覆盖时用 diff 库输出最小变更（formatMinimalDiff），无实际改动则跳过
- step 类型覆盖：file 复制、dir 建目录、command 执行（incremental 标记仅作用于 folders 构建）、results 期望输出、run_main（Python 版）
- onChange.diff / onChange.cp / newFiles.cat / newFiles.cp 控制展示方式（src/cli.ts targets 配置）
- folders target 为每节建独立工作目录并生成 README.md，skip 数组排除 cleanup 等纯维护节，final.dirName 累积最终工程（src/cli.ts）
- Python 版 walkthroughgen_py.py 把 yaml 转 Jupyter notebook，内嵌 Colab BAML 安装、userdata 处理与 get_baml_client 绕行（CLAUDE.md）
- jest 测试覆盖 CLI 基础行为（--help/缺参/不存在的 yaml 等）与 e2e 生成流程（test/e2e/test-e2e.ts）

## 为什么 (why)

- 手工维护教程时 markdown、示例目录、最终工程三处极易失同步，单一 YAML 源驱动全部输出
- 自动生成 diff 与 cp 命令，让读者精确复现每一步文件变更
- 虚拟文件状态避免重复展示相同内容，仅呈现真正变化
- incremental 标记区分「文档里展示命令」与「构建工作目录时真实执行命令」两种语义
- 双语言扩展（TS markdown+folders / Python ipynb）验证方法论跨栈可复现
- 每节一个可运行检查点，降低入门门槛

## 如何实践 (how)

- walkthrough/ 目录按 00-、01- 前缀存放每步快照文件，yaml 的 file 步骤声明 src/dest（examples/typescript）
- targets 配置输出：onChange.diff 对已存在文件打印最小 diff，newFiles.cat/cp 控制新文件展示方式（src/cli.ts）
- folders target：逐节复制工作状态到独立目录、生成节 README，final 目录累积全部步骤结果（src/cli.ts）
- command+incremental:true 才在 applyStepsToWorkingDir 中执行，否则仅展示（src/cli.ts applyStepsToWorkingDir）
- formatMinimalDiff 用 Diff.createPatch 加 context:2 滤掉无实际变化行对，输出干净 diff 块（src/cli.ts）
- Python 版由 walkthroughgen_py.py 将 yaml 转为 nbformat notebook，注入 baml-cli generate 与 Colab secrets 辅助单元
- run_main 步骤支持 regenerate_baml:true 标记，BAML 变更后自动重新生成（2025-07-16 walkthrough.yaml）
- 生成 markdown 时对既有文件先 diff 后决定展示「show file」还是「skip this step」折叠块（src/cli.ts）

## 案例 (cases)

- 官方 2025-05-17 TS 工作坊：walkthrough.yaml 驱动生成 build/walkthrough.md + build/sections + build/final 完整工程
- 2025-07-16 Python 工作坊：targets 指向 ipynb，生成 workshop_final.ipynb Colab 兼容 notebook
- examples/typescript 最小示例：yaml + walkthrough/00-02 快照生成 TypeScript CLI 入门教程
- examples/walkthroughgen 自举示例：用 walkthroughgen 教如何用 walkthroughgen

## 反模式/易错点

- 教程文档与 walkthrough 快照文件手工编辑不同步，导致生成的 diff 失真
- incremental 标记错用使 npm install 等命令在 markdown 流程中也被执行（应只发生在构建工作目录时）
- 把命令结果直接写死进 yaml 而非用 results 声明，读者无法验证期望输出
- 忽略 folders skip 配置使 cleanup 残留脏状态混入 final 工程
- 改动 CLI 参数却不跑 jest 回归，--help/缺参/缺文件等边界行为静默损坏

## 源码索引（实践参考）

- `08-source/agent-packages/walkthroughgen/src/cli.ts` — 
- `08-source/agent-packages/walkthroughgen/src/index.ts` — 
- `08-source/agent-packages/walkthroughgen/readme.md` — 
- `08-source/agent-packages/walkthroughgen/prompt.md` — 
- `08-source/agent-packages/walkthroughgen/examples/typescript/walkthrough.yaml` — 
- `08-source/agent-packages/walkthroughgen/examples/walkthroughgen/walkthrough.yaml` — 
- `08-source/agent-packages/walkthroughgen/test/e2e/test-e2e.ts` — 
- `08-source/agent-packages/walkthroughgen/package.json` — 

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| tool-walkthroughgen → tool-workshops | 前置依赖 | 工作坊由 walkthroughgen 生成 |
