# L3 — Element Design Concept

## Purpose and Shape

The non-technical design of **one element**, described in enough detail to implement it. An element can be a smartphone app, a web app, a server element, or a whole complicated system.

| | |
|---|---|
| **Audience** | Digital designers and developers implementing this element |
| **Scope** | Exactly one element |
| **Detail** | Sufficient for implementation |

**One document per element.** Name the file for the element it covers and record the L2 software element ID in `METADATA`. A system with four software elements has four L3 documents.

## Which sections apply — four profiles

This is the section most worth reading before starting. Not all sections apply to every element type, and the framework gives four concrete profiles. Set `ELEMENT_PROFILE` in the document metadata, then state in the opening section which sections apply and why.

**User-facing frontend** — web app, mobile app, kiosk

All sections apply. `UI-` and `UC-` are the core. Technical interfaces describe inbound calls from users and outbound calls to backend services. Technical functions cover rendering logic, validation and local state management.

**Backend service / API** — application server, microservice

`G-`, `UC-`, `TI-`, `TO-`, `TF-` and `E-` are the core. User interfaces typically do not apply. Quality requirements and constraints are particularly important — a backend element's behaviour under load and failure is most of what distinguishes a good one.

**Integration / middleware** — adapter, message broker, API gateway

`TI-` and `TO-` are the core. Use cases may be limited or absent, which is normal rather than an omission. Focus on data transformation, routing logic in technical functions, and error handling. Entities describe the structures being passed through rather than stored.

**Hardware-bound element** — embedded device, display terminal, sensor gateway

`G-` and `C-` are central. Technical interfaces describe physical protocols and data formats. Use cases cover operational modes and interactions. User interfaces apply only if the device has a local UI. Technical functions cover device-specific logic — firmware triggers, signal processing.

**When in doubt**, start with goals and use cases to establish what the element must achieve, then add only sections where there is meaningful content. **An empty section is less useful than a focused, well-populated set of relevant ones.** Where a section half-applies, say what it does instead of omitting it: a language server has no interface of its own, but it supplies content *to* the host editor's surfaces, and saying so is more useful than a blank section.

## Goals

What the element shall achieve. Goals provide the rationale for the element's existence and guide design decisions; use cases and technical functions reference them to show how they contribute.

- `SUCCESS_CRITERIA` *(optional)* — measurable criteria. "Users complete the task within three taps", "requests processed within 10 seconds", "95% complete checkout on first attempt".
- `RATIONALE` *(optional)* — which L2 system goal this supports.
- Relation `Satisfies → SG-`

## Use Cases

A use case is a functionality the element provides to a user: exactly one main scenario plus any number of alternative scenarios.

**Actors must be elements of the L2 system architecture.** The template is explicit about this. An actor is a `UT-`, `SE-` or `PE-` from the System Design Concept, referenced by ID — not a free-text role invented here. If the needed actor does not exist at L2, that is a gap at L2.

`PREREQUISITES` — events or other use cases that must have occurred first. Where another use case is a prerequisite, name it and give its ID.

### Step classification

Every step is one of four kinds, recorded in `STEP_TYPE`:

| `STEP_TYPE` | What it is | Must name |
|---|---|---|
| `User-interaction` | User interacts with a user interface | the `UI-`, and the data entered or shown |
| `Function-call` | Invokes internal logic | the `TF-`, its input, and what happens to its output |
| `Outbound-call` | Technical interaction with another element | the `TO-` — but prefer a function call |
| `Activity` | Internal processing by the element | nothing external |

Making the kind an enum rather than leaving it implicit is worth the field: it forces the author to notice when a step is doing two things, which is the commonest defect in a scenario.

### Prefer function calls over outbound calls

The template is firm on this and the reasoning is sound. Most logic, including calls to external interfaces, should be encapsulated in a technical function. A direct `Outbound-call` step is justified only where creating a function would be unnecessary overhead — which is rare. When unsure, use a function call: it reads better, and it keeps retry and error handling in one place rather than scattered through scenarios.

**Where a called function fails, the error is handled in that function's specification, not in the use case.** Alternative scenarios at this level cover failures the *use case* must respond to, not every error the machinery beneath it can produce.

### Alternative Scenarios

The template's convention is to reference the step and append a letter — `3a`, and `3a, 4a, 5a` for multi-step alternatives. Here an `EX-` node carries `Extends → ST-` instead, which makes the anchor a checked reference rather than a lettering convention that goes stale the moment a step is inserted. `OUTCOME` records `Resume`, `Terminate` or `Alternative-success`.

## User Interfaces

A user interface gives a user access to the element's functionality. The focus is on **what is visible**, what data is displayed, and what actions are available — not the implementation of those actions.

`USER_TYPE` names the L2 user type that may use this interface.

Four content fields, following the template:

- `VISIBLE_DATA` — per item: attribute name and data type, what is displayed, the `Source` (an entity attribute such as `E-01.1`, or a `TF-`), and any conditions on visibility or state
- `ACTIONS` — per action: name, what it represents (button press, link, selection), the related use case, and any conditions such as "enabled only when fields are filled"
- `INPUT_FIELDS` *(if applicable)* — per field: name and data type, what the user enters, UI-level validation only (required, format, length), related use cases
- `NAVIGATION` *(if applicable)* — per target: the `UI-` navigated to, when navigation occurs, and the use case describing the flow

**Reference a use case** for user-facing multi-step actions with feedback. **Reference a technical function** for instant data operations.

**Detailed behaviour belongs elsewhere.** Which functions are called, how data is processed, how errors are handled, what happens next — all of that is in the referenced use cases and technical functions. A UI specification that explains error handling has absorbed content from two other sections.

## Technical Functions

Internal functionality the element performs. `TF-` is composite, with `FS-` steps and `FA-` alternatives as children.

**The description must explain how the output is created.** This is the template's own emphasis, and it is the test for whether a function specification is finished.

### Step classification

| `STEP_TYPE` | What it is | Must name |
|---|---|---|
| `Data-operation` | Manipulates known data | data from input, an entity, or another call |
| `Entity-access` | Reads or writes stored data | the `E-` and the specific attributes, e.g. `E-02.3` |
| `Function-call` | Invokes another function | the `TF-`, its input, what happens to its output |
| `Outbound-call` | Calls an external element | the `TO-`, input, expected output, **and call behaviour** |

Note the difference from use case steps: no `User-interaction`, and `Data-operation` and `Entity-access` replace `Activity`. A function does not touch a UI.

### Outbound calls must specify call behaviour

`CALL_BEHAVIOUR` on the calling step, covering:

- **Timeout** for synchronous calls, or callback handling for asynchronous ones
- **Retry logic** — number of attempts, delays, which errors trigger a retry
- **Error handling** per error case from the outbound interface specification
- **Anything else relevant** — caching, rate limiting, correlation for async

Create an alternative flow for each error case that needs different handling. Grouping similar handling is explicitly fine — "for 500 errors or timeouts…".

This is where the division of labour with `TO-` matters: the outbound interface section describes *what the interface is*, and the function describes *how this element calls it*. Timeouts in the interface section are misplaced.

### Referencing a goal is deliberate

The template gives criteria in both directions, which is unusual and worth honouring:

**Reference a goal when** the function is central to fulfilling it, implements important business logic, or is a critical performance factor for it.

**Do not reference a goal when** the function is a utility (sort, filter, format), when it is only called by use cases that already reference the goal, or when it is purely technical with no direct business relevance.

So a function with no goal relation is normal, not an orphan. `DERIVED: Yes` is for the stronger case — the function exists because of an implementation decision nobody asked for — and then `RATIONALE` should say which decision.

`DETAIL_LEVEL` records whether the flow is elaborated into step nodes (`Stepwise`) or described in prose (`Narrative`). A utility function rarely warrants steps; recording the choice stops a reviewer reading the variation as inconsistency.

## Technical Interfaces (inbound)

Interfaces this element **provides** so other elements can access its data or functionality.

- `CALL_TYPE` — `Synchronous` or `Asynchronous`. Required, because everything else about the specification depends on it.
- `CALLING_ELEMENTS` — elements that may call this, with their outbound interface ID where documented
- `INPUT` — per parameter: name, data type, required or optional, description
- `OUTPUT` — per value: name, data type, description, and the conditions under which it is returned
- `ACTION` — what the interface does, at a high level
- `ERROR_CASES` — per case: error code or type, and when it occurs

### Writing the Action field

*Simple interface:* reference the function implementing the logic — "Calls TF-01 with the provided credentials and returns the result."

*Complex interface, or where no single function exists:* which entities are accessed, the major processing steps, what determines the output, and the relevant functions for key steps.

**Avoid** specific attribute IDs, exact algorithms and detailed conditional logic. Those belong in technical functions.

*Synchronous:* state that the response returns immediately after processing, with the expected response time if relevant.

*Asynchronous:* what happens immediately on receipt (validation, queueing, acknowledgement time), the background processing and which function performs it, how the result reaches the caller (callback URL, notification interface), and the expected processing time range.

`ERROR_CASES` should separate immediate errors — validation, authentication — from processing errors, which an asynchronous interface may report via callback.

## Technical Interfaces (outbound)

Interfaces this element **uses** to reach partner elements in the system context.

**Call behaviour is not specified here.** Timeouts, retry logic and error handling live in the technical functions that make the calls. This section describes the interface; the function describes the calling.

- `STATEMENT` follows a set form: "This interface [what it does] by calling [partner element] ([PE-ID]). Used for [purpose in this element]."
- **Name the interface for what *this* element does with it**, not for what the partner offers. "Request authentication" rather than "Identity API".
- `INPUT` — every parameter this element must provide
- `OUTPUT` — every value this element receives
- `ERROR_CASES` — every error this element must be prepared to handle
- `AUTHORITATIVE_SPEC` — where the complete specification lives: the provider element's L3 document and its inbound interface ID. This section holds the consumer's view only.
- Relation `Calls → PE-`

The `AUTHORITATIVE_SPEC` pointer matters because the same interface appears twice in a full document set: as `TI-` in the provider's document and as `TO-` in each consumer's. The provider's is authoritative; the consumers' are views. Recording which is which prevents two specifications drifting apart with no indication of who is right.

## Entities

The entities this element **stores**. Include a diagram for complex data structures.

`PERSISTENCE` — `In-memory`, `Cached`, `Persistent`, `Derived` or `Transient`.

`ATTRIBUTES` is a **table**, following the template exactly:

```
| ID | Attribute | Type | Required | Description |
|---|---|---|---|---|
| E-01.1 | userId | uuid | required | Identifier of the owning user |
| E-01.2 | createdAt | datetime | required | When the record was created |
```

- **Naming:** camelCase — `userId`, `createdAt`, `orderTotal`
- **Types:** be specific. Primitives `string` `integer` `decimal` `boolean` `datetime` `date` `time`; collections `array` `object`; special `enum` `uuid` `url` `email` `phoneNumber`; references to another entity by its ID
- **Required vs optional:** `required` cannot be null or empty; `optional` can
- **Descriptions:** what it stores, constraints (min/max length, range, format), references to other entities, and whether the value is derived

Relation `Refines → BE-` where the entity implements an L1 business entity. Entities that are purely technical — a session record, a cache entry — legitimately have no business counterpart.

**One thing StrictDoc cannot check, but the skill's scripts can.** The `E-01.1` attribute IDs are referenced from technical function steps ("read username from E-02 attribute E-02.3"). They are table content rather than node identifiers, so **StrictDoc does not link-check them** — a renamed or renumbered attribute would otherwise leave stale references behind with no error.

The attribute-reference check closes that gap. It reports references to attributes no entity declares, attributes declared under the wrong entity (an `E-02.3` row inside `E-01`), and duplicates within one entity. It also lists declared attributes that nothing references, as information rather than a defect — an attribute can exist because the data needs it without any step naming it.

Still prefer referring to attributes by name as well as ID, so that a reference remains readable to a person even when the ID is correct.

## Quality Requirements

How well the element performs its functions.

`QUALITY_CATEGORY` uses the same nine technical categories as L2: `Performance`, `Scalability`, `Availability`, `Security`, `Usability`, `Maintainability`, `Compatibility`, `Data-integrity`, `Compliance`.

- `APPLIES_TO` *(optional)* — the parts of this element design affected: user interfaces, use cases, technical functions, either interface section, entities, or the overall architecture
- `ACCEPTANCE_CRITERIA` — quantitative where performance, availability, scalability, security or numerical standards can be measured; qualitative where assessment is subjective, compliance is binary, or a practice is required
- Relation `Supports → SQR-`

`ELEMENT_SPECIFIC: Yes` marks a requirement that is a purely element-level technical goal with no system-level counterpart. The template notes this is legitimate — not every element quality requirement supports a system one.

## Constraints

Non-negotiable requirements limiting design and implementation choices for this element.

`CONSTRAINT_CATEGORY` uses the same five as L2: `Legal-regulatory`, `Technical`, `Business`, `Integration`, `Standards`.

- `SOURCE` *(optional)* — the specific law, standard document, business decision, existing infrastructure or partner requirement
- `APPLIES_TO` — the parts of this element design affected
- `ACCEPTANCE_CRITERIA` — what demonstrates compliance
- `CONSEQUENCE` — what this rules out for the implementer
- Relation `Implements → SC-`

`ELEMENT_SPECIFIC: Yes` for purely technical constraints — implementation choices, library versions — which the template notes need not relate to a system constraint.

## Traceability at this level

**Upward, to L2 and L1:**

| L3 element | Target | Role |
|---|---|---|
| `G-` | `SG-` system goal | `Satisfies` |
| `UC-` | `SSc-` system scenario | `Realises` |
| `TO-` | `PE-` partner element | `Calls` |
| `E-` | `BE-` business entity (L1) | `Refines` |
| `QR-` | `SQR-` system quality requirement | `Supports` |
| `C-` | `SC-` system constraint | `Implements` |

**Within L3:**

| From | To | Role |
|---|---|---|
| `UC-` | `G-` | `Achieves` |
| `TF-` | `G-` | `Achieves` |
| `UI-` | `UC-` | `Realises` |
| `TF-` | `C-` | `Constrained by` |
| `EX-` | `ST-` | `Extends` |
| `FA-` | `FS-` | `Extends` |

**Lateral, as inline links rather than relations:** a step referencing the `UI-`, `TF-` or `TO-` it involves; a UI referencing entities and functions for its data sources; an inbound interface naming its calling elements; quality requirements and constraints applying to parts of the design.

**Into code, once it exists:** `TF-` declares `TYPE: File` relations, so a technical function can point at the function implementing it and StrictDoc will report coverage.

**Downward — nothing.** L3 is the lowest of the four levels. The one thing below it is source code, via `File` relations. Deployment and infrastructure detail belong in the System Realization Concept, alongside the four levels rather than beneath them.
