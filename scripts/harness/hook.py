"""Run the check behind one hook event. Exit 2 hands the failure back to the agent, in every tool that reads hooks this way."""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BLOCK = 2


def run(script, *args):
    result = subprocess.run([sys.executable, str(HERE / script), *args], cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        print((result.stdout + result.stderr).strip(), file=sys.stderr)
    return result.returncode


def after_edit(payload):
    path = payload.get("tool_input", {}).get("file_path", "")
    # The document check enforces rules/docs.rules.md, so it runs only where that file is.
    docs = (ROOT / "rules/docs.rules.md").exists()
    if not path:
        # A tool that edits by patch names no single file: check everything git sees as changed.
        return (run("check_docs.py", "--changed") if docs else 0) | run("sync_agents.py", "--check")
    failed = 0
    if docs and path.endswith(".md"):
        failed |= run("check_docs.py", path)
    if "/.agents/" in Path(path).as_posix() + "/":
        failed |= run("sync_agents.py", "--check")
    return failed


def on_stop(payload):
    if payload.get("stop_hook_active"):
        return 0
    return run("test_harness.py")


def before_commit(payload):
    command = payload.get("tool_input", {}).get("command", "")
    if "git commit" not in command:
        return 0
    return run("check_attribution.py", "--staged", "--text", command)


def after_agent(payload):
    log = ROOT / "harness/usage/agents.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "agent": payload.get("agent_type") or payload.get("subagent_type") or "unknown",
        "session": payload.get("session_id", ""),
    }
    with log.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")
    return 0


EVENTS = {"after-edit": after_edit, "on-stop": on_stop, "before-commit": before_commit, "after-agent": after_agent}


def main():
    raw = "" if sys.stdin.isatty() else sys.stdin.read()
    payload = json.loads(raw) if raw.strip() else {}
    if len(sys.argv) != 2 or sys.argv[1] not in EVENTS:
        print(f"usage: hook.py {' | '.join(EVENTS)}", file=sys.stderr)
        return 1
    return BLOCK if EVENTS[sys.argv[1]](payload) else 0


if __name__ == "__main__":
    sys.exit(main())
