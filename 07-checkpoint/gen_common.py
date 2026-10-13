#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""12 Factor 方法论图谱生成 —— 公共工具模块（数据加载 / 拓扑 / 样式 / HTML 片段）

被 gen-nodes.py / gen-groups.py / gen-views.py / gen-interactive.py 共享。
数据源：01-dag-data/methodology-dag.json + 01-dag-data/node-content.json，不硬编码节点数据。
"""
import html as html_mod
import json
import os
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, '01-dag-data')
DAG_PATH = os.path.join(DATA_DIR, 'methodology-dag.json')
CONTENT_PATH = os.path.join(DATA_DIR, 'node-content.json')

TITLE = '12 Factor 方法论合并知识图谱'
SUBTITLE = '12 Factor App × 12 Factor Agent — 软件工程方法论统一图谱'


def load_dag():
    with open(DAG_PATH, encoding='utf-8') as f:
        return json.load(f)


def load_content():
    with open(CONTENT_PATH, encoding='utf-8') as f:
        return json.load(f)


def load_all():
    dag = load_dag()
    content = load_content()
    by_id = {n['id']: n for n in dag['nodes']}
    c_by_id = {n['id']: n for n in content['nodes']}
    group_by_id = {g['id']: g for g in dag['groups']}
    return dag, content, by_id, c_by_id, group_by_id


def esc(s):
    return html_mod.escape(str(s), quote=True)


def build_indexes(dag):
    group_by_id = {g['id']: g for g in dag['groups']}
    node_by_id = {n['id']: n for n in dag['nodes']}
    node_to_group = {}
    for g in dag['groups']:
        for nid in g['node_ids']:
            node_to_group[nid] = g['id']
    group_node_index = {}
    for g in dag['groups']:
        for i, nid in enumerate(g['node_ids']):
            group_node_index[nid] = i
    return group_by_id, node_by_id, node_to_group, group_node_index


def topo_sort(node_ids, edges):
    """对给定节点集合，用 prerequisite 边做 Kahn 拓扑排序（返回稳定顺序，DAG 保证无环）。"""
    idset = set(node_ids)
    adj = defaultdict(list)
    indeg = {n: 0 for n in node_ids}
    for e in edges:
        f, t = e['from'], e['to']
        if e['type'] == 'prerequisite' and f in idset and t in idset:
            adj[f].append(t)
            indeg[t] += 1
    q = deque(sorted(n for n in node_ids if indeg[n] == 0))
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    for n in node_ids:
        if n not in order:
            order.append(n)
    return order


# ---------------------------------------------------------------- 样式常量
STAGE_STYLE = {
    'basic':        {'fg': '#2fb98a',  'bg': '#122b22', 'brd': '#2fb98a',  'label': '基础'},
    'intermediate': {'fg': '#e0a75e',  'bg': '#332412', 'brd': '#e8933b',  'label': '进阶'},
    'advanced':     {'fg': '#c9a8ef',  'bg': '#2b2040', 'brd': '#b48ae0',  'label': '高级'},
}

SRC_STYLE = {
    'app':    {'fg': '#9cc2ff', 'bg': '#16273f', 'brd': '#4f8cff', 'label': 'App 体系'},
    'agent':  {'fg': '#ff8a97', 'bg': '#3a1520', 'brd': '#e05563', 'label': 'Agent 体系'},
    'bridge': {'fg': '#6fd3ae', 'bg': '#0f2b1f', 'brd': '#2fb98a', 'label': '桥接主题'},
    'tool':   {'fg': '#e8c66a', 'bg': '#3a2f12', 'brd': '#e0c35e', 'label': '工具'},
}

KIND_STYLE = {
    'source':    {'fg': '#9cc2ff', 'bg': '#16273f', 'brd': '#4f8cff', 'label': '来源组'},
    'bridge':    {'fg': '#6fd3ae', 'bg': '#0f2b1f', 'brd': '#2fb98a', 'label': '主题组'},
    'crosscut':  {'fg': '#c9a8ef', 'bg': '#2b2040', 'brd': '#b48ae0', 'label': '横切组'},
    'tool':      {'fg': '#e8c66a', 'bg': '#3a2f12', 'brd': '#e0c35e', 'label': '工具组'},
}

EDGE_STYLE = {
    'prerequisite': {'fg': '#8fb5ff', 'bg': '#16273f', 'brd': '#4f8cff', 'label': '前置依赖'},
    'variant':      {'fg': '#e8c66a', 'bg': '#3a2f12', 'brd': '#e0c35e', 'label': '变体'},
    'combination':  {'fg': '#c9a8ef', 'bg': '#2b2040', 'brd': '#b48ae0', 'label': '组合'},
    'cooccurrence': {'fg': '#7fe0d8', 'bg': '#12302c', 'brd': '#5ad0d0', 'label': '共现'},
    'dependency':   {'fg': '#e8a25e', 'bg': '#332412', 'brd': '#e8933b', 'label': '依赖关联'},
}

GROUP_COLOR = {}
KIND_ORDER = ['source', 'bridge', 'crosscut', 'tool']


def stage_badge(stage):
    st = STAGE_STYLE.get(stage, STAGE_STYLE['basic'])
    return ('<span class="badge st" style="color:%s;background:%s;border-color:%s">%s</span>'
            % (st['fg'], st['bg'], st['brd'], st['label']))


def src_badge(src):
    s = SRC_STYLE.get(src, SRC_STYLE['bridge'])
    return ('<span class="badge src" style="color:%s;background:%s;border-color:%s">%s</span>'
            % (s['fg'], s['bg'], s['brd'], s['label']))


def kind_badge(kind):
    k = KIND_STYLE.get(kind, KIND_STYLE['source'])
    return ('<span class="badge kind" style="color:%s;background:%s;border-color:%s">%s</span>'
            % (k['fg'], k['bg'], k['brd'], k['label']))


def group_badge(gid, gname):
    return ('<span class="badge grp">%s · %s</span>' % (esc(gid), esc(gname)))


def type_badge(node):
    if node['type'] == 'bridge':
        return '<span class="badge tp" style="color:#6fd3ae;background:#0f2b1f;border-color:#2fb98a">桥接主题</span>'
    if node['type'] == 'tool':
        return '<span class="badge tp" style="color:#e8c66a;background:#3a2f12;border-color:#e0c35e">工具</span>'
    return '<span class="badge tp" style="color:#9cc2ff;background:#16273f;border-color:#4f8cff">方法原则</span>'


def edge_chip(e, node_id, node_by_id, other_dir_ok=True):
    st = EDGE_STYLE.get(e['type'], EDGE_STYLE['dependency'])
    other = e['to'] if e['from'] == node_id else e['from']
    arrow = '&#8594;' if e['from'] == node_id else '&#8592;'
    oname = node_by_id.get(other, {}).get('name', other)
    return ('<a class="chip e-%s" href="%s.html">%s%s%s<span class="etype">%s</span></a>'
            % (e['type'], esc(other), esc(oname), arrow, esc(e['label']), st['label']))


# ---------------------------------------------------------------- 共享 CSS
BASE_CSS = """
:root{--text:#e6e8ee;--dim:#9aa3b2;--accent:#4f8cff;--border:#6b7280;--border-subtle:#2a2f3a;--bg:#0f1117;--panel:#161a22;--ok:#2fb98a;--warn:#e8933b;--err:#e05563;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,'PingFang SC','Microsoft YaHei',sans-serif;line-height:1.7;}
header{background:var(--panel);border-bottom:0.0625rem solid var(--border);padding:0.875rem 1.5rem;}
header .crumb{color:var(--dim);font-size:0.8125rem;margin-bottom:0.375rem;}
header .crumb a{color:var(--accent);text-decoration:none;}
header .crumb a:hover{text-decoration:underline;}
header h1{font-size:1.25rem;font-weight:650;color:#f0f3f9;display:inline-block;margin-right:0.75rem;}
.badges{display:inline-flex;gap:0.375rem;flex-wrap:wrap;vertical-align:middle;}
.badge{display:inline-block;padding:0.125rem 0.625rem;border-radius:1.25rem;font-size:0.75rem;font-weight:600;border:0.0625rem solid transparent;letter-spacing:0.01875rem;}
.badge.grp{background:#1d2a3f;color:#7fb0ff;border-color:#2b3d5f;}
.badge.cnt{background:#23272f;color:#9aa0ab;border-color:#3a3f4a;}
main{padding:1.5rem;max-width:71.875rem;margin:0 auto;}
h2{font-size:1.125rem;margin:2.125rem 0 0.75rem;color:#cfd6e4;border-bottom:0.0625rem solid var(--border);padding-bottom:0.5rem;}
h2 .dim{font-size:0.8125rem;font-weight:400;}
h3{font-size:0.9375rem;margin:1.25rem 0 0.5rem;color:#b8c2d4;}
p,li{font-size:0.875rem;}
ul{padding-left:1.375rem;}
a{color:var(--accent);text-decoration:none;}
a:hover{text-decoration:underline;}
.dim{color:var(--dim);}
.section{scroll-margin-top:0.5rem;}
.brieflead{background:#0d1a14;border:0.0625rem solid #2f5a4a;border-left:0.25rem solid var(--ok);border-radius:0.5rem;padding:0.75rem 1rem;font-size:0.9375rem;color:#cfe8dd;margin:0.75rem 0;}
.whybox{background:var(--panel);border:0.0625rem solid var(--border-subtle);border-left-width:0.25rem;border-radius:0.5rem;padding:0.875rem 1.125rem;margin:0.625rem 0;}
.tag{font-size:0.75rem;font-weight:600;letter-spacing:0.01875rem;margin-bottom:0.375rem;}
.bullet{background:var(--panel);border:0.0625rem solid var(--border-subtle);border-radius:0.5rem;padding:0.625rem 1rem;margin:0.375rem 0;font-size:0.875rem;color:#d3d9e4;}
.pit li{margin:0.3125rem 0;font-size:0.875rem;}
.pit li::marker{color:var(--warn);}
.tblwrap{overflow-x:auto;margin:0.5rem 0;}
table{border-collapse:collapse;width:100%;}
th,td{border:0.0625rem solid var(--border-subtle);padding:0.4375rem 0.6875rem;font-size:0.8125rem;text-align:left;vertical-align:top;}
th{background:var(--panel);color:#b8c2d4;white-space:nowrap;}
td.nid{white-space:nowrap;font-family:Consolas,monospace;font-size:0.75rem;}
td.nid a{color:#8fb5ff;}
td .nname{font-weight:600;color:var(--text);}
td.brief{font-size:0.78125rem;color:#b6c0d0;}
.navseq{display:flex;gap:0.625rem;margin:1rem 0;flex-wrap:wrap;}
.navseq a{display:inline-block;background:var(--panel);border:0.0625rem solid var(--border-subtle);border-radius:0.5rem;padding:0.625rem 1.125rem;font-size:0.875rem;color:#b8c2d4;text-align:center;min-width:9.375rem;}
.navseq a .dir{display:block;font-size:0.6875rem;color:var(--dim);margin-bottom:0.125rem;}
.navseq a .v{font-weight:600;color:var(--accent);}
.navseq a.nav-index .v{color:var(--ok);}
.navseq .spacer{flex:1;min-width:3.75rem;}
.chips{display:flex;flex-wrap:wrap;gap:0.375rem;margin:0.375rem 0;}
.chip{font-size:0.75rem;background:#1d2a3f;border:0.0625rem solid #2b3d5f;border-radius:0.375rem;padding:0.125rem 0.5rem;color:#7fb0ff;text-decoration:none;}
.chip:hover{background:#2b3d5f;}
.chip .etype{font-size:0.625rem;opacity:.85;margin-left:0.25rem;}
.chip.e-prerequisite{background:#16273f;border-color:#2b3d5f;color:#9cc2ff;}
.chip.e-variant{background:#3a2f12;border-color:#4a3f20;color:#e8c66a;}
.chip.e-combination{background:#2b2040;border-color:#4a3560;color:#c9a8ef;}
.chip.e-cooccurrence{background:#12302c;border-color:#2b4a44;color:#7fe0d8;}
.chip.e-dependency{background:#332412;border-color:#4a3a20;color:#e8a25e;}
.pathbox{background:var(--panel);border:0.0625rem solid var(--border-subtle);border-radius:0.5rem;padding:0.75rem 1rem;margin:0.625rem 0;}
.path-label{font-size:0.75rem;color:var(--dim);margin-bottom:0.5rem;}
.path-seq{display:flex;flex-wrap:wrap;gap:0.25rem 0;font-size:0.8125rem;}
.path-seq a{display:inline-block;background:#16273f;border:0.0625rem solid #2b3d5f;border-radius:0.375rem;padding:0.125rem 0.5rem;color:#7fb0ff;text-decoration:none;margin:0.125rem;}
.path-seq a:hover{background:#2b3d5f;}
.dep-list{list-style:none;padding-left:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(21.25rem,1fr));gap:0.5rem;margin-top:0.5rem;}
.dep-list li{background:var(--panel);border:0.0625rem solid var(--border-subtle);border-radius:0.5rem;padding:0.5rem 0.75rem;font-size:0.8125rem;border-left:0.1875rem solid var(--warn);}
.dep-list .evi{display:block;font-size:0.6875rem;color:var(--dim);margin-top:0.125rem;}
.treenav{background:var(--panel);border:0.0625rem solid var(--border-subtle);border-radius:0.5rem;padding:0.625rem 1rem;margin:0.375rem 0 1.125rem;display:flex;flex-wrap:wrap;gap:0.125rem 0.625rem;}
.treenav .label{font-size:0.75rem;color:var(--dim);align-self:center;flex-shrink:0;}
.treenav a{color:var(--dim);font-size:0.75rem;text-decoration:none;border-radius:0.3125rem;padding:0.0625rem 0.375rem;}
.treenav a:hover{color:var(--accent);background:#1d2a3f;}
footer{margin-top:2.75rem;padding:1rem 1.5rem;border-top:0.0625rem solid var(--border);color:var(--dim);font-size:0.75rem;text-align:center;}
@media (max-width:720px){
  main{padding:0.875rem;}
  header{padding:0.75rem 0.875rem;}
  header h1{font-size:1.0625rem;}
  .navseq a{min-width:100%;}
  .badges{display:flex;margin-top:0.375rem;}
}
@media print{
  body{background:#fff;color:#000;}
  header,footer,.navseq,.treenav{display:none;}
  th,td{border-color:#999;color:#000;}
}
"""


# ============================================================================
# ★ 批 J：页面骨架与元数据（a11y / SEO 实缺修实）—— 唯一注入口
# ============================================================================
import re as _re

REPO = "12-factor-methodology-kg"
BASE_URL = "https://zako-mio.github.io/12-factor-methodology-kg/"
OG_IMAGE = BASE_URL + "og.png"
FAVICON_HREF = "/12-factor-methodology-kg/favicon.svg"
SITE_DESC = "12 要素方法论知识图谱：节点页、分组目录、阶段视图与交互式 DAG 总览。"

J_SHELL_CSS = (
    ":focus-visible{outline:0.125rem solid var(--accent,#4f8cff);outline-offset:0.125rem}\n"
    ".skip-link{position:absolute;left:-9999px;top:0;background:var(--accent,#4f8cff);"
    "color:#fff;padding:0.5rem 1rem;z-index:1000;border-radius:0 0 0.375rem 0}\n"
    ".skip-link:focus{left:0}\n")

_META_ANCHOR = _re.compile(r'(<meta\s+name="viewport"[^>]*>)', _re.I)
_BODY_ANCHOR = _re.compile(r'(<body[^>]*>)', _re.I)
_MAIN_ANCHOR = _re.compile(r'<main(?![^>]*\bid\s*=)([^>]*)>', _re.I)


def page_url(rel):
    if rel == "index.html":
        return BASE_URL
    if rel.endswith("/index.html"):
        return BASE_URL + rel[: -len("index.html")]
    return BASE_URL + rel


def _plain(frag):
    t = _re.sub(r"<[^>]+>", " ", frag)
    for a, b in (("&nbsp;", " "), ("&amp;", "&"), ("&larr;", "\u2190"), ("&rarr;", "\u2192"),
                 ("&#10003;", "\u2713")):
        t = t.replace(a, b)
    return _re.sub(r"\s+", " ", t).strip()


def page_title(html):
    m = _re.search(r"<title[^>]*>(.*?)</title>", html, _re.S | _re.I)
    return _plain(m.group(1)) if m else TITLE


def make_desc(html):
    tt = page_title(html)
    m = _re.search(r"<main[^>]*>(.*?)</main>", html, _re.S | _re.I)
    body = _plain(m.group(1)) if m else ""
    d = ("%s ｜ %s" % (tt, body)).strip(" ｜")
    d = d[:150].rstrip("，。、；：:;,. ")
    if len(d) < 24:
        d = "%s ｜ %s" % (tt, SITE_DESC)
    return d + "。"


def inject_shell(html, rel):
    """★ 三处插入：`<head>` 元数据 / `<body>` 后 skip link / 首个 `<main>` 补 id。

    ⛔ 不改任何既有模板变量与结构；★ 幂等（已注入则原样返回）。
    """
    if 'name="description"' in html and 'class="skip-link"' in html:
        return html
    desc = make_desc(html)
    title = page_title(html)
    u = page_url(rel)
    meta = (
        '<meta name="description" content="%s">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:title" content="%s">\n'
        '<meta property="og:description" content="%s">\n'
        '<meta property="og:url" content="%s">\n'
        '<meta property="og:image" content="%s">\n'
        '<link rel="canonical" href="%s">\n'
        '<link rel="icon" type="image/svg+xml" href="%s">\n'
        '<style>\n%s</style>\n'
        % (esc(desc), esc(title), esc(desc), u, OG_IMAGE, u, FAVICON_HREF, J_SHELL_CSS))
    out = _META_ANCHOR.sub(lambda m: m.group(1) + "\n" + meta, html, count=1)
    out = _BODY_ANCHOR.sub(
        lambda m: m.group(1) + '\n<a class="skip-link" href="#main">跳到主要内容</a>', out, count=1)
    out = _MAIN_ANCHOR.sub(lambda m: '<main id="main"%s>' % m.group(1), out, count=1)
    return out
