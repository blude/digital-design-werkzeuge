# L0 — Digital Design Brief

## Purpose and shape

A concise, high-level summary of a planned initiative that gives management enough to make a Go/No-Go decision without technical detail.

| | |
| --- | --- |
| **Audience** | Management, executives, decision-makers |
| **Purpose** | Enable an informed Go/No-Go decision on proceeding to a vision and initial solution design |
| **Typical length** | 2–3 pages for a small solution; more only as size and complexity demand |
| **Typical effort** | 1–3 days to create |
| **Reading time** | 15–20 minutes |

**Take the length constraint literally.** This document's value comes from being read in full by people whose attention is scarce. A brief that runs to fifteen pages has failed regardless of content quality, because the audience will skim the recommendation and ignore the analysis. When a section runs long, the detail belongs at L1 or below — write the summary here and the substance there.

## Two rules that shape everything else

**Present options, not decisions.** The Solution Space section explores what is possible. It does not choose. Selection happens at L1 and L2, informed by this brief. The grammar reflects this: `SOLUTION_OPTION.ASSESSMENT` offers `Carry-forward`, `Deprioritised`, `Rejected` and `TBD` — deliberately not "Recommended", which would overcommit at this level.

**The Go/No-Go is about proceeding, not about picking.** The decision being asked for is whether to invest in solution design, not which approach to build. A recommendation that names a winning option has usually skipped a phase. If a brief genuinely does recommend one, use the `Selects` relation — but the `STATEMENT` should still be about proceeding.

## What the brief is not

- Not a requirements specification — that is L1
- Not a technical architecture — that is L2
- Not a project plan — that comes after approval
- Not a final commitment — decisions can be revised during detailed planning

## When to write one, and when to say no

**Write a brief when** a new initiative is starting, significant investment is required, multiple stakeholders need to align, management approval is needed, or a strategic decision is required.

**Say so when a brief is not warranted:** small enhancements to existing systems, bug fixes and maintenance, internal tools with clear requirements, prototypes and experiments. If the user's initiative falls in this category, tell them a brief is probably ceremony and offer to go straight to L1 or to a lighter document. Producing an eight-section brief for a two-week internal tool discredits the framework rather than serving it.

## Sections

Two of the six top-level sections are optional. The template marks both, and the guidance is worth honouring rather than filling them with placeholders.

| Section | Subsections | Element types |
| --- | --- | --- |
| 1. Context of the initiative | Current Situation · Motivation for Change · Potential Customers and Users · Key Stakeholders · Related Solutions · Competitive Landscape | `SH-` `RS-` |
| 2. Vision | Future State Description · Expected Impact · Strategic Alignment *(optional)* | `IMP-` |
| 3. Solution Space | Solution Approach Options · Potential Functionality · Potential Technologies | `SO-` |
| 4. Constraints | Resource · Budget · Timeline · Other | `BRC-` |
| 5. Decision & Recommendation *(optional)* | Success Criteria · Risk Assessment · Go/No-Go Recommendation | `SUC-` `RSK-` `REC-` |
| 6. Implementation Planning *(optional)* | Project Timeline · Transformation Framework · Process & Stakeholder Acceptance | — |
| Appendices *(optional)* | Supporting Data · References | — |

**Section 5** is included when the brief documents a formal decision with defined success criteria, structured risk assessment, or explicit Go/No-Go conditions. It can be omitted when the decision context is straightforward.

**Section 6** is included when the brief needs to record agreed timelines, a transformation framework, or post-approval process steps. Omit it when planning detail belongs in the subsequent Solution Design.

When omitting an optional section, delete it rather than leaving it stubbed. An empty section reads as an oversight; an absent one reads as a decision — and the reader can ask.

## Writing each section

### Context of the initiative

Six subsections, of which four are prose and two carry identified elements.

**Current Situation** — what exists today, what problem or opportunity, and the business impact of not acting. Quantify. "62% satisfaction, 20–30 minute waits at peak" lands with this audience in a way that "students are dissatisfied" does not.

**Motivation for Change** — why now. What changed, what triggers this, what the consequences of inaction are. This answers "why not next year", usually the first question asked.

**Potential Customers and Users** — `STAKEHOLDER` nodes with `STAKEHOLDER_TYPE: Primary-user` or `Secondary-user`. Include `GROUP_SIZE`: the scale of each group changes the investment case, and it is the number executives look for.

**Key Stakeholders** — more `STAKEHOLDER` nodes, using the other types. `Approver` for veto or sign-off authority, `Resource-owner` for budget and capacity holders, `Consulted` where input is needed, `Affected` where the change lands on people who did not ask for it. Use `INFLUENCE` to record what each can block — that is the field that matters when the initiative stalls.

Making stakeholders identified nodes rather than a bullet list is what lets L1's `VP-` value propositions and L2's `UT-` user types trace back to a named group at L0.

**Related Solutions** and **Competitive Landscape** — both use `RELATED_SOLUTION`, distinguished by `SOLUTION_CATEGORY`: `Internal-existing`, `External-comparable`, `Direct-competitor`, `Indirect-competitor`. Record `STRENGTHS` and `WEAKNESSES` from the user's point of view rather than ours, and use `LESSONS` to say what each one tells us. A related solution recorded without a lesson is trivia.

Include the do-nothing alternative where it is real. People skipping the service, working around it, or continuing with a spreadsheet is frequently the strongest competitor and the one most often left out.

### Vision

**Future State Description** — the desired future written as observable experience, in the present tense, as though describing a working system to someone watching it. Not a feature list.

**Expected Impact** — `IMPACT` nodes. `IMPACT_TYPE` separates the three kinds this audience reads differently:

- `Quantitative` — measurable operational change
- `Qualitative` — real effects that resist measurement
- `Financial` — revenue, savings, avoided cost, payback period

Set `BASELINE` and `TARGET` wherever a number exists. A target without a baseline cannot be evaluated after the fact, which defeats the purpose of stating it.

**Strategic Alignment** *(optional)* — name the specific strategic pillar, objective or value rather than gesturing at alignment. If there is no strategy document to point at, delete the section.

### Solution Space

**Solution Approach Options** — `SOLUTION_OPTION` nodes with `ADVANTAGES` and `DISADVANTAGES`. Two options is the minimum for the section to mean anything; a single option is a decision presented as an analysis. Describe each on the same terms so they can be compared.

**Potential Functionality** — prose, grouped so the reader sees the shape of the scope: core functions, possible extended functions, integration possibilities. These are candidates. They become `BG-` and `VCA-` items at L1.

**Potential Technologies** — prose, grouped by the decision each option belongs to, with the trade-off named. Note existing infrastructure that creates a preference. Selection happens at L2.

### Constraints

Four subsections matching the framework's categories. Use `CONSTRAINT_TYPE` `Resource`, `Budget` or `Timeline` for the first three. For "Other", prefer the specific value — `Legal`, `Technical`, `Organisational`, `Operational` — over `Other` itself.

One node per constraint, not one node listing several. Each constraint gets refined separately at L1, and a compound node cannot be traced.

`BREAKDOWN` carries the detail this audience expects:

- Budget → cost components, and funding sources with amounts, marked approved or merely available
- Resource → teams and capacity percentages, skills available, skills needed externally
- Timeline → critical dates with what makes each one hard, and timeline risks

### Decision & Recommendation *(optional)*

**Success Criteria** — `SUCCESS_CRITERION` nodes, each with a `TARGET` threshold and a `MEASURED_BY` method, related to the `IMPACT` it measures. Both fields are required because a criterion without a threshold cannot be assessed later, and one without a method cannot be assessed at all.

**Risk Assessment** — `RISK` nodes with `PROBABILITY` and `SEVERITY` recorded separately, so the combination can be reasoned about rather than asserted. The template's High/Medium/Low grouping is the product of the two; order the nodes so high-probability, high-severity risks appear first. Every risk gets a `MITIGATION` — a risk with none is an argument against the recommendation, and should be presented as one.

**Go/No-Go Recommendation** — one `RECOMMENDATION` node. `VERDICT` is `Go`, `No-Go`, `Conditional-Go` or `TBD`. `CONDITIONS` for a conditional go. `NEXT_STEPS` as a short numbered list of what happens on approval. `DECISION_REQUIRED_BY` and `DECIDED_BY` because a recommendation with no named decision-maker and no date tends not to get decided.

### Implementation Planning *(optional)*

All prose. Timeline phases with durations, stating whether they are estimates or commitments. Transformation framework, evaluation windows, agreed fallback conditions. Process steps, formal acceptance criteria and stakeholder commitments — referencing the relevant `RSK-` node where adoption is a named risk.

## Document Control

The framework expects version, date, authors, reviewers, approvers, status and next review date. These live in the document's `METADATA` block rather than as a section, so they appear in the header rather than competing with content:

```
METADATA:
  LEVEL: L0 - Digital Design Brief
  AUDIENCE: Management, executives, decision-makers
  PURPOSE: Enable an informed Go/No-Go decision on proceeding to solution design
  AUTHORS: TBD
  REVIEWERS: TBD
  APPROVERS: TBD
  DOC_STATUS: Draft
  NEXT_REVIEW: TBD
```

`DOC_STATUS` rather than `STATUS`, to avoid confusion with the per-node status field. Values follow the framework: Draft, Under Review, Approved.

## What L1 traces up to

Only three L0 element types are relation targets from below:

| L0 element | Referenced from | Role |
| --- | --- | --- |
| `IMP-` Expected impact | `BG-` business goals at L1 | `Satisfies` |
| `BRC-` Constraints | `BC-` business constraints at L1 | `Refines` |
| `SH-` Stakeholders | `VP-` value propositions at L1, `UT-` user types at L2 | `Refines` |

`SO-`, `SUC-`, `RSK-` and `REC-` are not referenced from below. They document the decision rather than the solution, and the solution is what gets refined downward.

## Note on the L0 identifiers

The framework describes L0 as narrative, and most of it is. The six typed element classes exist because L1 needs anchors to trace up to, and because stakeholders, options, constraints, criteria and risks are the enumerable parts of a brief.

If a project prefers L0 purely narrative, deleting element types from `assets/L0_design_brief.sgra` costs only the upward relations from L1 — nothing else breaks. Worth confirming against the source framework before treating the prefixes as canonical.
