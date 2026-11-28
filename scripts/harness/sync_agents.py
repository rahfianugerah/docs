"""Generate every tool's agent files from .agents/, or check that they are in sync."""

import argparse
import importlib
import json
import re
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

TIERS = ("deep", "build", "fast")
TOOLS = ("read", "search", "edit", "run", "web", "delegate")
HEADINGS = ["## Job", "## Read first", "## Do", "## Never", "## Ask the advisor when", "## Output"]
OPTIONAL_HEADING = "## Ask the advisor when"
NAME = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*\Z")
MODEL_WORD = re.compile(r"\b(opus|sonnet|haiku|fable|grok|gemini|llama|mistral|deepseek|gpt[- ]?\d|claude-[a-z]+-\d)", re.I)
SKILL_KEYS = {"name", "description"}
# Other tools read this frontmatter as real YAML, where these would start a mapping, a comment, or a quoted scalar.
UNSAFE_YAML = re.compile(r": | #|:$|^[\"'\[\]{}>|*&!%@`]")
# The standards folders only: `harness/usage/` and `harness/generated.json` are written at run time.
REPO_PATH = re.compile(r"`((rules|component|template|cloud|ai)/[\w./-]+)`")
OTHER_SKILL = re.compile(r"\.\./[\w-]+/(SKILL\.md|references/|assets/|scripts/)")
HOOK_EVENTS = ("after-edit", "on-stop", "before-commit", "after-agent")
SKILL_PREFIX = "agentic-"
# `scripts/harness/...` names a script of the harness itself, not a file of the skill.
SKILL_FILE_REF = re.compile(r"`((?:references|assets|scripts)/(?!harness/)[^`\s]+)`")
ROSTER = ".agents/skills/agentic-orchestrate/references/roster.md"
LESSON_FIELDS = {
    "Lesson:": None,
    "Evidence:": None,
    "Confidence:": {"low", "medium", "high"},
    "Verdict:": {"helped", "hurt", "no observed effect", "confounded"},
}


def parse(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("has no frontmatter")
    head, sep, body = text[4:].partition("\n---\n")
    if not sep:
        raise ValueError("frontmatter is not closed")
    meta = {}
    for line in head.splitlines():
        key, colon, value = line.partition(":")
        if not colon or not key or key != key.strip():
            raise ValueError(f"frontmatter line is not `key: value`: {line!r}")
        meta[key] = value.strip()
    return meta, body.lstrip("\n")


def load_agents(root, budget, errors):
    agents = []
    for path in sorted((root / ".agents/agents").glob("*.md")):
        if path.name == "README.md":
            continue
        rel = path.relative_to(root).as_posix()
        try:
            meta, body = parse(path)
        except ValueError as error:
            errors.append(f"{rel}: {error}")
            continue
        if set(meta) != {"name", "description", "tier", "tools"}:
            errors.append(f"{rel}: frontmatter keys must be exactly name, description, tier, tools")
            continue
        tools = [tool.strip() for tool in meta["tools"].split(",")]
        if meta["name"] != path.stem or not NAME.match(meta["name"]):
            errors.append(f"{rel}: name must be kebab-case and equal the file name")
        if meta["tier"] not in TIERS:
            errors.append(f"{rel}: tier must be one of {', '.join(TIERS)}")
        if not meta["description"] or UNSAFE_YAML.search(meta["description"]):
            errors.append(f"{rel}: description must be one plain line, with no `: `, no ` #`, and no leading quote or bracket")
        if len(meta["description"]) > budget["agent_description_max_chars"]:
            errors.append(f"{rel}: description is {len(meta['description'])} characters, over the budget of {budget['agent_description_max_chars']}")
        reviewer = meta["name"] == "verifier" or meta["name"].endswith("-reviewer")
        if reviewer and "edit" in tools:
            errors.append(f"{rel}: a verifier or a reviewer never has the `edit` tool")
        if "delegate" in tools and meta["name"] != "orchestrator":
            errors.append(f"{rel}: only the orchestrator has the `delegate` tool")
        unknown = [tool for tool in tools if tool not in TOOLS]
        if unknown:
            errors.append(f"{rel}: unknown tools {unknown}; the vocabulary is {', '.join(TOOLS)}")
        text = path.read_text(encoding="utf-8")
        if MODEL_WORD.search(text):
            errors.append(f"{rel}: names a model ({MODEL_WORD.search(text).group(0)}); name a tier instead")
        found = [line for line in body.splitlines() if line.startswith("## ")]
        wanted = [h for h in HEADINGS if h != OPTIONAL_HEADING or meta["tier"] != "deep"]
        if found != wanted:
            errors.append(f"{rel}: body headings must be {', '.join(wanted)}, in that order; a deep agent has no advisor section")
        check_paths(root, rel, text, errors)
        lines = len(text.splitlines())
        if lines > budget["agent_max_lines"]:
            errors.append(f"{rel}: {lines} lines, over the budget of {budget['agent_max_lines']}")
        agents.append({**meta, "tools": tools, "body": body})
    return agents


def load_skills(root, budget, errors):
    skills = []
    base = root / ".agents/skills"
    for folder in sorted(path for path in base.iterdir() if path.is_dir()):
        rel = folder.relative_to(root).as_posix()
        if not folder.name.startswith(SKILL_PREFIX):
            errors.append(f"{rel}: a skill folder must start with `{SKILL_PREFIX}`")
            continue
        try:
            meta, _ = parse(folder / "SKILL.md")
        except (ValueError, FileNotFoundError) as error:
            errors.append(f"{rel}/SKILL.md: {error}")
            continue
        if set(meta) != SKILL_KEYS:
            errors.append(f"{rel}/SKILL.md: frontmatter keys must be exactly name and description")
        if UNSAFE_YAML.search(meta.get("description", "")):
            errors.append(f"{rel}/SKILL.md: description must be one plain line, with no `: `, no ` #`, and no leading quote or bracket")
        if meta.get("name") != folder.name or not NAME.match(folder.name) or len(folder.name) > 64:
            errors.append(f"{rel}/SKILL.md: name must equal the folder name, kebab-case, 64 characters at most")
        if not 1 <= len(meta.get("description", "")) <= budget["skill_description_max_chars"]:
            errors.append(f"{rel}/SKILL.md: description must be 1 to {budget['skill_description_max_chars']} characters")
        text = (folder / "SKILL.md").read_text(encoding="utf-8")
        lines = len(text.splitlines())
        if lines > budget["skill_max_lines"]:
            errors.append(f"{rel}/SKILL.md: {lines} lines, over the budget of {budget['skill_max_lines']}")
        files = {
            path.relative_to(folder).as_posix(): path.read_bytes()
            for path in sorted(folder.rglob("*"))
            if path.is_file()
        }
        for ref in sorted(set(SKILL_FILE_REF.findall(text))):
            if ref not in files and f"{rel}/{ref}" != ROSTER:
                errors.append(f"{rel}/SKILL.md: names `{ref}`, which is not in the skill folder")
        for name, content in files.items():
            if name.endswith(".md"):
                page = content.decode("utf-8", errors="replace")
                if OTHER_SKILL.search(page):
                    errors.append(f"{rel}/{name}: reaches into another skill's folder; a skill is self-contained")
                check_paths(root, f"{rel}/{name}", page, errors)
        skills.append({"name": folder.name, "description": meta.get("description", ""), "files": files})
    return skills


def check_paths(root, rel, text, errors):
    """A path an agent is told to read exists. Skipped where the harness was copied without that folder."""
    for ref, top in sorted(set(REPO_PATH.findall(text))):
        if (root / top).is_dir() and not (root / ref).exists():
            errors.append(f"{rel}: names `{ref}`, which does not exist")


def check_listed(root, index, names, key_prefix, errors):
    """Every name has a row in its folder's README, and a BibTeX entry keyed after it."""
    path = root / index
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    for name in names:
        key = key_prefix + re.sub(r"[.-]", "_", name.removesuffix(".md"))
        # The name as a whole word in the first cell of a table row: `verifier` is not found in `formal-verifier`.
        if not re.search(r"^\|[^|\n]*(?<![\w.-])" + re.escape(name) + r"(?![\w.-])[^|\n]*\|", text, re.M):
            errors.append(f"{index}: has no row for `{name}`")
        if not re.search(r"@\w+\{" + re.escape(key) + ",", text):
            errors.append(f"{index}: has no citation keyed `{key}`")


def check_handbook(root, agents, skills, budget, errors):
    for name in ("AGENTS.md", "CLAUDE.md"):
        path = root / name
        if path.exists():
            lines = len(path.read_text(encoding="utf-8").splitlines())
            if lines > budget["agents_md_max_lines"]:
                errors.append(f"{name}: {lines} lines, over the budget of {budget['agents_md_max_lines']}")
    if not (root / "AGENTS.md").exists():
        errors.append("AGENTS.md: missing")
        return
    text = (root / "AGENTS.md").read_text(encoding="utf-8")
    for skill in skills:
        if f"/{skill['name']}`" not in text:
            errors.append(f"AGENTS.md: never names `/{skill['name']}`, so nothing triggers that skill")
    for agent in agents:
        if agent["name"] != "orchestrator" and f"`{agent['name']}`" not in text:
            errors.append(f"AGENTS.md: never names `{agent['name']}`, so nothing routes to that agent")
    check_listed(root, ".agents/agents/README.md", [agent["name"] for agent in agents], "agent_", errors)
    check_listed(root, ".agents/skills/README.md", [skill["name"] for skill in skills], "skill_", errors)
    if (root / "rules").is_dir():
        rules = [path.name for path in sorted((root / "rules").glob("*.md")) if path.name != "README.md"]
        check_listed(root, "rules/README.md", rules, "rule_", errors)


def check_lessons(root, errors):
    path = root / "harness/lessons.md"
    if not path.exists():
        return
    entries = path.read_text(encoding="utf-8").split("\n### ")[1:]
    for entry in entries:
        cue = entry.splitlines()[0]
        for field, allowed in LESSON_FIELDS.items():
            value = next((line[len(field):].strip() for line in entry.splitlines() if line.startswith(field)), None)
            if not value:
                errors.append(f"harness/lessons.md: the entry `{cue}` has no `{field}` line")
            elif allowed and value not in allowed:
                errors.append(f"harness/lessons.md: the entry `{cue}` has `{field} {value}`; use one of {sorted(allowed)}")


def roster(agents):
    rows = sorted(agents, key=lambda agent: (TIERS.index(agent["tier"]) if agent["tier"] in TIERS else 9, agent["name"]))
    lines = ["# Roster", "", "| Agent | Tier | Launch it to |", "| :- | :- | :- |"]
    lines += [f"| `{a['name']}` | {a['tier']} | {a['description']} |" for a in rows]
    return "\n".join(lines) + "\n"


def build(root, scope):
    """Every generated file as {absolute path: bytes}, with the errors and warnings met on the way."""
    errors, warnings, files, owned = [], [], {}, set()
    config = tomllib.loads((root / ".agents/targets.toml").read_text(encoding="utf-8"))
    budget = config["budget"]
    hooks = tomllib.loads((root / ".agents/hooks.toml").read_text(encoding="utf-8")).get("hook", [])
    agents = load_agents(root, budget, errors)
    skills = load_skills(root, budget, errors)
    check_handbook(root, agents, skills, budget, errors)
    unknown = sorted({hook["event"] for hook in hooks} - set(HOOK_EVENTS))
    if unknown:
        errors.append(f".agents/hooks.toml: unknown events {unknown}; the events are {', '.join(HOOK_EVENTS)}")
        hooks = [hook for hook in hooks if hook["event"] in HOOK_EVENTS]
    check_lessons(root, errors)

    roster_bytes = roster(agents).encode("utf-8")
    for skill in skills:
        if f".agents/skills/{skill['name']}/references/roster.md" == ROSTER:
            skill["files"]["references/roster.md"] = roster_bytes
    if scope == "repo":
        files[root / ROSTER] = roster_bytes

    for name, target in config["targets"].items():
        missing = [tier for tier in TIERS if tier not in target.get("models", {})]
        if missing:
            errors.append(f".agents/targets.toml: target `{name}` maps no model to the tier {missing}")
            continue
        adapter = importlib.import_module(f"adapters.{target.get('adapter', name)}")
        folders = {
            "agents": target.get("agents_dir" if scope == "repo" else "user_agents_dir", ""),
            "skills": target.get("skills_dir" if scope == "repo" else "user_skills_dir", ""),
        }
        for (kind, rel), content in adapter.render(agents, skills, target).items():
            if folders[kind]:
                base = Path(folders[kind]).expanduser() if scope == "user" else root / folders[kind]
                files[base / rel] = content if isinstance(content, bytes) else content.encode("utf-8")
        if scope == "repo":
            owned.update(root / folder for folder in folders.values() if folder)
        if scope == "repo" and target.get("hooks_file"):
            path = root / target["hooks_file"]
            existing = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
            files[path] = (json.dumps(adapter.render_hooks(hooks, existing), indent=2) + "\n").encode("utf-8")
        warnings += [f"{name}: {warning}" for warning in adapter.warnings(agents, hooks)]
    return files, errors, warnings, owned


def manifest_path(root, scope):
    return root / "harness/generated.json" if scope == "repo" else Path("~/.agents/agentic-generated.json").expanduser()


def label(path, root, scope):
    return path.relative_to(root).as_posix() if scope == "repo" else path.as_posix()


def same(path, content):
    return path.exists() and path.read_bytes().replace(b"\r\n", b"\n") == content.replace(b"\r\n", b"\n")


def can_create(root, name):
    if not NAME.match(name):
        return f"`{name}` is not kebab-case"
    if (root / ".agents/agents" / f"{name}.md").exists():
        return f"the agent `{name}` already exists; extend it instead of creating a second one"
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail on drift, a broken rule, or a budget")
    parser.add_argument("--scope", choices=("repo", "user"), default="repo")
    parser.add_argument("--roster", action="store_true", help="print the roster")
    parser.add_argument("--can-create", metavar="NAME", help="exit 0 if an agent of this name may be created")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    root = args.root.resolve()

    if args.can_create:
        problem = can_create(root, args.can_create)
        print(problem or f"`{args.can_create}` is free")
        return 1 if problem else 0

    files, errors, warnings, owned = build(root, args.scope)
    if args.roster:
        print(files[root / ROSTER].decode("utf-8") if args.scope == "repo" else roster([]), end="")
        return 0

    manifest = manifest_path(root, args.scope)
    listed = sorted(label(path, root, args.scope) for path in files)
    previous = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else []
    stale = [Path(entry) if args.scope == "user" else root / entry for entry in previous if entry not in listed]
    for folder in sorted(owned):
        for path in sorted(folder.rglob("*")) if folder.is_dir() else []:
            if path.is_file() and path not in files and path not in stale:
                errors.append(f"{path.relative_to(root).as_posix()}: written by hand in a generated folder; move it to .agents/ or delete it")

    if args.check:
        errors += [f"{label(path, root, args.scope)}: out of sync, run sync_agents.py" for path, content in files.items() if not same(path, content)]
        errors += [f"{label(path, root, args.scope)}: no longer generated, run sync_agents.py" for path in stale if path.exists()]
        if previous != listed:
            errors.append(f"{label(manifest, root, args.scope) if args.scope == 'repo' else manifest}: out of sync, run sync_agents.py")
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    if args.check:
        print(f"in sync: {len(files)} generated files")
        return 0

    for path in stale:
        if path.exists():
            path.unlink()
            if not any(path.parent.iterdir()):
                path.parent.rmdir()
    for path, content in files.items():
        if not same(path, content):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(listed, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"generated {len(files)} files for the {args.scope} scope")
    return 0


if __name__ == "__main__":
    sys.exit(main())
