# L2 — System Design Concept

## Purpose and Shape

The overall technical architecture of the solution at system level: structure, components and their interactions, before any individual element is designed in detail.

| | |
| --- | --- |
| **Audience** | Digital designers and developers, while remaining accessible to non-technical stakeholders |
| **Purpose** | Describe **how** the solution works, as system-level architecture |
| **Provides** | Context for the L3 element designs |

## Scope Boundaries — including a fifth document

Three boundaries matter here, and the third is easy to miss:

**L1 above** provides the business context, information architecture and business processes that this document implements.

**L3 below** provides the detailed specification per software element — technical interfaces, use cases, technical functions, entities, element-specific quality requirements.

**A System Realization Concept alongside** holds deployment architecture, infrastructure specification, integration configuration and technical implementation detail. The framework names it explicitly, and it is not one of the three design concepts. When a description in L2 starts naming processor counts, memory sizes or connection pool settings, it has left this level — that content belongs there.

The practical test on hardware: "10–12 inch touchscreen with camera" belongs at L2; "2.4 GHz quad-core, 4 GB RAM" does not.

## Document Evolution

Created early in the design phase to establish the architecture. References to element designs accumulate as those get written. System goals, quality requirements and constraints get refined as implementation detail emerges. The architecture diagram must be kept current — a stale diagram is actively worse than none, because readers trust it.

## Sections

| Section | Element types |
| --- | --- |
| System Goals | `SG-` |
| System Architecture → Architecture Overview | `AP-` |
| System Architecture → Architecture Diagram | — |
| System Architecture → System Elements | `UT-` `SE-` `HE-` `PE-` |
| System Scenarios | `SSc-` `SSt-` `SA-` |
| Quality Requirements | `SQR-` |
| Constraints | `SC-` |
| Appendix *(optional)* | — |

## System Goals

What the technical system shall achieve as part of the solution, stated so technical people can act on it. Focus on the *what* and *why* at system level; the *how* is system scenarios and element designs.

`SUCCESS_CRITERIA` *(optional)* — quantitative where the goal is time-based, volume-based, quality-metricated or efficiency-based; qualitative where it concerns subjective user experience, a binary capability, an integration, or completeness of coverage.

`RATIONALE` *(optional)* — which L1 vision or value proposition this supports.

**One rule worth enforcing: every system goal should have at least one system scenario demonstrating how the system achieves it.** The template states this directly. A goal with no scenario is either untested or unnecessary, and the traceability view makes the gap visible — an `SG-` with no "Achieved by" entries.

This is checked mechanically by the coverage script, which also reports the related case of a scenario whose prose claims a coverage its relations do not declare.

## Architecture Overview

**Architecture style** — client-server, three-tier, microservices, event-driven, layered. One line, stated explicitly rather than left for the reader to infer from the diagram.

**Key architecture principles** — three to seven fundamental decisions. These get `AP-` IDs rather than sitting in a bullet list, because they are the choices most often violated silently later. An identified principle can be cited by a later design decision; a bulleted one cannot.

Each `AP-` carries a `STATEMENT` of the decision, a `RATIONALE` saying why and what the alternative would have cost, and `IMPLICATIONS` saying what it rules out. The implications field is the one that earns its place: a principle whose consequences are unstated gets broken by someone who never realised they were breaking it.

Examples of the right grain: separation of concerns between client and backend; authentication delegated to the institutional system; payment processing outsourced to a certified gateway; data held centrally and cached on clients.

Note that `AP-` is an addition to the source template, which presents principles as a bulleted list. The section content is identical; only the addressability differs.

## Architecture Diagram

The diagram should show every user type, software element, hardware element and partner element; the primary interactions and data flows; the system boundary between internal and external; and the major groupings or layers.

The template recommends a specific notation. Mermaid equivalents:

| Notation | Meaning | Mermaid |
| --- | --- | --- |
| Rectangle | Software element | `SE01["SE-01 Name"]` |
| Cylinder | Database | `SE04[("SE-04 Name")]` |
| Stick figure | User type | `UT01(["UT-01 Name"])` |
| Dashed rectangle | Partner element | node plus a dashed link `-. label .->` |
| Cloud / device | Hardware element | `HE01[/"HE-01 Name"/]` |
| Arrow | Primary data flow | `-->` |
| Dashed line | System boundary crossing | `-. label .->` |
| Grouping | Layer or tier | `subgraph` |

**Label every node with its element ID.** A diagram whose boxes correspond to identified elements can be checked against the prose; one with free-text boxes drifts silently, and nobody notices until an element is renamed.

Detailed interaction flows belong in system scenarios, not in the diagram.

## System Elements

### User Types

The human users who interact with the system.

- `STATEMENT` — role and characteristics, one or two sentences
- `PRIMARY_GOALS` — three to five things they want to achieve
- `INTERACTS_WITH` — which software elements they use directly, as inline links
- Relation `Represents → VCA-` — which L1 value creation element this user type corresponds to

Note the relation target: **a user type represents a `VCA-` element, not a `VP-` value proposition.** The template is explicit ("Represents VCA-01 (Students)"), and it follows from the L1 model, where `VCA-` elements include `Customer` and `Organisation` types alongside digital elements. If the L1 document has no customer-type `VCA-` elements, that is a gap at L1 rather than a reason to point the relation elsewhere.

### Software Elements

Applications, services and systems that are part of this solution and will be developed, configured or customised as part of the project.

`ELEMENT_TYPE` follows the template: `Mobile-application`, `Web-application`, `Backend-service`, `Database`, `Desktop-application`, `Library`, `Other`.

- `KEY_RESPONSIBILITIES` — three to seven main functions. Action verbs: manages, provides, processes, stores, displays. What it does, not how. **Each responsibility should be distinct from every other element's** — overlapping responsibility lists are the first sign the decomposition is wrong.
- `INTERACTS_WITH` — software elements, hardware it runs on, partner elements it calls, user types who use it directly. Inline links.
- Relation `Realises → VCA-` — which L1 value creation element this implements or contributes to.

Every software element needing detailed design gets an L3 document. The template asks for an "Element Design" reference field; do not add one — see the derived-references rule below.

### Hardware Elements

The physical devices and infrastructure the software runs on. This section is what gives a reader a tangible sense of the system's physical presence.

**`PROCUREMENT` must always be explicit:**

| Value | Meaning |
|---|---|
| `Procurement-required` | Something must be bought |
| `Assumed-existing` | Users or the institution already have it |
| `Managed-service` | A provider supplies it |

An unstated procurement position is how hardware cost gets discovered late in a project. The field is required for that reason.

- `MANAGED_BY` — who owns or manages it: users, the institution, a cloud provider
- `LOCATION` — include where hardware is fixed in place, or where location affects the design ("EU data centre for GDPR compliance"). Omit for portable user devices unless it matters.
- `RUNS` — which software elements run on it, as inline links
- `CHARACTERISTICS` — minimum OS versions, connectivity, form factor, quantities. **High-level only.** Processor and memory specifications belong in the System Realization Concept.

Where a system genuinely has no hardware elements, keep one stating that explicitly rather than deleting the section. An absent section reads as an oversight; "no server-side deployment; runs entirely on user devices" is information.

### Partner Elements

External systems, services and platforms the solution integrates with but does not own or control — payment gateways, authentication systems, cloud services, third-party APIs.

- `PROVIDER` — the company, organisation or system name
- `PARTNER_TYPE` — `External-SaaS`, `Institutional-system`, `Cloud-platform-service`, `Third-party-API`, `Other`
- `DEPENDENCY` — `Critical`, `Important` or `Replaceable`. Set it honestly: `Critical` means the system does not function without it. This is the field a risk review reads first.
- `USED_BY` — which software elements integrate with it

**Technical integration detail does not belong here.** API specifications, authentication methods, data exchange formats, error handling and retry strategy go in the outbound technical interface sections (`TO-`) of the calling elements' L3 documents.

## System Scenarios

Essential end-to-end flows showing how the system as a whole achieves its goals, focused on which elements interact with which.

`SSc-` is composite, with `SSt-` steps and `SA-` alternatives as children. Relations: `Achieves → SG-` and, where one exists, `Realises → BP-`.

### Differentiated depth is intentional

The template makes a point worth preserving: not every scenario needs the same elaboration. A complex cross-element flow where the interplay is non-obvious warrants detailed steps; a simple path through one or two elements needs only a concise narrative.

`DETAIL_LEVEL` records which was chosen — `Detailed` or `Narrative`. Recording it stops a reviewer reading variation as inconsistency, which is the usual fate of a document with mixed depth.

### Writing Steps

**Always use element IDs.**

- Good: "SE-01 sends the order to SE-02"
- Avoid: "the app sends the order to the server"

**Describe what happens, not how it is implemented.**

- Good: "SE-02 processes payment via PE-01"
- Avoid: "SE-02 calls TF-15, which validates order fields and calls TO-04"

**Keep data references light.**

- Good: "SE-01 sends the order to SE-02"
- Acceptable: "SE-01 sends the order (meals, pickup time) to SE-02"
- Avoid: naming fields and types — that is L3

**Show partner involvement explicitly.** "SE-02 processes payment via PE-01", "PE-01 confirms payment to SE-02".

`SSt-` fields: `PERFORMED_BY` for the acting element, `AFFECTS` for the elements affected.

### Alternative Flows

`SA-` nodes for significant alternative paths: errors affecting the overall flow, alternative user choices leading to different element interactions, partner element failures. Each carries `Extends → SSt-` naming the step it branches from, and an `OUTCOME` of `Resume`, `Terminate` or `Alternative-success`.

Keep them high-level. Detailed error handling belongs at L3.

### Use case references

The template offers a "Realized through Use Cases" field for simple scenarios, and inline references within steps for complex ones. **Do not add the field** — `UC-` nodes at L3 declare `Realises → SSc-`, so the scenario page shows "Realised by" automatically. Inline references inside a step are fine where they genuinely aid comprehension, as prose.

## Quality Requirements

How well the *entire system* performs — not individual elements, which is L3. This is where an L1 business quality requirement becomes a number.

**`QUALITY_CATEGORY` uses the template's nine technical categories:**

| Value | Covers |
| --- | --- |
| `Performance` | Response times, throughput, resource usage across the system |
| `Scalability` | Handling growing workload |
| `Availability` | Uptime, reliability, fault tolerance |
| `Security` | Authentication, authorisation, data protection, encryption |
| `Usability` | Ease of use, learnability, accessibility of user-facing elements |
| `Maintainability` | System-wide code quality, documentation, testability |
| `Compatibility` | Platform support, browser support, integration compatibility |
| `Data-integrity` | Consistency, accuracy, validation across the system |
| `Compliance` | Regulatory requirements, standards adherence |

These are deliberately technical, unlike L1's business categories. A `BQR-` says "customers are satisfied"; the `SQR-` supporting it says "95th percentile response under 200 ms".

- `APPLIES_TO` — the elements primarily affected, or the overall system architecture
- `ACCEPTANCE_CRITERIA` — clear, testable, unambiguous. Quantitative where performance, availability, scalability, security, numerical standards or resource usage can be measured; qualitative where assessment is subjective, compliance is binary, or a practice is required.
- Relation `Supports → BQR-`

**`EXTERNALLY_SOURCED: Yes`** marks a requirement arriving from a regulation, standard or platform rather than from a business quality requirement. The template notes such requirements legitimately have no business counterpart. Marking them distinguishes a deliberate absence from a forgotten link — the same purpose `DERIVED` serves at L3.

## Constraints

Non-negotiable requirements limiting design and implementation choices for the system as a whole.

**`CONSTRAINT_CATEGORY` follows the template:**

| Value | Covers |
| --- | --- |
| `Legal-regulatory` | Laws, regulations, compliance requirements |
| `Technical` | Technology choices, platform limitations, existing infrastructure |
| `Business` | Budget, timeline, organisational policies |
| `Integration` | Requirements from partner or institutional systems |
| `Standards` | Industry or company standards that must be followed |

- `SOURCE` *(optional)* — the specific law with its reference, the standard document ("ISO 27001:2013", "WCAG 2.1 Level AA"), the business decision, the partner requirement
- `APPLIES_TO` — which elements are affected. Reference only the most relevant ones.
- `ACCEPTANCE_CRITERIA` — what must be done to satisfy the constraint
- `CONSEQUENCE` — what this rules out. A constraint whose consequence is unstated tends to get ignored.
- Relation `Refines → BC-` where a business constraint exists

**Many system constraints come from external sources and have no business counterpart.** The template says this is normal and expected. Mark those `EXTERNALLY_SOURCED: Yes` rather than inventing a business parent to satisfy a traceability rule.

## Traceability at this level

**Upward, to L1:**

| L2 element | Target | Role |
| --- | --- | --- |
| `SG-` | `BG-` business goal | `Satisfies` |
| `UT-` | `VCA-` value creation element | `Represents` |
| `SE-` | `VCA-` value creation element | `Realises` |
| `SSc-` | `BP-` business process | `Realises` |
| `SQR-` | `BQR-` business quality requirement | `Supports` |
| `SC-` | `BC-` business constraint | `Refines` |

**Within L2:**

| From | To | Role |
| --- | --- | --- |
| `AP-` | `SG-` | `Satisfies` |
| `SSc-` | `SG-` | `Achieves` |
| `SE-` | `SG-` | `Satisfies` |
| `SE-` | `SC-` | `Constrained by` |
| `SA-` | `SSt-` | `Extends` |

**Lateral, as inline links rather than relations:** `UT-` interacting with `SE-`, `SE-` interacting with `SE-`/`HE-`/`PE-`/`UT-`, `HE-` running `SE-`, `PE-` used by `SE-`, `SQR-`/`SC-` applying to elements.

**Downward, from L3 — never written here:** `G- Satisfies SG-`, `UC- Realises SSc-`, `TF- Refines SE-`, `QR- Refines SQR-`, `C- Refines SC-`. The template's "Element Design", "Realized through Use Cases", "Implemented by Element Quality Requirements" and "Implemented by Element Constraints" fields are all reverse views StrictDoc generates automatically. Do not add fields for them.
