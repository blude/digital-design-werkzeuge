---
name: digital-design-docs
description: Generate hierarchical design documentation using the four-level framework (L0 Digital Design Brief, L1 Solution Design Concept, L2 System Design Concept, L3 Element Design Concept) as validated StrictDoc documents with typed requirements and cross-level traceability. Use this skill whenever the user mentions a design brief, solution design concept, system design concept, element design concept, L0/L1/L2/L3 design documents, or asks to write, extend, review or validate requirements documentation in this four-level structure — including when they only name one level, refer to it loosely as "the design docs" or "the spec", ask for a Go/No-Go brief, or want requirements with IDs like BG-01, SE-02, UC-03. Also use it when they ask to add a requirement, use case, system element or constraint to existing documents in this structure, since new nodes must match the level's grammar and trace to a parent.
---

# Four-level digital design documentation

Generates the L0–L3 design documentation framework as StrictDoc `.sdoc` documents. Each level is a separate document with its own grammar, which means the tool enforces that a statement sits at the right level of abstraction, and validates every cross-level reference.

The output is a working StrictDoc project: `strictdoc export .` produces browsable HTML with traceability views, and fails the build on a broken reference.

## What makes this worth doing properly

The framework's value is the traceability between levels, not the documents individually. An L3 requirement that traces to an L0 impact tells you why it exists; one that doesn't is something being built for no recorded reason. So relations matter more than prose volume, and a validated document with fewer nodes beats a long one whose references don't resolve.

## Setup

Check StrictDoc is available, install if not:

```bash
strictdoc --version || pip install strictdoc --break-system-packages
```

Create the project and copy the grammars in. The four `.sgra` grammar files are the shared vocabulary — they define every element type, its fields, and its permitted relations. Documents import them, so the grammar is defined once and the documents stay short:

```bash
mkdir -p <project>/docs
cp <skill>/assets/*.sgra <project>/docs/
```

Copy the templates for the levels being written:

```bash
cp <skill>/assets/templates/L1_solution_design_concept.sdoc <project>/docs/
```

The templates carry the full section skeleton for their level, plus one stub node per element type with the fields in the order the grammar requires. Fill them in rather than writing from scratch — field order is the single most common parse failure, and the templates already have it right.

The four templates validate together as a set, so copying all of them gives a working skeleton immediately.

## Procedure

### 1. Establish which levels are in scope

Ask if it isn't clear. Writing all four is common for a new initiative; writing one is common for an addition. Note that L3 is **one document per element** — a system with four software elements has four L3 documents.

Then read `references/framework.md` for the section structure, audience and ID prefixes, followed by the per-level reference file for each level in scope — `references/L0-design-brief.md`, `references/L1-solution-design-concept.md`, `references/L2-system-design-concept.md` or `references/L3-element-design-concept.md`. The overview alone is not enough to write a level well; each per-level file carries rules that only apply there.

### 2. Work out what the content actually is

Before writing anything, establish:

- What the initiative is, in the user's own terms
- Who the stakeholders and users are
- What constraints exist, and where they come from
- For L2: what the elements are — software, hardware, partner, user types
- For L3: which element this document covers, and which sections apply to it

Pull as much as possible from the conversation, uploaded documents, or existing higher-level documents in the project. Ask about the gaps rather than inventing. Invented content in a design document is worse than a `TBD`, because `TBD` is visible and gets counted on the statistics screen while an invention reads as a decision.

Where something genuinely isn't known, write `TBD` (unknown) or `TBC` (known but not yet agreed). These are accepted in any Choice field regardless of its options.

### 3. Write top-down

Write L0 first, then L1, L2, L3. Lower levels reference upward, so the parent IDs must exist before a child can point at them.

**If a parent level is out of scope**, omit the `RELATIONS` blocks that would point into it rather than referencing IDs that don't exist — an unresolvable target is a hard build failure. Tell the user which relations were omitted and why, so they can be added when the parent document appears.

Read `references/traceability.md` before writing relations. Getting the roles right is most of the value.

### 4. Validate after every document

Do not write all four and validate at the end. Validate each one as it's finished, from the project root:

```bash
python3 <skill>/scripts/validate.py
```

This runs three stages in the order that fails fastest, and exits non-zero if any fail:

1. **`strictdoc export`** — syntax, grammar conformance, relation targets. Authoritative. If it fails the run stops here, because the later checks would be reading an incompletely parsed project.
2. **Entity attribute references** — the `E-01.1` style IDs that StrictDoc cannot link-check.
3. **Framework coverage** — the traceability expectations the framework states.

Add `--quick` to skip stage 1 while iterating on structure.

When stage 1 fails, `references/sdoc-syntax.md` lists every failure mode with its actual error message — several point at the wrong line, so match on the message rather than trusting the line number. The most frequent causes:

- **Wrong field order** — the error prints the order received; compare against the `.sgra`
- **Missing blank line** after a `[[SECTION]]` header, or between nodes
- **Document header order** — `PREFIX` before `ROOT`; `[GRAMMAR]` before any content
- **`OPTIONS` key order** — `ENABLE_MID, MARKUP, AUTO_LEVELS, VIEW_STYLE, NODE_IN_TOC`
- **A field name starting with `RELATIONS`** is illegal — use `ASSOCIATIONS`
- **Unresolvable relation target** — check the UID exists and is spelled exactly

**Read the INFO and WARNING sections, don't just check the exit code.** Stages 2 and 3 pass while still reporting things worth a human decision: an attribute nothing references, a requirement with no upward relation that was deliberately marked exempt, or prose claiming a relationship the relations do not declare. That last one is the most valuable output either script produces, because it catches a document asserting coverage it has not actually recorded.

### 5. Check the shape, not just the correctness

A clean validation means the syntax parses, references resolve, and the expected relations exist. It does not mean the result is well-proportioned. From the project root:

```bash
python3 <skill>/scripts/trace_report.py
```

This reports nodes per level, relations by role, level crossings, nodes per type, and the most-referenced requirements. What to look for:

- **A downward crossing** is flagged explicitly and is always wrong — relations point upward.
- **Many `Refines` with almost no `Satisfies`** usually means requirements are being restated rather than justified.
- **A thin type count** — one `VP-` for four `BG-`, or no `SSc-` at all — shows a section that was outlined and never written.
- **The most-referenced list** should contain the requirements the design would actually break without. If it doesn't, the traceability is recording something other than what the design depends on.

Then confirm one chain actually reaches the top:

```bash
python3 <skill>/scripts/trace_report.py --chain TF-01
```

An L3 requirement should walk up through L2 and L1 to an L0 impact. A chain that stops early usually means an intermediate relation is missing rather than that the requirement is unnecessary.

### 6. Report

Tell the user:

- Which documents were created and how to run them
- The traceability edge count by role
- Every `TBD`/`TBC` left behind, and what decision each is waiting on
- Any judgement call made on their behalf — an assumed constraint, an inferred element boundary, a relation whose role was ambiguous
- Any relations omitted because a parent level was out of scope

Then present the files.

## Rules that matter most

**One statement, one level.** The grammar enforces this — putting a `BUSINESS_GOAL` in the L2 document fails with `Semantic error: Invalid node type: BUSINESS_GOAL`. When that error appears, the fix is almost never to change the grammar; it's that the content belongs in a different document.

**At L3, classify every step.** Use case steps are `User-interaction`, `Function-call`, `Outbound-call` or `Activity`; technical function steps are `Data-operation`, `Entity-access`, `Function-call` or `Outbound-call`. The enum forces the author to notice when a step is doing two things, which is the commonest defect in a scenario. Prefer a function call over a direct outbound call — it keeps retry and error handling in one place.

**At L3, actors come from L2.** An actor in a use case must be a `UT-`, `SE-` or `PE-` from the System Design Concept, referenced by ID. If the needed actor does not exist at L2, that is a gap at L2, not a licence to invent a role here.

**Never number steps in their text.** Step order is document order. Written numbers go stale the moment a step is inserted, and stale numbers in a scenario are the specific defect this structure exists to prevent.

**Alternative flows anchor to a step by relation, not by convention.** An `EX-` node carries `Extends` pointing at the `ST-` it branches from, so a branch pointing at a step that doesn't exist fails the build. This only happens at L3.

**Never model a lateral relation as `Parent`.** `conflicts with` and `depends on` are not hierarchical, and forcing them in crashes the tool with `maximum recursion depth exceeded` rather than reporting a cycle. Use `[LINK: UID]` in the statement text — validated for existence, no false hierarchy — and state the relationship in the prose.

**Mark derived requirements.** A node with no parent because it follows from an implementation decision rather than a stated need gets `DERIVED: Yes` and a `RATIONALE` saying what decision it follows from. Otherwise it's indistinguishable from an orphan.

**Executive summaries at L1 are for people who read nothing else.** Each major L1 section opens with one. Write it so a stakeholder who skips the specifications still understands the section.

**Use element IDs in diagrams.** Mermaid node labels should carry the `SE-`/`UT-`/`PE-` ID. A diagram whose boxes correspond to identified elements can be checked against the prose; one with free-text boxes drifts silently.

**Never hand-write a downward reference.** The framework templates ask for optional fields like "Implemented by SQR-02", "Realized by SSc-01" and "Implemented As: SE-01". Do not write these, and do not add grammar fields for them. Each is the reverse view of a relation the child already declares at the level below, and StrictDoc renders it automatically because the grammar sets `REVERSE_ROLE`. Hand-maintained back-references are the classic failure mode of layered documentation — written once, never updated. Derived ones cannot go stale.

**At L0, brevity is a requirement, not a preference.** A design brief is 2–3 pages for a small solution and readable in 15–20 minutes. Its whole value is being read in full by people whose attention is scarce, so a fifteen-page brief has failed regardless of content quality. When a section runs long, the detail belongs at L1 or below — summarise here, elaborate there.

**At L0, present options rather than choosing between them.** The Go/No-Go decision is about whether to proceed to solution design, not about which approach to build. `SOLUTION_OPTION.ASSESSMENT` offers `Carry-forward` and `Deprioritised` rather than `Recommended` for exactly this reason.

**Delete optional sections rather than stubbing them.** L0's Decision & Recommendation and Implementation Planning are both optional, and Strategic Alignment and Appendices are too. An empty section reads as an oversight; an absent one reads as a decision the reader can ask about. The same applies to L3, where several sections do not apply to every element type — there, say which and why, because the reader cannot tell an inapplicable section from a forgotten one.

**Deployment detail belongs in a fifth document.** The framework names a **System Realization Concept** for deployment architecture, infrastructure specification, integration configuration and implementation detail. It sits alongside the four levels, not within them. If an L2 description reaches processor counts, memory sizes or connection pool settings, move it there.

**Say so when a document is not warranted.** A design brief is for new initiatives, significant investment, multi-stakeholder alignment or strategic decisions. For a small enhancement, a bug fix, an internal tool with clear requirements, or a prototype, a full brief is ceremony — offer to go straight to L1 or write something lighter instead.

## Reference files

Read these as needed rather than upfront. Every pointer to a reference file lives here — the reference files do not route to each other.

### Always, for any level

**`references/framework.md`** — the overview. Section structure, audience and ID prefixes for all four levels, plus the tests for deciding which level a statement belongs to. Read this first, then the file for the level being written.

### One per level

**`references/L0-design-brief.md`** — before writing an L0. The length constraint and why it matters, when a brief is *not* warranted, guidance for each of the fifteen subsections, the element fields, document control, and which L0 elements are relation targets from below.

**`references/L1-solution-design-concept.md`** — before writing an L1. The future press release format, field-level guidance per element type, the business-versus-technical quality distinction, and which references are derived rather than authored.

**`references/L2-system-design-concept.md`** — before writing an L2. The Mermaid mapping for the recommended diagram notation, the procurement-status rule on hardware, scenario step-writing conventions, and the nine technical quality categories.

**`references/L3-element-design-concept.md`** — before writing an L3. The four element profiles, both step classifications, the goal-referencing criteria for technical functions, the entity attribute table, and the inbound-versus-outbound division of labour.

### Cross-cutting

**`references/traceability.md`** — before writing relations. The roles and their reverse names, which level links to which, why downward references are derived rather than written, when a same-level relation is legitimate, the two ways to record a constraint's reach, and how to handle derived requirements and lateral links.

**`references/sdoc-syntax.md`** — when the parser rejects something, or before using an unfamiliar construct. Every failure mode with its real error message, the four ordering rules, reserved field names, and the rendering controls.

### Grammar files

The `.sgra` files in `assets/` are worth reading directly when writing nodes of an unfamiliar type: the field declaration order **is** the required node field order, and the `SingleChoice(...)` lists are the permitted values.

## Scripts

Pure standard library, no dependencies beyond the Python that StrictDoc already requires. Run them from the project root — the directory containing `docs/`.

| Script | Purpose |
|---|---|
| `scripts/validate.py` | **The one to run.** StrictDoc export, then attribute references, then coverage. Exits non-zero on failure, so it works as a CI gate. `--quick` skips the export. |
| `scripts/trace_report.py` | Graph shape: nodes per level, relations by role, level crossings, most-referenced requirements. `--chain <UID>` walks one requirement upward to its L0 impact. |
| `scripts/check_attribute_refs.py` | Entity attribute IDs (`E-01.1`) — references to attributes no entity declares, attributes declared under the wrong entity, duplicates. StrictDoc cannot check these. |
| `scripts/check_coverage.py` | The framework's traceability expectations — goals with no scenario, requirements with no upward relation, and prose claiming a relationship the relations do not declare. |
| `scripts/enable_mid.py` | Turns StrictDoc machine identifiers on or off across a project — grammar fields and the document setting. `--dry-run` to preview, `--disable` to reverse. |
| `scripts/sdoc.py` | Shared parser. Not run directly. |

Two design points worth knowing when reading their output:

**A rule is skipped when the relevant kind of node is absent.** Writing one level in isolation produces no spurious findings, because a rule expecting an L1 parent does not fire when no L1 node exists anywhere in the project.

**Machine identifiers are off by default, and that is a deliberate default rather than an oversight.** A MID survives a UID rename, so a diff can tell a renamed requirement from a deleted one — but it costs an opaque 32-character line on every node in documents meant to be read by executives. Suggest enabling them when a document set has stabilised and renames start to matter, not while it is being drafted. `scripts/enable_mid.py` handles the migration in both directions; `references/sdoc-syntax.md` covers the constraints.

**Deliberate exemptions are reported, not hidden.** A requirement with no upward relation is an error unless it carries `EXTERNALLY_SOURCED: Yes`, `ELEMENT_SPECIFIC: Yes` or `DERIVED: Yes`, in which case it appears under INFO with the marker shown. That keeps a considered decision visible without failing the build.

## Working with existing documents

When adding to a project that already has these documents:

1. Read the existing `.sgra` for the level being extended — the project may have customised it
2. Read enough of the target document to match its conventions and find the next free ID
3. Never renumber an existing ID. Leave gaps where nodes were deleted
4. Add the node, then validate the whole project, not just the changed file — a new relation can break another document

If the project has inline grammars rather than imported ones, offer to extract them to `.sgra` files. It shortens the documents by 25–30% and removes the duplication of choice-value lists across levels. Verify the export is still clean afterwards.
