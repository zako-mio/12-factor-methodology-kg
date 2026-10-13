#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gate_responsive.py — 12-factor-methodology-kg 的**响应式门控**（批 H 标准档新增 · report_only）。

★ **本机无浏览器**（agent-browser 不在 PATH）⇒ 本门控按 SH3 §4.2 的判据对象**降级实现**为
  「读 `@media` 与固定宽度的**静态判据**」，并在 `gate-manifest.json` 的 `not_enforced_here` 与
  本文件头**如实声明像素/渲染层未测**。⛔ 不把静态判据冒充成 `documentElement.scrollWidth` 实测。

判据对象（SH5 §4.2 六类表的第 5 类）：
    四视口（320 / 375 / 768 / 1280）下的 `documentElement.scrollWidth` —— **本机未测**；
    替代静态判据 = viewport meta ＋ `@media` 断点 ＋ 固定宽度不得超出最窄视口。

执行强度：**report_only**（Q7 裁定 A）。⛔ 不进 `hard_blocking`。
★ **空集守卫不随报告模式放宽**：扫到 0 个文件 / 0 页声明 viewport / 全部页都没有任何 `@media` ⇒ exit 1。

判据（6 条）：
  R1 [blind]  空集守卫：产物页数 > 0，viewport 声明页数 > 0，`@media` 总数 > 0
  R2 [hard]   每页必须有 `viewport` meta（`width=device-width`）
  R3 [hard]   每页必须至少有 1 组 `@media` 断点（豁免项逐页登记）
  R4 [hard]   固定宽度不得超出最窄被测视口：`width`（非 max-/min-）的 px 值 > 320px 或
              rem 值 > 20rem（= 320px @ base16）即 FAIL
  R5 [hard]   豁免登记不得过期（`no_breakpoint_exempt` 的页须存在且真的无断点）
  R6 [blind]  解析口径自检：每页必须解析出 ≥1 个 `<style>` 块

★ 未覆盖面（如实声明，⛔ 不得读作「已测」）：
  1. 四视口 `documentElement.scrollWidth` **未测**（无浏览器）；
  2. 「侧栏覆盖画布」这类**可视区被盖**的缺陷（C6-N10）本门控**测不出**（它不是溢出，是覆盖）；
  3. 断点的**有效性**（改了什么、够不够）未判 —— 只判「存在一组断点」。

用法：
    python3 gate_responsive.py --site-root . --profile build/profile.json
    python3 gate_responsive.py --selftest
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
STYLE_BLOCK = re.compile(r"<style[^>]*>(.*?)</style>", re.S)
VIEWPORT = re.compile(r'<meta[^>]*name\s*=\s*"viewport"[^>]*>', re.I)
VP_CONTENT = re.compile(r'content\s*=\s*"([^"]*)"', re.I)
MEDIA = re.compile(r"@media\s*\(([^)]*)\)")
FIXED_W = re.compile(r"(?<!max-)(?<!min-)\bwidth\s*:\s*([0-9.]+)\s*(px|rem)")
NARROW_PX, NARROW_REM = 320.0, 20.0


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
    skip = set((profile.get("responsive") or {}).get("not_products") or [])
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
        css = "\n".join(STYLE_BLOCK.findall(raw))
        vp = VIEWPORT.search(raw)
        content = VP_CONTENT.search(vp.group(0)).group(1) if (vp and VP_CONTENT.search(vp.group(0))) else ""
        d[rel] = {"vp": bool(vp), "vp_content": content, "media": MEDIA.findall(css),
                  "styles": len(STYLE_BLOCK.findall(raw)),
                  "fixed": [(float(v), u) for v, u in FIXED_W.findall(css)]}
    return d


def exempt_pages(v):
    """归一化豁免声明为 `{page}`：接受 ["a.html"] 或 [{"page": "a.html", "why": "…"}]。"""
    out = set()
    for e in v or []:
        if isinstance(e, str):
            out.add(e)
        elif isinstance(e, dict) and e.get("page"):
            out.add(e["page"])
    return out


def judge(ctx):
    R = []
    site_root, profile = ctx["site_root"], ctx["profile"]
    cfg = profile.get("responsive") or {}
    ex = exempt_pages(cfg.get("no_breakpoint_exempt"))
    rels = product_pages(site_root, profile)
    P = scan(site_root, rels)

    def add(cid, name, ok, detail, klass):
        R.append((cid, name, bool(ok), detail, klass))

    n_vp = sum(1 for v in P.values() if v["vp"])
    n_media = sum(len(v["media"]) for v in P.values())

    why = []
    if not rels:
        why.append("产物 HTML 扫描面 0 个文件")
    if rels and n_vp == 0:
        why.append("没有任何一页声明 viewport meta")
    if rels and n_media == 0:
        why.append("全部产物的 @media 总数 = 0（响应式判据无从谈起）")
    add("R1", "空集守卫（页数 / viewport / @media 总数均非空）", not why,
        "；".join(why) if why else
        "产物 %d 页 · 声明 viewport %d 页 · @media 共 %d 组" % (len(rels), n_vp, n_media), BLIND)

    nostyle = sorted(r for r, v in P.items() if not v["styles"])
    add("R6", "解析口径自检（每页都解析出 ≥1 个 <style> 块）", not nostyle,
        "无 <style> 块的页：%s" % nostyle if nostyle else "%d 页全部解析出 <style> 块" % len(rels), BLIND)

    bad2 = sorted(r for r, v in P.items() if not v["vp"] or "width=device-width" not in v["vp_content"])
    add("R2", "每页声明 viewport（width=device-width）", not bad2,
        "违反的页：%s" % bad2[:6] if bad2 else "%d 页全部声明 width=device-width" % len(rels), HARD)

    bad3 = sorted(r for r, v in P.items() if not v["media"] and r not in ex)
    add("R3", "每页至少一组 @media 断点（豁免项逐页登记）", not bad3,
        "无断点的页：%d 页（例：%s）" % (len(bad3), bad3[:4]) if bad3 else
        "%d 页全部有断点（豁免登记 %d 项：%s）" % (len(rels), len(ex), sorted(ex) or "无"), HARD)

    bad4 = []
    for rel, v in sorted(P.items()):
        for val, unit in v["fixed"]:
            if (unit == "px" and val > NARROW_PX) or (unit == "rem" and val > NARROW_REM):
                bad4.append("%s 的固定 width:%s%s 超出最窄视口（%spx/%srem）"
                            % (rel, val, unit, NARROW_PX, NARROW_REM))
    add("R4", "固定宽度不超出最窄被测视口（320px / 20rem @base16）", not bad4,
        "；".join(bad4[:4]) if bad4 else "全部固定宽度均在 320px（20rem）以内", HARD)

    stale = []
    for r in sorted(ex):
        if r not in P:
            stale.append("no_breakpoint_exempt 声明的页不存在：%s" % r)
        elif P[r]["media"]:
            stale.append("no_breakpoint_exempt 登记过期（该页其实有断点）：%s" % r)
    add("R5", "豁免登记不得过期（声明项须存在且真的无断点）", not stale,
        "；".join(stale[:4]) if stale else "豁免登记 %d 项全部成立" % len(ex), HARD)

    # 报告类：断点档位分布（供人看，⛔ 不阻断）
    tiers = {}
    for v in P.values():
        for m in v["media"]:
            tiers[m] = tiers.get(m, 0) + 1
    add("R7", "断点档位分布（仅报告，⛔ 不判「够不够」）", True,
        "；".join("%s ×%d 页" % (k, n) for k, n in sorted(tiers.items())) or "无", REPORT)
    return R


def summarize(R):
    return {"judges": len(R), "fail_total": sum(1 for r in R if not r[2]),
            "blind_fail": sum(1 for r in R if r[4] == BLIND and not r[2]),
            "hard_fail": sum(1 for r in R if r[4] == HARD and not r[2])}


# --------------------------------------------------------------------------- selftest
FIX_CSS = (":root{--text:#e6e8ee;}\n"
           ".card{color:var(--text);width:auto;max-width:68.75rem;}\n"
           "@media (max-width:45rem){ .card{padding:1rem;} }\n")
FIX_PAGE = ('<!DOCTYPE html><html lang="zh-CN"><head>'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<style>\n' + FIX_CSS + '</style></head><body><main>hi</main></body></html>\n')
FIX_PROFILE = {
    "site": "t", "form": "inline-single-source", "publish_dir": ".", "value_file": "v.json",
    "targets": [{"path": "a.html", "mode": "root-block", "family": "default"}],
    "gates": {"manifest": "m.json", "hard_blocking": ["token-consistency"], "commands": ["x"]},
    "responsive": {"not_products": ["hand.html"], "no_breakpoint_exempt": []},
}


def _fixture(tmp):
    for n in ("a.html", "b.html"):
        with open(os.path.join(tmp, n), "w", encoding="utf-8") as fh:
            fh.write(FIX_PAGE)
    with open(os.path.join(tmp, "hand.html"), "w", encoding="utf-8") as fh:
        fh.write("<!DOCTYPE html><html><body>手写页</body></html>\n")
    p = os.path.join(tmp, "profile.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(FIX_PROFILE, fh, ensure_ascii=False)
    return p


def _run_fixture(mutate=None):
    tmp = tempfile.mkdtemp(prefix="resp-")
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

    def edit_all(fn):
        def _m(tmp, prof):
            for n in ("a.html", "b.html"):
                fp = os.path.join(tmp, n)
                out = fn(open(fp, encoding="utf-8").read())
                with open(fp, "w", encoding="utf-8") as fh:
                    fh.write(out)
        return _m

    def setp(fn):
        def _m(tmp, prof):
            p = json.load(open(prof, encoding="utf-8"))
            fn(p)
            json.dump(p, open(prof, "w", encoding="utf-8"), ensure_ascii=False)
        return _m

    # R1 空集守卫（两个负例）
    case("R1 负例：扫描面 0 个文件", "R1",
         setp(lambda p: p["responsive"].__setitem__("not_products", ["a.html", "b.html", "hand.html"])))
    case("R1 负例：全部产物都没有任何 @media", "R1",
         edit_all(lambda s: s.replace("@media (max-width:45rem){ .card{padding:1rem;} }\n", "")))
    # R2 viewport
    case("R2 负例：某页缺 viewport meta", "R2",
         edit("b.html", lambda s: s.replace(
             '<meta name="viewport" content="width=device-width, initial-scale=1.0">', "")))
    case("R2 负例：viewport 未含 width=device-width", "R2",
         edit("b.html", lambda s: s.replace("width=device-width, initial-scale=1.0", "width=1024")))
    # R3 断点
    case("R3 负例：某页无断点", "R3",
         edit("b.html", lambda s: s.replace("@media (max-width:45rem){ .card{padding:1rem;} }\n", "")))
    # R4 固定宽度（假阳样本）
    case("R4 负例：固定 width 超出最窄视口（px）", "R4",
         edit("a.html", lambda s: s.replace(".card{color:var(--text);width:auto;",
                                            ".card{color:var(--text);width:480px;")))
    case("R4 负例：固定 width 超出最窄视口（rem）", "R4",
         edit("a.html", lambda s: s.replace("width:auto;", "width:30rem;")))
    # R5 豁免过期
    case("R5 负例：豁免登记过期（该页其实有断点）", "R5",
         setp(lambda p: p["responsive"]["no_breakpoint_exempt"].append("a.html")))
    case("R5 负例：豁免声明的页不存在", "R5",
         setp(lambda p: p["responsive"]["no_breakpoint_exempt"].append("ghost.html")))
    # R6 解析口径
    case("R6 负例：某页解析不出 <style> 块", "R6",
         edit("b.html", lambda s: re.sub(r"<style>.*?</style>", "", s, flags=re.S)))

    ok = all(v for _, v, _ in cases)
    for name, res, note in cases:
        print("  [%s] %s%s" % ("PASS" if res else "FAIL", name, ("  ← " + note) if note else ""))
    print("\n=== gate_responsive.py 自检：%d 项，%d FAIL ===" % (len(cases), sum(1 for _, v, _ in cases if not v)))
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
    print("\n=== 响应式门控（mode=report_only；★ 像素层未测，见文件头与清单 not_enforced_here）："
          "%d 项判据，%d FAIL（blind %d / hard %d）==="
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
