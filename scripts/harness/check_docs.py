"""Check Markdown documents against the mechanical rules of rules/docs.rules.md."""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
LOCAL = {"memory", "graph", "pattern", "report"}
PROMPTS = {".agents", ".claude", ".codex"}
PROMPT_FILES = {"AGENTS.md", "CLAUDE.md"}
CALLOUT_LIMIT = 3
CALLOUT_EXEMPT = {"rules/callout.rules.md"}
TAGS = {
    "kind": {"rule", "component", "runbook", "template", "pattern", "journal"},
    "layer": {"frontend", "backend", "database", "infra", "docs"},
    "topic": {"security", "accessibility", "data", "ux", "state", "workflow", "deploy", "memory", "performance"},
    "project": None,
}
WORKFLOW_KINDS = {"rule", "component", "runbook", "template"}
COUNT_BADGES = {
    "Rules": ("rules/*.md",),
    "Components": ("component/**/*.md",),
    "Templates": ("template/*.template.*", "cloud/**/*.template.*"),
    "Agents": (".agents/agents/*.md",),
    "Skills": (".agents/skills/*/SKILL.md",),
}

ARROWS = ((0x2190, 0x21FF), (0x27F0, 0x27FF), (0x2900, 0x297F), (0x2B00, 0x2BFF))
PICTOGRAPHS = ((0x2300, 0x23FF), (0x25A0, 0x25FF), (0x2600, 0x27BF), (0x1F000, 0x1FAFF), (0xFE0F, 0xFE0F))
SMART_QUOTES = {0x2018, 0x2019, 0x201C, 0x201D}

FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
INLINE_CODE = re.compile(r"(`+).+?\1")
LIST_ITEM = re.compile(r"^\s*([-*+]|\d+[.)])\s")
BLOCK_START = re.compile(r"^\s*(#|>|\||<|!\[|\[[^\]]+\]:|([-*_])\s*\2\s*\2)")
RULE_LINE = re.compile(r"^ {0,3}([-*_])(\s*\1){2,}\s*$")
CALLOUT = re.compile(r"^\s*(>\s*)+\[![A-Za-z-]+\]")
STYLED = re.compile(r'<\w+\s+style="color[^"]*"')
STATUS = re.compile(r'<code style="color: (green|yellow|red)">')
WIKILINK = re.compile(r"\[\[([^\]|#]*)[^\]]*\]\]")
TOC_LINK = re.compile(r"\]\(#([^)]+)\)")
COUNT_BADGE = re.compile(r"img\.shields\.io/badge/([^-)]+)-(\d+)-")


def parse(rel, text):
    lines = text.splitlines()
    code, opens, fence = [], {}, None
    for i, line in enumerate(lines):
        m = FENCE.match(line)
        if fence is None and m:
            fence, opens[i] = m.group(1), m.group(2).strip()
            code.append(True)
        elif fence is not None:
            code.append(True)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip():
                fence = None
        else:
            code.append(False)
    fm_end = 0
    if lines and lines[0] == "---":
        fm_end = next((i + 1 for i in range(1, len(lines)) if lines[i] == "---"), 0)
    return {"path": rel, "lines": lines, "code": code, "opens": opens, "fm_end": fm_end}


def prose(doc):
    """Yield (line number, line) for every line outside the frontmatter and fenced code."""
    for i, line in enumerate(doc["lines"]):
        if i >= doc["fm_end"] and not doc["code"][i]:
            yield i + 1, line


def tags(doc):
    lines = doc["lines"][: doc["fm_end"]]
    for i, line in enumerate(lines):
        if line.startswith("tags:"):
            inline = line[5:].strip()
            if inline:
                return [(i + 1, t.strip(" '\"")) for t in inline.strip("[]").split(",") if t.strip()]
            found = []
            for j in range(i + 1, len(lines)):
                m = re.match(r"^\s+-\s*(\S+)", lines[j])
                if not m:
                    break
                found.append((j + 1, m.group(1).strip("'\"")))
            return found
    return []


def banned_name(text, i):
    c = ord(text[i])
    if c == 0x2014:
        return "em dash"
    if c == 0x2013 and not (text[i - 1 : i].isdigit() and text[i + 1 : i + 2].isdigit()):
        return "en dash used as punctuation"
    if c in SMART_QUOTES:
        return "smart quote"
    if any(lo <= c <= hi for lo, hi in ARROWS):
        return "unicode arrow"
    if any(lo <= c <= hi for lo, hi in PICTOGRAPHS):
        return "emoji or pictograph"
    return None


def check_banned_chars(doc, vault):
    for n, line in enumerate(doc["lines"], 1):
        found = {}
        for i, ch in enumerate(line):
            if ord(ch) > 0x2000 and ch not in found and (name := banned_name(line, i)):
                found[ch] = name
        for ch, name in found.items():
            yield n, f"U+{ord(ch):04X} ({name})"


def check_trailing_whitespace(doc, vault):
    for n, line in enumerate(doc["lines"], 1):
        if line != line.rstrip():
            yield n, "trailing whitespace"


FILLER = re.compile(r"\b(basically|simply|in order to|it should be noted that)\b", re.I)
QUOTED = re.compile(r'"[^"]*"|`[^`]*`')


def check_filler(doc, vault):
    for n, line in prose(doc):
        match = FILLER.search(QUOTED.sub("", line))
        if match:
            yield n, f"filler: delete `{match.group(0)}`"


def line_kind(line):
    if not line.strip():
        return "blank"
    if BLOCK_START.match(line):
        return "block"
    if LIST_ITEM.match(line):
        return "list"
    return "continuation" if line[0] in " \t" else "prose"


def check_hard_wrap(doc, vault):
    rows = list(prose(doc))
    for (n, line), (m, after) in zip(rows, rows[1:]):
        if m == n + 1 and line_kind(line) in ("prose", "list") and line_kind(after) in ("prose", "continuation"):
            yield n, "paragraph or list item continues on the next line; write it as one line"


def check_blank_lines(doc, vault):
    rows = list(prose(doc))
    for (n, line), (m, after) in zip(rows, rows[1:]):
        if m == n + 1 and not line.strip() and not after.strip():
            yield m, "more than one blank line between blocks"


def check_fence_language(doc, vault):
    for i, info in doc["opens"].items():
        if not info:
            yield i + 1, "fenced code block without a language tag"


def check_horizontal_rule(doc, vault):
    for n, line in prose(doc):
        if RULE_LINE.match(line):
            yield n, "horizontal rule in the body"


def check_callout_limit(doc, vault):
    if doc["path"] in CALLOUT_EXEMPT:
        return
    starts = [n for n, line in prose(doc) if CALLOUT.match(line)]
    for count, n in enumerate(starts[CALLOUT_LIMIT:], CALLOUT_LIMIT + 1):
        yield n, f"callout {count} of {len(starts)}; the limit is {CALLOUT_LIMIT} per document"


def check_status_indicator(doc, vault):
    for n, line in prose(doc):
        line = INLINE_CODE.sub("", line)
        for m in STYLED.finditer(line):
            if not STATUS.match(line, m.start()):
                yield n, 'status indicator is not <code style="color: green|yellow|red">'


def check_tags(doc, vault):
    found = tags(doc)
    if not found:
        return
    axes = [t.split("/", 1)[0] for _, t in found]
    for n, tag in found:
        axis, _, value = tag.partition("/")
        if axis not in TAGS or not value or (TAGS[axis] is not None and value not in TAGS[axis]):
            yield n, f"tag {tag} is not in the closed lists"
    first = found[0][0]
    if axes.count("kind") != 1:
        yield first, f"{axes.count('kind')} kind/ tags; exactly one is required"
    if axes.count("topic") > 2:
        yield first, f"{axes.count('topic')} topic/ tags; at most two"
    if "project" in axes and "kind/journal" not in [t for _, t in found]:
        yield first, "project/ tag on a document that is not a journal"


def check_breadcrumb(doc, vault):
    if not tags(doc):
        return
    first = next(((n, line) for n, line in prose(doc) if line.strip()), (doc["fm_end"], ""))
    if not first[1].startswith("> Up: [["):
        yield first[0], "breadcrumb > Up: [[...]] is not directly under the frontmatter"


def check_workflow(doc, vault):
    kinds = {t.split("/", 1)[1] for _, t in tags(doc) if t.startswith("kind/")}
    if not kinds & WORKFLOW_KINDS:
        return
    in_section = False
    for i, line in enumerate(doc["lines"]):
        if doc["code"][i] and i not in doc["opens"]:
            continue
        if line.startswith("## "):
            in_section = line.strip() == "## Workflow"
        elif in_section and doc["opens"].get(i) == "mermaid":
            return
    yield doc["fm_end"] or 1, "no ## Workflow section with a mermaid diagram"


def resolves(target, rel, vault):
    if not target or target.endswith(".memory.md"):
        return True
    if "/" not in target:
        return target in vault["names"]
    if PurePosixPath(target).parts[0] in LOCAL:
        return True
    near = os.path.normpath(os.path.join(os.path.dirname(rel), target)).replace("\\", "/")
    return near in vault["paths"] or any(p == target or p.endswith("/" + target) for p in vault["paths"])


def check_wikilinks(doc, vault):
    for n, line in prose(doc):
        for m in WIKILINK.finditer(INLINE_CODE.sub("", line)):
            target = m.group(1).strip().rstrip("\\")
            if resolves(target, doc["path"], vault):
                continue
            if resolves(target + ".md", doc["path"], vault):
                yield n, f"[[{target}]] lacks its .md extension"
            else:
                yield n, f"[[{target}]] names no file in the vault"


def heading_slug(text):
    return re.sub(r"[^\w\- ]", "", text.strip().lower()).replace(" ", "-")


def check_toc(doc, vault):
    if tags(doc):
        return
    rows = list(prose(doc))
    headings = [(n, line[3:].strip()) for n, line in rows if line.startswith("## ")]
    toc = next((n for n, h in headings if h == "Table of Contents"), None)
    if toc is None:
        return
    end = next((n for n, _ in headings if n > toc), len(doc["lines"]) + 1)
    anchors = {a for n, line in rows if toc < n < end for a in TOC_LINK.findall(line)}
    slugs = {heading_slug(h) for n, h in headings if n != toc}
    for n, h in headings:
        if n != toc and heading_slug(h) not in anchors:
            yield n, f"heading '{h}' is missing from the Table of Contents"
    for a in sorted(anchors - slugs):
        yield toc, f"Table of Contents entry #{a} names no ## heading"


def check_badge_counts(doc, vault):
    if doc["path"] != "README.md":
        return
    for n, line in enumerate(doc["lines"], 1):
        for label, value in COUNT_BADGE.findall(line):
            label = label.replace("_", " ")
            if label in vault["counts"] and int(value) != vault["counts"][label]:
                globs = " + ".join(COUNT_BADGES[label])
                yield n, f"{label} badge says {value}, {globs} holds {vault['counts'][label]}"


CHECKS = {
    "banned-char": check_banned_chars,
    "trailing-whitespace": check_trailing_whitespace,
    "filler": check_filler,
    "hard-wrap": check_hard_wrap,
    "blank-lines": check_blank_lines,
    "fence-language": check_fence_language,
    "horizontal-rule": check_horizontal_rule,
    "callout-limit": check_callout_limit,
    "status-indicator": check_status_indicator,
    "tags": check_tags,
    "breadcrumb": check_breadcrumb,
    "workflow": check_workflow,
    "wikilink": check_wikilinks,
    "toc": check_toc,
    "badge-count": check_badge_counts,
}


def checks_for(rel):
    first = PurePosixPath(rel).parts[0]
    if first in LOCAL:
        return []
    if first in PROMPTS or rel in PROMPT_FILES:
        return ["banned-char"]
    return list(CHECKS)


def build_vault():
    names, paths = set(), set()
    for folder, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("__pycache__", "node_modules")]
        for name in files:
            names.add(name)
            paths.add((Path(folder) / name).relative_to(ROOT).as_posix())
    counts = {
        label: len({p for g in globs for p in ROOT.glob(g) if p.is_file() and p.name != "README.md"})
        for label, globs in COUNT_BADGES.items()
    }
    return {"names": names, "paths": paths, "counts": counts}


def git_files(*args):
    out = subprocess.run(["git", *args, "-z"], cwd=ROOT, capture_output=True, encoding="utf-8", check=True).stdout
    return [p for p in out.split("\0") if p]


def target_files(args):
    if args.all:
        return git_files("ls-files", "--cached", "--others", "--exclude-standard")
    if args.changed:
        return git_files("ls-files", "--modified", "--others", "--exclude-standard") + git_files("diff", "--cached", "--name-only", "--diff-filter=ACM")
    rels = []
    for p in args.paths:
        path = Path(p).resolve()
        rels.append(path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix())
    return rels


def check_file(rel, text, vault):
    doc = parse(rel, text)
    for name in checks_for(rel):
        for n, message in CHECKS[name](doc, vault):
            yield f"{rel}:{n}: {name}: {message}"


SELF_TEST = {
    "banned-char": (
        "rules/x.md",
        "A {} B {} done {} ok {} {}q{}\n".format(*map(chr, (0x2192, 0x2014, 0x2013, 0x1F680, 0x201C, 0x201D))),
        'A > B - done, pages 10{}20, "q".\n'.format(chr(0x2013)),
    ),
    "trailing-whitespace": ("rules/x.md", "text  \n", "text\n"),
    "filler": ("rules/x.md", "Run it in order to check.\n", 'Delete "simply" and `basically`.\n\n```text\nsimply\n```\n'),
    "hard-wrap": (
        "rules/x.md",
        "One sentence that\ncontinues here.\n\n- an item that\n  wraps\n",
        "# T\n\nOne line.\n\n- item\n- item\n  - nested\n\n| a |\n| - |\n\n```text\nwrapped\nlines\n```\n",
    ),
    "blank-lines": ("rules/x.md", "a\n\n\nb\n", "a\n\nb\n\n```text\n\n\n```\n"),
    "fence-language": ("rules/x.md", "```\nls\n```\n", "```bash\nls\n```\n\n````markdown\n```\nx\n```\n````\n"),
    "horizontal-rule": (
        "rules/x.md",
        "---\ntags:\n  - kind/rule\n---\n\ntext\n\n---\n",
        "---\ntags:\n  - kind/rule\n---\n\ntext\n\n```text\n---\n```\n",
    ),
    "callout-limit": (
        "rules/x.md",
        "> [!info]\n> a\n\n> [!note]\n> b\n\n> [!tip]\n> c\n\n> [!warning]\n> d\n",
        "> [!info]\n> a\n\n> [!note]\n> b\n\n> [!tip]\n> c\n\n```markdown\n> [!warning]\n```\n",
    ),
    "status-indicator": (
        "rules/x.md",
        '<code style="color:red">Not Used</code>\n<span style="color: red">X</span>\n',
        '<code style="color: red">Not Used</code> not `<span style="color: red">`\n',
    ),
    "tags": (
        "rules/x.md",
        "---\ntags:\n  - kind/rule\n  - kind/component\n  - topic/auth\n---\n",
        "---\ntags:\n  - kind/rule\n  - layer/docs\n  - topic/workflow\n---\n",
    ),
    "breadcrumb": ("rules/x.md", "---\ntags:\n  - kind/rule\n---\n\n# Title\n", "---\ntags:\n  - kind/rule\n---\n\n> Up: [[README.md]]\n"),
    "workflow": (
        "rules/x.md",
        "---\ntags:\n  - kind/rule\n---\n\n## Workflow\n\nText.\n\n## Other\n\n```mermaid\nflowchart TD\n```\n",
        "---\ntags:\n  - kind/rule\n---\n\n## Workflow\n\n```mermaid\nflowchart TD\n  A --> B\n```\n",
    ),
    "wikilink": (
        "rules/x.md",
        "See [[missing.md]] and [[commit.rules]].\n",
        "[[commit.rules.md]], [[README.md|home]], [[agents/qa/SKILL.md]], [[graph/README.md]], `[[no.md]]`,"
        " [[x.decision.memory.md]], [[commit.rules.md#Tags]]\n\n```text\n[[no.md]]\n```\n",
    ),
    "toc": (
        "README.md",
        "# T\n\n## Table of Contents\n\n1. [Setup](#setup)\n2. [Gone](#gone)\n\n## Setup\n\n## Usage\n",
        "# T\n\n## Table of Contents\n\n1. [Setup](#setup)\n2. [Known Limitations](#known-limitations)\n\n## Setup\n\n## Known Limitations\n",
    ),
    "badge-count": (
        "README.md",
        "![Rules](https://img.shields.io/badge/Rules-3-4C1D95)\n",
        "![Rules](https://img.shields.io/badge/Rules-2-4C1D95)\n![Python](https://img.shields.io/badge/Python-3.13-3776AB)\n",
    ),
}


def self_test():
    vault = {
        "names": {"README.md", "commit.rules.md", "SKILL.md"},
        "paths": {"README.md", "rules/commit.rules.md", "agents/qa/SKILL.md"},
        "counts": {"Rules": 2},
    }
    failures = []
    for name, (rel, bad, good) in SELF_TEST.items():
        if not list(CHECKS[name](parse(rel, bad), vault)):
            failures.append(f"{name} missed its bad sample")
        if hits := list(CHECKS[name](parse(rel, good), vault)):
            failures.append(f"{name} flagged its good sample: {hits}")
    failures += [f"{name} has no self-test" for name in CHECKS if name not in SELF_TEST]
    if checks_for("memory/a.md") or checks_for("report/p/a.md"):
        failures.append("a local folder is checked")
    if checks_for(".agents/agents/a.md") != ["banned-char"] or checks_for("AGENTS.md") != ["banned-char"]:
        failures.append("an agent prompt gets more than the banned-character check")
    for failure in failures:
        print(f"self-test: {failure}")
    print(f"self-test: {len(CHECKS)} checks, {len(failures)} failures")
    return 1 if failures else 0


def main(argv=None):
    sys.stdout.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Check Markdown documents against rules/docs.rules.md.")
    parser.add_argument("paths", nargs="*", help="files to check")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--changed", action="store_true", help="files git reports as modified, added, or untracked")
    mode.add_argument("--all", action="store_true", help="every tracked or untracked non-ignored .md file")
    mode.add_argument("--self-test", action="store_true", help="run every check against a bad and a good sample")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    rels = sorted({rel for rel in target_files(args) if rel.endswith(".md")})
    vault = build_vault() if rels else {}
    violations = []
    for rel in rels:
        path = Path(rel) if Path(rel).is_absolute() else ROOT / rel
        if path.is_file():
            violations += check_file(rel, path.read_text(encoding="utf-8-sig", errors="replace"), vault)
    if violations:
        print("\n".join(violations))
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
