# 官方工作坊材料 (Official Workshops)

- ID: `tool-workshops`
- 类型: 工具
- 来源: 工具
- 分组: G-TOOLS · 辅助工具集
- 阶段: 高级 advanced

> 2025 年两次官方工作坊（TS/Python 双版本）的演练材料与样例

## 核心主张 (what)

- 两次官方工作坊均以 walkthrough.yaml 为唯一源，主题都是「从裸仓库逐章构建 12-factor agent」
- 2025-05-17 TS 版：14 节（cleanup + Chapter 0-11 + Chapter XX），从 Hello World 一路到 email 审批与 HumanLayer Webhook 集成
- 2025-07-16 Python 版：8 章（hello-world→context-window），targets 为 ipynb 输出 Jupyter notebook，面向 Google Colab
- 两种形态：walkthroughgen 的 markdown+folders（TS）vs walkthroughgen_py 的 notebook（Python）

## 为什么 (why)

- 把抽象方法论变成可跟随的动手路径，每章一个可运行检查点，降低入门门槛
- TS/Python 双语言 + CLI/notebook 双形态，验证方法论跨技术栈可复现

## 如何实践 (how)

- 以 walkthrough.yaml 声明章节与步骤（file/dir/command/results），walkthrough/ 目录存每章快照
- TS 版生成 by-section 工作目录与 final 工程，每个增量命令标注 incremental 只用于目录构建
- Python 版由 walkthroughgen_py 转 notebook，注入 baml-cli generate 与 Colab secrets（OpenAI key）辅助单元
- 章节递进覆盖：工具定义→工具循环→BAML 测试→人类工具→状态管理→人类审批→webhook

## 案例 (cases)

- 05-17 TS 版 14 节从空目录构建出含 email/webhook 审批的完整 agent
- 07-16 Python 版 8 节 + Colab 环境，终点指向「微代理在确定性 DAG」模式

## 反模式/易错点

- 跳章节不跑前序步骤，导致后续文件变更缺少依赖上下文、diff 对不上
- 把工作坊当演示 PPT 而非动手构建，跳过 walkthrough 快照文件手敲内容
- 忽略 cleanup 节残留旧文件，使后续生成的 final 工程混入脏状态

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| tool-walkthroughgen → tool-workshops | 前置依赖 | 工作坊由 walkthroughgen 生成 |
| tool-workshops → ag-prompts | 组合 | 工作坊演练 prompt 管理与工具编排 |
