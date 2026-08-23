# 12 Factor 方法论合并知识图谱

> 将 **12 Factor App**（12 条传统 SaaS 工程原则）与 **12 Factor Agent**（12 条 LLM Agent 工程原则）合并为一个统一的软件工程方法论知识图谱。

[![GitHub Pages](https://img.shields.io/badge/在线预览-GitHub%20Pages-blue)](https://zako-mio.github.io/12-factor-methodology-kg/)
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Nodes](https://img.shields.io/badge/Nodes-38-orange)]()
[![Edges](https://img.shields.io/badge/Edges-61-yellow)]()

两套方法论本质都是**软件工程思路**：一个面向传统云原生应用，一个面向 LLM 驱动的 Agent 应用。本图谱用「双体系 + 桥接主题」的方式将它们组织为一张无环 DAG，让工程师能看到：哪些原则是**一脉相承**的（如无状态进程 ↔ 无状态 Reducer），哪些是**方法论演化**的新增维度（如上下文窗口工程）。

## 图谱核心

| 构成 | 数量 | 说明 |
|---|---|---|
| App 原则 | 12 | 12 Factor App（代码库 → 管理进程） |
| Agent 原则 | 12 | 12 Factor Agent（自然语言→工具调用 → 无状态 Reducer） |
| 桥接主题 | 10 | 无状态 / 生命周期 / 配置 / 可观测 / 依赖 / 控制流 / 入口 / 规模 / 人机 / 环境 |
| 辅助工具 | 4 | create-12-factor-agent 脚手架 / walkthroughgen / 官方工作坊 / 12factor.net 站点 |
| 关系边 | 61 | prerequisite 40 / variant 7 / combination 8 / cooccurrence 2 / dependency 4 |
| 分组 | 16 | 来源 2 + 主题 10 + 横切 3 + 工具 1 |

DAG 由 prerequisite 边构成无环主干（Kahn 校验通过），学习路径由拓扑序自动生成。

## 在线预览

- **GitHub Pages**: <https://zako-mio.github.io/12-factor-methodology-kg/>
- 本地打开 `index.html` 亦可完整浏览（纯静态、离线可用）。

## 快速开始

1. 打开根入口 `index.html`（或在线预览），查看核心统计与入口导航。
2. 进入**交互 DAG 总览**（`04-interactive/`），组级视图 + 点击下钻 + 桥接高亮模式（只看主题↔原则连接）。
3. 从**分组目录**（`03-groups/`）或交互图进入组页。
4. 点入节点页读 what（核心主张）→ why（为什么）→ how（如何实践）→ 案例 → 反模式；桥接主题节点含 **App 侧 | Agent 侧 | 差异根源** 三栏对比。
5. 按**阶段视图**（`05-views/02-stage.html`）或**学习路径**（`05-views/03-learning-path.html`）安排阅读顺序。
6. **跨体系对照**（`05-views/04-cross-mapping.html`）逐条比对 App ↔ Agent 的方法原则与差异根源。

## 目录结构

```
12-factor-methodology-kg/
├── index.html                  # 根入口（统计 + 导航 + 快速开始）
├── quality-gate.md             # 质量门控报告（七项全通过）
├── report.md / report.html     # 项目报告（AI 友好 + 人类可读）
├── 01-dag-data/                # 核心数据
│   ├── methodology-dag.json    # DAG（38 节点 / 16 组 / 61 边）
│   ├── node-content.json       # 节点五段式内容（bridge 含三栏对比）
│   └── stats.md                # DAG 统计与拓扑说明
├── 02-node-pages/              # 38 个节点详情页（HTML）
├── 03-groups/                  # 16 组页 + 组总索引
├── 04-interactive/             # 交互 DAG 总览（cytoscape + dagre）
│   └── vendor/                 # 本地依赖（cytoscape.min.js + dagre）
├── 05-views/                   # 人类入口视图（总览/阶段/学习路径/跨体系对照）
├── 06-md/                      # AI 友好 Markdown 镜像
│   ├── 00-index.md / 01-groups.md / 02-stage.md / 03-learning-path.md
│   └── nodes/                  # 38 个节点 MD
├── 07-checkpoint/              # 生成脚本 gen-*.py（可重复构建全部交付物）
└── research/                   # 内容来源（App 摘录 / Agent 摘录 / 联网调研）
```

## 数据来源

- **12 Factor App**: [heroku/12factor](https://github.com/heroku/12factor)（12factor.net 官方内容，2011 年由 Adam Wiggins 提出）
- **12 Factor Agent**: [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents)（2025 年由 Dex Horthy 提出，25k+ stars）
- 桥接主题设计与对比分析基于两份官方原文 + 业界解读（见 `research/web-research.json`）

## 可再构建性

所有交付物均由 `07-checkpoint/gen-*.py` 从 `01-dag-data/` 数据生成（依赖仅 Python 标准库 + 本地 vendor）：

```bash
cd 07-checkpoint
python3 gen-nodes.py        # 38 节点页
python3 gen-groups.py       # 16 组页
python3 gen-views.py        # 阶段 / 学习路径 / 跨体系对照视图
python3 gen-interactive.py  # 交互图（cytoscape DATA 注入）
python3 gen-index.py        # 根入口
python3 gen-md.py           # AI 友好 MD 镜像
```

修改 `01-dag-data/` 后重跑即可全量更新。

## 许可

- 内容：基于 [12factor.net](https://12factor.net/)（CC BY-SA 4.0 同类）与 [12-factor-agents](https://github.com/humanlayer/12-factor-agents)（CC BY-SA 4.0）整理
- 代码：MIT（见各生成脚本）
