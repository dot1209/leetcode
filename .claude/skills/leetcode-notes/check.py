#!/usr/bin/env python3
"""Lint the LeetCode notes repo against the conventions in SKILL.md.

    python .claude/skills/leetcode-notes/check.py              # lint, exit 1 on any ERROR
    python .claude/skills/leetcode-notes/check.py --fix-punct  # rewrite half-width punctuation in Chinese prose

ERROR = the notes are structurally broken or off-template; fix before finishing.
WARN  = style drift worth a look (never fails the run).
No third-party dependencies.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

PROBLEM_H2 = [  # canonical order; (title, required)
    ("Trigger Signals", True), ("Core Insight", True), ("Why It's Correct", False),
    ("Complexity Analysis", True), ("Solution Code", True), ("Alternatives / Optimization", False),
    ("Pitfalls", True), ("Side Notes", False), ("Follow-ups", False), ("Related Problems", True),
]
PATTERN_REQUIRED = {
    "single": ["When to Use", "Typical Complexity", "Pitfalls", "Problems"],
    "readme": ["When to Use", "Typical Complexity", "Common Variations"],
    "variation": ["When to Use", "Pitfalls", "Problems"],
}
LAST_H2 = {"single": "Problems", "readme": "Common Variations", "variation": "Problems"}

FENCE = re.compile(r"^\s*```(.*)$")
LINK = re.compile(r"\]\(([^)\s]+)\)")
SUMMARY = re.compile(r"^### \[\[(\d+)\] [^\]]+\]\(([^)]+)\)\s*$")
CJK_IDEOGRAPH = re.compile(r"[㐀-䶿一-鿿]")

errors, warns = [], []


def rel(p):
    return p.relative_to(ROOT).as_posix()


def err(p, ln, msg):
    errors.append(f"ERROR {rel(p)}:{ln}: {msg}")


def warn(p, ln, msg):
    warns.append(f"WARN  {rel(p)}:{ln}: {msg}")


def lines_of(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")


def walk(lines):
    """Yield (lineno, line, in_fence, fence_lang, current_h2) for every line."""
    in_fence, lang, h2 = False, "", None
    for ln, line in enumerate(lines, 1):
        m = FENCE.match(line)
        if m:
            if not in_fence:
                in_fence, lang = True, m.group(1).strip()
            else:
                in_fence, lang = False, ""
            yield ln, line, True, lang, h2
            continue
        if not in_fence and line.startswith("## "):
            h2 = line[3:].strip()
        yield ln, line, in_fence, lang, h2


def h2_list(lines):
    return [(ln, line[3:].strip()) for ln, line, inf, _, _ in walk(lines) if not inf and line.startswith("## ")]


# ---------------------------------------------------------------- punctuation
PROTECT = re.compile(r"`[^`]*`|\]\([^)]*\)|https?://\S+|<!--.*?-->")
PUNCT = {",": "，", ";": "；", ":": "：", "!": "！", "?": "？"}


def is_cjk(ch):
    if ch is None or ch == "CODE":
        return False
    o = ord(ch)
    return 0x4E00 <= o <= 0x9FFF or 0x3400 <= o <= 0x4DBF or 0x3000 <= o <= 0x303F or 0xFF00 <= o <= 0xFFEF


def fix_punct(line):
    """Half-width punctuation that belongs to Chinese text -> full-width. Code/links/O(n) untouched."""
    chars, n = list(line), len(line)
    mask = [False] * n
    for m in PROTECT.finditer(line):
        mask[m.start():m.end()] = [True] * (m.end() - m.start())

    def sig(i, step):  # nearest neighbour, skipping markdown '*'; 'CODE' if protected
        k = i + step
        while 0 <= k < n and chars[k] == "*" and not mask[k]:
            k += step
        return None if not 0 <= k < n else ("CODE" if mask[k] else chars[k])

    line_cjk = any(is_cjk(c) for k, c in enumerate(chars) if not mask[k])
    stack, drop = [], set()
    for i, ch in enumerate(chars):  # pass 1: bracket pairs
        if mask[i]:
            continue
        if ch == "(":
            stack.append(i)
        elif ch == ")" and stack:
            o = stack.pop()
            before = chars[o - 1] if o > 0 and not mask[o - 1] else None
            call_like = before is not None and before.isascii() and (before.isalnum() or before in "_]>")
            inner = any(is_cjk(chars[k]) for k in range(o + 1, i) if not mask[k])
            outer = is_cjk(sig(o, -1)) or is_cjk(sig(i, +1))
            if inner or (outer and not call_like):
                chars[o], chars[i] = "（", "）"
                if o > 1 and chars[o - 1] == " " and not mask[o - 1] and chars[o - 2] != " ":
                    drop.add(o - 1)
                if i + 1 < n and chars[i + 1] == " " and not mask[i + 1]:
                    drop.add(i + 1)
    depth, d = [0] * n, 0
    for k, c in enumerate(chars):  # surviving half-width paren depth (math like min(m,n))
        if not mask[k] and c == "(":
            d += 1
        depth[k] = d
        if not mask[k] and c == ")" and d > 0:
            d -= 1
    for i, ch in enumerate(chars):  # pass 2: , ; : ! ?
        if mask[i] or ch not in PUNCT:
            continue
        p, nx = sig(i, -1), sig(i, +1)
        tight = (ch in ",;:" and line_cjk and depth[i] == 0 and p not in (None, " ", ":")
                 and nx not in (None, " ", ":") and not (nx != "CODE" and nx.isdigit()))
        ideograph_next = nx not in (None, "CODE") and bool(CJK_IDEOGRAPH.match(nx))
        if is_cjk(p) or (ch in ",;:" and is_cjk(nx)) or (ch in "?!" and ideograph_next) or tight:
            chars[i] = PUNCT[ch]
            if i + 1 < n - 1 and chars[i + 1] == " " and not mask[i + 1]:
                drop.add(i + 1)
    return "".join(c for k, c in enumerate(chars) if k not in drop)


def punct_pass(path, fix):
    lines, out, hits = lines_of(path), [], 0
    for ln, line, inf, _, _ in walk(lines):
        new = line if inf else fix_punct(line)
        for _ in range(3):  # a converted bracket can unlock the punctuation next to it
            nxt = new if inf else fix_punct(new)
            if nxt == new:
                break
            new = nxt
        if new != line:
            hits += 1
            if not fix:
                warn(path, ln, "half-width punctuation in Chinese prose (run with --fix-punct)")
        out.append(new)
    if fix and hits:
        path.write_text("\n".join(out), encoding="utf-8", newline="\n")
        print(f"fixed {hits:3d} lines  {rel(path)}")


# ---------------------------------------------------------------- checks
def check_links(path, lines):
    for ln, line, inf, _, _ in walk(lines):
        if inf:
            continue
        for target in LINK.findall(re.sub(r"`[^`]*`", "", line)):
            if re.match(r"[a-z]+://|#|mailto:", target):
                continue
            if not (path.parent / target.split("#")[0]).exists():
                err(path, ln, f"broken link -> {target}")


def check_code_comments(path, lines, is_problem):
    for ln, line, inf, lang, h2 in walk(lines):
        if inf and lang and not FENCE.match(line) and CJK_IDEOGRAPH.search(line):
            if is_problem and h2 == "Solution Code":
                warn(path, ln, "Chinese in Solution Code (fine only if this is the user's verbatim code)")
            else:
                err(path, ln, "Chinese inside a code block - comments you write must be English")


def check_problem(path, summaries):
    lines = lines_of(path)
    if not re.fullmatch(r"[a-z0-9]+(_[a-z0-9]+)*\.md", path.name) or re.match(r"\d+_", path.name):
        err(path, 1, "filename must be snake_case with no problem-number prefix")
    m = re.match(r"# \[(\d+)\] .+", lines[0])
    if not m:
        err(path, 1, "first line must be '# [<number>] <Problem Name>'")
    head = "\n".join(lines[:6])
    for label in ("**Pattern:**", "**Complexity:**", "**Link:**"):
        if label not in head:
            err(path, 1, f"header is missing {label}")

    titles = h2_list(lines)
    order = [t for t, _ in PROBLEM_H2]
    seen = []
    for ln, t in titles:
        if t not in order:
            err(path, ln, f"off-template H2 '## {t}' - use a canonical H2 and put this title in a ### under it")
        elif t in seen:
            err(path, ln, f"duplicate H2 '## {t}'")
        else:
            seen.append(t)
    if seen != [t for t in order if t in seen]:
        err(path, titles[0][0] if titles else 1, "H2 sections out of template order: " + " > ".join(seen))
    for t, required in PROBLEM_H2:
        if required and t not in seen:
            err(path, 1, f"missing required section '## {t}'")

    # back-link: **Pattern:** must point at the file that holds this problem's summary
    pm = re.search(r"\*\*Pattern:\*\*\s*\[[^\]]*\]\(([^)]+)\)", head)
    holders = summaries.get(path.resolve(), [])
    if len(holders) == 0:
        err(path, 1, "no summary under any pattern file's '## Problems' links to this problem")
    elif len(holders) > 1:
        err(path, 1, "summarized more than once: " + ", ".join(rel(h) for h, _, _ in holders))
    if pm:
        target = (path.parent / pm.group(1)).resolve()
        if holders and all(h.resolve() != target for h, _, _ in holders):
            err(path, 2, f"**Pattern:** links to {pm.group(1)} but the summary lives in {rel(holders[0][0])}")
    if m and holders and holders[0][1] != m.group(1):
        err(path, 1, f"problem number [{m.group(1)}] differs from its summary [{holders[0][1]}]")
    check_links(path, lines)
    check_code_comments(path, lines, True)


def check_pattern(path, kind, summaries):
    lines = lines_of(path)
    titles = h2_list(lines)
    names = [t for _, t in titles]
    for t in PATTERN_REQUIRED[kind]:
        if t not in names:
            err(path, 1, f"missing required section '## {t}' ({kind} pattern file)")
    for ln, t in titles:
        if t == "General Template":
            err(path, ln, "'## General Template' was renamed - use '## Template Code'")
    if names and names[-1] != LAST_H2[kind]:
        err(path, titles[-1][0], f"'## {LAST_H2[kind]}' must be the last H2 (found '## {names[-1]}')")
    dup = {t for t in names if names.count(t) > 1}
    for t in dup:
        err(path, 1, f"duplicate H2 '## {t}'")

    # summaries: heading link + Complexity + the three bullets
    in_problems = False
    for i, (ln, line, inf, _, h2) in enumerate(walk(lines)):
        in_problems = h2 == "Problems"
        if inf or not in_problems or not line.startswith("### "):
            continue
        sm = SUMMARY.match(line)
        if not sm:
            err(path, ln, "summary heading must be '### [[<num>] <Name>](<path-to-problem-file>)'")
            continue
        summaries.setdefault((path.parent / sm.group(2)).resolve(), []).append((path, sm.group(1), ln))
        block = []
        for nxt in lines[ln:]:
            if nxt.startswith("#"):
                break
            block.append(nxt)
        text = "\n".join(block)
        for label in ("**Complexity:**", "**Trigger:**", "**Insight:**", "**Pitfall:**"):
            if label not in text:
                err(path, ln, f"summary is missing {label}")

    if kind == "readme":
        listed = set()
        for ln, line, inf, _, h2 in walk(lines):
            if not inf and h2 == "Common Variations":
                listed.update(t for t in LINK.findall(line) if t.endswith(".md"))
        for v in sorted(path.parent.glob("*.md")):
            if v.name != "README.md" and v.name not in listed:
                err(path, 1, f"'## Common Variations' does not list {v.name}")
    check_links(path, lines)
    check_code_comments(path, lines, False)


def check_readme_index(pattern_files):
    path = ROOT / "README.md"
    lines = lines_of(path)
    text = "\n".join(lines)
    if "<!-- INDEX START -->" not in text or "<!-- INDEX END -->" not in text:
        err(path, 1, "missing <!-- INDEX START --> / <!-- INDEX END --> markers")
        return
    index = text.split("<!-- INDEX START -->")[1].split("<!-- INDEX END -->")[0]
    linked = [t for t in LINK.findall(index) if t.startswith("patterns/")]
    expected = {rel(p) for p in pattern_files}
    for t in sorted(expected - set(linked)):
        err(path, 1, f"index does not list {t}")
    for t in sorted(set(linked) - expected):
        err(path, 1, f"index lists {t}, which does not exist")
    for t in {t for t in linked if linked.count(t) > 1}:
        err(path, 1, f"index lists {t} more than once")
    tops = re.findall(r"(?m)^### \[[^\]]+\]\(patterns/([^)/]+)(?:/README\.md)?\)\n(.*)", index)
    stems = [t.removesuffix(".md") for t, _ in tops]
    if stems != sorted(stems):
        err(path, 1, "index patterns are not sorted by name: " + ", ".join(stems))
    for t, desc in tops:
        if not desc.strip() or desc.startswith(("-", "#")):
            err(path, 1, f"index entry for {t} has no one-sentence description")
    for block in re.split(r"(?m)^(?=### \[)", index)[1:]:
        subs = re.findall(r"(?m)^- \[[^\]]+\]\(patterns/[^)/]+/([^)]+)\)", block)
        if subs != sorted(subs):
            err(path, 1, "variations not sorted by filename: " + ", ".join(subs))
    check_links(path, lines)


def main():
    fix = "--fix-punct" in sys.argv
    pdir, qdir = ROOT / "patterns", ROOT / "problems"
    pattern_files = []
    for p in sorted(pdir.iterdir()):
        if p.is_file() and p.suffix == ".md":
            pattern_files.append((p, "single"))
        elif p.is_dir():
            if not (p / "README.md").exists():
                err(p, 1, "pattern folder has no README.md")
            for v in sorted(p.glob("*.md")):
                pattern_files.append((v, "readme" if v.name == "README.md" else "variation"))
    problem_files = sorted(qdir.glob("*/*.md"))
    everything = [ROOT / "README.md"] + [p for p, _ in pattern_files] + problem_files

    if fix:
        for p in everything:
            punct_pass(p, True)
        return 0

    summaries = {}
    for p, kind in pattern_files:
        check_pattern(p, kind, summaries)
    known = {q.resolve() for q in problem_files}
    for target, holders in summaries.items():
        if target not in known:
            for h, num, ln in holders:
                err(h, ln, f"summary [{num}] links to a problem file that does not exist")
    for q in problem_files:
        pattern_dir = q.parent.name
        if not (pdir / f"{pattern_dir}.md").exists() and not (pdir / pattern_dir).is_dir():
            err(q, 1, f"problems/{pattern_dir}/ has no matching pattern under patterns/")
        check_problem(q, summaries)
    check_readme_index([p for p, _ in pattern_files])
    for p in everything:
        punct_pass(p, False)

    for line in warns + errors:
        print(line)
    print(f"\n{len(pattern_files)} pattern files, {len(problem_files)} problem files: "
          f"{len(errors)} error(s), {len(warns)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
