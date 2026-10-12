#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成根入口：index.html（统计 + 导航 + 快速开始，引用 05-views/04-cross-mapping.html 等）。"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_common import ROOT, TITLE, SUBTITLE, load_all, esc, BASE_CSS

OUT = os.path.join(ROOT, 'index.html')

# ------------------------------------------------------------------ 令牌单源
# ★ 本页令牌块**不再自持字面值**：直接取 gen_common.BASE_CSS 的首行（该行即 `:root{...}` 块）。
#   BASE_CSS 的令牌块由 pipeline 的派生器从站点值件写入，故本站的令牌字面值只有
#   gen_common.BASE_CSS（default 族）与 gen-interactive.CSS（04-interactive 族）两处来源，
#   本文件不再持有第三份。不变量（BASE_CSS 首个非空行即 :root 块）由仓内 gate_tokens.py
#   的 G9 判据看住（见 gate-manifest.json）。
ROOT_TOKENS = BASE_CSS.strip().split('\n', 1)[0]


def main():
    dag, content, by_id, c_by_id, group_by_id = load_all()
    stats = ('<div class="stat"><b>%d</b><span>方法节点</span></div>'
             '<div class="stat"><b>%d</b><span>分组</span></div>'
             '<div class="stat"><b>%d</b><span>关系边</span></div>'
             '<div class="stat"><b>3</b><span>学习阶段</span></div>'
             '<div class="stat"><b>12+12+10+4</b><span>App+Agent+桥接+工具</span></div>'
             % (len(dag['nodes']), len(dag['groups']), len(dag['edges'])))

    src_desc = []
    for src, label in (('app', '12 Factor App'), ('agent', '12 Factor Agent'), ('bridge', '桥接主题'), ('tool', '辅助工具')):
        cnt = sum(1 for n in dag['nodes'] if n['src'] == src)
        src_desc.append('%d 个 %s' % (cnt, label))
    quick = ('<ol class="steps">'
             '<li><b>先总览</b>：打开交互 DAG 总览，看 %d 组 %d 节点在拓扑中的分布，理解 App 与 Agent 的桥接关系。</li>'
             '<li><b>点组下钻</b>：点击组节点展开组内 DAG，或从分组目录选一组进入组页。</li>'
             '<li><b>选路径</b>：三条学习路径分别面向传统工程 / Agent 工程 / 打通双体系。</li>'
             '<li><b>对照</b>：跨体系对照表逐条比对 App 与 Agent 的 12 条方法原则与差异根源。</li>'
             '<li><b>读节点</b>：读 what / why / how / 案例 / 反模式，桥接节点含两体系三栏对比。</li>'
             '</ol>' % (len(dag['groups']), len(dag['nodes'])))

    cards = (
        '<div class="card"><h3>交互 DAG 总览</h3><p>组级视图 + 点击下钻组内 DAG + 桥接高亮模式，cytoscape 渲染。</p>'
        '<p><a href="04-interactive/index.html">打开交互总览</a></p></div>'
        '<div class="card"><h3>分组目录</h3><p>%d 个组：来源组（App/Agent）、主题组（桥接）、横切组、工具组四色区分。</p>'
        '<p><a href="03-groups/index.html">打开分组目录</a></p></div>'
        '<div class="card"><h3>阶段视图</h3><p>按 basic → intermediate → advanced 三档浏览全部 %d 个节点。</p>'
        '<p><a href="05-views/02-stage.html">按阶段浏览</a></p></div>'
        '<div class="card"><h3>学习路径</h3><p>传统工程入门 / Agent 工程入门 / 打通三条自动生成路径。</p>'
        '<p><a href="05-views/03-learning-path.html">查看三条路径</a></p></div>'
        '<div class="card"><h3>跨体系对照</h3><p>App 12 条 ↔ Agent 12 条逐条对照，含桥接主题与差异根源。</p>'
        '<p><a href="05-views/04-cross-mapping.html">打开对照表</a></p></div>'
        % (len(dag['groups']), len(dag['nodes']))
    )

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — 总览入口</title>
<style>
  {root_tokens}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,'PingFang SC','Microsoft YaHei',sans-serif; line-height:1.7; }}
  header {{ background:var(--panel); border-bottom:1px solid var(--border); padding:28px 32px; }}
  header h1 {{ font-size:24px; margin-bottom:6px; }}
  header p {{ color:var(--dim); font-size:14px; max-width:900px; }}
  main {{ padding:28px 32px; max-width:1100px; margin:0 auto; }}
  h2 {{ font-size:18px; margin:28px 0 14px; color:#cfd6e4; border-bottom:1px solid var(--border); padding-bottom:8px; }}
  .cards {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:14px; margin:12px 0; }}
  .card {{ background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:16px 18px; }}
  .card h3 {{ font-size:15px; color:var(--accent); margin-bottom:6px; }}
  .card a {{ color:var(--accent); text-decoration:none; }}
  .card a:hover {{ text-decoration:underline; }}
  .card p {{ font-size:13px; color:var(--dim); }}
  .stat {{ display:inline-block; background:#1d2a3f; border:1px solid #2b3d5f; border-radius:8px; padding:10px 16px; margin:4px; text-align:center; }}
  .stat b {{ display:block; font-size:22px; color:#fff; }}
  .stat span {{ font-size:12px; color:var(--dim); }}
  .links a {{ display:inline-block; margin:4px 8px 4px 0; padding:6px 14px; background:var(--panel); border:1px solid var(--border); border-radius:8px; color:var(--accent); text-decoration:none; font-size:13px; }}
  .links a:hover {{ border-color:var(--accent); }}
  ol.steps {{ padding-left:22px; margin:10px 0; }}
  ol.steps li {{ margin:6px 0; font-size:14px; color:#cfd6e4; }}
  ol.steps b {{ color:#fff; }}
</style>
</head>
<body>
<header>
  <h1>{title}</h1>
  <p>{subtitle}。{src_desc}，关系边分 prerequisite / variant / combination / cooccurrence / dependency 五类，DAG 无环。每个桥接节点含 App 侧 | Agent 侧 | 差异根源三栏对比。</p>
</header>
<main>
  <h2>核心统计</h2>
  <div>{stats}</div>

  <h2>入口导航</h2>
  <div class="cards">{cards}</div>

  <h2>快速开始</h2>
  {quick}

  <h2>方法说明</h2>
  <div class="cards">
    <div class="card"><h3>双体系合并</h3><p>传统 12 Factor App 与新兴 12 Factor Agent 在同一图谱中桥接，10 个桥接主题承接双体系对照。</p></div>
    <div class="card"><h3>三级下钻</h3><p>根入口 → 组页（03-groups/*.html）→ 节点页（02-node-pages/*.html）。交互图支持组→节点直接下钻。</p></div>
    <div class="card"><h3>五类关系边</h3><p>prerequisite（前置）/ variant（变体）/ combination（组合）/ cooccurrence（共现）/ dependency（依赖关联）。</p></div>
    <div class="card"><h3>自动路径</h3><p>学习路径由 prerequisite 边做拓扑排序自动生成，不硬编码。</p></div>
    <div class="card"><h3>内容深度</h3><p>每节点 1500-3000 字，基于两库完整原文撰写，含真实技术细节与反模式详解。</p></div>
    <div class="card"><h3>源码资产</h3><p>08-source/ 精选两库源码与原文（脚手架/工作坊/部署参考），节点页实践资源区块可直达查看。</p></div>
    <div class="card"><h3>AI 双索引</h3><p>06-md/ 节点 MD 含源码索引段，AI 可按路径读取方法论 + 例子 + 调用对应工具源码。</p></div>
  </div>
</main>
</body>
</html>
""".format(title=esc(TITLE), subtitle=esc(SUBTITLE), src_desc='，'.join(src_desc),
           stats=stats, cards=cards, quick=quick, root_tokens=ROOT_TOKENS)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html)
    print('root index written')


if __name__ == '__main__':
    main()
