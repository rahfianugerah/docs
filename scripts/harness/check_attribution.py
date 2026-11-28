"""Fail when a commit message or a file credits a tool or a model for the work.

A list of names is never complete. The check stops the known forms; the rule itself is in AGENTS.md.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Named only for a tool, so any mention in a commit message is a credit.
ALWAYS = r"claude|anthropic|openai|chatgpt|copilot|codex|gpt|deepseek|qwen|llms?"
# Also ordinary words (a cursor, a fable, a haiku), so they count only capitalised and only after "with", "by", and the like.
IN_CREDIT = r"Cursor|Gemini|Devin|Grok|Llama|Mistral|Bard|Aider|Windsurf|Cline|Opus|Sonnet|Haiku|Fable|AI|LLM|o[134]"
VERSIONED = r"(opus|sonnet|haiku|fable|gemini|grok|llama|mistral)[- ]\d"

# A document may show a generic trailer as the example of what is forbidden, so a file is flagged only for a named tool.
TOOL_TRAILER = re.compile(rf"^\s*[\w-]+-by:.*\b({ALWAYS}|cursor|gemini|devin|grok|aider)\b", re.I | re.M)
BOT_ADDRESS = re.compile(r"noreply@(anthropic|openai)\.com", re.I)
GENERATED = re.compile(rf"generated\s+(with|by)\s+\W*({ALWAYS}|cursor|gemini)\b|\U0001F916", re.I)
SESSION_LINK = re.compile(r"claude\.ai/code/|chatgpt\.com/codex/", re.I)

# The owner works alone: a commit message carries no co-author or assistant trailer, whoever it names.
SHARED_CREDIT_TRAILER = re.compile(r"^\s*(co-?authored|assisted|generated|written|created|suggested|helped|pair(ed)?[\w-]*)-by:", re.I | re.M)
NAMED = re.compile(rf"\b({ALWAYS})|\b{VERSIONED}", re.I)
CREDITED = re.compile(rf"\b(with|by|using|via|thanks\s+to|help\s+of|assistance\s+of)\s+(the\s+|an?\s+)?({IN_CREDIT})\b")
AI_MADE = re.compile(r"\b(ai|llm)[- ](assisted|generated|written|authored)\b", re.I)
# `.claude/agents`, `CLAUDE.md`, and `scripts/harness/` are files, not credits. `claude/opus` is not a file.
PATH_TOKEN = re.compile(
    r"(?<![\w/])[.~][\w.-]*/[\w./~-]*"
    r"|\b[\w.-]+(?:/[\w.-]+)*\.(?:md|json|toml|py|js|ts|ya?ml|txt|sh)\b"
    r"|(?<![\w/])[\w.-]+(?:/[\w.-]+)*/(?![\w.-])"
    r"|(?<![\w/])\.[A-Za-z][\w-]*"
)

IN_ANY_TEXT = [
    (TOOL_TRAILER, "a trailer credits a tool"),
    (BOT_ADDRESS, "a tool's no-reply address"),
    (GENERATED, "a generated-with line"),
    (SESSION_LINK, "a session link"),
]
IN_A_MESSAGE = [
    (SHARED_CREDIT_TRAILER, "a co-author or assistant trailer; the work is the owner's alone"),
    (AI_MADE, "says a model made it"),
    (CREDITED, "credits a tool or a model"),
    (NAMED, "names a tool, a vendor, or a model"),
]


def problems(text, message=False):
    found = [reason for pattern, reason in IN_ANY_TEXT if pattern.search(text)]
    if message:
        lines = [line for line in text.splitlines() if not line.startswith("#")]
        if not "\n".join(lines).isascii():
            # A look-alike letter or a typographic dash is how a name gets past a pattern.
            found.append("is not plain ASCII")
        prose = "\n".join(PATH_TOKEN.sub(" ", line) for line in lines)
        for pattern, reason in IN_A_MESSAGE:
            match = pattern.search(prose)
            if match:
                found.append(f"{reason}: `{match.group(0).strip()}`")
    return found


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


def check_files(paths, read):
    return [f"{path}: {reason}" for path in paths for reason in problems(read(path))]


def check_commits(revision_range):
    out = []
    for commit in git("log", "--format=%H", revision_range).split():
        out += [f"commit {commit[:7]}: {reason}" for reason in problems(git("log", "-1", "--format=%B", commit), message=True)]
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--message", type=Path, help="a commit message file, as the commit-msg hook passes it")
    parser.add_argument("--text", help="a string, such as the command about to be run")
    parser.add_argument("--staged", action="store_true", help="the staged files")
    parser.add_argument("--commits", metavar="RANGE", help="the commit messages in a revision range")
    parser.add_argument("--all", action="store_true", help="every tracked file, and the commits not yet pushed")
    args = parser.parse_args()

    found = []
    if args.message:
        found += [f"commit message: {reason}" for reason in problems(args.message.read_text(encoding="utf-8", errors="replace"), message=True)]
    if args.text:
        found += [f"command: {reason}" for reason in problems(args.text)]
    if args.staged:
        staged = git("diff", "--cached", "--name-only", "--diff-filter=ACM").splitlines()
        found += check_files(staged, lambda path: git("show", f":{path}"))
    if args.all:
        tracked = git("ls-files").splitlines()
        found += check_files(tracked, lambda path: Path(path).read_text(encoding="utf-8", errors="replace") if Path(path).is_file() else "")
    revision_range = args.commits
    if args.all and not revision_range:
        if git("rev-parse", "--abbrev-ref", "@{upstream}").strip():
            revision_range = "@{upstream}..HEAD"
        else:
            print("note: this branch has no upstream, so no commit message was checked; pass --commits RANGE", file=sys.stderr)
    if revision_range:
        found += check_commits(revision_range)

    for line in found:
        print(line, file=sys.stderr)
    if found:
        print("The work is attributed to the owner alone. Remove the credit and try again.", file=sys.stderr)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
