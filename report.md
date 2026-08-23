# Mission 报告：12 Factor 方法论合并知识图谱

- **日期**：2026-08-23
- **任务目录**：`~/opencode/archive/Mission-file/2026-08/0823-12factor-methodology/`
- **GATE**：Plan 阶段 范围=4 深度=5 操作=3 风险=1 → 13 → Deep；Build 阶段 范围=5 深度=5 操作=5 风险=2 → 17 → Deep；后续 GitHub 上传 范围=1 深度=2 操作=3 风险=3 → 9 → Daily；内容扩充 范围=5 深度=5 操作=5 风险=3 → 18 → Deep
- **[COMPLEXITY: 15/20]**（Plan 收敛标记，Build 按 Deep 推理执行）
- **GitHub**：https://github.com/zako-mio/12-factor-methodology-kg（公开）｜ Pages：https://zako-mio.github.io/12-factor-methodology-kg/

## 一、当时情况

用户先下载了 12 Factor App（heroku/12factor）与 12 Factor Agent（humanlayer/12-factor-agents）两个项目，随后提出：参考此前两个方法论库（0822-plugin-dag 的动态图技术、0820-algorithm-knowledge-graph 的知识图谱组织思路），将这两套 12-factor 方法论**合并为一个统一的知识图谱**（本质都是软件工程思路），并保留"AI 友好 + 人类友好"双交付结构。Plan 阶段用户补充：两库中存在的**工具类内容**（脚手架、教程生成器、工作坊等）也应设法融入图谱。

**后续期望演进**（Build 后两轮用户反馈）：
1. 用户要求**上传 GitHub**（公开仓库 + 在线 Pages 浏览），并补充 LICENSE、Actions 自动重建、仓库描述与主题标签。
2. 用户指出**知识图谱内容量太少**（每节点页子 HTML 应详细准确解释），困惑"原库那么大（109M）、图谱这么小（1.7M）"。
3. 用户升级期望：图谱不只是方法论，还要**融入两个原库的工具源码作为实践参考**，实现**有机重构索引**，并让 **AI 友好侧不仅读方法论、还能读例子和按索引调用工具**。

## 二、制定计划

1. **Grill-Me 需求澄清**（20 项决策收敛）：合并策略=双体系+桥接；节点粒度=原则+桥接主题；边=继承四类+依赖；分组=来源+主题+横切三层；视图=四视图+对照；阶段=三档；路径=多路径自动生成；内容=官方+联网；语言=中文为主；规模=30-40 节点；位置=新建 0823-12factor-methodology/；保留脚本链。
2. **内容采集**：3 路并行子Agent——App 12 要素官方摘录、Agent 12 条官方摘录、联网补充（中文解读/HN/桥接长文）。
3. **数据设计**：主Agent 亲写 methodology-dag.json（34 节点→后扩 38），桥接主题含三栏对比设计。
4. **生成链路**：07-checkpoint/gen-*.py 脚本化生成节点页/组页/视图/交互图/MD 镜像/根索引。
5. **工具融入**：新增 4 工具节点（create-agent/walkthroughgen/workshops/12factor.net 站点），重跑生成链。
6. **质量门控**：七项门控（覆盖/结构/断链/无环/四向覆盖/抽查/交互一致）+ 报告双版本。

**后续阶段计划**（用户反馈驱动的增量）：
7. **GitHub 上传**：公开仓库 + Pages 在线浏览 + README/LICENSE/.gitignore/Actions 自动重建 + 仓库描述与主题标签。
8. **构建可复现性保障**：Actions 环境与本地产物一致性（拓扑排序稳定性修复，防重建循环）。
9. **内容深度扩充**：38 节点从摘要级（17KB）扩充为原文级（105KB），每节点 1500-3000 字。
10. **源码资产融入**：精选复制两原库源码到 08-source/（454 文件），节点页 + MD 双索引。

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

**后续阶段执行**：
10. **GitHub 上传**：`gh repo create` 创建公开仓库 `zako-mio/12-factor-methodology-kg`；配置 Pages（master 分支 root）；补 README.md/.gitignore/.nojekyll/LICENSE（MIT）；设置仓库描述与 7 个主题标签；GitHub Actions 自动重建 workflow（数据/脚本变更自动重建并提交）。
11. **workflow scope 授权**：推送 `.github/workflows/rebuild.yml` 被 GitHub 拒绝（OAuth token 缺 `workflow` scope）。用户执行 `gh auth refresh --scopes workflow` 失败（浏览器访问 GitHub 需代理）→ 走代理后授权成功 → 推送通过。
12. **构建可复现性修复**：Actions 重建产生"重新生成交付物"提交（拓扑排序不稳定——gen-md.py 独立 topo 实现用 set 无序遍历，不同 Python 环境顺序不同）。修复为字典序稳定版；闭环验证：修复后 Actions 重建不再产生新提交（产物一致）。
13. **12 Factor 自我审查**：用户要求用刚学到的 12 Factor 原则审查图谱库本身。发现并修复：①无 .git（补 git init+提交）；②gen-interactive.py 硬依赖外部 0820 vendor（改库内自包含优先）；③gen-md.py 硬编码绝对路径（改相对定位）。可再构建性实测：数据+脚本在 /tmp 全新重建 61 HTML+42 MD 零失败。
14. **内容深度扩充**：用户指出内容量太少。3 路并行子Agent 基于完整原文扩充——expansion-app.json（12 节点 20,960 字）、expansion-agent.json（12 节点 31,264 字）、expansion-bridge.json（10 桥接+4 工具+64 项源码索引 39,382 字）。合并后 node-content 17KB → 105KB。
15. **源码资产融入**：精选复制两原库到 08-source/（agent-content 原文/packages 脚手架/workshops 工作坊/app-content-en 原文/app-deploy 部署参考），排除翻译/图片/博客/git 历史（109M → 2.3M 精选）。选择"索引引用+精选复制"方案（全量复制 100M+ 无意义：80% 是翻译/图片低价值内容）。
16. **双索引实现**：gen-nodes.py 增加"实践资源"区块（节点页链接 08-source 源码可点击查看）；gen-md.py 增加"源码索引"段（06-md AI 按路径读取工具）。修复路径双写 bug（08-source/08-source/）与 source_refs 字符串/dict 格式不一致（规范化 113 条）。
17. **README/index 更新**：补充 08-source 目录说明、内容深度与源码资产说明、方法说明卡片。
18. **最终推送与闭环**：提交 `2eeccd0` 推送 → Actions 自动重建 success → 无多余重建提交（防循环闭环）→ Pages 在线全部 200（含 08-source 源码文件）。

## 四、完成情况

| 交付物 | 数量 | 说明 |
|---|---|---|
| `01-dag-data/methodology-dag.json` | 38 节点/16 组/61 边 | 5 类边，DAG 无环 |
| `01-dag-data/node-content.json` | 38 节点 | **深度内容 105KB**（扩充后），bridge 含三栏对比，含 source_refs |
| `01-dag-data/expansion-*.json` | 3 文件 | 三路扩充中间产物（app/agent/bridge+工具+源码索引） |
| `01-dag-data/source-inventory.json` | 1 | 64 项源码资产索引映射 |
| `01-dag-data/stats.md` | 1 | DAG 统计与拓扑说明 |
| `02-node-pages/` | 38 页 | 节点详情页（**13-16KB/页**，含实践资源区块） |
| `03-groups/` | 17 文件 | 16 组页 + 组总索引 |
| `05-views/` | 4 页 | 总览/阶段/学习路径/跨体系对照 |
| `04-interactive/` | index + vendor | cytoscape 两级下钻 + 桥接高亮 |
| `06-md/` | 42 文件 | AI 友好镜像（含源码索引段） |
| `07-checkpoint/` | 7 个 py | 可重复生成脚本链（含 Actions 自动重建） |
| **`08-source/`** | **454 文件 / 3.9MB** | **精选源码资产**（原文/脚手架/工作坊/部署参考） |
| `.github/workflows/rebuild.yml` | 1 | GitHub Actions 自动重建 |
| `research/` | 3 文件 | 内容来源与桥接设计依据 |
| `README.md / LICENSE / .gitignore / .nojekyll` | 4 | GitHub 发布配套 |
| `quality-gate.md` | 1 | 七项门控全部通过 |
| `report.md / report.html` | 2 | 本报告双版本 |

- 根入口 `index.html`：统计 38 节点/16 组/61 边，12+12+10+4 构成，快速开始指引，方法说明含内容深度/源码资产/AI 双索引卡片。
- **GitHub 仓库**：https://github.com/zako-mio/12-factor-methodology-kg（公开，2 次发布提交：`0a054ac` 完整交付 → `2eeccd0` 内容扩充+源码融入）
- **GitHub Pages**：https://zako-mio.github.io/12-factor-methodology-kg/（在线可浏览，含 08-source 源码）
- **git 历史**：6 次提交（feat 完整交付 / docs 发布准备 / chore LICENSE+Actions / fix 拓扑稳定 / feat 内容扩充+源码融入 / chore 重建）

## 五、反思 / 分析 / 建议

1. **用户中途补充"工具融入"需求**验证了脚本链价值：数据更新 → 重跑 gen-*.py 即全量再生成（约 10 秒），无需手改任何页面。这正是保留 07-checkpoint 的意义。
2. **硬编码文案陷阱**：gen-index.py 中 3 处"15 组/34 节点"硬编码未随数据变化自动更新，靠人工 grep 才发现。教训：生成脚本中的统计类文案应一律从 DAG meta 动态取数，不写死数字（已修复）。
3. **MD 镜像曾被遗漏**：子Agent 生成的 6 个脚本未覆盖 06-md（设计决策 12 要求）。主Agent 补写 gen-md.py。教训：委派 prompt 应显式列出全部交付物清单并逐一核对，不能默认子Agent 全覆盖。
4. **工具节点是加分项**：create-12-factor-agent 模板、walkthroughgen、工作坊材料让图谱从"纯理论原则"升级为"可实操方法论"，12factor.net 站点作为 App 原则参考实现补齐了 App 侧工具视角。
5. **桥接主题设计是灵魂**：10 个主题经 prerequisite（App→主题→Agent）构成"打通路径"，variant 标注语义对应——这是两套方法论合并的价值核心，也是后续扩展（如新增第 13 因子）的挂载点。

**后续阶段反思**：
6. **用方法论审查产物本身是高效的质量手段**：用户要求"应用 12 Factor 原则检查图谱库"——立刻抓出 3 个常规验证发现不了的缺陷（无 .git、gen-interactive 硬依赖外部 vendor、gen-md 硬编码路径）。知识库也是"应用"，可再构建性（V）与依赖显式化（II）的审视视角可直接复用。
7. **构建可复现性必须防"环境漂移"**：Actions 重建产生额外提交的根因是 gen-md.py 独立 topo 实现用 set 无序遍历——同一份数据在不同 Python 环境生成不同顺序。教训：①生成脚本应统一使用排序稳定的算法（字典序拓扑）；②"重建后 diff 为零"是验证可复现性的黄金标准，也天然防 Actions 重建循环。
8. **委派内容的"深度预期"要显式设定**：第一轮子Agent 摘录产出 17KB 摘要级内容（用户不满），因为 prompt 只说"提取摘要"未要求详细度。第二轮明确"每节点 1500-3000 字 + 忠实原文 + 保留技术细节"，产出 105KB。教训：内容类委派的 prompt 必须显式给出字数下限与忠实度要求。
9. **精选复制 vs 全量复制的决策需量化论证**：全量复制 109M（80% 是翻译/图片/博客低价值内容）vs 精选复制 2.3M（100% 方法论+工具核心）——用"对学习实践的价值"逐类分析而非直觉选择，最终用户认可精选方案。
10. **GitHub workflow scope 的坑**：首次推送含 `.github/workflows/` 会被 GitHub 拒绝（OAuth token 需 `workflow` scope）；且授权走代理才能成功（境外访问）。这是发布配置类任务的常见阻塞点，应提前告知用户。
11. **用户期望的动态演进**：从"合并方法论"→"上传分享"→"内容要详细准确"→"融入源码资产+AI 可调用索引"——知识图谱定位从"方法论摘要库"升级为"方法论+实践+工具索引"三合一体系。脚本链+数据驱动架构使每次演进都是增量（改数据→重跑→推送），而非推翻重来，这是本任务最大的架构红利。
