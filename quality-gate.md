# 质量门控报告

日期：2026-08-23｜项目：12 Factor 方法论合并知识图谱（`0823-12factor-methodology`）

## 门控项与结果

| # | 门控项 | 判据 | 结果 |
|---|--------|------|:---:|
| 1 | 文件覆盖 | 38 节点页 / 16 组页 / 4 视图 / 交互图 / 根索引全部存在 | ✅ |
| 2 | HTML 结构 | 61 个 HTML：UTF-8 无 U+FFFD、div 开闭平衡 | ✅ |
| 3 | 断链 | 内部相对链接全部可达（0 断链） | ✅ |
| 4 | DAG 无环 | Kahn 拓扑校验：38/38 节点全排序 | ✅ |
| 5 | 四向覆盖 | DAG ↔ 02-node-pages ↔ 06-md/nodes ↔ node-content = 38 全一致 | ✅ |
| 6 | 内容抽查 | tool 节点含真实源码细节、bridge 节点三栏对比完整、跨体系对照 12 行无空 | ✅ |
| 7 | 交互图一致性 | 04-interactive DATA = 38 节点 / 61 边 / 16 组，与 DAG 完全一致 | ✅ |

## 实测明细

### 1. 文件覆盖
- `02-node-pages/`：38 个节点页（12 App 原则 + 12 Agent 原则 + 10 桥接主题 + 4 工具）
- `03-groups/`：16 个组页（GA / GB / GT01-GT10 / GX1-GX3 / G-TOOLS）+ `index.html` 组总索引
- `05-views/`：index.html（总览）+ 02-stage.html（三档阶段）+ 03-learning-path.html（三路径）+ 04-cross-mapping.html（跨体系对照）
- `04-interactive/index.html` + vendor/（cytoscape + dagre）
- `06-md/`：00-index / 01-groups / 02-stage / 03-learning-path + nodes/（38 个节点 MD）
- 根入口 `index.html`

### 2-3. HTML 结构与断链
- 扫描 61 个 HTML：无 UTF-8 替换字符，div 开闭平衡，内部相对链接 0 断链。

### 4. DAG 无环
- prerequisite 边 40 条，Kahn 算法输出 38 节点全拓扑序，无环。

### 5. 四向覆盖
- DAG nodes（38）== node-pages（38）== MD nodes（38）== node-content（38），id 全对齐。

### 6. 内容抽查
- `tool-create-agent` 页含 template 六模块（cli/agent/state/server/a2h/index）+ BAML 工具定义 + ThreadStore 可替换接口等真实细节。
- `t-stateless` 页三栏对比：App share-nothing 进程 vs Agent 可序列化线程 vs 物理/逻辑外置差异。
- `04-cross-mapping.html` 12 行 App↔Agent 对照，差异根源无空。

### 7. 交互图一致性
- `04-interactive/index.html` 内联 DATA：38 节点 / 61 边 / 16 组，与 methodology-dag.json 完全一致；含组级视图、点击下钻、桥接高亮模式。

## 结论

七项门控全部通过。生成链路（07-checkpoint/gen-*.py）可重复运行：数据在 `01-dag-data/`，页面由脚本生成，改数据后重跑即可。
