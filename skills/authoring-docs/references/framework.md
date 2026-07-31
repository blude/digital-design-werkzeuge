# The four-level framework

Four documents, each written for a different audience at a different level of abstraction. A statement belongs at exactly one level. The commonest authoring mistake is writing a solution at a level meant for needs, or a need at a level meant for implementation.

## Contents

- [L0 — Digital Design Brief](#l0--digital-design-brief)
- [L1 — Solution Design Concept](#l1--solution-design-concept)
- [L2 — System Design Concept](#l2--system-design-concept)
- [L3 — Element Design Concept](#l3--element-design-concept)
- [Deciding which level a statement belongs to](#deciding-which-level-a-statement-belongs-to)
- [ID prefix summary](#id-prefix-summary)

---

## L0 — Digital Design Brief

**Purpose.** A concise, high-level summary of a planned initiative, giving management enough to make a Go/No-Go decision without technical detail.

**Audience.** Management, executives, decision-makers.

**Shape.** 2–3 pages for a small solution, readable in 15–20 minutes, 1–3 days to produce. The document's whole value comes from being read in full by people whose attention is scarce.

**Sections.**

- Context of the initiative
  - Current Situation
  - Motivation for Change
  - Potential Customers and Users — `SH-xx`
  - Key Stakeholders — `SH-xx`
  - Related Solutions — `RS-xx`
  - Competitive Landscape — `RS-xx`
- Vision
  - Future State Description
  - Expected Impact — `IMP-xx`
  - Strategic Alignment *(optional)*
- Solution Space
  - Solution Approach Options — `SO-xx`
  - Potential Functionality
  - Potential Technologies
- Constraints — `BRC-xx`
  - Resource / Budget / Timeline / Other
- Decision & Recommendation *(optional section)*
  - Success Criteria — `SUC-xx`
  - Risk Assessment — `RSK-xx`
  - Go/No-Go Recommendation — `REC-xx`
- Implementation Planning *(optional section)*
  - Project Timeline
  - Transformation Framework / Implementation Approach
  - Process and Stakeholder Acceptance
- Appendices *(optional)*
  - Supporting Data
  - References

Two things worth knowing before writing one: the brief **presents options rather than choosing between them**, and the Go/No-Go decision is about **whether to proceed to solution design**, not about which option to build.

`ROOT: True` goes on this document, which exempts its nodes from the "not connected to any parent" statistic.

---

## L1 — Solution Design Concept

**Purpose.** The structure of the solution from the client's business perspective. Bridges business strategy and technical implementation, and is the agreement point between business stakeholders and the technical team.

**Audience.** Business stakeholders, clients and project sponsors primarily; designers and developers secondarily, for business context.

**Language.** Business language throughout. Describe *what* the solution does, never *how* it is built.

**Layered approach.** Each major section opens with an **executive summary** for stakeholders, followed by identified specifications that give designers structure and provide traceability downward.

**Sections.**

- Vision
  - Executive Summary — written as a **future press release**
  - Business Goals — `BG-xx`
- Value Proposition
  - Executive Summary *(only if 4+ customer segments)*
  - Value Propositions by Customer Segment — `VP-xx`
- Value Creation Architecture
  - Executive Summary, with diagram
  - Value Creation Elements — `VCA-xx`
- Information Architecture
  - Executive Summary, with diagram
  - Business Entities — `BE-xx`
- Business Processes
  - Executive Summary, with diagram
  - Business Process Specifications — `BP-xx`, with `PS-xx` steps and `PA-xx` alternative flows
- Quality Requirements — `BQR-xx`
- Constraints — `BC-xx`
- Appendix *(optional)*

Two things distinguish this level. Quality requirements use **business categories** rather than technical quality attributes — those belong at L2. And the template's optional "Implemented by" and "Realized by" fields are **never written by hand**: StrictDoc derives them from the relations declared at L2 and L3.

## L2 — System Design Concept

**Purpose.** The overall technical architecture at system level: structure, components and their interactions, before any individual element is designed in detail.

**Audience.** Digital designers and developers, while remaining accessible to non-technical stakeholders.

**Sections.**

- System Goals — `SG-xx`
- System Architecture
  - Architecture Overview, including architecture style and Key Architecture Principles — `AP-xx`
  - Architecture Diagram
  - System Elements
    - User Types — `UT-xx`
    - Software Elements — `SE-xx`
    - Hardware Elements — `HE-xx`
    - Partner Elements — `PE-xx`
- System Scenarios — `SSc-xx`, with `SSt-xx` steps and `SA-xx` alternative flows
- Quality Requirements — `SQR-xx`
- Constraints — `SC-xx`
- Appendix *(optional)*

**A fifth document exists.** Deployment architecture, infrastructure specification, integration configuration and technical implementation detail belong in a **System Realization Concept**, which sits alongside the four levels rather than within them. When an L2 description starts naming processor counts or connection pool sizes, it has left this level.

Two rules worth knowing before writing one: **every system goal should have at least one system scenario** demonstrating how the system achieves it, and **differentiated depth between scenarios is intentional** — the `DETAIL_LEVEL` field records the choice so a reviewer does not read variation as inconsistency.

## L3 — Element Design Concept

**Purpose.** The non-technical design of **one element**, in enough detail to implement it. An element can be a smartphone app, a web app, a server element, or a whole complicated system.

**Audience.** Digital designers and developers implementing that element.

**One document per element.** Record the L2 software element ID in the document `METADATA`.

**Sections.**

- Goals — `G-xx`
- Use Cases — `UC-xx`, with `ST-xx` steps and `EX-xx` alternative scenarios
- User Interfaces — `UI-xx`
- Technical Functions — `TF-xx`, with `FS-xx` steps and `FA-xx` alternative flows
- Technical Interfaces (inbound) — `TI-xx`
- Technical Interfaces (outbound) — `TO-xx`
- Entities — `E-xx`
- Quality Requirements — `QR-xx`
- Constraints — `C-xx`
- Appendix *(optional)*

**Not all sections apply to every element type.** The framework gives four profiles — user-facing frontend, backend service, integration/middleware, and hardware-bound — each with a different core set. Record the profile in `ELEMENT_PROFILE` and state which sections apply and why. An empty section is less useful than a focused, well-populated set.

Three rules distinguish this level. **Actors must be elements of the L2 system architecture**, not free-text roles. **Every step carries a `STEP_TYPE`** from a fixed set, different for use cases and for technical functions. And **outbound calls specify their call behaviour on the calling function step**, never on the interface itself.

## Deciding which level a statement belongs to

Work down, and ask what kind of claim the statement makes:

| The statement says… | Level | Example |
|---|---|---|
| A benefit someone wants, or a decision about whether to proceed | L0 | "Clerical maintenance effort is eliminated" |
| What the business needs to be true, without saying how | L1 | "Authors shall spend no manual effort maintaining cross-references" |
| What the system does, seen from outside, and what it is made of | L2 | "The system shall re-analyse only what changed" |
| What one component does, in implementable detail | L3 | "The element shall delay analysis by a configurable interval" |

Two tests that catch most misplacements:

**Is a solution smuggled into a needs level?** If an L1 business goal names a technology, it belongs at L2 or lower. Solutions at L1 over-constrain everything beneath them.

**Is a need restated rather than refined?** If an L3 requirement says the same thing as its L2 parent in slightly different words, the pair carries no information. Either the L3 item should add detail, or it should not exist.

The grammar enforces the boundary mechanically: each document accepts only its own level's element types. Putting a `BUSINESS_GOAL` in the L2 document fails with `Semantic error: Invalid node type: BUSINESS_GOAL`.

---

## ID prefix summary

| Level | Prefixes |
| --- | --- |
| L0 | `SH-` `RS-` `IMP-` `SO-` `BRC-` `SUC-` `RSK-` `REC-` |
| L1 | `BG-` `VP-` `VCA-` `BE-` `BP-` `PS-` `PA-` `BQR-` `BC-` |
| L2 | `SG-` `AP-` `UT-` `SE-` `HE-` `PE-` `SSc-` `SSt-` `SA-` `SQR-` `SC-` |
| L3 | `G-` `UC-` `ST-` `EX-` `UI-` `TF-` `FS-` `FA-` `TI-` `TO-` `E-` `QR-` `C-` |

The framework writes these as `BG-xx`, so use zero-padded two-digit numbers: `BG-01`, `BG-02`. Child nodes of a composite take the parent's number plus a position: `ST-01-1`, `ST-01-2`.

IDs are identity. Never renumber one because something was deleted or reordered — leave the gap. Step *positions* are the exception: they are positional by nature, which is why steps carry no number in their text and their order is document order.
