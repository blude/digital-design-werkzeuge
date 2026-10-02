# Digital Design Werkzeuge

Agent skills for writing four-level digital design documentation as validated, traceable [StrictDoc](https://strictdoc.readthedocs.io/) documents.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Validate](https://github.com/blude/digital-design-werkzeuge/actions/workflows/validate.yml/badge.svg)](https://github.com/blude/digital-design-werkzeuge/actions/workflows/validate.yml)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Works with Claude Code and any agent supported by the [`skills`](https://skills.sh) CLI.

## What it does

A design initiative usually starts as a vague idea and ends as scattered documents nobody can trace back to a decision. This repository gives your agent a framework that keeps each statement at the right level of abstraction and links it to its parent:

| Level | Document | Audience | Answers |
| --- | --- | --- | --- |
| L0 | Digital Design Brief | Management | Should we do this? (Go/No-Go) |
| L1 | Solution Design Concept | Business stakeholders, sponsors | What does the solution need to do for the business? |
| L2 | System Design Concept | Designers, developers | How is the system structured? |
| L3 | Element Design Concept | Implementers | How is one element designed in enough detail to build? |

Each level has its own StrictDoc grammar, so the tool rejects a requirement written at the wrong level and fails the build on a broken cross-level reference. A requirement that traces to an L0 impact has a recorded reason to exist; one that doesn't is a finding.

## Install

With the `skills` CLI:

```bash
npx skills add blude/digital-design-werkzeuge
```

As a Claude Code plugin:

```text
/plugin marketplace add blude/digital-design-werkzeuge
/plugin install digital-design
```

The skill needs [StrictDoc](https://strictdoc.readthedocs.io/) and Python 3 for validation:

```bash
pipx install strictdoc
```

## Usage

Ask your agent in plain language. The skill triggers on mentions of a design brief, solution/system/element design concept, L0–L3 documents, or requirement IDs like `BG-01` and `UC-03`.

```text
Write an L0 design brief for a self-service returns portal.
Add a use case to the L1 document and trace it to IMP-02.
Validate the design docs.
```

For live drafting and stakeholder interviews, the `digital-designer` agent adjusts register between executive and implementer audiences.

To validate a project yourself, from its root:

```bash
python3 skills/authoring-docs/scripts/validate.py
```

It runs `strictdoc export` (syntax, grammar, relation targets), checks entity attribute references, and checks the framework's coverage expectations. The exit code is non-zero on any failure, so it works as a CI gate.

## Repository layout

```text
.claude-plugin/        plugin manifest
agents/                digital-designer agent
skills/authoring-docs/
  SKILL.md             skill entry point
  assets/grammars/     StrictDoc grammars, one per level
  assets/templates/    starter documents, one per level
  references/          framework, per-level, drafting and syntax guidance
  scripts/             validation and traceability tooling
```

## Acknowledgements

The templates in the [Canteen App Design Story](https://ireb.atlassian.net/wiki/spaces/TCADS/overview?homepageId=2429386869) by Kim Lauenroth served as source material for this skill.

## Contributing

Contributions are open and welcome: bug reports, framework corrections, new references, better templates, and improvements to the skill and agent instructions. Read [CONTRIBUTING.md](CONTRIBUTING.md) to get started, and open an [issue](https://github.com/blude/digital-design-werkzeuge/issues) first if you plan a larger change.

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

[MIT](LICENSE) © 2026 Sarah Pratti
