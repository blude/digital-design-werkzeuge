# Traceability

Relations are what make the four documents one artifact rather than four. Get them right and the tool can answer "what breaks if this changes" and "what asked for this". Get them wrong and the graph is decorative.

## The roles

| Role | Meaning | Reverse | Typical use |
| --- | --- | --- | --- |
| `Satisfies` | delivers a goal at the level above | Satisfied by | `BG-01` → `IMP-01`, `SG-01` → `BG-01`, `G-01` → `SG-01` |
| `Refines` | same concept, more detail or more measurable | Refined by | `SQR-01` → `BQR-01`, `E-01` → `BE-01`, `SC-01` → `BC-01` |
| `Realises` | an element or flow implements a business concept | Realised by | `SE-01` → `VCA-01`, `SSc-01` → `BP-01`, `UC-01` → `SSc-01` |
| `Supports` | a process or requirement serves a goal or business quality | Supported by | `BP-01` → `BG-01`, `SQR-01` → `BQR-01` |
| `Achieves` | a scenario demonstrates a goal | Achieved by | `SSc-01` → `SG-01` |
| `Represents` | a user type stands for a business element | Represented by | `UT-01` → `VCA-01` |
| `Constrained by` | limited by a constraint | Constrains | `TF-03` → `SC-02` |
| `Extends` | alternative flow branching from a step | Extended by | `EX-01-1` → `ST-01-2` |
| `Measures` | success criterion observing an impact (L0 only) | Measured by | `SUC-01` → `IMP-01` |
| `Selects` | recommendation choosing an option (L0 only) | Selected by | `REC-01` → `SO-02` |
| `Implements` | an element constraint satisfies a system constraint | Implemented by | `C-01` → `SC-01` |
| `Calls` | an outbound interface reaches a partner | Called by | `TO-01` → `PE-01` |

Choosing between `Refines` and `Realises` is the judgement call that comes up most. `Refines` keeps the same kind of thing and adds detail — a quality requirement becoming measurable. `Realises` changes the kind of thing — a business concept becoming a component. If the parent and child are the same species, it's `Refines`.

**Why one role is passive.** Every role above reads as *child verb parent* — "SG-01 satisfies BG-01" — except `Constrained by`, which reads "TF-03 is constrained by SC-02". That is deliberate, not an oversight.

A relation is always declared on the child, pointing at the parent. For every other role the natural direction of the verb already runs child to parent: a goal is satisfied, a concept is refined, a step is extended. Constraint is the one relation whose natural direction runs the other way — a constraint constrains a requirement; the requirement does nothing *to* the constraint. Stating it from the child therefore needs the passive voice, and the active form is the reverse role, `Constrains`, which is how it reads on the constraint's own page. That is the direction you would normally read it from anyway.

Renaming it to an active child-side verb — `Respects`, `Complies with` — would make the column uniform at the cost of making the sentence less true, and would read worse in the document. The asymmetry in the table reflects a real asymmetry in the relationship.

## Downward references are derived, never written

The framework templates ask for optional downward references — "Implemented by SQR-02", "Realized by SSc-01", "Implemented As: SE-01", "Implemented by SC-08". None of these should be written by hand, and no grammar field exists for them.

Every one is the reverse view of a relation the child declares. `SQR-01` declaring `Refines → BQR-02` causes "Refined by SQR-01" to appear on the `BQR-02` page, because the grammar sets `REVERSE_ROLE`. The reference is therefore always current, and an empty reverse view is real information: nothing below has claimed that requirement yet.

This is the largest maintenance saving the tooling offers on layered documentation. Declare relations upward only, once, at the lower level.

## Which level links to which

Every non-L0 node should have at least one parent. Typical patterns:

```
L1 → L0    BG- Satisfies IMP-        BC- Refines BRC-
           VP- Refines SH-
within L1  VP- Satisfies BG-         VCA- Realises VP-
           BP- Supports BG-          BQR- Satisfies BG-
           PA- Extends PS-
L2 → L1    SG- Satisfies BG-         UT- Represents VCA-
           SE- Realises VCA-         SSc- Realises BP-
           SQR- Supports BQR-        SC- Refines BC-
within L2  AP- Satisfies SG-         SSc- Achieves SG-
           SE- Constrained by SC-    SA- Extends SSt-
L3 → L2    G- Satisfies SG-          UC- Realises SSc-
           TO- Calls PE-             QR- Supports SQR-
           C- Implements SC-
L3 → L1    E- Refines BE-
within L3  UC- Achieves G-           TF- Achieves G-
           UI- Realises UC-          TF- Constrained by C-
           EX- Extends ST-           FA- Extends FS-
```

`E- Refines BE-` reaches past L2 deliberately: business entities are declared at L1 and the technical entities that implement them live at L3, with nothing to say at L2.

## Direction

`Parent` means "is more abstract than". Relations point **upward and outward** — from the detailed thing to the thing that asked for it. Never sideways, never downward.

Two checks worth running mentally on any relation:

- **Could the parent exist without the child?** If yes, the direction is right. A business goal exists whether or not any system goal serves it; the reverse is not true.
- **Is the parent something the child exists in service of?** If not, the direction is backwards.

**Same-level relations are normal, not suspect.** What matters is the abstraction gradient, not the document boundary. Every level has an internal gradient — goals at the top, then the things serving them, then the steps and alternatives within those:

```
within L0  SUC- Measures IMP-        REC- Selects SO-
within L1  VP- Satisfies BG-         VCA- Realises VP-
           BP- Supports BG-          BQR- Satisfies BG-
           PA- Extends PS-
within L2  AP- Satisfies SG-         SSc- Achieves SG-
           SE- Satisfies SG-         SE- Constrained by SC-
           SA- Extends SSt-
within L3  UC- Achieves G-           TF- Achieves G-
           UI- Realises UC-          TF- Constrained by C-
           EX- Extends ST-           FA- Extends FS-
```

What is genuinely wrong is a relation pointing *downward* — a goal declaring a relation to the requirement that serves it — or *sideways with no gradient*, which is the lateral case below.

## Lateral relations do not use Parent

`conflicts with`, `depends on`, `duplicates`, and cross-perspective references between an entity and a process are not hierarchical. Forcing them into `Parent` crashes the tool with `maximum recursion depth exceeded` rather than reporting a cycle.

Use an inline link in the statement text instead:

```strictdoc
STATEMENT: >>>
Cannot be satisfied together with [LINK: SQR-02] under the current
constraint SC-03.
<<<
```

The link target is checked for existence but creates no hierarchy. The semantics live in the prose. This is a genuine limitation of the model, not a workaround to feel clever about — record the reasoning in the text so a reader understands the relationship the graph cannot express.

## Two ways to record a constraint's reach

Constraints are the one place where the framework offers two mechanisms for the same information, and it is worth knowing which to use.

**`APPLIES_TO`** is a field on the constraint or quality requirement, listing what it touches as inline links. It is the template-native mechanism and exists on all six such element types across L1, L2 and L3. Link targets are validated for existence, but **no graph edge is created** — an inline link is not a relation.

**`Constrained by`** is a relation declared on the constrained thing, pointing at the constraint. It creates a real edge, so the constraint's page shows "Constrains SE-01, TF-03" and impact analysis picks the dependency up. It is declared on only two element types: `SOFTWARE_ELEMENT` at L2 and `TECHNICAL_FUNCTION` at L3.

Use them for different purposes:

- **`APPLIES_TO` is the inventory.** Complete, written once from the constraint's side, cheap to maintain. Every constraint should have it.
- **`Constrained by` is selective.** Use it where the constraint materially shaped that specific design and you want the dependency traceable — the cases where someone revisiting the requirement needs to know why it looks the way it does.

They can disagree, and the disagreement is informative rather than symmetrical. A node listed in `APPLIES_TO` with no relation is normal and expected — that is most of them. A `Constrained by` relation whose target does not list the child in its `APPLIES_TO` is probably an oversight in the constraint, since a constraint that shaped a design should know it did.

## Orphans and derived requirements

An orphan — a node with no parent — is usually a defect. It means something is being built that nothing asked for.

The legitimate exception is a **derived requirement**: something that follows from an implementation decision rather than from a stated need. Debouncing analysis is a good example — no stakeholder asked for it; it falls out of the decision to analyse on every keystroke.

Derived requirements are allowed, but must be marked and justified. The L3 grammar carries a `DERIVED: Yes | No` field for this. When `DERIVED: Yes`:

- Set the field explicitly rather than leaving it absent
- Write a `RATIONALE` explaining what decision it follows from
- Say why no parent exists

A derived requirement with no rationale is indistinguishable from a mistake, which is the whole reason for the field.

## Checking the graph

```bash
strictdoc export .                      # fails on any unresolved relation target
strictdoc export . --formats=json       # the graph as data
```

An unresolved target is a hard error naming both ends:

```
error: Requirement F-1 references parent requirement which doesn't exist: UC-77.
```

In the HTML output, the **Deep Traceability** view is where a full chain becomes visible in one screen. Use it to sanity-check that every L3 item reaches an L0 impact. A chain that stops at L2 usually means an intermediate `Satisfies` is missing rather than that the requirement is unnecessary.

Counting edges by role is a quick health check. A document set with many `Refines` and almost no `Satisfies` tends to mean requirements are being restated rather than justified.
