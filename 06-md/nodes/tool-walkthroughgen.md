# Walkthroughgen 教程生成器 (Walkthroughgen)

- ID: `tool-walkthroughgen`
- 类型: 工具
- 来源: 工具
- 分组: G-TOOLS · 辅助工具集
- 阶段: 进阶 intermediate

> 从 YAML 配置生成分步教程/文档与工作目录，跟踪增量 diff

## 核心主张 (what)

- 从单个 walkthrough.yaml 生成教程、README、文档的 CLI 工具，`walkthroughgen generate <yaml>`
- 多 targets：markdown 输出（含 diff 代码块、可折叠段落、语法高亮）、folders 逐节工作目录（by-section + final 最终工程）、ipynb（Python 版扩展出 notebook）
- 增量变更：以虚拟文件状态跟踪每节文件，同一文件被覆盖时用 diff 库输出最小变更，无实际改动则跳过
- step 类型覆盖 file 复制、dir 建目录、command 执行（incremental 标记仅作用于 folders 构建）、results 期望输出

## 为什么 (why)

- 手工维护教程时 markdown、示例目录、最终工程三处极易失同步，单一 YAML 源驱动全部输出
- 自动生成 diff 与 cp 命令，让读者精确复现每一步文件变更

## 如何实践 (how)

- walkthrough/ 目录按 00-、01- 前缀存放每步快照文件，yaml 的 file 步骤声明 src/dest
- targets 配置输出：onChange.diff 对已存在文件打印最小 diff，newFiles.cat/cp 控制新文件展示方式
- folders target 为每节建独立工作目录并生成 readme.md，skip 数组排除 cleanup 等纯维护节
- Python 版由 walkthroughgen_py.py 把 yaml 转 Jupyter notebook，内嵌 Colab BAML 安装与 userdata 处理

## 案例 (cases)

- 官方 2025-05-17 TS 工作坊：walkthrough.yaml 驱动生成 build/walkthrough.md + build/sections + final 完整工程
- 2025-07-16 Python 工作坊：targets 指向 ipynb，生成 Colab 兼容 notebook

## 反模式/易错点

- 教程文档与 walkthrough 快照文件手工编辑不同步，导致生成的 diff 失真
- incremental 标记错用使 npm install 等命令在 markdown 流程中也被执行（应只发生在构建工作目录时）
- 把命令结果直接写死进 yaml 而非用 results 声明，读者无法验证期望输出

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| tool-walkthroughgen → tool-workshops | 前置依赖 | 工作坊由 walkthroughgen 生成 |
