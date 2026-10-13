#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gate_dead_css.py — 12-factor-methodology-kg 的**死 CSS 门控**（批 H 标准档新增 · report_only）。

判据对象（SH5 §4.2 六类表的第 3 类）：
    产物的 `class` 集合  vs  产物样式表里的**选择器集合**  ⇒  差集必须为空。

执行强度：**report_only**（Q7 裁定 A：首轮报告模式；转硬条件见 build/profile.json 的
`gates.mode_now_transition`）。⛔ 四类新门控**只能**进 `gates.report_only`——`site-profile.schema.json`
的 `hard_blocking` 枚举只有四项（token-consistency / contrast / empty-set-guard / artifact-existence），
扩枚举＝改 schema，须走独立决策。

★ 但**空集守卫不随报告模式放宽**（Q7 的「不随报告模式放宽」那条）：
  「扫到 0 个文件」「class 集合为空」「选择器集合为空」一律 exit 1 —— 否则「全绿」是假绿。

判据（5 条）：
  C1 [blind] 空集守卫：文件数 / class 集合 / 选择器集合 / 样式表字符数 均须 > 0
  C2 [hard]  死 class 差集为空（`产物 class − 选择器 class − 语义专用白名单 = ∅`）
  C3 [hard]  白名单不得过期（声明的「语义专用 class」必须**真的**出现在产物里，且**真的**没有选择器）
  C4 [report] 反向差集（选择器里出现了、但没有任何产物元素用的 class）——**报告**，⛔ 不阻断
  C5 [blind] 解析口径自检：每个产物页必须**真的**解析出 ≥1 个 `<style>` 块（防「正则哑火导致
             选择器集合为空 ⇒ 差集假性为空 ⇒ 假绿」）

用法：
    python3 gate_dead_css.py --site-root . --profile build/profile.json
    python3 gate_dead_css.py --site-root . --profile build/profile.json --json
    python3 gate_dead_css.py --selftest
退出码：0 全过（或报告模式且仅 report 类 FAIL）/ 1 有阻断级 FAIL / 2 输入错误 / 3 护栏拒读
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

CLS_ATTR = re.compile(r'class\s*=\s*"([^"]*)"')
STYLE_BLOCK = re.compile(r"<style[^>]*>(.*?)</style>", re.S)
SEL_CLASS = re.compile(r"\.(-?[A-Za-z_][\w-]*)")


class GuardError(Exception):
    """护栏拒读（exit 3）：输入缺失/非法，⛔ 不静默降级为「跳过」。"""


def load_json(path, label):
    if not os.path.isfile(path):
        raise GuardError("%s 不存在：%s" % (label, path))
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:  # noqa: BLE001
        raise GuardError("%s 非法 JSON：%s" % (label, exc))


def product_pages(site_root, profile):
    """产物 HTML = 全树 *.html 去掉 vendor/ 与非产物页（profile.dead_css.not_products）。"""
    skip = set((profile.get("dead_css") or {}).get("not_products") or [])
    out = []
    for p in sorted(glob.glob(os.path.join(site_root, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(p, site_root).replace(os.sep, "/")
        if "/vendor/" in "/" + rel or rel in skip:
            continue
        out.append(rel)
    return out


def scan(site_root, rels):
    """→ (class 集合, 选择器 class 集合, 每页样式表字符数, 无 <style> 的页)"""
    classes, sels, style_bytes, nostyle = set(), set(), {}, []
    for rel in rels:
        raw = open(os.path.join(site_root, rel), encoding="utf-8", errors="replace").read()
        for m in CLS_ATTR.finditer(raw):
            classes |= {c for c in m.group(1).split() if c}
        blocks = STYLE_BLOCK.findall(raw)
        css = "\n".join(blocks)
        style_bytes[rel] = len(css)
        if not blocks:
            nostyle.append(rel)
        sels |= set(SEL_CLASS.findall(css))
    return classes, sels, style_bytes, nostyle


def judge(ctx):
    R = []
    site_root, profile = ctx["site_root"], ctx["profile"]
    cfg = profile.get("dead_css") or {}
    whitelist = {e["class"]: e for e in (cfg.get("semantic_only_classes") or [])}
    rels = product_pages(site_root, profile)
    classes, sels, style_bytes, nostyle = scan(site_root, rels)

    def add(cid, name, ok, detail, klass):
        R.append((cid, name, bool(ok), detail, klass))

    # ---- C1 空集守卫
    why = []
    if not rels:
        why.append("产物 HTML 扫描面 0 个文件（glob 未命中）")
    if not classes:
        why.append("产物 class 集合为空")
    if not sels:
        why.append("样式表选择器 class 集合为空")
    if rels and sum(style_bytes.values()) == 0:
        why.append("全部产物的 <style> 内容合计 0 字符")
    add("C1", "空集守卫（文件/class/选择器/样式表字符数均非空）", not why,
        "；".join(why) if why else
        "产物 %d 页 · class %d 枚 · 选择器 class %d 枚 · 样式表 %d 字符"
        % (len(rels), len(classes), len(sels), sum(style_bytes.values())), BLIND)

    # ---- C5 解析口径自检（防正则哑火 ⇒ 差集假性为空）
    add("C5", "解析口径自检（每页都解析出 ≥1 个 <style> 块）", not nostyle,
        "无 <style> 块的页：%s" % nostyle if nostyle else
        "%d 页全部解析出 <style> 块" % len(rels), BLIND)

    # ---- C2 死 class 差集
    dead = sorted(classes - sels - set(whitelist))
    add("C2", "死 class 差集为空（产物 class ⊆ 选择器 ∪ 语义专用白名单）", not dead,
        "产物用了但样式表无对应选择器：%s" % dead if dead else
        "差集为空（产物 %d 枚 class；白名单 %d 枚）" % (len(classes), len(whitelist)), HARD)

    # ---- C3 白名单不得过期
    stale = []
    for c, e in sorted(whitelist.items()):
        if c not in classes:
            stale.append("%s 声明为语义专用，但产物里根本没用到" % c)
        elif c in sels:
            stale.append("%s 声明为语义专用，但样式表里其实有 .%s 选择器" % (c, c))
    add("C3", "语义专用白名单不得过期（声明项须真的无选择器且真的在用）", not stale,
        "；".join(stale[:4]) if stale else
        "%d 条声明全部成立（逐条：%s）" % (len(whitelist), ",".join(sorted(whitelist)) or "无"), HARD)

    # ---- C4 反向差集（报告，⛔ 不阻断）
    unused_sel = sorted(sels - classes)
    add("C4", "反向差集（选择器有、产物未用的 class）· 仅报告", not unused_sel,
        "样式表里存在但产物未使用：%s（%d 枚）" % (unused_sel, len(unused_sel)) if unused_sel
        else "无反向差集", REPORT)

    return R


def summarize(R):
    return {"judges": len(R), "fail_total": sum(1 for r in R if not r[2]),
            "blind_fail": sum(1 for r in R if r[4] == BLIND and not r[2]),
            "hard_fail": sum(1 for r in R if r[4] == HARD and not r[2]),
            "report_fail": sum(1 for r in R if r[4] == REPORT and not r[2])}


# --------------------------------------------------------------------------- selftest
FIX_PROFILE = {
    "site": "t", "form": "inline-single-source", "publish_dir": ".", "value_file": "v.json",
    "targets": [{"path": "a.html", "mode": "root-block", "family": "default"}],
    "gates": {"manifest": "m.json", "hard_blocking": ["token-consistency"], "commands": ["x"]},
    "dead_css": {"not_products": ["hand.html"],
                 "semantic_only_classes": [{"class": "js-hook", "why": "夹具：只被 JS 查询"}]},
}
FIX_A = ('<!DOCTYPE html><html><head><style>\n'
         ':root{--text:#e6e8ee;}\n.card{color:var(--text);}\n.bullet{padding:1px;}\n'
         '</style></head><body><div class="card bullet js-hook">hi</div></body></html>\n')
FIX_B = ('<!DOCTYPE html><html><head><style>\n.card{color:red;}\n</style></head>'
         '<body><div class="card">b</div></body></html>\n')
FIX_HAND = '<!DOCTYPE html><html><body>手写页，无 style</body></html>\n'


def _fixture(tmp):
    for n, t in (("a.html", FIX_A), ("b.html", FIX_B), ("hand.html", FIX_HAND)):
        with open(os.path.join(tmp, n), "w", encoding="utf-8") as fh:
            fh.write(t)
    p = os.path.join(tmp, "profile.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(FIX_PROFILE, fh, ensure_ascii=False)
    return p


def _run_fixture(mutate=None, debug=False):
    tmp = tempfile.mkdtemp(prefix="deacss-")
    prof = _fixture(tmp)
    if mutate:
        mutate(tmp, prof)
    if debug:  # noqa: SIM108 —— 仅排障用（--selftest 默认不开）
        for f in sorted(os.listdir(tmp)):
            print("   [debug] %s = %r" % (f, open(os.path.join(tmp, f), encoding="utf-8").read()[:160]))
    return judge({"site_root": tmp, "profile": json.load(open(prof, encoding="utf-8"))})


def selftest():
    cases = []

    def case(name, cid, mutate, expect_pass=False, debug=False):
        try:
            R = _run_fixture(mutate, debug=debug)
        except Exception as exc:  # noqa: BLE001
            cases.append((name, False, "异常：%s" % exc))
            return
        got = {r[0]: r[2] for r in R}
        ok = all(r[2] for r in R) if expect_pass else (got.get(cid) is False)
        det = {r[0]: r[3] for r in R}.get(cid, "")
        cases.append((name, ok, "" if ok else "cid=%s → %s" % (cid, det[:200])))

    case("正向夹具应 0 FAIL", None, None, expect_pass=True)

    def setp(fn):
        def _m(tmp, prof):
            p = json.load(open(prof, encoding="utf-8"))
            fn(p)
            json.dump(p, open(prof, "w", encoding="utf-8"), ensure_ascii=False)
        return _m

    def edit(name, fn):
        def _m(tmp, prof):
            fp = os.path.join(tmp, name)
            # ★ 必须先读后写：`open(fp,'w')` 会**立即截断**，写在参数位会把文件清空
            #   （本自检第一版就踩到这个：a.html 被清空 ⇒ 负例不触发 ⇒ 假绿）。
            src = open(fp, encoding="utf-8").read()
            out = fn(src)
            assert out, "夹具自检：%s 的替换结果为空（解析口径或夹具坏了）" % name
            with open(fp, "w", encoding="utf-8") as fh:
                fh.write(out)
        return _m

    def strip_styles(*names):
        def _m(tmp, prof):
            for n in names:
                fp = os.path.join(tmp, n)
                src = open(fp, encoding="utf-8").read()
                out = re.sub(r"<style>.*?</style>", "", src, flags=re.S)
                assert out != src, "夹具自检：%s 未命中 <style> 块" % n
                with open(fp, "w", encoding="utf-8") as fh:
                    fh.write(out)
        return _m

    # C1 空集守卫（两个负例）
    case("C1 负例：扫描面 0 个文件（not_products 把全部页排除）", "C1",
         setp(lambda p: p["dead_css"].__setitem__("not_products", ["a.html", "b.html", "hand.html"])))
    case("C1 负例：全部产物都无 <style>（选择器集合为空）", "C1",
         strip_styles("a.html", "b.html"))
    # C2 死 class（假阳样本：产物新增一个没有任何选择器的 class）
    case("C2 负例：产物出现无选择器的 class（假阳样本）", "C2",
         edit("a.html", lambda s: re.sub(r'class="card bullet js-hook"',
                                         'class="card bullet js-hook ghost-cls"', s, flags=re.S)))
    # C3 白名单过期（两种）
    case("C3 负例：白名单项在产物里根本没用到", "C3",
         setp(lambda p: p["dead_css"]["semantic_only_classes"].append(
             {"class": "never-used", "why": "夹具：过期登记"})))
    case("C3 负例：白名单项其实有选择器（登记过期）", "C3",
         edit("a.html", lambda s: s.replace(".bullet{padding:1px;}",
                                            ".bullet{padding:1px;}\n.js-hook{outline:0;}")))
    # C5 解析口径自检（正则哑火 ⇒ 差集假性为空）
    case("C5 负例：某页解析不出 <style> 块（解析口径哑火）", "C5",
         edit("b.html", lambda s: re.sub(r"<style>.*?</style>", "", s, flags=re.S)))

    ok = all(v for _, v, _ in cases)
    for name, res, note in cases:
        print("  [%s] %s%s" % ("PASS" if res else "FAIL", name, ("  ← " + note) if note else ""))
    print("\n=== gate_dead_css.py 自检：%d 项，%d FAIL ===" % (len(cases), sum(1 for _, v, _ in cases if not v)))
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
    # ★ `--profile` 传相对路径时按 **--site-root** 解析（与 profile.gates.commands 的写法一致：
    #   `python3 gate_dead_css.py --site-root . --profile build/profile.json`）。
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
    print("\n=== 死 CSS 门控（mode=report_only）：%d 项判据，%d FAIL（blind %d / hard %d / report %d）==="
          % (c["judges"], c["fail_total"], c["blind_fail"], c["hard_fail"], c["report_fail"]))
    if a.json:
        print(json.dumps([{"id": i, "name": n, "ok": o, "class": k, "detail": d} for i, n, o, d, k in R],
                         ensure_ascii=False, indent=1))
    if c["blind_fail"]:
        print("阻断：空集守卫 FAIL（门控致盲，报告模式也不宽恕）")
        return 1
    if c["hard_fail"]:
        print("报告模式：hard 类 FAIL 已记基线，不阻断（Q7 裁定 A；转硬条件见 profile.gates.mode_now_transition）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
