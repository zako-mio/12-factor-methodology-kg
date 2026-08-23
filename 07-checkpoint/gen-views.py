#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 05-views/ 下的 4 个视图页：
  index.html              总览（统计卡+导航）
  02-stage.html           三档阶段视图（basic/intermediate/advanced 分组列出节点）
  03-learning-path.html   三条自动生成路径
  04-cross-mapping.html   跨体系对照表（App 12 条 | 对应主题 | Agent 12 条 | 关系类型 | 差异根源）
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_common import (ROOT, TITLE, SUBTITLE, load_all, esc, build_indexes,
                        topo_sort, stage_badge, src_badge, BASE_CSS,
                        STAGE_STYLE, SRC_STYLE, EDGE_STYLE, KIND_ORDER)

VIEWS_DIR = os.path.join(ROOT, '05-views')


def views_header(title, subtitle):
    return ('<header><h1>%s</h1><p>%s</p></header>'
            '<main><div class="back"><a href="index.html">&larr; 返回视图入口</a></div>'
            % (esc(title), esc(subtitle)))


def views_footer(src_name):
    return ('</main><footer>%s · 由 07-checkpoint/gen-views.py 生成 · '
            '数据源 01-dag-data/methodology-dag.json + node-content.json</footer>'
            % esc(TITLE))


def stage_index_html(dag, by_id, group_by_id):
    stats = ('<div class="stat"><b>%d</b><span>节点</span></div>'
             '<div class="stat"><b>%d</b><span>组</span></div>'
             '<div class="stat"><b>%d</b><span>关系边</span></div>'
             '<div class="stat"><b>3</b><span>学习阶段</span></div>'
             '<div class="stat"><b>12+12+10</b><span>App+Agent+桥接</span></div>'
             % (len(dag['nodes']), len(dag['groups']), len(dag['edges'])))
    cards = ('<div class="card"><h3>阶段视图</h3><p>按 basic → intermediate → advanced 三档浏览全部节点。</p>'
             '<a class="go" href="02-stage.html">按阶段浏览</a></div>'
             '<div class="card"><h3>学习路径</h3><p>传统工程入门 / Agent 工程入门 / 打通三条自动生成路径。</p>'
             '<a class="go" href="03-learning-path.html">查看三条路径</a></div>'
             '<div class="card"><h3>跨体系对照</h3><p>App 12 条 ↔ Agent 12 条，含桥接主题与差异根源。</p>'
             '<a class="go" href="04-cross-mapping.html">跨体系对照表</a></div>'
             '<div class="card"><h3>交互 DAG 总览</h3><p>组级视图 + 点击下钻 + 桥接高亮模式。</p>'
             '<a class="go" href="../04-interactive/index.html">打开交互总览</a></div>')
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>视图入口 · {title}</title>
<style>
{extra_css}
.back a{{color:var(--accent);text-decoration:none;font-size:14px;}}
.stat{{display:inline-block;background:#1d2a3f;border:1px solid #2b3d5f;border-radius:8px;padding:10px 16px;margin:4px;text-align:center;}}
.stat b{{display:block;font-size:22px;color:#fff;}}
.stat span{{font-size:12px;color:var(--dim);}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;margin:12px 0;}}
.card{{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:18px;}}
.card h3{{font-size:16px;color:var(--accent);margin:0 0 8px;}}
.card p{{font-size:13px;color:var(--dim);margin-bottom:12px;}}
.card .go{{display:inline-block;background:#1d2a3f;border:1px solid #2b3d5f;border-radius:8px;padding:6px 14px;color:#fff;font-size:13px;}}
.card .go:hover{{border-color:var(--accent);}}
</style>
</head>
<body>
{header}
{stats_sec}
<h2>视图入口</h2>
<div class="cards">{cards}</div>
<h2>快速开始</h2>
<ul style="padding-left:22px;font-size:14px;color:#cfd6e4;">
<li style="margin:6px 0"><b>总览</b>：交互 DAG 总览看 15 组、34 节点在拓扑中的分布。</li>
<li style="margin:6px 0"><b>按阶段</b>：阶段视图按 basic → intermediate → advanced 逐档推进。</li>
<li style="margin:6px 0"><b>按路径</b>：三条学习路径分别面向传统工程 / Agent 工程 / 打通双体系。</li>
<li style="margin:6px 0"><b>对照</b>：跨体系对照表逐条比对 App 与 Agent 的 12 条方法原则。</li>
</ul>
{footer}
</body>
</html>
""".format(title=esc(TITLE), extra_css=BASE_CSS, header=views_header('视图入口', SUBTITLE),
           stats_sec='<h2>核心统计</h2><div>%s</div>' % stats, cards=cards,
           footer=views_footer('views-index'))
    return html


def stage_html(dag, by_id, group_by_id):
    stages = ['basic', 'intermediate', 'advanced']
    nav = '<div class="layer-nav">' + ''.join(
        '<a href="#layer-%d">%s（%d）</a>' % (i, STAGE_STYLE[s]['label'],
                                              sum(1 for n in dag['nodes'] if n['stage'] == s))
        for i, s in enumerate(stages)) + '</div>'
    secs = []
    for i, s in enumerate(stages):
        st = STAGE_STYLE[s]
        nodes = [n for n in dag['nodes'] if n['stage'] == s]
        nodes.sort(key=lambda n: (n['group'], n['id']))
        rows = []
        for n in nodes:
            gname = group_by_id[n['group']]['name']
            brief = n['definition']
            rows.append(
                '<div class="row"><span class="nm"><a href="../02-node-pages/%s.html">%s</a></span>'
                '%s<span class="badge b-grp">%s · %s</span>'
                '<span class="brief">%s</span></div>'
                % (esc(n['id']), esc(n['name']), src_badge(n['src']),
                   esc(n['group']), esc(gname), esc(brief)))
        secs.append(
            '<div class="sec-head" id="layer-%d"><h2>Layer %d · %s</h2><span>%d 个节点</span></div>'
            '<div class="sec-card">%s</div>' % (i, i, st['label'], len(nodes), ''.join(rows)))
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>阶段视图 · {title}</title>
<style>
{extra_css}
.back a{{color:var(--accent);text-decoration:none;font-size:14px;}}
.row{{display:flex;align-items:baseline;gap:10px;padding:9px 6px;border-bottom:1px solid var(--border);flex-wrap:wrap;}}
.row:hover{{background:rgba(79,140,255,.06);}}
.row .nm{{min-width:200px;flex:0 0 auto;font-size:14px;font-weight:600;}}
.row .nm a{{color:#dbe4f2;}}
.row .brief{{flex:1 1 320px;font-size:12.5px;color:var(--dim);min-width:240px;}}
.badge.b-grp{{background:#1d2a3f;color:#7fb0ff;border-color:#2b3d5f;}}
.sec-head{{display:flex;align-items:baseline;gap:10px;margin:34px 0 8px;border-bottom:1px solid var(--border);padding-bottom:8px;}}
.sec-head h2{{margin:0;border:none;padding:0;}}
.sec-head span{{color:var(--dim);font-size:13px;}}
.sec-card{{background:var(--panel);border:1px solid var(--border);border-left-width:4px;border-radius:10px;padding:10px 18px;margin:12px 0;}}
.layer-nav{{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 4px;}}
.layer-nav a{{display:inline-block;background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:4px 12px;font-size:13px;color:#b8c2d4;}}
.layer-nav a:hover{{border-color:var(--accent);color:#fff;}}
</style>
</head>
<body>
{header}
<p class="dim" style="margin:6px 0 10px">分层: basic(基础) → intermediate(进阶) → advanced(高级)。层内按组排列。</p>
{nav}
{secs}
{footer}
</body>
</html>
""".format(title=esc(TITLE), extra_css=BASE_CSS,
           header=views_header('阶段视图', '按 basic → intermediate → advanced 三档列出全部 34 个节点，层内按组排列。'),
           nav=nav, secs='\n'.join(secs), footer=views_footer('stage'))
    return html


def build_path(app_ids, bridge_ids, agent_ids, edges):
    """构建三条路径：
       A 传统工程入门 = app 体系 prerequisite 拓扑序
       B Agent 工程入门 = ag 体系 prerequisite 拓扑序
       C 打通 = App → 桥接主题 → Agent 拓扑序（全 prerequisite 子图）
    """
    def only(nodes, types=('prerequisite',)):
        idset = set(nodes)
        es = [e for e in edges if e['type'] in types and e['from'] in idset and e['to'] in idset]
        return topo_sort(nodes, es)
    path_a = only(app_ids)
    path_b = only(agent_ids)
    path_c_ids = app_ids + bridge_ids + agent_ids
    path_c = only(path_c_ids)
    return path_a, path_b, path_c


def path_html(dag, by_id, group_by_id, edges):
    app_ids = [n['id'] for n in dag['nodes'] if n['src'] == 'app']
    agent_ids = [n['id'] for n in dag['nodes'] if n['src'] == 'agent']
    bridge_ids = [n['id'] for n in dag['nodes'] if n['src'] == 'bridge']
    pa, pb, pc = build_path(app_ids, bridge_ids, agent_ids, edges)

    def seq_html(nids):
        return ' &rarr; '.join(
            '<a href="../02-node-pages/%s.html">%s</a>' % (esc(nid), esc(by_id[nid]['name']))
            for nid in nids)

    paths = [
        ('A · 传统工程入门', 'app 体系 prerequisite 拓扑序（12 条）', pa),
        ('B · Agent 工程入门', 'ag 体系 prerequisite 拓扑序（12 条）', pb),
        ('C · 打通', 'App → 桥接主题 → Agent 全 prerequisite 拓扑序（34 条）', pc),
    ]
    secs = []
    for i, (title, desc, nids) in enumerate(paths, 1):
        secs.append(
            '<div class="sec-head" id="path-%d"><h2>路径 %s</h2><span>%d 个节点 · %s</span></div>'
            '<div class="pathbox"><div class="path-label">推荐顺序</div>'
            '<div class="path-seq">%s</div></div>'
            % (i, title, len(nids), desc, seq_html(nids)))
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>学习路径 · {title}</title>
<style>
{extra_css}
.back a{{color:var(--accent);text-decoration:none;font-size:14px;}}
.pathbox{{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:12px 16px;margin:10px 0;}}
.path-label{{font-size:12px;color:var(--dim);margin-bottom:8px;}}
.path-seq{{display:flex;flex-wrap:wrap;gap:4px 0;font-size:13px;}}
.path-seq a{{display:inline-block;background:#16273f;border:1px solid #2b3d5f;border-radius:6px;padding:2px 8px;color:#7fb0ff;text-decoration:none;margin:2px;}}
.path-seq a:hover{{background:#2b3d5f;}}
.sec-head{{display:flex;align-items:baseline;gap:10px;margin:34px 0 8px;border-bottom:1px solid var(--border);padding-bottom:8px;}}
.sec-head h2{{margin:0;border:none;padding:0;}}
.sec-head span{{color:var(--dim);font-size:13px;}}
</style>
</head>
<body>
{header}
<p class="dim" style="margin:6px 0 10px">三条路径均由 prerequisite 边做拓扑排序自动生成。</p>
{secs}
{footer}
</body>
</html>
""".format(title=esc(TITLE), extra_css=BASE_CSS,
           header=views_header('学习路径', '传统工程入门 / Agent 工程入门 / 打通双体系三条自动生成路径。'),
           secs='\n'.join(secs), footer=views_footer('learning-path'))
    return html


def cross_mapping_html(dag, by_id, c_by_id, edges):
    """跨体系对照表：App 12 条 | 对应主题 | Agent 12 条 | 关系类型 | 差异根源

    以 12 个 app 节点为行主序，逐一匹配 variant/dependency 边到 agent 节点；
    主题来自桥接节点（app→t→agent 路径）。差异根源取自对应桥接节点 difference。
    """
    app_nodes = [n for n in dag['nodes'] if n['src'] == 'app']
    app_nodes.sort(key=lambda n: n['id'])
    agent_by_id = {n['id']: n for n in dag['nodes'] if n['src'] == 'agent'}

    rows = []
    for a in app_nodes:
        # 直接 variant/dependency 边：app -> agent
        rel_agent = None
        rel_type = None
        rel_label = ''
        for e in edges:
            if e['from'] == a['id'] and e['to'] in agent_by_id and e['type'] in ('variant', 'dependency'):
                rel_agent = agent_by_id[e['to']]
                rel_type = e['type']
                rel_label = e['label']
                break
        # 主题：找 app -> bridge 的 prerequisite 边，桥接节点名
        topic = None
        for e in edges:
            if e['from'] == a['id'] and by_id[e['to']]['src'] == 'bridge' and e['type'] == 'prerequisite':
                topic = by_id[e['to']]
                break
        # 若无直接 variant/dependency 边，尝试经桥接的二跳路径 app -> bridge -> agent（prerequisite）
        via_bridge = False
        if rel_agent is None and topic:
            for e in edges:
                if e['from'] == topic['id'] and e['to'] in agent_by_id and e['type'] == 'prerequisite':
                    rel_agent = agent_by_id[e['to']]
                    rel_type = 'prerequisite'
                    rel_label = '经桥接主题 %s 映射' % topic['name']
                    via_bridge = True
                    break
        # 差异根源：若主题存在，取 bridge 的 difference；否则退回关系边标签
        diff = ''
        if topic:
            diff = ' '.join(c_by_id.get(topic['id'], {}).get('difference', []) or [])
        if not diff and rel_label:
            diff = rel_label
        if not diff:
            diff = '—'
        # 主题链接
        topic_txt = ('<a href="../02-node-pages/%s.html">%s</a>' % (esc(topic['id']), esc(topic['name']))
                     if topic else '<span class="dim">—</span>')
        agent_txt = ('<a href="../02-node-pages/%s.html">%s</a>' % (esc(rel_agent['id']), esc(rel_agent['name']))
                     if rel_agent else '<span class="dim">—</span>')
        rel_txt = ('<span class="badge rl rl-%s">%s</span>%s' % (
            esc(rel_type), EDGE_STYLE.get(rel_type, EDGE_STYLE['dependency'])['label'],
            ('<span class="rl-evi">%s</span>' % esc(rel_label)) if rel_label else ''))
        if rel_agent:
            agent_txt = ('<a href="../02-node-pages/%s.html">%s</a><div class="nname"><a href="../02-node-pages/%s.html">%s</a></div>'
                         % (esc(rel_agent['id']), esc(rel_agent['id']),
                            esc(rel_agent['id']), esc(rel_agent['name'])))
        else:
            agent_txt = '<span class="dim">—</span>'
        rows.append(
            '<tr><td class="nid"><a href="../02-node-pages/%s.html">%s</a><div class="nname">%s</div></td>'
            '<td>%s</td>'
            '<td class="nid">%s</td>'
            '<td>%s</td>'
            '<td class="diff">%s</td></tr>'
            % (esc(a['id']), esc(a['id']), esc(a['name']), topic_txt,
               agent_txt, rel_txt, esc(diff)))

    legend = ('<p class="dim">关系类型：<span class="badge rl rl-variant" style="color:#e8c66a;background:#3a2f12;border-color:#e0c35e">变体 variant</span>'
              ' <span class="badge rl rl-dependency" style="color:#e8a25e;background:#332412;border-color:#e8933b">依赖关联 dependency</span>'
              ' 差异根源取自对应桥接主题 difference 字段。</p>')

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>跨体系对照 · {title}</title>
<style>
{extra_css}
.back a{{color:var(--accent);text-decoration:none;font-size:14px;}}
.badge.rl{{font-size:11px;padding:1px 8px;border-radius:20px;font-weight:600;border:1px solid transparent;margin-right:6px;}}
.rl-evi{{font-size:11px;color:var(--dim);}}
td.diff{{color:#cfe8dd;font-size:12.5px;}}
td .nname{{font-weight:600;color:var(--text);font-size:13px;margin-top:2px;}}
</style>
</head>
<body>
{header}
{legend}
<div class="tblwrap"><table class="cmp">
<thead><tr>
<th>App 12 条</th><th>对应桥接主题</th><th>Agent 12 条</th><th>关系类型</th><th>差异根源（一句话）</th>
</tr></thead><tbody>
{rows}
</tbody></table></div>
{footer}
</body>
</html>
""".format(title=esc(TITLE), extra_css=BASE_CSS,
           header=views_header('跨体系对照',
                               '逐条比对 12 Factor App 与 12 Factor Agent 的方法原则，映射经由 10 个桥接主题。'),
           legend=legend, rows='\n'.join(rows), footer=views_footer('cross-mapping'))
    return html


def main():
    os.makedirs(VIEWS_DIR, exist_ok=True)
    dag, content, by_id, c_by_id, group_by_id = load_all()
    edges = dag['edges']

    files = {
        'index.html': stage_index_html(dag, by_id, group_by_id),
        '02-stage.html': stage_html(dag, by_id, group_by_id),
        '03-learning-path.html': path_html(dag, by_id, group_by_id, edges),
        '04-cross-mapping.html': cross_mapping_html(dag, by_id, c_by_id, edges),
    }
    for name, html in files.items():
        with open(os.path.join(VIEWS_DIR, name), 'w', encoding='utf-8') as f:
            f.write(html)
        print('view written:', name)


if __name__ == '__main__':
    main()
