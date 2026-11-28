# Agents

This folder holds the neutral source of every agent, one file per agent in `.agents/agents/<name>.md`, in the format described in `harness/README.md`. It is the only place an agent is edited; the folder of each tool is generated from it. The tier says which model class the agent runs on: `deep` for reasoning, `build` for code, `fast` for mechanical work.

| Agent | Tier | Job |
| :- | :- | :- |
| `orchestrator` | `deep` | Splits a request, launches the other agents, and passes findings forward; never writes code. |
| `research-agent` | `deep` | Answers what is unknown before planning, from the code, the documents, and the web. |
| `system-analyst` | `deep` | Turns a request into requirements and acceptance criteria, and writes Needs Decision reports. |
| `architect` | `deep` | Designs a boundary, an API, or a data model where one changes. |
| `planner` | `deep` | Turns the requirements into ordered tasks, each with its files, risks, and agent. |
| `advisor` | `deep` | Gives a second opinion to a build or fast agent before a hard-to-reverse decision. |
| `verifier` | `deep` | Verifies a diff independently, from the requirements and the diff alone. |
| `slop-reviewer` | `deep` | Finds comments that restate code, dead code, and quick-fix patterns. |
| `security-reviewer` | `deep` | Reviews a design and a diff against the security rules and names the requirements. |
| `formal-verifier` | `deep` | Writes and runs a TLA+ or Lean check for one module. |
| `harness-improver` | `deep` | Improves the agents, skills, and hooks from evidence of past runs. |
| `backend-engineer` | `build` | Builds one backend task on the backend standards. |
| `frontend-engineer` | `build` | Builds one frontend task on the component standards. |
| `devops-engineer` | `build` | Builds the pipeline, container, and deploy files for one task. |
| `test-designer` | `build` | Chooses and writes the tests a change needs. |
| `statechart-modeler` | `build` | Models a flow with complex state before it is built. |
| `chore-agent` | `fast` | Does mechanical work: syncing documents, renames, and formatting. |

## Citations

Each entry credits where the idea came from: an organisation or a person when it came from one, and the owner when it is the owner's own. An entry with a `note` field was adapted and written in this repository.

```bibtex
@misc{agent_orchestrator,
  title={orchestrator},
  author={Cursor},
  year={2026},
  url={https://github.com/cursor/plugins/tree/main/orchestrate},
  note={Adapted for this repository by rahfianugerah}
}

@misc{agent_research_agent,
  title={research-agent},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{agent_system_analyst,
  title={system-analyst},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{agent_architect,
  title={architect},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{agent_planner,
  title={planner},
  author={Cursor},
  year={2026},
  url={https://github.com/cursor/plugins/tree/main/orchestrate},
  note={Adapted for this repository by rahfianugerah}
}

@misc{agent_advisor,
  title={advisor},
  author={Cursor},
  year={2026},
  url={https://github.com/cursor/plugins/tree/main/advisor},
  note={Adapted for this repository by rahfianugerah}
}

@misc{agent_verifier,
  title={verifier},
  author={Cursor},
  year={2026},
  url={https://github.com/cursor/plugins/tree/main/orchestrate},
  note={Adapted for this repository by rahfianugerah}
}

@misc{agent_slop_reviewer,
  title={slop-reviewer},
  author={Lauren Tan},
  year={2026},
  url={https://github.com/cursor/plugins/tree/main/pstack},
  note={Adapted for this repository by rahfianugerah}
}

@misc{agent_security_reviewer,
  title={security-reviewer},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{agent_formal_verifier,
  title={formal-verifier},
  author={Lauren Tan},
  year={2026},
  url={https://github.com/cursor/plugins/tree/main/pstack},
  note={Adapted for this repository by rahfianugerah}
}

@misc{agent_harness_improver,
  title={Harness2: Recursive Agent Harnessing for an Open World},
  author={Ruiyao Xu and Yanfei Chen and Zhongying CuiZhu and Bhavana Dalvi Mishra and Yifei Ming and Han Yu and Rujun Han and Chen-Yu Lee and Tomas Pfister},
  year={2026},
  eprint={2610.14224},
  archivePrefix={arXiv},
  url={https://arxiv.org/abs/2610.14224},
  note={Adapted for this repository by rahfianugerah}
}

@misc{agent_backend_engineer,
  title={backend-engineer},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{agent_frontend_engineer,
  title={frontend-engineer},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{agent_devops_engineer,
  title={devops-engineer},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{agent_test_designer,
  title={Testing in Production, the safe way},
  author={Cindy Sridharan},
  year={2018},
  url={https://copyconstruct.medium.com/testing-in-production-the-safe-way-18ca102d0ef1},
  note={Adapted for this repository by rahfianugerah}
}

@misc{agent_statechart_modeler,
  title={statechart-modeler},
  author={Lauren Tan},
  year={2026},
  url={https://github.com/cursor/plugins/tree/main/pstack},
  note={Adapted for this repository by rahfianugerah}
}

@misc{agent_chore_agent,
  title={chore-agent},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}
```
