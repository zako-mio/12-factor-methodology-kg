# Mission 报告：12 Factor 方法论合并知识图谱

- **日期**：2026-08-23
- **任务目录**：`~/opencode/archive/Mission-file/2026-08/0823-12factor-methodology/`
- **GATE**：Plan 阶段 范围=4 深度=5 操作=3 风险=1 → 13 → Deep；Build 阶段 范围=5 深度=5 操作=5 风险=2 → 17 → Deep
- **[COMPLEXITY: 15/20]**（Plan 收敛标记，Build 按 Deep 推理执行）

## 一、当时情况

用户先下载了 12 Factor App（heroku/12factor）与 12 Factor Agent（humanlayer/12-factor-agents）两个项目，随后提出：参考此前两个方法论库（0822-plugin-dag 的动态图技术、0820-algorithm-knowledge-graph 的知识图谱组织思路），将这两套 12-factor 方法论**合并为一个统一的知识图谱**（本质都是软件工程思路），并保留"AI 友好 + 人类友好"双交付结构。Plan 阶段用户补充：两库中存在的**工具类内容**（脚手架、教程生成器、工作坊等）也应设法融入图谱。

## 二、制定计划

1. **Grill-Me 需求澄清**（20 项决策收敛）：合并策略=双体系+桥接；节点粒度=原则+桥接主题；边=继承四类+依赖；分组=来源+主题+横切三层；视图=四视图+对照；阶段=三档；路径=多路径自动生成；内容=官方+联网；语言=中文为主；规模=30-40 节点；位置=新建 0823-12factor-methodology/；保留脚本链。
2. **内容采集**：3 路并行子Agent——App 12 要素官方摘录、Agent 12 条官方摘录、联网补充（中文解读/HN/桥接长文）。
3. **数据设计**：主Agent 亲写 methodology-dag.json（34 节点→后扩 38），桥接主题含三栏对比设计。
4. **生成链路**：07-checkpoint/gen-*.py 脚本化生成节点页/组页/视图/交互图/MD 镜像/根索引。
5. **工具融入**：新增 4 工具节点（create-agent/walkthroughgen/workshops/12factor.net 站点），重跑生成链。
6. **质量门控**：七项门控（覆盖/结构/断链/无环/四向覆盖/抽查/交互一致）+ 报告双版本。

## 三、执行情况

1. **需求澄清**：Grill-Me 协议逐项访谈 11 轮，收敛 20 项决策，用户确认后进入 Build。
2. **内容采集**：3 个 general 子Agent 并行成功——`research/app-12-elements.json`（12 要素）、`research/agent-12-factors.json`（12 条，警告 factor-12 原文极短）、`research/web-research.json`（11 条联网 findings）。
3. **DAG 设计**：主Agent 设计 34 节点（12 App + 12 Agent + 10 桥接主题）、16 组、53 边；Kahn 无环验证通过；修正 meta 计数（15→16 组）。
4. **节点内容**：子Agent 生成 node-content.json（34 节点五段式，bridge 含三栏），校验 34/34 一致。
5. **页面生成**：子Agent 编写 6 个生成脚本并产出全部 HTML（节点页/组页/视图/交互图/根索引），vendor 从 0820 复制；自检 56 HTML div 平衡、0 断链。
6. **工具融入**（用户补充需求）：新增 G-TOOLS 工具组 + 4 工具节点 + 10 条工具边；gen_common.py 扩展 tool 类型样式；子Agent 基于真实源码撰写 4 工具五段式内容（template 六模块/BAML/Procfile 等）；node-content 38 节点；重跑生成链全部成功。
7. **MD 镜像补齐**：发现 06-md 缺失，主Agent 亲写 gen-md.py 生成 42 文件（4 索引 + 38 节点 MD）。
8. **文案修正**：gen-index.py 3 处硬编码旧数字（15 组/34 节点）改为动态取数并加工具统计。
9. **质量门控**：独立脚本实测——61 HTML 0 错误（UTF-8/div 平衡/断链）；DAG Kahn 无环（38/38）；四向覆盖 38 全一致；交互图 DATA 与 DAG 一致（38/61/16）。

## 四、完成情况

| 交付物 | 数量 | 说明 |
|---|---|---|
| `01-dag-data/methodology-dag.json` | 38 节点/16 组/61 边 | 5 类边，DAG 无环 |
| `01-dag-data/node-content.json` | 38 节点 | 五段式内容，bridge 含三栏对比 |
| `01-dag-data/stats.md` | 1 | DAG 统计与拓扑说明 |
| `02-node-pages/` | 38 页 | 节点详情页（五段式） |
| `03-groups/` | 17 文件 | 16 组页 + 组总索引 |
| `05-views/` | 4 页 | 总览/阶段/学习路径/跨体系对照 |
| `04-interactive/` | index + vendor | cytoscape 两级下钻 + 桥接高亮 |
| `06-md/` | 42 文件 | AI 友好镜像（4 索引 + 38 节点 MD） |
| `07-checkpoint/` | 7 个 py | 可重复生成脚本链 |
| `research/` | 3 文件 | 内容来源与桥接设计依据 |
| `quality-gate.md` | 1 | 七项门控全部通过 |
| `report.md / report.html` | 2 | 本报告双版本 |

- 根入口 `index.html`：统计 38 节点/16 组/61 边，12+12+10+4 构成，快速开始指引。

## 五、反思 / 分析 / 建议

1. **用户中途补充"工具融入"需求**验证了脚本链价值：数据更新 → 重跑 gen-*.py 即全量再生成（约 10 秒），无需手改任何页面。这正是保留 07-checkpoint 的意义。
2. **硬编码文案陷阱**：gen-index.py 中 3 处"15 组/34 节点"硬编码未随数据变化自动更新，靠人工 grep 才发现。教训：生成脚本中的统计类文案应一律从 DAG meta 动态取数，不写死数字（已修复）。
3. **MD 镜像曾被遗漏**：子Agent 生成的 6 个脚本未覆盖 06-md（设计决策 12 要求）。主Agent 补写 gen-md.py。教训：委派 prompt 应显式列出全部交付物清单并逐一核对，不能默认子Agent 全覆盖。
4. **工具节点是加分项**：create-12-factor-agent 模板、walkthroughgen、工作坊材料让图谱从"纯理论原则"升级为"可实操方法论"，12factor.net 站点作为 App 原则参考实现补齐了 App 侧工具视角。
5. **桥接主题设计是灵魂**：10 个主题经 prerequisite（App→主题→Agent）构成"打通路径"，variant 标注语义对应——这是两套方法论合并的价值核心，也是后续扩展（如新增第 13 因子）的挂载点。
