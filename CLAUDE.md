# Claude guidance for this repository

This repository contains reusable Claude skills, agent guidance, and supporting assets for digital-design documentation workflows. Treat it as a content-first, instruction-driven project rather than a general application codebase.

## Repository purpose

- Maintain high-quality skills for authoring structured design documents.
- Keep agent and skill guidance clear, specific, and easy to route to the right capability.
- Preserve the relationship between prompts, templates, references, and validation scripts.

## Working principles

- Prefer small, focused changes over broad rewrites.
- Keep instructions explicit, practical, and grounded in the repository’s actual workflow.
- When adding or modifying a skill, make the behavior easy to understand and easy to trigger.
- Avoid inventing requirements or design content; ask for clarification or mark the gap clearly when needed.
- Preserve existing structure unless there is a strong reason to change it.

## Structure to respect

- skills/ contains reusable skill definitions and supporting assets.
- agents/ contains agent-oriented guidance for specialized workflows.
- references/ contains framework-specific guidance used by the skills.
- assets/ contains templates, grammars, and other reusable inputs.
- scripts/ contains validation and helper utilities.

## When working on skills

- Update the skill’s main instruction file, usually SKILL.md, first.
- Keep the skill description short, action-oriented, and specific enough for routing.
- Make the instructions reflect the real workflow, including setup, procedure, validation, and output expectations.
- If a skill relies on templates, grammars, or references, keep those files aligned with the instructions.
- Prefer reusable patterns over one-off examples.

## When working on agent or plugin-style guidance

- Keep the guidance focused on one clearly defined capability.
- State when the agent should be used, what inputs it expects, and what output it should produce.
- Define boundaries clearly so the agent does not overreach into unrelated tasks.
- If a new capability needs new assets or references, add them alongside the guidance rather than embedding everything inline.

## Documentation and content conventions

- Write in a concise, practical style.
- Prefer clear step-by-step procedures over abstract explanations.
- Use examples where they help, but keep them minimal and realistic.
- When a document or design detail is uncertain, say so explicitly instead of guessing.

## Validation expectations

If a change affects templates, references, or document structure, validate it before considering the work complete.

- Run the relevant validation script from the repository root when available.
- For documentation-oriented changes, check that the updated instructions still match the repository structure and examples.
- If validation fails, fix the root cause rather than patching around the symptom.

## Preferred workflow

1. Understand the existing skill or agent behavior before editing it.
2. Make the smallest change that solves the problem.
3. Keep related assets and documentation in sync.
4. Validate the result and summarize the change clearly.

## Important reminder

This repository is most effective when skills and agent guidance are precise, reusable, and tightly connected to the supporting assets they depend on.
