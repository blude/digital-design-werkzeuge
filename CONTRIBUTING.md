# Contributing

Contributions are open and welcome: bug reports, framework corrections, new references, better templates, and improvements to the skill and agent instructions.

For anything larger than a small fix, open an [issue](https://github.com/blude/digital-design-werkzeuge/issues) first so we can agree on the approach before you invest time.

## What lives where

| Path | Purpose |
| --- | --- |
| `skills/authoring-docs/SKILL.md` | Skill entry point. Update this first when behavior changes. |
| `skills/authoring-docs/assets/grammars/` | StrictDoc grammars, one per level. |
| `skills/authoring-docs/assets/templates/` | Starter documents. Must stay in sync with the grammars. |
| `skills/authoring-docs/references/` | Framework and syntax guidance the skill reads. |
| `skills/authoring-docs/scripts/` | Validation and traceability tooling. |
| `scripts/` | Repository tooling. `build-skill.sh` packages the skill as a zip for Claude desktop. |
| `agents/` | Agent definitions. One capability per agent. |

## Setup

```bash
pipx install strictdoc   # needed for validation
```

## Making a change

1. Fork the repo and create a branch.
2. Make the smallest change that solves the problem. Avoid unrelated refactors.
3. If you touch a grammar, template, or reference, keep the others aligned with it.
4. Validate. Copy the grammars and templates into a scratch project and run:

   ```bash
   python3 skills/authoring-docs/scripts/validate.py <scratch-project>
   ```

   CI also runs `strictdoc export` on the shipped templates, so a grammar change that breaks a template fails the build.
5. Open a pull request and fill in the checklist.

## Writing guidelines

- Skill descriptions are short, action-oriented, and specific enough for routing. They decide when the skill triggers.
- Explain *why*, not just *what*. Prefer step-by-step procedures over abstract explanation.
- Do not invent requirements or design content. State uncertainty explicitly.
- Keep examples minimal and realistic.

## Commits

One logical change per commit. Use a short imperative subject, optionally with a type prefix (`fix:`, `docs:`, `chore:`).

## Conduct

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

Contributions are licensed under the [MIT License](LICENSE).
