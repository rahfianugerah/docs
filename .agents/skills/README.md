# Skills

This folder holds the source of every skill, one folder per skill in `.agents/skills/agentic-<command>/`, in the Agent Skills format described in `harness/README.md`. Each skill runs as a slash command, and this folder is the only place a skill is edited.

| Command | Use it to |
| :- | :- |
| `/agentic-orchestrate` | Run the whole loop on a request |
| `/agentic-verify` | Verify the current diff independently |
| `/agentic-no-slop` | Remove comments that restate code, dead code, and quick-fix patterns |
| `/agentic-root-cause` | Analyse a bug to its cause before any fix |
| `/agentic-statechart` | Draw a feature's states and list the ones nothing handles |
| `/agentic-test-matrix` | Pick the kinds of test a change needs |
| `/agentic-boundaries` | Write the lint rules that enforce the directory boundaries |
| `/agentic-create-formal-verification-skill` | Scaffold a TLA+ or Lean check for one module |
| `/agentic-create` | Add a new agent to the roster |
| `/agentic-harness-improve` | Improve the harness from evidence |
| `/agentic-outer-loop` | Set up the triggers that start the loop unattended |

## Citations

Each entry credits where the idea came from: an organisation or a person when it came from one, and the owner when it is the owner's own. An entry with a `note` field was adapted and written in this repository.

```bibtex
@misc{skill_agentic_orchestrate,
  title={agentic-orchestrate},
  author={Cursor},
  year={2026},
  url={https://github.com/cursor/plugins/tree/main/orchestrate},
  note={Adapted for this repository by rahfianugerah}
}

@misc{skill_agentic_verify,
  title={agentic-verify},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{skill_agentic_no_slop,
  title={agentic-no-slop},
  author={Lauren Tan},
  year={2026},
  url={https://github.com/cursor/plugins/tree/main/pstack},
  note={Adapted for this repository by rahfianugerah}
}

@misc{skill_agentic_root_cause,
  title={agentic-root-cause},
  author={Lauren Tan},
  year={2026},
  url={https://github.com/cursor/plugins/tree/main/pstack},
  note={Adapted for this repository by rahfianugerah}
}

@misc{skill_agentic_statechart,
  title={agentic-statechart},
  author={Lauren Tan},
  year={2026},
  url={https://github.com/cursor/plugins/tree/main/pstack},
  note={Adapted for this repository by rahfianugerah}
}

@misc{skill_agentic_test_matrix,
  title={Testing in Production, the safe way},
  author={Cindy Sridharan},
  year={2018},
  url={https://copyconstruct.medium.com/testing-in-production-the-safe-way-18ca102d0ef1},
  note={Adapted for this repository by rahfianugerah}
}

@misc{skill_agentic_boundaries,
  title={agentic-boundaries},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{skill_agentic_create_formal_verification_skill,
  title={agentic-create-formal-verification-skill},
  author={Lauren Tan},
  year={2026},
  url={https://github.com/cursor/plugins/tree/main/pstack},
  note={Adapted for this repository by rahfianugerah}
}

@misc{skill_agentic_create,
  title={agentic-create},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{skill_agentic_harness_improve,
  title={Harness2: Recursive Agent Harnessing for an Open World},
  author={Ruiyao Xu and Yanfei Chen and Zhongying CuiZhu and Bhavana Dalvi Mishra and Yifei Ming and Han Yu and Rujun Han and Chen-Yu Lee and Tomas Pfister},
  year={2026},
  eprint={2610.14224},
  archivePrefix={arXiv},
  url={https://arxiv.org/abs/2610.14224},
  note={Adapted for this repository by rahfianugerah}
}

@misc{skill_agentic_outer_loop,
  title={agentic-outer-loop},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}
```
