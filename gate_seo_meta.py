#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gate_seo_meta.py — 12-factor-methodology-kg 的**元数据门控**（批 H 标准档新增 · report_only）。

判据对象（SH5 §4.2 六类表的第 6 类 · 判据定义见 solutions/_shared/SH4-seo-meta.md §4.2）：
    产物的 description / og / canonical / favicon / sitemap / robots。

执行强度：**report_only**（Q7 裁定 A）。⛔ 不进 `hard_blocking`。
★ **空集守卫不随报告模式放宽**：扫到 0 个文件 / `<title>` 页数为 0 / `<html lang>` 页数为 0 ⇒ exit 1。

判据（8 条）：
  S1 [blind]  空集守卫：产物页数 > 0 且 `<title>`、`<html lang>` 的覆盖页数均 > 0
  S2 [hard]   每页有 `<title>`
  S3 [hard]   每页有 `<html lang>`
  S4 [hard]   每页有 `<meta name="description">`（非空）
  S5 [hard]   每页有 `og:title` / `og:description` / `og:type`（`og:url` 与 `og:image` 逐页登记豁免）
  S6 [hard]   每页有 `<link rel="canonical">`
  S7 [hard]   favicon：每页有 `<link rel="icon">`，**或**仓根存在 `favicon.ico`（逐页登记豁免）
  S8 [hard]   `sitemap.xml` 存在；`robots.txt` 存在且含 `Sitemap:` 指向它
              （**或**在 `seo_meta.sitemap_optional_reason` 里显式声明为何不适用）
  S9 [blind]  解析口径自检：每页必须解析出 ≥1 个 `<head>` 块

用法：
    python3 gate_seo_meta.py --site-root . --profile build/profile.json
    python3 gate_seo_meta.py --selftest
退出码：0 全过 / 1 有阻断级 FAIL / 2 输入错误 / 3 护栏拒读
"""
import argparse
import glob
import json
import os
import re
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8")

BLIND, HARD, REPORT = "blind", "hard", "report"
HEAD_BLOCK = re.compile(r"<head[^>]*>(.*?)</head>", re.I | re.S)
TITLE = re.compile(r"<title\s*>\s*[^<\s]", re.I)
LANG = re.compile(r"<html[^>]*\blang\s*=\s*\"[^\"]+\"", re.I)
DESC = re.compile(r'<meta[^>]*name\s*=\s*"description"[^>]*content\s*=\s*"([^"]*)"', re.I)
OG = re.compile(r'property\s*=\s*"(og:[a-z_]+)"', re.I)
CANON = re.compile(r'<link[^>]*rel\s*=\s*"canonical"', re.I)
ICON = re.compile(r'<link[^>]*rel\s*=\s*"(?:icon|shortcut icon|apple-touch-icon)"', re.I)


class GuardError(Exception):
    """护栏拒读（exit 3）。"""


def load_json(path, label):
    if not os.path.isfile(path):
        raise GuardError("%s 不存在：%s" % (label, path))
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:  # noqa: BLE001
        raise GuardError("%s 非法 JSON：%s" % (label, exc))


def product_pages(site_root, profile):
    cfg = profile.get("seo_meta") or {}
    skip = set(cfg.get("not_products") or [])
    out = []
    for p in sorted(glob.glob(os.path.join(site_root, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(p, site_root).replace(os.sep, "/")
        if "/vendor/" in "/" + rel or rel in skip:
            continue
        out.append(rel)
    return out


def scan(site_root, rels):
    d = {}
    for rel in rels:
        raw = open(os.path.join(site_root, rel), encoding="utf-8", errors="replace").read()
        heads = HEAD_BLOCK.findall(raw)
        head = "\n".join(heads)
        desc = DESC.search(head)
        d[rel] = {"head": head, "heads": len(heads), "title": bool(TITLE.search(head)),
                  "lang": bool(LANG.search(raw)), "desc": desc.group(1).strip() if desc else "",
                  "og": sorted(set(OG.findall(head))), "canon": bool(CANON.search(head)),
                  "icon": bool(ICON.search(head))}
    return d


def judge(ctx):
    R = []
    site_root, profile = ctx["site_root"], ctx["profile"]
    cfg = profile.get("seo_meta") or {}
    ex_og = set(cfg.get("og_url_image_exempt") or [])
    ex_icon = set(cfg.get("favicon_exempt") or [])
    sitemap_reason = (cfg.get("sitemap_optional_reason") or "").strip()
    rels = product_pages(site_root, profile)
    P = scan(site_root, rels)

    def add(cid, name, ok, detail, klass):
        R.append((cid, name, bool(ok), detail, klass))

    n_title = sum(1 for v in P.values() if v["title"])
    n_lang = sum(1 for v in P.values() if v["lang"])

    why = []
    if not rels:
        why.append("产物 HTML 扫描面 0 个文件")
    if rels and n_title == 0:
        why.append("没有任何一页有 <title>")
    if rels and n_lang == 0:
        why.append("没有任何一页有 <html lang>")
    add("S1", "空集守卫（页数 / <title> / <html lang> 覆盖均非空）", not why,
        "；".join(why) if why else
        "产物 %d 页 · 有 <title> %d 页 · 有 <html lang> %d 页" % (len(rels), n_title, n_lang), BLIND)

    nostyle = sorted(r for r, v in P.items() if not v["heads"])
    add("S9", "解析口径自检（每页都解析出 ≥1 个 <head> 块）", not nostyle,
        "无 <head> 块的页：%s" % nostyle if nostyle else "%d 页全部解析出 <head> 块" % len(rels), BLIND)

    b2 = sorted(r for r, v in P.items() if not v["title"])
    add("S2", "每页有 <title>", not b2,
        "缺 <title> 的页：%s" % b2[:6] if b2 else "%d 页全部有 <title>" % len(rels), HARD)

    b3 = sorted(r for r, v in P.items() if not v["lang"])
    add("S3", "每页有 <html lang>", not b3,
        "缺 lang 的页：%s" % b3[:6] if b3 else "%d 页全部有 <html lang>" % len(rels), HARD)

    b4 = sorted(r for r, v in P.items() if not v["desc"])
    add("S4", "每页有非空 <meta name=\"description\">", not b4,
        "缺 description 的页：%d 页（例：%s）" % (len(b4), b4[:3]) if b4 else
        "%d 页全部有非空 description" % len(rels), HARD)

    b5 = []
    for rel, v in sorted(P.items()):
        need = {"og:title", "og:description", "og:type"}
        if rel not in ex_og:
            need |= {"og:url", "og:image"}
        miss = sorted(need - set(v["og"]))
        if miss:
            b5.append("%s 缺 %s" % (rel, miss))
    add("S5", "每页有 og:title/description/type（url/image 逐页登记豁免）", not b5,
        "；".join(b5[:3]) if b5 else
        "%d 页 og 齐备（og:url/og:image 豁免登记 %d 项）" % (len(rels), len(ex_og)), HARD)

    b6 = sorted(r for r, v in P.items() if not v["canon"])
    add("S6", "每页有 <link rel=\"canonical\">", not b6,
        "缺 canonical 的页：%d 页（例：%s）" % (len(b6), b6[:3]) if b6 else
        "%d 页全部有 canonical" % len(rels), HARD)

    root_icon = [f for f in ("favicon.ico", "favicon.png", "favicon.svg")
                 if os.path.isfile(os.path.join(site_root, f))]
    b7 = sorted(r for r, v in P.items() if not v["icon"] and r not in ex_icon and not root_icon)
    add("S7", "favicon（每页 <link rel=icon>，或仓根有 favicon 文件）", not b7,
        "缺 favicon 的页：%d 页（例：%s）；仓根 favicon 文件：%s" % (len(b7), b7[:3], root_icon or "无")
        if b7 else "每页有 <link rel=icon> 或仓根有 favicon（%s）" % (root_icon or "link"), HARD)

    sm = os.path.isfile(os.path.join(site_root, "sitemap.xml"))
    rb = os.path.isfile(os.path.join(site_root, "robots.txt"))
    rb_has = bool(rb and re.search(r"^\s*Sitemap\s*:", open(os.path.join(site_root, "robots.txt"),
                                                           encoding="utf-8", errors="replace").read(),
                                   re.I | re.M))
    b8 = []
    if not sm:
        b8.append("sitemap.xml 不存在")
    if not rb:
        b8.append("robots.txt 不存在")
    elif not rb_has:
        b8.append("robots.txt 未声明 Sitemap: 指向 sitemap.xml")
    if sitemap_reason:
        b8 = []            # ★ 显式声明「为何不适用」时放行（声明本身进 detail，可复核）
    add("S8", "sitemap.xml ＋ robots.txt(含 Sitemap:)", not b8,
        "；".join(b8) if b8 else ("sitemap 与 robots 齐备" if not sitemap_reason
                                  else "未适用，理由已声明：%s" % sitemap_reason), HARD)

    # 报告类：description 长度分布（供人看，⛔ 不阻断）
    lens = sorted(len(v["desc"]) for v in P.values() if v["desc"])
    add("S10", "description 长度分布（仅报告）", True,
        "有值 %d 条；长度 min/max = %s/%s" % (len(lens), lens[0] if lens else "-",
                                              lens[-1] if lens else "-"), REPORT)
    return R


def summarize(R):
    return {"judges": len(R), "fail_total": sum(1 for r in R if not r[2]),
            "blind_fail": sum(1 for r in R if r[4] == BLIND and not r[2]),
            "hard_fail": sum(1 for r in R if r[4] == HARD and not r[2])}


# --------------------------------------------------------------------------- selftest
FIX_HEAD = ('<meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<title>t</title>'
            '<meta name="description" content="夹具描述">'
            '<meta property="og:title" content="t"><meta property="og:description" content="d">'
            '<meta property="og:type" content="website"><meta property="og:url" content="u">'
            '<meta property="og:image" content="i">'
            '<link rel="canonical" href="https://e/"><link rel="icon" href="/favicon.ico">')
FIX_PAGE = ('<!DOCTYPE html><html lang="zh-CN"><head>' + FIX_HEAD +
            '</head><body><main>hi</main></body></html>\n')
FIX_PROFILE = {
    "site": "t", "form": "inline-single-source", "publish_dir": ".", "value_file": "v.json",
    "targets": [{"path": "a.html", "mode": "root-block", "family": "default"}],
    "gates": {"manifest": "m.json", "hard_blocking": ["token-consistency"], "commands": ["x"]},
    "seo_meta": {"not_products": ["hand.html"], "og_url_image_exempt": [], "favicon_exempt": [],
                 "sitemap_optional_reason": ""},
}


def _fixture(tmp):
    for n in ("a.html", "b.html"):
        with open(os.path.join(tmp, n), "w", encoding="utf-8") as fh:
            fh.write(FIX_PAGE)
    with open(os.path.join(tmp, "hand.html"), "w", encoding="utf-8") as fh:
        fh.write("<!DOCTYPE html><html><body>手写页</body></html>\n")
    with open(os.path.join(tmp, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0"?><urlset></urlset>\n')
    with open(os.path.join(tmp, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write("User-agent: *\nAllow: /\nSitemap: https://e/sitemap.xml\n")
    p = os.path.join(tmp, "profile.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(FIX_PROFILE, fh, ensure_ascii=False)
    return p


def _run_fixture(mutate=None):
    tmp = tempfile.mkdtemp(prefix="seo-")
    prof = _fixture(tmp)
    if mutate:
        mutate(tmp, prof)
    return judge({"site_root": tmp, "profile": json.load(open(prof, encoding="utf-8"))})


def selftest():
    cases = []

    def case(name, cid, mutate, expect_pass=False):
        try:
            R = _run_fixture(mutate)
        except Exception as exc:  # noqa: BLE001
            cases.append((name, False, "异常：%s" % exc))
            return
        got = {r[0]: r[2] for r in R}
        ok = all(r[2] for r in R) if expect_pass else (got.get(cid) is False)
        det = {r[0]: r[3] for r in R}.get(cid, "")
        cases.append((name, ok, "" if ok else "cid=%s → %s" % (cid, det[:160])))

    case("正向夹具应 0 FAIL", None, None, expect_pass=True)

    def edit(name, fn):
        def _m(tmp, prof):
            fp = os.path.join(tmp, name)
            src = open(fp, encoding="utf-8").read()   # ★ 先读后写
            out = fn(src)
            assert out and out != src, "夹具自检：%s 未命中" % name
            with open(fp, "w", encoding="utf-8") as fh:
                fh.write(out)
        return _m

    def rm(name):
        def _m(tmp, prof):
            os.remove(os.path.join(tmp, name))
        return _m

    def setp(fn):
        def _m(tmp, prof):
            p = json.load(open(prof, encoding="utf-8"))
            fn(p)
            json.dump(p, open(prof, "w", encoding="utf-8"), ensure_ascii=False)
        return _m

    # S1 空集守卫
    case("S1 负例：扫描面 0 个文件", "S1",
         setp(lambda p: p["seo_meta"].__setitem__("not_products", ["a.html", "b.html", "hand.html"])))
    # S2/S3
    case("S2 负例：某页缺 <title>", "S2", edit("b.html", lambda s: s.replace("<title>t</title>", "")))
    case("S3 负例：某页缺 <html lang>", "S3", edit("b.html", lambda s: s.replace(' lang="zh-CN"', "")))
    # S4 description（含「假阳样本」：空 content）
    case("S4 负例：某页缺 description", "S4",
         edit("b.html", lambda s: s.replace('<meta name="description" content="夹具描述">', "")))
    case("S4 负例：description 为空串（假阳样本）", "S4",
         edit("b.html", lambda s: s.replace('content="夹具描述"', 'content=""')))
    # S5 og
    case("S5 负例：某页缺 og:type", "S5",
         edit("b.html", lambda s: s.replace('<meta property="og:type" content="website">', "")))
    case("S5 负例：某页缺 og:image 且未登记豁免", "S5",
         edit("b.html", lambda s: s.replace('<meta property="og:image" content="i">', "")))
    # S6 canonical
    case("S6 负例：某页缺 canonical", "S6",
         edit("b.html", lambda s: s.replace('<link rel="canonical" href="https://e/">', "")))
    # S7 favicon
    case("S7 负例：某页缺 <link rel=icon> 且仓根无 favicon", "S7",
         edit("a.html", lambda s: s.replace('<link rel="icon" href="/favicon.ico">', "")))
    # S8 sitemap/robots
    case("S8 负例：sitemap.xml 不存在", "S8", rm("sitemap.xml"))
    case("S8 负例：robots.txt 未声明 Sitemap:", "S8",
         edit("robots.txt", lambda s: s.replace("Sitemap: https://e/sitemap.xml", "")))
    case("S8 负例：robots.txt 不存在", "S8", rm("robots.txt"))
    # S9 解析口径
    case("S9 负例：某页解析不出 <head> 块", "S9",
         edit("b.html", lambda s: re.sub(r"<head>.*?</head>", "", s, flags=re.S)))

    ok = all(v for _, v, _ in cases)
    for name, res, note in cases:
        print("  [%s] %s%s" % ("PASS" if res else "FAIL", name, ("  ← " + note) if note else ""))
    print("\n=== gate_seo_meta.py 自检：%d 项，%d FAIL ===" % (len(cases), sum(1 for _, v, _ in cases if not v)))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-root", default=".")
    ap.add_argument("--profile", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    site_root = os.path.abspath(a.site_root)
    # ★ 相对 --profile 按 --site-root 解析（与 profile.gates.commands 的写法一致）
    pp = a.profile or "build/profile.json"
    if not os.path.isabs(pp):
        pp = os.path.join(site_root, pp)
    try:
        profile = load_json(pp, "profile")
        R = judge({"site_root": site_root, "profile": profile})
    except GuardError as exc:
        print("GUARD-REJECT: %s" % exc)
        return 3
    for cid, name, ok, detail, klass in R:
        print("[%s] %s %s %s — %s" % ("PASS" if ok else "FAIL", cid, name, klass, detail))
    c = summarize(R)
    print("\n=== 元数据门控（mode=report_only）：%d 项判据，%d FAIL（blind %d / hard %d）==="
          % (c["judges"], c["fail_total"], c["blind_fail"], c["hard_fail"]))
    if a.json:
        print(json.dumps([{"id": i, "name": n, "ok": o, "class": k, "detail": d} for i, n, o, d, k in R],
                         ensure_ascii=False, indent=1))
    if c["blind_fail"]:
        print("阻断：空集守卫 FAIL（门控致盲，报告模式也不宽恕）")
        return 1
    if c["hard_fail"]:
        print("报告模式：hard 类 FAIL 已记基线，不阻断（Q7 裁定 A）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
