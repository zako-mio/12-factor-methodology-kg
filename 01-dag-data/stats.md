# DAG 数据统计

来源：`01-dag-data/methodology-dag.json`（生成时间 2026-08-23）

## 总览

| 指标 | 值 |
|---|---|
| 版本 | 1.0.0 |
| 节点总数 | 38 |
| 边总数 | 61 |
| 分组总数 | 16 |
| 学习阶段 | 3 档（basic / intermediate / advanced） |
| 边类型 | prerequisite / variant / combination / cooccurrence / dependency（5 类） |
| DAG 合法性 | ✅ Kahn 拓扑校验无环（38/38 全排序） |

## 节点构成

| 类型 | 数量 | 说明 |
|---|---|---|
| 方法原则（App） | 12 | 12 Factor App 体系 |
| 方法原则（Agent） | 12 | 12 Factor Agent 体系 |
| 桥接主题 | 10 | 跨体系共性抽象，含三栏对比 |
| 辅助工具 | 4 | create-agent / walkthroughgen / workshops / 12factor.net 站点 |

## 分组构成（16 组）

| 类别 | 分组 | 数量 |
|---|---|---|
| 来源组 | GA（App 体系）、GB（Agent 体系） | 2 |
| 主题组 | GT01-GT10（无状态/生命周期/配置/可观测/依赖/控制流/入口/规模/人机/环境） | 10 |
| 横切组 | GX1（基础与运行时）、GX2（配置与交付）、GX3（交互与运维） | 3 |
| 工具组 | G-TOOLS（辅助工具集） | 1 |

## 边构成（61 条）

| 类型 | 语义 | 数量 |
|---|---|---|
| prerequisite | 前置依赖（拓扑与环检测判据） | 40 |
| variant | 跨体系变体映射（App ↔ Agent 经主题桥接） | 7 |
| combination | 组合关系 | 8 |
| cooccurrence | 同源共现 | 2 |
| dependency | 依赖关联（含跨体系直接桥接与工具连接） | 4 |

## 拓扑说明

- prerequisite 边构成 DAG 主干：同体系内表达学习顺序，跨体系经桥接主题（App 原则 → 主题 → Agent 原则）表达"打通路径"。
- 学习路径 A/B/C 均由 prerequisite 拓扑序自动生成，不硬编码。
- variant/combination/cooccurrence/dependency 为语义关系标注，不参与环检测。
