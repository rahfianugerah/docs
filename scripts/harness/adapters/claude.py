"""Claude Code: Markdown agents, copied skills, hooks and attribution in settings.json."""

import json
import re

TOOLS = {
    "read": ["Read"],
    "search": ["Grep", "Glob"],
    "edit": ["Edit", "Write"],
    "run": ["Bash"],
    "web": ["WebFetch", "WebSearch"],
    "delegate": ["Agent"],
}
EVENTS = {
    "after-edit": ("PostToolUse", {"matcher": "Edit|Write"}, {}),
    "on-stop": ("Stop", {}, {}),
    "before-commit": ("PreToolUse", {"matcher": "Bash"}, {"if": "Bash(git commit *)"}),
    "after-agent": ("SubagentStop", {}, {}),
}
ROOT = '"$CLAUDE_PROJECT_DIR"'
PLAIN_YAML = re.compile(r"[A-Za-z0-9][^:#\"']*\Z")


def scalar(text):
    return text if PLAIN_YAML.match(text) else json.dumps(text)


def render(agents, skills, target):
    out = {}
    for agent in agents:
        tools = ", ".join(tool for name in agent["tools"] for tool in TOOLS.get(name, []))
        out[("agents", f"{agent['name']}.md")] = (
            f"---\nname: {agent['name']}\ndescription: {scalar(agent['description'])}\n"
            f"tools: {tools}\nmodel: {target['models'].get(agent['tier'], '')}\n---\n{agent['body']}"
        )
    for skill in skills:
        for rel, content in skill["files"].items():
            out[("skills", f"{skill['name']}/{rel}")] = content
    return out


def render_hooks(hooks, existing):
    settings = dict(existing)
    settings["attribution"] = {"commit": "", "pr": "", "sessionUrl": False}
    settings["hooks"] = {}
    for hook in hooks:
        event, group, handler = EVENTS[hook["event"]]
        command = hook["command"].replace("{root}", ROOT)
        settings["hooks"].setdefault(event, []).append(
            {**group, "hooks": [{"type": "command", "command": command, **handler}]}
        )
    return settings


def warnings(agents, hooks):
    return []
