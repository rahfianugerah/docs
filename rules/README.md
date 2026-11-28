> Up: [[README.md]]

# Rules

Every rule file in this folder owns one subject and is named `<subject>.rules.md`, with a few named for what they govern. Every project follows them, and each rule says why it exists, so it is not dropped the first time it is inconvenient.

| Rule | Owns |
| :- | :- |
| [[agent.rules.md]] | When an agent writes a memory note, and how many |
| [[analytics.rules.md]] | Which chart a shape of data earns, the guardrails against distortion, and the no-3D gate |
| [[api.rules.md]] | The REST contract: the route shape, the error shape, pagination, and tool endpoints |
| [[auth.rules.md]] | One identity source, one identity key, one swappable abstraction, and the non-human account |
| [[automation.rules.md]] | Scheduled and triggered work: one folder, deployed apart, tested before release, with a force stop |
| [[badge.rules.md]] | shields.io badges: the two kinds, the product name, and Title Case on every state |
| [[branch.rules.md]] | The two branch shapes, trunk and promotion, and which one a project declares |
| [[callout.rules.md]] | The callout types, where one is required, and where it is forbidden |
| [[codes.rules.md]] | YAGNI, KISS, DRY, readability, Python 3.13, conda and `.venv`, and the ML practices that differ |
| [[commit.rules.md]] | Conventional Commits, an `exp` type for experiments, and what never enters a commit |
| [[data.rules.md]] | Four data classes: the schema is readable, rows need explicit approval, and protected data is never read |
| [[database.rules.md]] | PostgreSQL and SQLAlchemy, which cases take the ORM and which take raw SQL, and the restore nobody tested |
| [[docs.rules.md]] | What every project documents, how it is written, the tag taxonomy, and the Obsidian conventions |
| [[env.rules.md]] | Why a real environment file is never read, what belongs in a table instead, and the notebook cell |
| [[journal.rules.md]] | The journal written when a piece of work ends, its four questions, and the numbers it must carry |
| [[media.rules.md]] | Document and media upload, covering PDF and photo |
| [[memory.codes.rules.md]] | Reference code kept beside a note that explains it |
| [[memory.rules.md]] | The write and recall protocol every model follows, and why the memory stays local |
| [[notes.rules.md]] | The project note: one brief, digits-only numbering, and a Done When table a tester can tick |
| [[path.rules.md]] | Every path relative to a named anchor, and the three path namespaces that never mix |
| [[pr.rules.md]] | When a pull request is worth opening, what an experiment must record, and when an AI may open or merge one |
| [[prd.rules.md]] | The PRD every project carries, written before the code, and the non-goals that bound it |
| [[pwa.rules.md]] | The PWA layer of a frontend: manifest, icons, and offline behavior |
| [[report.automation.md]] | What an automated report delivers: the header, the caption, the file type, the numbers, and the colours |
| [[report.rules.md]] | Where an agent report is written, its file name, timestamp, levels, and statuses |
| [[repository.rules.md]] | One deployable per repository, git hygiene, and what every project documents |
| [[secret.rules.md]] | Which values are secrets, where each one lives, and why a frontend holds none |
| [[security.rules.md]] | The OWASP checklist, the stack controls it turns into, personal data, and the audit trail |
| [[srs.rules.md]] | The numbered, checkable requirements that follow the PRD and precede the code |
| [[stacks.rules.md]] | The stack every project starts from, and what needs a written exception |
| [[versioning.rules.md]] | Semantic Versioning: which commit raises MAJOR, MINOR, or PATCH, the reset, version 0, and the tag on `main` |

## Citations

Each entry credits where the idea came from: the publisher of an outside standard when a rule is built on one, and the owner when the rule is the owner's own. An entry with a `note` field was adapted for this repository.

```bibtex
@misc{rule_agent_rules,
  title={agent.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_analytics_rules,
  title={analytics.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_api_rules,
  title={OpenAPI Specification},
  author={OpenAPI Initiative},
  url={https://spec.openapis.org/oas/latest.html},
  note={Adapted for this repository by rahfianugerah}
}

@misc{rule_auth_rules,
  title={auth.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_automation_rules,
  title={automation.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_badge_rules,
  title={Shields.io},
  author={Shields.io},
  url={https://shields.io/},
  note={Adapted for this repository by rahfianugerah}
}

@misc{rule_branch_rules,
  title={branch.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_callout_rules,
  title={callout.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_codes_rules,
  title={PEP 8 - Style Guide for Python Code},
  author={Guido van Rossum and Barry Warsaw and Alyssa Coghlan},
  year={2001},
  url={https://peps.python.org/pep-0008/},
  note={Adapted for this repository by rahfianugerah}
}

@misc{rule_commit_rules,
  title={Conventional Commits 1.0.0},
  author={Conventional Commits},
  year={2019},
  url={https://www.conventionalcommits.org/en/v1.0.0/},
  note={Adapted for this repository by rahfianugerah}
}

@misc{rule_data_rules,
  title={data.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_database_rules,
  title={database.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_docs_rules,
  title={docs.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_env_rules,
  title={env.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_journal_rules,
  title={journal.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_media_rules,
  title={media.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_memory_codes_rules,
  title={memory.codes.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_memory_rules,
  title={memory.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_notes_rules,
  title={notes.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_path_rules,
  title={path.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_pr_rules,
  title={pr.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_prd_rules,
  title={prd.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_pwa_rules,
  title={pwa.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_report_automation,
  title={report.automation.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_report_rules,
  title={report.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_repository_rules,
  title={repository.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_secret_rules,
  title={secret.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_security_rules,
  title={OWASP Secure Coding Practices - Quick Reference Guide},
  author={OWASP Foundation},
  url={https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/},
  note={Adapted for this repository by rahfianugerah}
}

@misc{rule_srs_rules,
  title={srs.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_stacks_rules,
  title={stacks.rules.md},
  author={rahfianugerah},
  year={2026},
  url={https://github.com/rahfianugerah/agentic}
}

@misc{rule_versioning_rules,
  title={Semantic Versioning 2.0.0},
  author={Tom Preston-Werner},
  year={2013},
  url={https://semver.org/spec/v2.0.0.html},
  note={Adapted for this repository by rahfianugerah}
}
```
