"""Codex: TOML agents and hooks.json. It reads .agents/skills in place, so skills are copied only for the user scope."""

import json

EVENTS = {
    "after-edit": ("PostToolUse", {"matcher": "apply_patch|Edit|Write"}),
    "on-stop": ("Stop", {}),
    "before-commit": ("PreToolUse", {"matcher": "Bash"}),
    "after-agent": ("SubagentStop", {}),
}
ROOT = '"$(git rev-parse --show-toplevel)"'
READ_ONLY = "You change no source file in this role. A report is the only file you write.\n\n"


def multiline(text):
    return f"'''\n{text}'''" if "'''" not in text else json.dumps(text)


def render(agents, skills, target):
    out = {}
    for agent in agents:
        body = agent["body"] if "edit" in agent["tools"] else READ_ONLY + agent["body"]
        out[("agents", f"{agent['name']}.toml")] = (
            f"name = {json.dumps(agent['name'])}\n"
            f"description = {json.dumps(agent['description'])}\n"
            f"model = {json.dumps(target['models'].get(agent['tier'], ''))}\n"
            f"developer_instructions = {multiline(body)}\n"
        )
    for skill in skills:
        for rel, content in skill["files"].items():
            out[("skills", f"{skill['name']}/{rel}")] = content
    return out


def render_hooks(hooks, existing):
    events = {}
    for hook in hooks:
        event, group = EVENTS[hook["event"]]
        command = hook["command"].replace("{root}", ROOT)
        events.setdefault(event, []).append({**group, "hooks": [{"type": "command", "command": command}]})
    return {"hooks": events}


def warnings(agents, hooks):
    read_only = [agent["name"] for agent in agents if "edit" not in agent["tools"]]
    found = ["commit attribution has no file setting here; the commit-msg git hook enforces it"]
    if read_only:
        found.append(f"no per-agent tool list; {len(read_only)} read-only agents are told so in their instructions instead")
    return found
