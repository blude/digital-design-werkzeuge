# SDoc syntax rules and gotchas

Everything here was verified against StrictDoc 0.27.1 by running the parser. The failure modes are listed with their actual error messages, because several produce messages that point at the wrong thing.

## Contents

- [Ordering rules](#ordering-rules) — the four places order matters
- [Reserved and illegal field names](#reserved-and-illegal-field-names)
- [Whitespace rules](#whitespace-rules)
- [Content fields](#content-fields)
- [Choice fields and TBD](#choice-fields-and-tbd)
- [Composite nodes](#composite-nodes)
- [Relations](#relations)
- [Markdown and Mermaid](#markdown-and-mermaid)
- [Machine identifiers (MID)](#machine-identifiers-mid)
- [External grammars](#external-grammars)
- [Rendering control](#rendering-control)

---

## Ordering rules

Four separate ordering constraints. Three of them produce the same unhelpful error.

**1. Document header fields.** Fixed sequence:

```
TITLE → UID → VERSION → DATE → CLASSIFICATION → PREFIX → ROOT → OPTIONS → METADATA → VIEWS
```

`PREFIX` before `ROOT` catches people out. Wrong order gives:

```
TextXSyntaxError: Expected 'OPTIONS:' or 'METADATA:' or 'VIEWS:' or '\r?\n' or EOF
```

**2. `OPTIONS` keys.** Also fixed:

```
ENABLE_MID → MARKUP → AUTO_LEVELS → VIEW_STYLE → NODE_IN_TOC
```

Putting `AUTO_LEVELS` after `NODE_IN_TOC` gives `TextXSyntaxError: Expected EOF`, which is misleading — the file is fine apart from two swapped lines.

**3. `[GRAMMAR]` position.** Must come immediately after the document header, before any content node. A grammar placed after the first node is a parse error.

**4. Node fields must match grammar declaration order.** If the grammar declares `UID, STATUS, PRIORITY, TITLE, STATEMENT`, a node supplying `UID, PRIORITY, STATUS, ...` fails:

```
Semantic error: Wrong field order for requirement: [UID, PRIORITY, STATUS, TITLE, STATEMENT].
```

This error is actually helpful — it prints the order it received. Compare against the `.sgra` file.

`RELATIONS` is always the last field of a node.

---

## Reserved and illegal field names

The field-name pattern is:

```
(?!^UID)(?!^RELATIONS)[A-Z]+[A-Za-z0-9_\-]*
```

So **any custom field name beginning with `RELATIONS` is rejected** — including `RELATIONSHIPS`, which is a natural name for an entity's associations. It fails with:

```
TextXSyntaxError: Expected 'MID' or 'UID' or '(?!^UID)(?!^RELATIONS)...' or 'RELATIONS:'
```

Use `ASSOCIATIONS` instead. The grammars in `assets/grammars/` already do.

Reserved field names with built-in meaning: `MID`, `UID`, `LEVEL`, `PREFIX`, `TITLE`, `STATEMENT`, `DESCRIPTION`, `CONTENT`, `RATIONALE`, `COMMENT`, `STATUS`. Using them is fine — just be aware `STATUS` feeds the project statistics screen, and `RATIONALE`/`COMMENT` get special rendering.

---

## Whitespace rules

**One blank line between nodes.** Not zero, not two.

**A blank line is required between a `[[SECTION]]` header and the next node.** This fails:

```strictdoc
[[SECTION]]
TITLE: Architecture overview
[TEXT]
STATEMENT: Something.
```

with `TextXSyntaxError: Expected ... => ' overview *[TEXT] STA'` — note the error points at the section title line, not at the missing blank line.

**Multiline field values** are wrapped in `>>>` and `<<<` on their own lines:

```strictdoc
STATEMENT: >>>
Multiple lines
of content.
<<<
```

Single-line values are written inline and are parsed as plain text — no markup, no `[LINK:]` resolution. Anything needing markup or links must be multiline.

---

## Content fields

Each grammar element must declare **exactly one** content field, named `STATEMENT`, `DESCRIPTION` or `CONTENT`.

Fields declared **before** the content field are treated as single-line metadata. Fields declared **after** it may be multiline.

This is why `ACCEPTANCE_CRITERIA`, `RATIONALE`, `CONSEQUENCE` and similar sit after `STATEMENT` in every grammar in `assets/grammars/`, even though they read like metadata. There is no way to have a multiline field before the content field.

---

## Choice fields and TBD

`SingleChoice(A, B, C)` and `MultipleChoice(A, B, C)` are validated. An out-of-set value fails:

```
Semantic error: Requirement field has an invalid SingleChoice value: Speediness.
```

Hyphenated values work (`In-Review`, `Conditional-Go`, `Alternative-success`). Avoid spaces in choice values.

**`TBD` and `TBC` are accepted in any Choice field regardless of its option set.** They are counted on the Project Statistics screen as a document-maturity metric. Use them rather than inventing a `Unknown` option — that way the count of undecided fields stays visible.

`Tag` fields accept comma-separated alphanumeric tokens.

---

## Composite nodes

A node type declared `IS_COMPOSITE: True` can contain child nodes. Composite instances use doubled brackets:

```strictdoc
[[USE_CASE]]
UID: UC-01
...

[STEP]
UID: ST-01-1
STATEMENT: First step.

[[/USE_CASE]]
```

Child order is document order. **Do not number steps in the statement text** — the position is the number, and hand-written numbers go stale the moment a step is inserted.

`SECTION` is composite and must be declared in any custom grammar that uses it.

---

## Relations

Declared per element in the grammar:

```strictdoc
  RELATIONS:
  - TYPE: Parent
    ROLE: Satisfies
    REVERSE_ROLE: Satisfied by
```

Only the declared roles are permitted on that element. `REVERSE_ROLE` controls how the backward view reads.

Used on a node:

```strictdoc
RELATIONS:
- TYPE: Parent
  VALUE: BG-01
  ROLE: Satisfies
```

**Cross-document relations work.** UIDs are global across the project, so a node in one file can point at a node in another with no import or declaration. An unresolvable target fails:

```
error: Requirement F-1 references parent requirement which doesn't exist: UC-77.
```

### Never model a non-hierarchical relation as Parent

`Parent` means "is more abstract than". Symmetric or lateral relations — `conflicts with`, `depends on`, `duplicates` — are not that. Modelling a symmetric relation as reciprocal `Parent` relations does not produce a clean circular-reference diagnostic; it produces:

```
error: maximum recursion depth exceeded
```

For lateral references use an inline link inside a multiline field:

```strictdoc
STATEMENT: >>>
This conflicts with [LINK: SQR-02] and cannot be satisfied simultaneously.
<<<
```

Inline links **are** checked for existence:

```
error: DocumentIndex: the inline link references an object with an UID that does not exist: NOPE-1.
```

So a lateral reference gets referential integrity without false hierarchy. What it loses is the semantics — nothing records that the link means "conflicts with", so state it in the surrounding prose.

`[ANCHOR: name]` marks a link target inside a document. Only nodes with a `UID` participate in the traceability graph at all.

---

## Markdown and Mermaid

Set `MARKUP: Markdown` in `OPTIONS` (RST is the default). Then `**bold**`, backticks, tables and lists behave as expected.

**Mermaid requires Markdown markup.** The RST `.. mermaid::` directive is not registered and fails with `Unknown directive type "mermaid"`. In Markdown, a fenced block works:

````
```mermaid
graph LR
  A[Editor] --> B[Language server]
```
````

Mermaid is enabled by default in 0.27.1 — the old `MERMAID` project feature flag is deprecated and no longer needed.

---

## Machine identifiers (MID)

A MID is a generated 32-character hexadecimal identifier StrictDoc attaches to a node alongside its human UID. It buys exactly one thing, and it is worth being precise about what:

**A MID survives a UID rename and a node move.** Rename `SG-01` to `SG-11` across a project and the MID is unchanged, so a diff between two revisions can distinguish a renamed requirement from a deletion plus an addition. Without MIDs that distinction is guesswork, and StrictDoc's own diff and changelog screens have to guess too.

That is the whole benefit. A project that never renames identifiers and never uses the web UI gains nothing.

### The cost

One opaque line per node, immediately under the node tag:

```strictdoc
[SYSTEM_GOAL]
MID: e7e53cb04d19471580f7046c259e7286
UID: SG-01
```

In a document set whose value depends on being read by people — and at L0 and L1 the readers are executives and business stakeholders — that is a real cost. Which is why MIDs are off by default in this framework and enabled deliberately, typically once a document set is stable enough that renames and history matter more than the noise.

### Turning it on

Two things are required together:

1. `ENABLE_MID: True` as the **first** key of the document's `OPTIONS` block.
2. A `MID` field declared on **every** element of the grammar.

Miss the second and StrictDoc refuses to parse, with an unusually clear message:

```
Semantic error: Grammar element 'GOAL' is missing the MID field which
contradicts to the DOCUMENT's ENABLE_MID setting.
```

The `MID` field does **not** have to be the first field declared. As with every other field, the node's field order follows the grammar's declaration order, so declaring `MID` after `UID` puts it after `UID` in the node.

### Values are injected by write-back, not by export

`strictdoc export` never writes to your documents, so it generates no MIDs. `strictdoc format` does, as do the web UI and the `manage` commands. So enabling MIDs is a two-step operation: change the setting, then run a write-back to populate it.

Injection is idempotent — running `format` repeatedly leaves existing MIDs alone.

**Commit before the first `format` after enabling.** It rewrites every document, and the diff is almost entirely MID lines.

### The gotcha that silently defeats a migration

`strictdoc format` writes the setting explicitly as `ENABLE_MID: False` when the feature is off. So any project that has ever been formatted already has the key present. A migration that checks whether the key *exists* rather than what its *value* is will conclude there is nothing to do, add the grammar fields, and produce a project that looks migrated and generates no MIDs.

Flip the value; do not insert the key.

### Turning it off

Set `ENABLE_MID: False`. Leave the `MID` fields and values in place — they are inert without the setting, StrictDoc parses them without complaint, and keeping them preserves the identity history if the feature is re-enabled later. Deleting them throws away the only thing that made them worth having.

## External grammars

A grammar can live in its own `.sgra` file and be imported:

```strictdoc
[GRAMMAR]
IMPORT_FROM_FILE: L1_solution_design_concept.sgra
```

The `.sgra` file contains the `[GRAMMAR]` header and the `ELEMENTS:` block, nothing else. Path is relative to the importing document.

**Importing does not weaken validation.** A document importing a grammar still rejects element types that grammar does not declare, so level enforcement is preserved. Verified: importing four different grammars into four documents keeps each document restricted to its own element types, while cross-document relations continue to resolve.

Externalising the grammars shortens the documents by roughly 25–30%.

---

## Rendering control

`VIEW_STYLE` takes five values, settable per document under `OPTIONS` or per element under `PROPERTIES`:

| Value | Effect |
| --- | --- |
| `Narrative` | Metadata shown, fields printed without tables. Default. Best for prose-heavy nodes. |
| `Inline` | Table-based variant |
| `Table` | Table-based variant |
| `Zebra` | Table-based variant, alternating rows |
| `Plain` | Field content only, no metadata |

Element-level setting wins over document-level. The grammars in `assets/grammars/` use `Plain` for step nodes and `Inline` for extensions, so scenarios read as flows rather than as stacks of metadata tables.

Other knobs: `NODE_IN_TOC: True/False` controls whether requirement titles clutter the table of contents; `AUTO_LEVELS: On/Off` controls automatic section numbering; `LEVEL: None` on a section excludes it from numbering and cascades to its children.

Note the documentation contradicts itself on `VIEW_STYLE`: the options summary table lists only `Inline, Table, Zebra` and calls `Inline` the default. The prose section is correct — all five are valid and `Narrative` is the default.

---

## Useful commands

```bash
strictdoc export .                          # HTML to output/html
strictdoc export . --formats=json           # machine-readable graph
strictdoc export . --formats=reqif-sdoc     # interchange format
strictdoc server .                          # web UI, 127.0.0.1:5111
strictdoc format .                          # canonical formatting
strictdoc manage auto-uid .                 # assign missing UIDs by prefix mask
strictdoc manage new --node-type USE_CASE   # scaffold a node with TBD fields
```

`strictdoc format` rewrites every document on first run even without `document_line_width` set. It is idempotent afterwards and preserves content, but commit before running it the first time.
