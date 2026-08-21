> Up: [[README.md]]

# PRD Standard Policy

> [!important]
> Every project starts from a PRD, written before the code. It states the problem and the non-goals, and never contains solution design.

## Core Requirement

**Every project has a `PRD.md`, and it is written before the code.** No feature is built without one, and no repository exists without one.

A PRD says what is being built, for whom, and why. It does not say how; that is the technical decision, and it belongs in the code, the API document, and the runbook.

The point is not process. It is that the most expensive mistake in this ecosystem is not a bug, it is a feature nobody needed, built correctly, deployed properly, and used by no one. A PRD is the cheapest place to find that out, because it costs an hour rather than a sprint.

## Where It Lives

- One `PRD.md` in the repository root, beside the `README.md`.
- Written in the language its readers use, because its readers are whoever asked for the project.
- Committed and versioned like any other document. It is not a chat message, not a spreadsheet, not a screenshot of a WhatsApp thread.
- A frontend and a backend that serve one app share the app's PRD. Put it in the backend repository and link to it from the frontend README, so the product intent is not split in half by a repository boundary, per `repository.rules.md`.

## When It Is Written

| Situation | What is required |
| :- | :- |
| A new app | A full `PRD.md` before the first feature commit |
| A significant feature in an existing app | A new section in that app's `PRD.md`, before the branch is cut |
| A bug fix, a refactor, a dependency bump | Nothing. A PRD describes intent, and these change none |
| A change the owner asked for verbally | The PRD section first, then the code. The verbal ask is the input, not the record |

**The test for whether a change needs a PRD section:** would somebody, in six months, be able to tell from the code alone *why* this exists? If not, it needs a section. If yes, it does not.

## What It Contains

Eight sections, in this order. Every one is required, and the shortest useful answer is the right length.

```markdown
# PRD: [Nama Aplikasi atau Fitur]

## Masalah
[Apa yang terjadi hari ini, siapa yang terganggu, dan berapa biayanya. Bukan "kami butuh fitur X".]

## Pengguna
[Divisi mana, jabatan apa, berapa orang. Sebutkan yang akan memakainya setiap hari.]

## Yang Dibangun
[Apa yang akan bisa dilakukan pengguna setelah ini ada. Ditulis sebagai kemampuan, bukan sebagai layar.]

## Yang Tidak Dibangun
[Daftar eksplisit hal yang sengaja tidak dikerjakan, dan alasannya.]

## Ukuran Keberhasilan
[Bagaimana kita tahu ini berhasil. Angka atau perilaku yang bisa diperiksa, bukan "lebih efisien".]

## Batasan
[Hal yang tidak bisa berubah: sumber data, aturan bisnis, kepatuhan, tenggat.]

## Data
[Data apa yang dibaca dan ditulis, dari mana asalnya, dan apakah ada data pribadi.]

## Pertanyaan Terbuka
[Yang belum diputuskan, dan siapa yang harus memutuskannya.]
```

Header fields sit above the first section: the owner as a named person with their NIP, the date, and a status of `Draft`, `Disetujui`, or `Selesai`.

## The Sections That Do the Work

Four of the eight carry almost all the value, and they are the four most often left thin.

**Masalah, written as a problem and not as a solution.** "Tim Legal kehilangan 3 hari per bulan merekap kontrak jatuh tempo dari lima spreadsheet" is a problem. "Kami butuh dashboard kontrak" is a solution with the problem removed, and it forecloses every cheaper answer before anyone has looked.

**Yang Tidak Dibangun is mandatory and is the most valuable section in the document.** It is where scope creep dies. An empty non-goals list means the scope was never bounded, and every conversation from then on can add to it without anyone noticing. Write down the obvious adjacent things and say no to them explicitly: no mobile app in this phase, no export to Excel, no approval workflow.

**Ukuran Keberhasilan has to be checkable.** "Lebih cepat" is not a measure. "Rekap bulanan selesai dalam satu hari, bukan tiga" is. If nobody can say afterwards whether it worked, nobody will, and the next request for the same area starts from zero.

**Pengguna names real people, not a role in the abstract.** An app for "manajemen" is an app with no one to ask when a decision is needed. An app for "empat orang di Legal & Corp Secretary, dipakai harian oleh dua di antaranya" has a person to sit with.

## What It Must Not Contain

- **No solution design.** No schema, no endpoint list, no component tree, no library choice. Those live in the code, in `API.md`, and in the standards under `rules/` and `component/`. A PRD that specifies a table layout has stopped being a PRD and started being an argument about implementation.
- **No estimate presented as a commitment.** A date belongs in Batasan only when something external actually depends on it.
- **No real secret, credential, or configuration value**, per `secret.rules.md`.
- **No personal data as an example.** Use a placeholder NIP such as `20230101`, never a real employee's data, per `security.rules.md`.
- **No feature with no named owner.** If nobody owns it, it is not ready to be built.

## Keeping It True

**A PRD is a living document, not a gate that swings once.** It is written before the code and updated whenever reality moves, in the same commit that moves it.

- When scope changes, the PRD changes first. A feature built beyond its PRD is a feature nobody agreed to.
- When something moves from Yang Dibangun to Yang Tidak Dibangun, say so and say why. That line is the record of a decision.
- When an open question is answered, move the answer into the section it belongs to and delete the question.
- When a feature ships, set its status to `Selesai`. A PRD full of `Draft` sections tells a reader nothing about what actually exists.
- A PRD that contradicts the running app is worse than no PRD, because it is believed. If they disagree, fix one of them in the same session.

## For an Agentic Session

An agentic coding tool reads the PRD before it writes code, and this is where it matters most: a model given a task with no PRD will infer the intent, build something coherent, and be confidently wrong about why.

- Read `PRD.md` before starting a feature. If the repository has none, say so and offer to draft one rather than inferring the intent from the code.
- Where the ask exceeds the PRD, name the gap before building. The PRD section comes first.
- A PRD drafted by an agent is a draft. It is not approved until the named owner says so, and `Draft` stays in the status field until then.
- A durable decision from a PRD conversation, especially a rejected approach, belongs in the memory too, per `agent.rules.md`.

## Definition of Done

- The repository has a `PRD.md` in its root, in that language, with a named owner and a status.
- All eight sections are present, and Yang Tidak Dibangun is not empty.
- Masalah describes a problem rather than a solution.
- Ukuran Keberhasilan is something a person can actually check afterwards.
- No schema, endpoint list, or library choice appears anywhere in it.
- No secret, no real configuration value, and no real personal data appears anywhere in it.
- The PRD matches what the app actually does today, or the difference is recorded.

## Conflict Resolution

If another instruction conflicts with this policy, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. This PRD policy
4. `docs.rules.md`
5. Existing project conventions

A direct user instruction must not override security or privacy requirements. If a request conflicts with this policy, tell the user which standard is affected before proceeding.

## Applies To

- [[docs.rules.md]]
- [[repository.rules.md]]
- [[pr.rules.md]]
- [[agent.rules.md]]
- [[security.rules.md]]
- [[secret.rules.md]]
