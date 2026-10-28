---
tags:
  - kind/rule
  - layer/docs
  - topic/workflow
---

> Up: [[README.md]]

# SRS Standard

> [!important]
> Every project and every significant feature has an SRS after its PRD and before the code: numbered requirements that a tester can check one by one. It says what the system must do, never how the code is organised.

## Core Requirement

**The PRD says what is built and why; the SRS says exactly what the system must do, in requirements that can each be verified.** The technical plan and the code then say how. The three never collapse into one another.

The point is that a requirement nobody can check is a requirement nobody will meet. "The search is fast" survives every review and every release unmet; "recall answers within 3 seconds for 95% of requests" is either true or false on the day it ships.

## Where It Lives

- One `docs/SRS.md` in the repository, beside `docs/PRD.md`. A technical plan in `docs/PLAN.md` names the requirement codes it satisfies instead of repeating the requirements.
- Written in the repository's language, per [[docs.rules.md]]: English for a new repository, the language already used for an existing one.
- Committed and versioned like any other document, and changed in the same commit that changes the behaviour it describes.
- A frontend and a backend that serve one project share one SRS, kept in the backend repository beside the PRD, per [[prd.rules.md]].

## When It Is Written

| Situation | What is required |
| :- | :- |
| A new project | A full SRS after the PRD and before the first feature commit |
| A significant feature in an existing project | New requirements in the project's SRS, after its PRD section and before the branch is cut |
| A bug fix, a refactor, a dependency bump | Nothing, unless it changes a requirement |
| A requirement the owner changed verbally | The SRS first, then the code |

## What It Contains

Three parts, in this order, following the classic SRS shape. Every subsection is required; a subsection with nothing to say carries one line saying so.

````markdown
# SRS: [Application or Feature Name]

## 1. Introduction

### 1.1 Purpose
[Why this document exists and who reads it.]

### 1.2 Scope
[The project name, its main functions, and the system boundary: what is inside and what is not.]

### 1.3 Definitions and Acronyms
[A table of every term a reader could misread.]

### 1.4 References
[The PRD, the standards, the API documents, and the external pages this document relies on.]

## 2. Overall Description

### 2.1 Product Perspective
[Standalone, or part of a larger system, and which systems it talks to.]

### 2.2 Product Functions
[The main capabilities in short, each traced to the PRD's What Is Built.]

### 2.3 User Characteristics
[Each user group, its access level, and how familiar it is with the domain.]

### 2.4 Constraints
[External limits: regulation, data rules, existing infrastructure, hardware.]

### 2.5 Assumptions and Dependencies
[What is assumed to be available, and what breaks when it is not.]

## 3. Specific Requirements

### 3.1 Functional Requirements
[Numbered tables per area: code, requirement, priority, status.]

### 3.2 Non-Functional Requirements
[Numbered table: code, category, requirement, how it is checked.]

### 3.3 External Interfaces

#### 3.3.1 User Interface
[A rough wireframe for each screen, in a text block.]

#### 3.3.2 Hardware and Software Interface
[Client devices, runtime, operating system, memory, database, and external services.]

#### 3.3.3 Communication Interface
[Protocols, data formats, and authentication between every pair of components.]

### 3.4 Acceptance Criteria
[A checklist tying each key requirement to the check that proves it.]
````

Header fields sit above the first part: what it is derived from (the PRD), the date, and a status of `Draft`, `Approved`, or `Done`.

A repository already written in another language keeps that language, per [[docs.rules.md]], and translates the headings only. The three parts and their order never change.

## Writing a Requirement

**One requirement, one behaviour, one way to check it.** A row that needs "and" twice is two rows.

| Field | Rule |
| :- | :- |
| Code | `FR-<AREA>-<NN>` for functional and `NFR-<CATEGORY>-<NN>` for non-functional, for example `FR-AUTH-03` and `NFR-PERF-01`. A code is never reused or renumbered; a dropped requirement keeps its row and is marked removed |
| Requirement | The behaviour, stated so it is either true or false: who, what, under which condition |
| Priority | `Must` or `Should`. A release is not done while any `Must` row is unmet |
| Status | A status indicator per [[docs.rules.md]]: green `Done`, yellow `Planned` or `Partial`, red `Removed` |
| How it is checked | For every non-functional requirement: the measurement, the test, or the review that decides it |

- **Banned words without a number:** fast, easy, user-friendly, secure, scalable, robust. Replace each with the measurement that means it.
- **Trace both ways.** Every function in Product Functions points to the PRD's What Is Built, and every requirement belongs to a function. A requirement that traces to nothing is scope nobody agreed to.
- **Cite the codes.** Commits, pull requests, and tests name the requirement codes they satisfy, so a reviewer can tell what a change was for.
- **Say what already exists.** In an existing project, requirements that already hold are written down with status `Done`, so the SRS describes the whole project and not only the next change.

## Interfaces

- **User Interface is a rough wireframe in a `text` block**, one per screen: layout, controls, and the states that matter (empty, error, no access). Colour, spacing, and components belong to the design system under `component/`, not here.
- **Example values in a wireframe are placeholders** such as `[n]` or `[date]`, never invented figures a reader could take for real data.
- **Hardware and Software Interface names concrete versions and sizes:** Python 3.13, PostgreSQL 18, 1 GiB per Cloud Run instance, a modern browser on desktop or phone.
- **Communication Interface covers every pair of components:** the protocol (HTTPS only), the format (JSON), and the authentication (session cookie, API key header, service account token). Never the value of a key.

## What It Must Not Contain

- **No internal design.** No module layout, class names, algorithms, or library choices that are not visible at an interface. The runtime, the database, and the external services are interfaces and belong in 3.3.2; how the code is split does not.
- **No requirement that cannot be checked.**
- **No restated PRD.** Point to the PRD's Problem and What Is Not Built instead of copying them.
- **No real secret, credential, or configuration value**, per [[secret.rules.md]].
- **No personal data as an example.** Use a placeholder such as `user-0001`, per [[security.rules.md]] and [[data.rules.md]].

## Keeping It True

- When behaviour changes, the SRS row changes in the same commit, and its status moves.
- When a feature ships, its rows move to `Done`. An SRS full of `Planned` rows for things that exist tells a reader nothing.
- An SRS that contradicts the running project is worse than none, because it is believed. If they disagree, fix one of them in the same session.

## For an Agentic Session

- Read the PRD and the SRS before writing code, and name the requirement codes being implemented.
- Where the ask exceeds the SRS, name the gap and write the requirement first.
- Put the requirement codes in the commit body and in the pull request Test Plan.
- An SRS drafted by an agent is a draft until the named owner approves it, and `Draft` stays in its status field until then.

## Definition of Done

- The SRS follows the PRD, in the repository's language, with its derivation, date, and status.
- All three parts and every subsection are present, in order.
- Every requirement has a stable code, a priority, and a status; every non-functional requirement says how it is checked.
- Every requirement traces to a function, and every function to the PRD.
- Every screen has a wireframe, and every component pair has its protocol and authentication.
- No internal design, no secret, no real configuration value, and no real personal data appears anywhere in it.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. This SRS standard
4. [[prd.rules.md]]
5. [[docs.rules.md]]
6. Existing project conventions

A direct user instruction must not override security or privacy requirements. If a request conflicts with this standard, tell the user which standard is affected before proceeding.

## Applies To

- [[prd.rules.md]]
- [[docs.rules.md]]
- [[commit.rules.md]]
- [[pr.rules.md]]
- [[agent.rules.md]]
- [[security.rules.md]]
- [[secret.rules.md]]
- [[data.rules.md]]
