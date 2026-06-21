---
name: leetcode-notes
description: Use this skill whenever the user describes a LeetCode problem they just solved, asks to add a problem to their notes, or wants to review/update pattern notes. Triggers on mentions of problem numbers, problem names, "I solved", "add this to notes", or any pattern name (sliding window, two pointers, DP, monotonic stack, etc.) in the context of note-taking. Also triggers when the user asks to reorganize, split, or browse existing notes.
---

# LeetCode Pattern Notes

Maintain a pattern-organized LeetCode notes repository. Notes are split between **patterns** (algorithmic insight) and **problems** (per-problem detail). The pattern/variation files hold *condensed summaries* of each problem with a link out; the full problem write-up lives in its own standalone `.md` file under `problems/`. The repo's root README is an auto-maintained index of all patterns and their variations.

## Repo Structure

```
leetcode-notes/
├── README.md                           # Auto-maintained index (see "README Maintenance")
├── patterns/
│   ├── monotonic-stack.md              # Single-file pattern (no variations yet)
│   ├── sliding-window/                 # Folder pattern (has variations)
│   │   ├── README.md                   # General pattern intro
│   │   ├── fixed-window.md
│   │   ├── variable-window.md
│   │   └── window-with-state.md
│   └── backtracking/
│       ├── README.md
│       └── grid-backtracking.md
├── problems/                           # Standalone problem files, grouped by pattern
│   ├── backtracking/
│   │   └── word_search.md
│   └── sliding-window/
│       └── longest_substring_without_repeating.md
└── templates/                          # Optional: standalone code templates
```

Patterns can live in two forms — a single file when small, a folder when they have variations. Problems are always standalone files under `problems/<pattern>/<problem_name>.md` (snake_case filename, no LC number prefix).

### When to Upgrade a Single File to a Folder

The real criterion is **categorizability, not count**: split only when the problems genuinely cluster into 2+ *distinct sub-patterns* (different core technique / loop structure / invariant), so each variation file earns a real identity. A problem count is just a symptom — N near-identical variants of one trick still belong in a single file, while even 2 problems can justify a split when they are truly different categories (e.g. fixed-window vs variable-window). Never split just to hit a number.

Once genuine sub-categories exist, upgrade when the split earns its browsing cost — rough signals:

- 3+ clearly distinct variations, or
- the single file exceeds ~300 lines, or
- the user explicitly asks to split it.

When upgrading, preserve all existing problem summaries — move each into the appropriate variation file. The standalone `problems/<pattern>/...` files do not move.

## Workflow: Adding a Solved Problem

When the user describes a solved problem:

1. **Identify the pattern.** Ask if unclear. Match against existing pattern files first before proposing a new one.
2. **Identify the variation** (if pattern is a folder). Ask if unclear.
3. **Read the target pattern/variation file** before editing — new summaries must be consistent with prior summaries in the same file.
4. **Create the standalone problem file** at `problems/<pattern>/<problem_name>.md` using the Problem File Template. If the problem has a genuine follow-up / natural extension, record it in the Follow-ups section (never invent one).
5. **Append a condensed summary** to the pattern/variation file's `## Problems` section using the Problem Summary Template, linking to the standalone file.
6. **Update root README.md** if a new pattern or variation file was created.

Always preserve existing content. Never rewrite a whole file when only adding one entry.

## Workflow: Creating a New Pattern

1. **Confirm with the user** that this is a genuinely new pattern, not a variation of an existing one.
2. **Decide single-file or folder.** Default to single-file. Use folder only if the user already knows there will be multiple variations.
3. **Create the file** using the Pattern File Template.
4. **Update root README.md.**

## Pattern File Template

Used for `patterns/<name>.md` (single-file) or `patterns/<name>/README.md` (folder).

**Single-file form** — has `## Problems` at the bottom:

```markdown
# <Pattern Name>

## When to Use
Trigger signals — phrases or constraints in problems that hint at this pattern.

## Typical Complexity
**Time:** O(...) — explain *why*, not just the number
**Space:** O(...) — explain *why*

## General Template
\`\`\`cpp
// Minimal skeleton code for this pattern
\`\`\`

---

## Problems

<problem summaries go here>
```

**Folder form** (`patterns/<name>/README.md`) — replaces `## Problems` with a `## Common Variations` list. Problem summaries live in the variation files, not here:

```markdown
# <Pattern Name>

## When to Use
...

## Typical Complexity
...

## General Template
\`\`\`cpp
// Minimal skeleton
\`\`\`

## Common Variations
- [Variation 1](variation-1.md) — brief description
- [Variation 2](variation-2.md) — brief description
```

## Variation File Template

Used for `patterns/<name>/<variation>.md`.

```markdown
# <Pattern Name> — <Variation Name>

## When to Use
What distinguishes this variation from the general pattern? What specific signals point to this variation rather than another?

## Template Code
\`\`\`cpp
// Skeleton specific to this variation
\`\`\`

## Pitfalls
Mistakes specific to this variation.

---

## Problems

<problem summaries>
```

## Problem Summary Template

Lives inside a pattern or variation file's `## Problems` section. Keep it tight — this is a digest, not the full write-up.

```markdown
### [[<number>] <Problem Name>](../../problems/<pattern>/<problem_name>.md)
**Complexity:** Time O(...), Space O(...)
- **Trigger:** 1 line — what in the problem pointed here
- **Insight:** 1 line — the key idea
- **Pitfall:** 1 line — the easiest mistake
```

The link path is relative from the pattern/variation file to the standalone problem file:
- From `patterns/<name>.md` → `problems/<pattern>/<problem_name>.md`
- From `patterns/<name>/<variation>.md` → `../../problems/<pattern>/<problem_name>.md`

## Problem File Template

Used for `problems/<pattern>/<problem_name>.md`. Filename is snake_case, no LC number prefix (e.g., `word_search.md`, not `79-word-search.md`).

```markdown
# [<number>] <Problem Name>
**Pattern:** [<Pattern Name> → <Variation Name>](<relative-path-to-pattern-or-variation>)
**Complexity:** Time O(...), Space O(...)
**Link:** <url>

## Trigger Signals
What in this specific problem pointed to this pattern/variation?

## Core Insight
The key observation in 1–2 sentences.

## Complexity Analysis
Explain *why* the complexity is what it is. For example: nested loops that look O(n²) but are amortized O(n) because each pointer moves at most n times.

## Solution Code
\`\`\`cpp
// or python — match the user's main language (C++ / Python)
\`\`\`

## Pitfalls
Edge cases, off-by-one errors, easy mistakes encountered on this problem.

## Follow-ups
Include ONLY if the problem has a genuine follow-up or natural extension — an official "Follow-up:" line, or a well-known variation (e.g. a key constraint relaxed). State what the extension is and how it changes the approach (often: which assumption breaks). Do NOT invent one — omit this section entirely if there is no real follow-up.

## Related Problems
- [<num>] <name> — same pattern, different twist
```

## README Maintenance

The root `README.md` is an auto-maintained index. Whenever a pattern file or variation file is added, removed, or renamed, regenerate the index section.

### Procedure

1. Scan `patterns/` directory.
2. For each entry:
   - If it's a single `.md` file → list as a single pattern link.
   - If it's a folder → list the folder's `README.md` as the main link, then list its variation `.md` files as nested bullets.
3. For each pattern, include a 1-sentence description. Pull from the pattern file's `## When to Use` section, or ask the user if unclear.
4. Replace the index section in the root README, preserving any other content (intro, usage notes, etc.) outside the index markers.

### Root README Template

```markdown
# LeetCode Pattern Notes

<optional intro paragraph — preserved across regenerations>

<!-- INDEX START -->
## Patterns

### [Sliding Window](patterns/sliding-window/README.md)
維護一個移動的 window，常用於 substring/subarray 問題。
- [Fixed Window](patterns/sliding-window/fixed-window.md)
- [Variable Window](patterns/sliding-window/variable-window.md)
- [Window with State](patterns/sliding-window/window-with-state.md)

### [Two Pointers](patterns/two-pointers/README.md)
用兩個指針掃過 array/string，常見於 sorted 結構。
- [Opposite Direction](patterns/two-pointers/opposite-direction.md)
- [Same Direction](patterns/two-pointers/same-direction.md)

### [Monotonic Stack](patterns/monotonic-stack.md)
維護單調性的 stack，用於 next greater/smaller 類問題。
<!-- INDEX END -->
```

Always regenerate content **between** `<!-- INDEX START -->` and `<!-- INDEX END -->` markers. Never touch content outside them.

## Rules

- **Preserve the user's own wording.** When the user describes their solution/thought process, build the notes around *their* phrasing and mental model (the exact words, analogies, and framing they used). Don't rewrite their explanation into your own voice — they remember their own words best. Polish and structure, but keep their language as the backbone.
- **Keep the user's own code; never edit their code block.** When the user pastes working code, put *that exact code* in the Solution Code section verbatim (their structure, naming, indexing, comments). Do NOT substitute a cleaner rewrite, and do NOT edit inside their code block — any addition (tidy-up suggestion, bug warning, alternative) goes in a *separate* section outside the block. If you proposed a cleaner version in chat, the notes still follow whichever version the user adopted; they edit their own code. Your job around their block is to add commentary separately and to **flag bugs explicitly** (never silently fix — see the wording-preservation and error-flagging rules).
- **Explain motivation naturally — no rigid template.** Concept explanations should convey the *motivation* (what it is, why you'd reach for it) as flowing prose. Do NOT stamp fixed bold labels like 「他是什麼 / 為什麼需要他 / 他改變了什麼」 onto every section — that reads stiff and mechanical. Just explain the why in natural language; if the user gave their own description, use theirs.
- **Point out the user's mistakes — don't silently fix them.** If the user's stated reasoning, complexity, code, or claim is wrong, flag it explicitly and explain the correction *before* writing it into the notes. Never quietly correct an error in the notes without telling them; they need to know they had it wrong so they can re-learn it.
- **Keep complexity analysis explanatory.** Don't just write `O(n)`. Write *why*.
- **Default code language: C++ or Python**, matching the user's stated preference. Ask if ambiguous.
- **No Chinese in code comments.** Inside any code block (templates, solution code, snippets), comments must be in English regardless of the surrounding prose language. Markdown prose around the code can stay Chinese; only the `//` / `#` lines need to be English.
- **Pattern-level insights > problem-level details.** When the user revisits notes, the pattern/variation file's `When to Use` and `Typical Complexity` sections should be the most polished part. Standalone problem files are reference material.
- **Pattern files hold summaries, not full write-ups.** Each problem entry in a pattern/variation file is a 3-bullet digest (Trigger / Insight / Pitfall) with a link to the standalone problem file.
- **Don't invent problems.** Only add entries the user explicitly mentions solving.
- **Ask before creating a new pattern.** A new pattern is a commitment — confirm it's not just a variation of an existing one.
- **Ask before upgrading a file to a folder.** This is a structural change — confirm with the user.
- **Always update the root README index** after any structural change.
