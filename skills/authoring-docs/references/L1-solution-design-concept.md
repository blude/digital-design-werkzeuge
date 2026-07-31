# L1 — Solution Design Concept

## Purpose and shape

The structure of the solution from the client's business perspective. It bridges business strategy and technical implementation: translating the vision into structured requirements, providing context for L2 and L3, and serving as the agreement point between business stakeholders and the technical team.

| | |
|---|---|
| **Primary audience** | Business stakeholders, clients, project sponsors |
| **Secondary audience** | Digital designers and developers, for business context |
| **Purpose** | Describe **what** the solution does from the business perspective |
| **Language** | Business language throughout. No technical jargon. |

**Where this sits.** The L0 brief provides justification and approval. This document says *what* the solution does. L2 says *how* it works technically. L3 gives the detailed specification per component.

**Layered approach.** Each major section opens with an executive summary for stakeholders, followed by identified specifications that give designers structure and provide traceability downward. Write the summary so a stakeholder who reads nothing else still understands the section.

**Develop it iteratively.** The template explicitly supports this, and it is the right way to work:

1. Vision and executive summaries first, for initial stakeholder alignment
2. Generate headings and outlines for the structured sections
3. Detail high-priority elements first, based on stakeholder feedback
4. Refine and expand as the project progresses
5. Keep synchronised with the evolving L2 and L3 designs

A complete-looking L1 produced in one pass without stakeholder contact is usually worth less than a vision plus three well-chosen specifications that have been reviewed.

## The one thing that changes how you use this framework

The template asks for several **downward** references, each marked optional:

- `VCA-` → "Implemented As" (SE-IDs from the System Design)
- `BE-` → "Implemented As" (`[Element]: E-nn`)
- `BP-` → "Realized by System Scenario" (SSc-ID)
- `BQR-` → "Implemented by System Quality Requirements" (SQR-IDs)
- `BC-` → "Implemented by System Constraints" (SC-IDs)

**Do not write these by hand, and do not add fields for them.** Every one is the reverse view of a relation the child already declares at L2 or L3. When `SQR-01` declares `Refines → BQR-02`, StrictDoc renders "Refined by SQR-01" on the BQR-02 page automatically, because the grammar sets `REVERSE_ROLE`. The same applies to all five.

This is the single largest maintenance saving the tooling offers on this document. Hand-maintained downward references are the classic failure mode of layered documentation: they are written once when the lower level is drafted, and never updated again. Here the reference cannot go stale, because it is derived.

The consequence for authoring: when a stakeholder asks "what implements this business goal?", the answer comes from the traceability view, not from a field. If the view is empty, that is real information — nothing at L2 has claimed it yet.

## Sections

| Section | Executive summary | Element types |
|---|---|---|
| Vision | Yes — as a future press release | `BG-` |
| Value Proposition | Only if 4+ customer segments | `VP-` |
| Value Creation Architecture | Yes, with diagram | `VCA-` |
| Information Architecture | Yes, with diagram | `BE-` |
| Business Processes | Yes, with diagram | `BP-` `PS-` `PA-` |
| Quality Requirements | No | `BQR-` |
| Constraints | No | `BC-` |
| Appendix *(optional)* | No | — |

## Vision

### The executive summary is a future press release

This is the template's most distinctive instruction and it is worth following literally. Write an announcement, dated one to two years out, of the solution's successful implementation.

**Structure**

1. Opening — the main achievement and its impact, two or three sentences
2. A quote from a key stakeholder describing the value they now get
3. Three or four paragraphs on specific improvements, with concrete examples of how daily work or operations changed
4. Closing — future outlook and next steps

**Rules**

- Past tense or present perfect. "Students now book a room in seconds", not "students will be able to book rooms". The tense is what does the work: it forces you to describe an outcome rather than an intention.
- More than one stakeholder perspective. Customers, staff and management read different things as evidence.
- Concrete examples over general claims. Name the situation that changed.
- No technical detail.
- One to two pages.

The point of the format is that vague visions survive bulleted lists but not press releases. "Improved efficiency" cannot be written as a quote from a named person describing their Tuesday.

### Business goals

`BG-` nodes break the vision into specific objectives. Each has a description of two or three sentences saying what should be achieved and why it matters from a business perspective.

**`SUCCESS_CRITERIA`** *(optional)* — measurable or observable criteria indicating the goal is achieved.

Use **quantitative** criteria where business metrics, satisfaction, operational efficiency or adoption can be measured: "reduce average processing time from 25 minutes to 5 minutes", "achieve 80% adoption within the first semester".

Use **qualitative** criteria where the goal is a strategic objective, an enabled capability, or compliance with a standard: "enable students to order without staff assistance", "provide complete allergen information for all menu items".

**`RATIONALE`** *(optional)* — how this goal supports the vision, linking the specific objective back to the broader change.

Note that `OBLIGATION`, `PRIORITY` and `STATUS` on business goals are additions to the source template, carried over from the IREB attribute scheme. They are useful for filtering and review workflow. Removing them from the grammar would not break anything else.

## Value proposition

One `VP-` node per customer segment. **The executive summary is only warranted with four or more segments** — below that it repeats the specifications that follow it.

Fields worth attention:

- `CUSTOMER_SEGMENT` and `SEGMENT_SIZE` — who they are and how many. Size changes the investment case and is what executives look for.
- `SEGMENT_CHARACTERISTICS` — what matters about them for design purposes.
- `VALUE_DELIVERED` — three to seven key benefits. Benefits and outcomes, never features.
- `PAINS_ADDRESSED` — the specific frustrations removed.
- `CURRENT_ALTERNATIVES` *(optional, competitive contexts)* — how the segment meets the need today without the solution. Be concrete: "standing in line for 20–30 minutes", not "an inefficient process".
- `WHY_BETTER` *(optional)* — why the proposal beats those alternatives, quantified where possible.

Each `VP-` should `Satisfies` a business goal, and where an L0 brief exists, `Refines` the `SH-` stakeholder group it corresponds to.

## Value creation architecture

`VCA-` nodes are the elements working together to deliver the value proposition. `ELEMENT_TYPE` follows the template exactly:

| Value | Meaning |
|---|---|
| `Customer` | Receives value |
| `Organisation-internal` | Part of the client organisation |
| `Organisation-external` | Partner, supplier, external entity |
| `Digital-element` | Software, platform, system |

**Granularity for digital elements.** For a simple solution, describe the whole technical system as one digital element — "The Platform", "The System". Break it into separate digital elements only where the distinction is business-relevant, such as "Student Portal" versus "Course Management System". L2 provides the technical decomposition into software elements regardless of how many digital elements appear here.

`INTERACTS_WITH` records peer relationships between value creation elements. **These are lateral, not hierarchical**, so they go in the field as inline `[LINK: VCA-02]` references rather than as `Parent` relations. Modelling a peer interaction as `Parent` corrupts the traceability graph and, if reciprocal, crashes the parser.

`VALUE_FLOW` records value received (for customers, referencing the VP) or value provided (for organisations and digital elements).

The executive summary here should carry a diagram showing customers who receive value, the internal and external organisations involved, the digital elements, and the key relationships. Mermaid is available; label nodes with their `VCA-` IDs.

## Information architecture

`BE-` nodes are the key information concepts in the business domain, described in one or two sentences each.

- `KEY_INFORMATION` — five to ten categories of business-relevant information: descriptive attributes, identifiers, business properties, status, lifecycle. Not technical implementation detail.
- `ASSOCIATIONS` — how the entity relates to others, as "description ([LINK: BE-02])". The field is `ASSOCIATIONS`, not `RELATIONSHIPS`; any field name beginning with `RELATIONS` is rejected by the parser.

Most solutions have three to six business entities at this level. An entity list that runs to twenty is usually a database schema in business clothing.

## Business processes

The main processes necessary for delivering value. Essential business activities only — what stakeholders need to understand.

`BP-` is composite, with `PS-` process steps and `PA-` process alternatives as children.

**Fields on the process**

- `STATEMENT` — two or three sentences: what happens, who is involved, what is achieved, and how often or how long it takes.
- `FREQUENCY` — how often this runs. Useful context that changes design decisions.
- `INVOLVED_PARTIES` — the value creation elements participating, as inline links. Customers who initiate, organisations that execute, digital elements that support, external partners.
- `CREATES_UPDATES` — business entities the process creates, modifies or uses, as "Action: entity ([LINK: BE-01])".
- Relation `Supports → BG-` — which business goals this process serves.

**Process steps**

Two formats are acceptable. Simple narrative steps, where each `PS-` node states an activity and refers to actors and entities in prose. Or the structured form, using `PERFORMED_BY`, `USES_CREATES` and `BUSINESS_RULES` fields. Use the structured form where business rules matter; use narrative where the flow is straightforward.

Guidelines: business language, not technical implementation. What happens and why, not how it is built. Include business rules and decision points. Keep steps at business activity level, not technical function calls. Typical processes have five to fifteen steps.

**Alternative flows**

`PA-` nodes describe major alternative paths: errors the business cares about, alternative user choices that change the flow, business-level exception handling. Each carries an `Extends` relation to the `PS-` step it branches from, so the anchor is checked rather than being a numbering convention, and an `OUTCOME` of `Resume`, `Terminate` or `Alternative-success`.

**Keep these high-level.** Detailed error handling belongs at L3. If an alternative flow is describing what happens when a field fails validation, it is at the wrong level.

## Quality requirements

`BQR-` nodes are business-level quality expectations, stated from the stakeholder perspective.

**`QUALITY_CATEGORY` uses business categories, not technical quality attributes:**

| Value | Covers |
|---|---|
| `Business-performance` | Revenue, cost, efficiency, productivity |
| `Customer-satisfaction` | Satisfaction, NPS, retention, adoption |
| `Service-quality` | Availability, reliability, accuracy as the business sees them |
| `Operational-excellence` | Process quality, staff efficiency, resource utilisation |
| `Compliance` | Regulatory requirements, industry standards, policies |
| `Sustainability` | Environmental impact, long-term viability, scalability |

This is a deliberate difference from L2 and L3, which use technical quality attributes — performance, usability, reliability, portability and so on. A `BQR-` says "customers are satisfied"; the `SQR-` refining it says "the 95th percentile response is under 200 ms". Using technical attributes at L1 collapses that distinction and pushes engineering decisions into the business document.

`APPLIES_TO` lists which business elements the requirement affects — processes, value propositions, value creation elements, or the overall solution.

`ACCEPTANCE_CRITERIA` should be clear, testable and verifiable from a business perspective. Quantitative where metrics, satisfaction, performance, adoption or service levels can be measured; qualitative where assessment is subjective, compliance is binary, or the requirement is a capability. Not every business quality requirement has a system-level counterpart — some are achieved through overall solution design rather than a specific technical attribute.

## Constraints

`BC-` nodes are non-negotiable requirements limiting design and implementation choices. They come from outside the project and are not trade-offs to be balanced.

**`CONSTRAINT_CATEGORY` follows the template:**

| Value | Covers |
|---|---|
| `Legal-regulatory` | Laws, regulations, compliance requirements |
| `Business` | Budget limits, timeline requirements, organisational policy |
| `Organisational` | Existing processes, structures or capabilities that must be accommodated |
| `Market` | Competitive pressure, customer expectations, industry norms |
| `Resource` | Available staff, skills, infrastructure limitations |

`SOURCE` *(optional)* — the specific law with its reference, the policy document, the budget approval, the partner requirement.

`APPLIES_TO` — which business elements are affected.

`ACCEPTANCE_CRITERIA` — what demonstrates compliance. Quantitative where the constraint has amounts, dates or limits; qualitative where compliance is binary or an approach is mandated.

Where an L0 brief exists, each `BC-` should `Refines` the `BRC-` brief-level constraint it derives from. As with quality requirements, not every business constraint translates into a system constraint — some are satisfied by the overall approach or by process design.

## Document control and appendix

The template carries a version table. In StrictDoc this belongs in the document `METADATA` block rather than as a section, since git already holds the history.

The template notes that on handover to a wiki, each artifact gets its own version history in the target system and the table becomes obsolete. The same logic applies here from the start — the document is in version control, so a hand-maintained changelog is duplicated effort.

The appendix holds supplementary material that supports but does not belong in the body: extended design rationale, records of discarded alternatives, results from technical spikes or prototypes, input from domain experts or external review.

## Traceability at this level

**Upward, to L0:**

| L1 element | Target | Role |
|---|---|---|
| `BG-` | `IMP-` expected impact | `Satisfies` |
| `VP-` | `SH-` stakeholder group | `Refines` |
| `BC-` | `BRC-` brief constraint | `Refines` |

**Within L1:**

| From | To | Role |
|---|---|---|
| `VP-` | `BG-` | `Satisfies` |
| `VCA-` | `VP-` | `Realises` |
| `BP-` | `BG-` | `Supports` |
| `BQR-` | `BG-` | `Satisfies` |
| `PA-` | `PS-` | `Extends` |

**Lateral, as inline links rather than relations:** `VCA-` interacting with `VCA-`, `BP-` involving `VCA-`, `BP-` touching `BE-`, `BE-` associating with `BE-`, `BQR-`/`BC-` applying to processes and propositions.

**Downward, from L2 and L3 — never written here:** `SG- Satisfies BG-`, `SE- Realises VCA-`, `SSc- Realises BP-`, `SQR- Refines BQR-`, `SC- Refines BC-`, `E- Refines BE-`. These appear on the L1 pages automatically as "Satisfied by", "Realised by" and "Refined by".
