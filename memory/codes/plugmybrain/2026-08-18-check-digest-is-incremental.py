# Project: plugmybrain
# Date: 2026-08-18
# Why kept: settles whether a repeat digest re-embeds, which decides if a --code-only flag is needed
# Note: 2026-08-18-check-digest-is-incremental.md
"""Count the embedded chunks before and after a repeat digest of an unchanged folder.

Run it from the plugmybrain checkout with the stack up. It prints two numbers; if they
match, incremental loading works and a repeat digest costs nothing.
"""

from __future__ import annotations

import subprocess
import sys

COUNT = 'SELECT count(*) FROM "DocumentChunk_text";'


def chunks() -> int:
    """The embedded chunk total, read straight from Postgres inside the compose network."""
    result = subprocess.run(
        ["docker", "compose", "exec", "-T", "postgres", "psql", "-U", "plugmybrain",
         "-d", "plugmybrain", "-t", "-c", COUNT],
        capture_output=True,
        text=True,
        check=True,
    )
    return int(result.stdout.strip())


def digest(folder: str, name: str) -> None:
    """Digest a folder in the container, which is the only place ingestion is allowed to run."""
    subprocess.run(
        ["docker", "compose", "run", "--rm", "-v", f"{folder}:/w/{name}",
         "pmb", "digest", f"/w/{name}"],
        check=True,
    )


def main(folder: str, name: str) -> int:
    digest(folder, name)
    before = chunks()
    digest(folder, name)
    after = chunks()

    print(f"before: {before}\nafter:  {after}")
    if before == after:
        print("incremental: a repeat digest embedded nothing")
        return 0
    print(f"NOT incremental: {after - before} chunks were embedded again")
    return 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: check-digest-is-incremental.py <folder> <brain-name>")
    sys.exit(main(sys.argv[1], sys.argv[2]))
