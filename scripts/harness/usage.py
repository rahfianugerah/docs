"""Turn the stream-json transcript of one headless run into tokens per agent and per tier.

python scripts/harness/usage.py run.jsonl --label routed
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sync_agents import parse  # noqa: E402

FIELDS = {
    "input": "input_tokens",
    "output": "output_tokens",
    "cache_read": "cache_read_input_tokens",
    "cache_write": "cache_creation_input_tokens",
}
SPAWN_TOOLS = ("Agent", "Task")
MAIN = "orchestrator"


def tier_of(agent):
    path = ROOT / ".agents/agents" / f"{agent}.md"
    return parse(path)[0]["tier"] if path.exists() else "unlisted"


def summarize(events):
    spawned, messages, result = {}, {}, {}
    for event in events:
        if event.get("type") == "assistant":
            message = event["message"]
            for block in message.get("content", []):
                if block.get("type") == "tool_use" and block.get("name") in SPAWN_TOOLS:
                    spawned[block["id"]] = block.get("input", {}).get("subagent_type", "general-purpose")
            # One API call arrives as several events with the same id and the same usage: count it once.
            messages[message["id"]] = (event.get("parent_tool_use_id"), message.get("model", ""), message.get("usage", {}))
        elif event.get("type") == "result":
            result = event

    agents = defaultdict(lambda: {"calls": 0, **{field: 0 for field in FIELDS}})
    for parent, model, usage in messages.values():
        name = MAIN if parent is None else spawned.get(parent, "unknown")
        row = agents[name]
        row["model"] = model
        row["calls"] += 1
        for field, key in FIELDS.items():
            row[field] += usage.get(key) or 0

    tiers = defaultdict(lambda: {field: 0 for field in FIELDS})
    for name, row in agents.items():
        row["tier"] = "deep" if name == MAIN else tier_of(name)
        for field in FIELDS:
            tiers[row["tier"]][field] += row[field]
    return {
        "cost_usd": result.get("total_cost_usd"),
        "turns": result.get("num_turns"),
        "duration_ms": result.get("duration_ms"),
        "agents": dict(agents),
        "tiers": dict(tiers),
        "models": result.get("modelUsage", {}),
    }


def table(summary):
    lines = ["| Agent | Tier | Model | Calls | Input | Output | Cache read | Cache write |", "| :- | :- | :- | -: | -: | -: | -: | -: |"]
    for name, row in sorted(summary["agents"].items()):
        lines.append(f"| `{name}` | {row['tier']} | `{row.get('model', '')}` | {row['calls']} | {row['input']} | {row['output']} | {row['cache_read']} | {row['cache_write']} |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transcript", type=Path)
    parser.add_argument("--label", required=True, help="the name of the run, used as the log's file name")
    args = parser.parse_args()

    events = [json.loads(line) for line in args.transcript.read_text(encoding="utf-8").splitlines() if line.startswith("{")]
    summary = {"label": args.label, **summarize(events)}
    log = ROOT / "harness/usage" / f"{args.label}.json"
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(table(summary))
    print(f"\ncost: {summary['cost_usd']} USD, turns: {summary['turns']}, log: {log.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
