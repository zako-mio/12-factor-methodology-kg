#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gate_a11y.py — 12-factor-methodology-kg 的**无障碍门控**（批 H 标准档新增 · report_only）。

判据对象（SH5 §4.2 六类表的第 4 类 · 判据定义见 solutions/_shared/SH2-a11y-baseline.md §4.2）：
    产物的 `<main>` 地标 / skip link / `:focus-visible` / 图件文本等价。

执行强度：**report_only**（Q7 裁定 A）。⛔ 不进 `hard_blocking`（schema 枚举只有四项）。
★ **空集守卫不随报告模式放宽**：扫到 0 个文件 / 0 个页有 `<main>` / 0 页有图件 ⇒ exit 1。

判据（7 条）：
  A1 [blind]  空集守卫：产物页数 > 0，且**至少一页**有 `<main>`、**至少一页**有图件文本等价载体
  A2 [hard]   每页必须有且仅有 1 个 `<main>`（`<main>` 是地标，重复即语义冲突）
  A3 [hard]   每页必须有 skip link（`href="#main|#content|#skip"`）
  A4 [hard]   每页的样式表必须声明 `:focus-visible`（键盘焦点可见）
  A5 [hard]   每个 `<img>` 必须有 `alt` 属性；`<svg>` 图件必须有 `role="img"` ＋ `aria-label`/`<title>`
  A6 [hard]   豁免声明不得过期（`main_landmark_exempt` / `skiplink_exempt` 的页必须真的存在且**真的**违反）
  A7 [blind]  解析口径自检：每页必须解析出 ≥1 个 `<style>` 块（防「正则哑火 ⇒ 判据恒真」）

用法：
    python3 gate_a11y.py --site-root . --profile build/profile.json
    python3 gate_a11y.py --site-root . --profile build/profile.json --json
    python3 gate_a11y.py --selftest
退出码：0 全过（或报告模式且仅报告类）/ 1 有阻断级 FAIL / 2 输入错误 / 3 护栏拒读
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
MAIN = re.compile(r"<main\b", re.I)
SKIP = re.compile(r'href\s*=\s*"#(?:main|content|skip)', re.I)
IMG = re.compile(r"<img\b[^>]*>", re.I)
SVG = re.compile(r"<svg\b[^>]*>(.*?)</svg>", re.I | re.S)
ALT = re.compile(r"\balt\s*=", re.I)
ROLE_IMG = re.compile(r'role\s*=\s*"img"', re.I)
ARIA_LABEL = re.compile(r'aria-label\s*=\s*"[^"]+"', re.I)


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
    skip = set((profile.get("a11y") or {}).get("not_products") or [])
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
        styles = "\n".join(STYLE_BLOCK.findall(raw))
        svgs = SVG.findall(raw)
        d[rel] = {
            "raw": raw, "css": styles,
            "main": len(MAIN.findall(raw)),
            "skip": bool(SKIP.search(raw)),
            "focus": ":focus-visible" in styles,
            "styles": len(STYLE_BLOCK.findall(raw)),
            "imgs": IMG.findall(raw),
            "svg_no_label": [s for s in svgs
                             if not (ROLE_IMG.search(s) and (ARIA_LABEL.search(s) or "<title" in s))],
            "svg": len(svgs),
        }
    return d


def exempt_pages(v):
    """把豁免声明归一化为 `{page}`：既接受 ["a.html"]，也接受
    [{"page": "a.html", "why": "…"}]（本站在 profile 里用后者，因为**每条豁免都要写明理由**）。"""
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
    cfg = profile.get("a11y") or {}
    ex_main = exempt_pages(cfg.get("main_landmark_exempt"))
    ex_skip = exempt_pages(cfg.get("skiplink_exempt"))
    rels = product_pages(site_root, profile)
    P = scan(site_root, rels)

    def add(cid, name, ok, detail, klass):
        R.append((cid, name, bool(ok), detail, klass))

    n_main = sum(1 for v in P.values() if v["main"])
    n_carrier = sum(1 for v in P.values()
                    if any(ALT.search(i) for i in v["imgs"]) or v["svg"] or ROLE_IMG.search(v["raw"]))

    # ---- A1 空集守卫
    why = []
    if not rels:
        why.append("产物 HTML 扫描面 0 个文件")
    if rels and n_main == 0:
        why.append("没有任何一页含 <main>（判据无从谈起）")
    if rels and n_carrier == 0:
        why.append("没有任何一页含图件文本等价载体（img/svg/role=img 全 0）")
    add("A1", "空集守卫（页数 > 0 且 <main> 与图件载体均非空）", not why,
        "；".join(why) if why else
        "产物 %d 页 · 含 <main> %d 页 · 含图件文本等价载体 %d 页" % (len(rels), n_main, n_carrier), BLIND)

    # ---- A7 解析口径自检
    nostyle = sorted(r for r, v in P.items() if not v["styles"])
    add("A7", "解析口径自检（每页都解析出 ≥1 个 <style> 块）", not nostyle,
        "无 <style> 块的页：%s" % nostyle if nostyle else "%d 页全部解析出 <style> 块" % len(rels), BLIND)

    # ---- A2 <main>
    bad = sorted(r for r, v in P.items() if v["main"] != 1 and r not in ex_main)
    add("A2", "每页有且仅有 1 个 <main>（豁免项逐页登记）", not bad,
        "违反的页：%s" % bad[:8] if bad else
        "%d 页全部合格（豁免登记 %d 项：%s）" % (len(rels), len(ex_main), sorted(ex_main) or "无"), HARD)

    # ---- A3 skip link
    bad3 = sorted(r for r, v in P.items() if not v["skip"] and r not in ex_skip)
    add("A3", "每页有 skip link（href=\"#main|#content|#skip\"）", not bad3,
        "缺 skip link 的页：%d 页（例：%s）" % (len(bad3), bad3[:3]) if bad3 else
        "%d 页全部有 skip link（豁免登记 %d 项）" % (len(rels), len(ex_skip)), HARD)

    # ---- A4 :focus-visible
    bad4 = sorted(r for r, v in P.items() if not v["focus"])
    add("A4", "每页样式表声明 :focus-visible（键盘焦点可见）", not bad4,
        "缺 :focus-visible 的页：%d 页（例：%s）" % (len(bad4), bad4[:3]) if bad4 else
        "%d 页全部声明 :focus-visible" % len(rels), HARD)

    # ---- A5 图件文本等价
    bad5, checked_img, checked_svg = [], 0, 0
    for rel, v in P.items():
        for i in v["imgs"]:
            checked_img += 1
            if not ALT.search(i):
                bad5.append("%s 的 <img> 缺 alt：%s" % (rel, i[:60]))
        for s in v["svg_no_label"]:
            checked_svg += 1
            bad5.append("%s 的 <svg> 缺 role=\"img\" 或 aria-label/<title>" % rel)
    add("A5", "图件文本等价（img 必有 alt；svg 必有 role=img ＋ 文本）", not bad5,
        "；".join(bad5[:4]) if bad5 else
        "核对 <img> %d 个 / 无标签 <svg> %d 个，全部合格" % (checked_img, checked_svg), HARD)

    # ---- A6 豁免不得过期
    stale = []
    for r in sorted(ex_main):
        if r not in P:
            stale.append("main_landmark_exempt 声明的页不存在：%s" % r)
        elif P[r]["main"] == 1:
            stale.append("main_landmark_exempt 登记过期（该页其实合格）：%s" % r)
    for r in sorted(ex_skip):
        if r not in P:
            stale.append("skiplink_exempt 声明的页不存在：%s" % r)
        elif P[r]["skip"]:
            stale.append("skiplink_exempt 登记过期（该页其实有 skip link）：%s" % r)
    add("A6", "豁免登记不得过期（声明项须存在且真的违反）", not stale,
        "；".join(stale[:4]) if stale else
        "豁免登记 %d 项全部成立" % (len(ex_main) + len(ex_skip)), HARD)

    return R


def summarize(R):
    return {"judges": len(R), "fail_total": sum(1 for r in R if not r[2]),
            "blind_fail": sum(1 for r in R if r[4] == BLIND and not r[2]),
            "hard_fail": sum(1 for r in R if r[4] == HARD and not r[2])}


# --------------------------------------------------------------------------- selftest
FIX_CSS = (":root{--text:#e6e8ee;}\n"
           "a:focus-visible{outline:2px solid #4f8cff;}\n"
           ".card{color:var(--text);}\n")


def _page(main='<main><a href="#main" class="skip">跳到主内容</a><img src="x.png" alt="示意图"></main>',
          css=FIX_CSS, extra=""):
    return ('<!DOCTYPE html><html lang="zh-CN"><head><style>\n' + css + '</style></head>'
            '<body>' + main + extra + '</body></html>\n')


FIX_PROFILE = {
    "site": "t", "form": "inline-single-source", "publish_dir": ".", "value_file": "v.json",
    "targets": [{"path": "a.html", "mode": "root-block", "family": "default"}],
    "gates": {"manifest": "m.json", "hard_blocking": ["token-consistency"], "commands": ["x"]},
    "a11y": {"not_products": ["hand.html"], "main_landmark_exempt": [], "skiplink_exempt": []},
}


def _fixture(tmp):
    with open(os.path.join(tmp, "a.html"), "w", encoding="utf-8") as fh:
        fh.write(_page())
    with open(os.path.join(tmp, "b.html"), "w", encoding="utf-8") as fh:
        fh.write(_page())
    with open(os.path.join(tmp, "hand.html"), "w", encoding="utf-8") as fh:
        fh.write("<!DOCTYPE html><html><body>手写页</body></html>\n")
    p = os.path.join(tmp, "profile.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(FIX_PROFILE, fh, ensure_ascii=False)
    return p


def _run_fixture(mutate=None):
    tmp = tempfile.mkdtemp(prefix="a11y-")
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
            src = open(fp, encoding="utf-8").read()   # ★ 先读后写（open(w) 会立即截断）
            out = fn(src)
            assert out and out != src, "夹具自检：%s 未命中" % name
            with open(fp, "w", encoding="utf-8") as fh:
                fh.write(out)
        return _m

    def setp(fn):
        def _m(tmp, prof):
            p = json.load(open(prof, encoding="utf-8"))
            fn(p)
            json.dump(p, open(prof, "w", encoding="utf-8"), ensure_ascii=False)
        return _m

    def no_main(tmp, prof):
        for n in ("a.html", "b.html"):
            with open(os.path.join(tmp, n), "w", encoding="utf-8") as fh:
                fh.write(_page().replace("<main>", "<div>").replace("</main>", "</div>"))

    # A1 空集守卫
    case("A1 负例：扫描面 0 个文件", "A1",
         setp(lambda p: p["a11y"].__setitem__("not_products", ["a.html", "b.html", "hand.html"])))
    case("A1 负例：没有任何一页含 <main>", "A1", no_main)
    # A2 <main> 数量
    case("A2 负例：某页出现两个 <main>（地标重复）", "A2",
         edit("b.html", lambda s: s.replace("</body>", "<main>dup</main></body>")))
    case("A2 负例：某页完全没有 <main>", "A2",
         edit("a.html", lambda s: s.replace("<main>", "<section>").replace("</main>", "</section>")))
    # A3 skip link
    case("A3 负例：某页缺 skip link", "A3",
         edit("b.html", lambda s: s.replace('<a href="#main" class="skip">跳到主内容</a>', "")))
    # A4 :focus-visible
    case("A4 负例：某页缺 :focus-visible", "A4",
         edit("b.html", lambda s: s.replace("a:focus-visible{outline:2px solid #4f8cff;}\n", "")))
    # A5 图件文本等价（假阳样本）
    case("A5 负例：<img> 缺 alt", "A5",
         edit("a.html", lambda s: s.replace(' alt="示意图"', "")))
    case("A5 负例：<svg> 缺 role=img/aria-label", "A5",
         edit("a.html", lambda s: s.replace("</main>", '<svg viewBox="0 0 10 10"><path d="M0 0"/></svg></main>')))
    # A6 豁免过期
    case("A6 负例：豁免登记过期（该页其实合格）", "A6",
         setp(lambda p: p["a11y"]["main_landmark_exempt"].append("a.html")))
    case("A6 负例：豁免声明的页不存在", "A6",
         setp(lambda p: p["a11y"]["skiplink_exempt"].append("ghost.html")))
    # A7 解析口径
    case("A7 负例：某页解析不出 <style> 块", "A7",
         edit("b.html", lambda s: re.sub(r"<style>.*?</style>", "", s, flags=re.S)))

    ok = all(v for _, v, _ in cases)
    for name, res, note in cases:
        print("  [%s] %s%s" % ("PASS" if res else "FAIL", name, ("  ← " + note) if note else ""))
    print("\n=== gate_a11y.py 自检：%d 项，%d FAIL ===" % (len(cases), sum(1 for _, v, _ in cases if not v)))
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
    print("\n=== 无障碍门控（mode=report_only）：%d 项判据，%d FAIL（blind %d / hard %d）==="
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
