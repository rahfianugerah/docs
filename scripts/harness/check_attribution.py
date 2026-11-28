"""Fail when a commit message or a file credits a tool or a model for the work."""

import argparse
import re
import subprocess
import sys
from pathlib import Path

BOTS = r"(claude|anthropic|codex|openai|chatgpt|copilot|cursor|gemini|devin)"
TRAILER = re.compile(rf"^\s*[\w-]+-by:.*\b{BOTS}\b", re.I | re.M)
BOT_ADDRESS = re.compile(r"noreply@(anthropic|openai)\.com", re.I)
GENERATED = re.compile(rf"generated\s+(with|by)\s+\W*{BOTS}\b|\U0001F916", re.I)
# A document may show this line as the example of what is forbidden; a commit message may not carry it.
GENERIC_CREDIT = re.compile(r"(generated|created|written)\s+(with|by)\s+(an?\s+)?ai\b", re.I)
SESSION_LINK = re.compile(r"claude\.ai/code/|chatgpt\.com/codex/", re.I)
NAMED = re.compile(rf"\b{BOTS}\b", re.I)
PATH_TOKEN = re.compile(r"\S*[./\\]\S*")

ANYWHERE = [
    (TRAILER, "a trailer credits a tool"),
    (BOT_ADDRESS, "a tool's no-reply address"),
    (GENERATED, "a generated-with line"),
    (SESSION_LINK, "a session link"),
]


def problems(text, message=False):
    found = [reason for pattern, reason in ANYWHERE if pattern.search(text)]
    if message:
        prose = "\n".join(PATH_TOKEN.sub(" ", line) for line in text.splitlines() if not line.startswith("#"))
        if GENERIC_CREDIT.search(prose):
            found.append("a generated-with line")
        match = NAMED.search(prose)
        if match:
            found.append(f"names `{match.group(0)}`; a commit message names no tool or vendor")
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
    parser = argparse.ArgumentParser(description=__doc__)
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
    revision_range = args.commits or ("@{upstream}..HEAD" if args.all and git("rev-parse", "--abbrev-ref", "@{upstream}").strip() else None)
    if revision_range:
        found += check_commits(revision_range)

    for line in found:
        print(line, file=sys.stderr)
    if found:
        print("The work is attributed to the owner alone. Remove the credit and try again.", file=sys.stderr)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
