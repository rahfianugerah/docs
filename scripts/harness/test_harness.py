"""The fast test suite of the harness. Run it directly: python scripts/harness/test_harness.py"""

import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import check_attribution  # noqa: E402

BOT = "Clau" + "de"
TRAILER = "Co-Authored-" + f"By: {BOT} <noreply@example.com>"


def sync(root, *args):
    return subprocess.run([sys.executable, str(HERE / "sync_agents.py"), "--root", str(root), *args], capture_output=True, text=True)


class Sandbox(unittest.TestCase):
    """A copy of the harness source that a test may break."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        shutil.copytree(ROOT / ".agents", self.root / ".agents")
        shutil.copy(ROOT / "AGENTS.md", self.root / "AGENTS.md")
        (self.root / "harness").mkdir()
        self.assertEqual(sync(self.root).returncode, 0)

    def assert_rejected(self, expected):
        result = sync(self.root, "--check")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(expected, result.stderr)

    def agent(self, name="verifier"):
        return self.root / ".agents/agents" / f"{name}.md"


class SyncTest(Sandbox):
    def test_repository_is_in_sync(self):
        result = sync(ROOT, "--check")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_an_edit_drifts_until_synced(self):
        skill = self.root / ".agents/skills/agentic-verify/SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\nOne more line.\n", encoding="utf-8")
        self.assert_rejected("out of sync")
        self.assertEqual(sync(self.root).returncode, 0)
        self.assertEqual(sync(self.root, "--check").returncode, 0)

    def test_a_skill_without_the_prefix_is_rejected(self):
        (self.root / ".agents/skills/agentic-verify").rename(self.root / ".agents/skills/verify")
        self.assert_rejected("must start with `agentic-`")

    def test_a_model_name_in_an_agent_is_rejected(self):
        path = self.agent()
        path.write_text(path.read_text(encoding="utf-8") + "\nRun this on son" + "net.\n", encoding="utf-8")
        self.assert_rejected("names a model")

    def test_an_unknown_tier_is_rejected(self):
        path = self.agent()
        path.write_text(path.read_text(encoding="utf-8").replace("tier: deep", "tier: huge", 1), encoding="utf-8")
        self.assert_rejected("tier must be one of")

    def test_a_tier_with_no_model_is_rejected(self):
        path = self.root / ".agents/targets.toml"
        path.write_text(path.read_text(encoding="utf-8").replace('fast = "gpt-6-luna"\n', ""), encoding="utf-8")
        self.assert_rejected("maps no model to the tier")

    def test_a_removed_agent_leaves_no_generated_file(self):
        self.agent("chore-agent").unlink()
        self.assertEqual(sync(self.root).returncode, 0)
        self.assertFalse((self.root / ".claude/agents/chore-agent.md").exists())
        self.assertFalse((self.root / ".codex/agents/chore-agent.toml").exists())

    def test_a_new_target_needs_only_a_table(self):
        path = self.root / ".agents/targets.toml"
        table = '\n[targets.dummy]\nadapter = "claude"\nagents_dir = ".dummy/agents"\nskills_dir = ".dummy/skills"\n[targets.dummy.models]\ndeep = "d"\nbuild = "b"\nfast = "f"\n'
        path.write_text(path.read_text(encoding="utf-8") + table, encoding="utf-8")
        self.assertEqual(sync(self.root).returncode, 0)
        self.assertIn("model: d\n", (self.root / ".dummy/agents/verifier.md").read_text(encoding="utf-8"))

    def test_generated_agents_resolve_a_model_and_parse(self):
        models = tomllib.loads((ROOT / ".agents/targets.toml").read_text(encoding="utf-8"))["targets"]
        for path in (self.root / ".codex/agents").glob("*.toml"):
            agent = tomllib.loads(path.read_text(encoding="utf-8"))
            self.assertIn(agent["model"], models["codex"]["models"].values())
            self.assertTrue(agent["developer_instructions"].strip())
        for path in (self.root / ".claude/agents").glob("*.md"):
            model = next(line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("model: "))
            self.assertIn(model.removeprefix("model: "), models["claude"]["models"].values())

    def test_a_taken_or_invalid_name_cannot_be_created(self):
        self.assertEqual(sync(self.root, "--can-create", "verifier").returncode, 1)
        self.assertEqual(sync(self.root, "--can-create", "Not_Kebab").returncode, 1)
        self.assertEqual(sync(self.root, "--can-create", "api-docs-writer").returncode, 0)


class AttributionTest(unittest.TestCase):
    def test_a_credit_is_rejected(self):
        for text in (f"fix: x\n\n{TRAILER}", "Generated " + f"with {BOT} Code", "see https://clau" + "de.ai/code/session_1"):
            self.assertTrue(check_attribution.problems(text), text)

    def test_a_commit_message_names_no_tool(self):
        self.assertTrue(check_attribution.problems(f"docs: describe the {BOT} adapter", message=True))

    def test_a_path_or_a_plain_message_passes(self):
        for text in ("docs(harness): add the sync script\n\n- Generate .claude/agents from .agents/", "docs: update CLAUDE.md"):
            self.assertEqual(check_attribution.problems(text, message=True), [], text)

    def test_a_generic_credit_fails_in_a_message_and_passes_as_a_documented_example(self):
        line = "Generated " + "with an AI coding tool"
        self.assertTrue(check_attribution.problems(line, message=True))
        self.assertEqual(check_attribution.problems(line), [])

    def test_prose_about_the_rule_passes(self):
        self.assertEqual(check_attribution.problems("- No co-author trailer and no generated-with line."), [])


class DocsTest(unittest.TestCase):
    def test_the_document_check_tests_itself(self):
        script = HERE / "check_docs.py"
        if script.exists():
            result = subprocess.run([sys.executable, str(script), "--self-test"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=1)
