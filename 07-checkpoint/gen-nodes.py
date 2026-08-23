#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 34 个节点页：02-node-pages/{node_id}.html（五段式 / 桥接三栏对比）

principle 节点：what/why/how/cases/anti_patterns 五段
bridge 节点：what/why/how + App 侧 | Agent 侧 | 差异根源 三栏对比表
页头：来源体系徽章(App/Agent/桥接) + 阶段徽章 + 所属组徽章
面包屑：总览 > 组 > 节点；含相关边列表（按边类型分组）。
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_common import (ROOT, TITLE, SUBTITLE, load_all, esc, build_indexes,
                        src_badge, stage_badge, group_badge, type_badge,
                        edge_chip, BASE_CSS, EDGE_STYLE)

OUT_DIR = os.path.join(ROOT, '02-node-pages')


def build_edges_for_node(edges, nid):
    out = []
    for e in edges:
        if e['from'] == nid or e['to'] == nid:
            out.append(e)
    out.sort(key=lambda e: (e['type'], e['from']))
    return out


def node_html(nid, node, content, group, edges, node_by_id):
    gid = group['id']
    gname = group['name']
    sections = []

    # ---------- What ----------
    what_items = content.get('what') or []
    what_lead = node['definition']
    w = ['<div class="section"><h2>What · 是什么</h2>']
    w.append('<div class="brieflead">%s</div>' % esc(what_lead))
    for item in what_items:
        w.append('<div class="bullet">%s</div>' % esc(item))
    w.append('</div>')
    sections.append(''.join(w))

    # ---------- Why ----------
    why_items = content.get('why') or []
    w = ['<div class="section"><h2>Why · 为什么</h2>']
    w.append('<div class="whybox" style="border-color:%s"><div class="tag" style="color:%s">原理 · Principle</div>'
             % (EDGE_STYLE['prerequisite']['brd'], EDGE_STYLE['prerequisite']['fg']))
    if why_items:
        for item in why_items:
            w.append('<p>%s</p>' % esc(item))
    else:
        w.append('<p class="dim">（本节点未展开原理说明）</p>')
    w.append('</div></div>')
    sections.append(''.join(w))

    # ---------- How ----------
    how_items = content.get('how') or []
    w = ['<div class="section"><h2>How · 怎么做</h2>']
    if how_items:
        for item in how_items:
            w.append('<div class="bullet">%s</div>' % esc(item))
    else:
        w.append('<div class="bullet" class="dim">（本节点未展开落地做法）</div>')
    w.append('</div>')
    sections.append(''.join(w))

    # ---------- bridge：三栏对比表 ----------
    if node['type'] == 'bridge':
        app_side = content.get('app_side') or []
        agent_side = content.get('agent_side') or []
        difference = content.get('difference') or []
        w = ['<div class="section"><h2>两体系对照 · App 侧 | Agent 侧 | 差异根源</h2>']
        w.append('<div class="tblwrap"><table class="cmp"><thead><tr>'
                 '<th style="width:33%%">App 侧</th>'
                 '<th style="width:33%%">Agent 侧</th>'
                 '<th style="width:34%%">差异根源</th></tr></thead><tbody>')
        rows = max(len(app_side), len(agent_side), len(difference))
        for i in range(rows):
            a = app_side[i] if i < len(app_side) else ''
            b = agent_side[i] if i < len(agent_side) else ''
            c = difference[i] if i < len(difference) else ''
            w.append('<tr><td>%s</td><td>%s</td><td class="diffsrc">%s</td></tr>'
                     % (esc(a), esc(b), esc(c)))
        w.append('</tbody></table></div></div>')
        sections.append(''.join(w))

    # ---------- cases / anti_patterns ----------
    cases = content.get('cases') or []
    anti = content.get('anti_patterns') or []
    if cases:
        w = ['<div class="section"><h2>案例 · Cases</h2><div class="tblwrap"><table>'
             '<tr><th>代表性案例</th></tr>']
        for c in cases:
            w.append('<tr><td>%s</td></tr>' % esc(c))
        w.append('</table></div></div>')
        sections.append(''.join(w))
    if anti:
        w = ['<div class="section"><h2>反模式 · Anti-patterns</h2><ul class="pit">']
        for a in anti:
            w.append('<li>%s</li>' % esc(a))
        w.append('</ul></div>')
        sections.append(''.join(w))

    # ---------- 相关边 ----------
    my_edges = build_edges_for_node(edges, nid)
    groups_edges = {}
    for e in my_edges:
        groups_edges.setdefault(e['type'], []).append(e)
    w = ['<div class="section"><h2>相关边</h2>']
    if my_edges:
        w.append('<div class="chips">')
        for et in sorted(groups_edges.keys(), key=lambda x: EDGE_STYLE.get(x, {}).get('label', x)):
            for e in groups_edges[et]:
                w.append(edge_chip(e, nid, node_by_id))
        w.append('</div>')
    else:
        w.append('<p class="dim">本节点没有与其他节点的关系边。</p>')
    w.append('</div>')
    sections.append(''.join(w))

    # ---------- 实践资源（源码引用） ----------
    refs = content.get('source_refs') or []
    if refs:
        w = ['<div class="section"><h2>实践资源 · 源码引用</h2><div class="tblwrap"><table>'
             '<tr><th>路径</th><th>说明</th></tr>']
        for r in refs:
            path = r.get('path', '')
            note = r.get('note', '')
            rel = path.lstrip('/')
            if rel.startswith('08-source/'):
                rel = rel[len('08-source/'):]
            display = '08-source/' + rel
            href = '../08-source/' + rel
            w.append('<tr><td><a href="%s" target="_blank" rel="noopener">%s</a></td><td>%s</td></tr>'
                     % (esc(href), esc(display), esc(note)))
        w.append('</table></div></div>')
        sections.append(''.join(w))

    body = '\n\n'.join(sections)

    crumb = ('<div class="crumb"><a href="../index.html">%s</a> / <a href="../03-groups/index.html">分组目录</a> / '
             '<a href="../03-groups/%s.html">%s</a> / <span>%s</span></div>'
             % (esc(TITLE), esc(gid), esc(gname), esc(node['name'])))

    badges = (src_badge(node['src']) + stage_badge(node['stage'])
              + type_badge(node) + group_badge(gid, gname))

    # 组内导航
    nav = ('<div class="navseq">'
           '<a class="nav-index" href="../04-interactive/index.html#%s"><span class="dir">全局</span><span class="v">交互总览</span></a>'
           '<a class="nav-index" href="../03-groups/%s.html"><span class="dir">返回组</span><span class="v">%s</span></a>'
           '<a class="nav-index" href="../04-interactive/index.html"><span class="dir">交互图</span><span class="v">打开总览</span></a>'
           '</div>'
           % (esc(gid), esc(gid), esc(gname)))

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} · {title}</title>
<style>
{extra_css}
table.cmp th{{text-align:center;}}
td.diffsrc{{color:#cfe8dd;background:#0d1a14;}}
</style>
</head>
<body>
<header>
  {crumb}
  <h1>{name}</h1>
  <div class="badges">{badges}</div>
</header>
<main>
{nav}
{body}
</main>
<footer>{title} · 节点页由 07-checkpoint/gen-nodes.py 生成 · 数据源 01-dag-data/methodology-dag.json + node-content.json</footer>
</body>
</html>
""".format(
        name=esc(node['name']), title=esc(TITLE), extra_css=BASE_CSS,
        crumb=crumb, badges=badges, nav=nav, body=body)
    return html


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    dag, content, by_id, c_by_id, group_by_id = load_all()
    edges = dag['edges']
    written = 0
    for node in dag['nodes']:
        gid = node['group']
        group = group_by_id[gid]
        cnt = c_by_id[node['id']]
        html = node_html(node['id'], node, cnt, group, edges, by_id)
        path = os.path.join(OUT_DIR, node['id'] + '.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        written += 1
    print('node pages written:', written)


if __name__ == '__main__':
    main()
