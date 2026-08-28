# Artifact Templates

Use these templates to keep the workflow visual, compact, and easy for the user to correct.

## Template Localization Rule

All human-readable text inside these templates, including table cells, node labels, Mermaid comments, and question prompts, is example content only. The agent must localize it to the user's current runtime language when rendering. Stable identifiers such as `F1` and `D1`, function names such as `loadConfig`, paths, target names, commands, and code remain in their source language.

## Markdown-Compatible HTML Components

Markdown preview artifacts are rendered through the bundled HTML Markdown renderer. Write them as GitHub Flavored Markdown plus safe, Markdown-compatible native HTML when visual structure matters. Use these classes instead of inline styles so the renderer can apply themes.

The bundled renderer supports selectable themes. Keep semantic class names stable and avoid hard-coded colors in artifact HTML. Native Markdown preview can be used only as a fallback when the HTML renderer cannot run.

Progress component:

```html
<section class="tlndr-progress" aria-label="Too Long Not Read Progress">
  <div class="tlndr-progress-head">
    <strong>Too Long Not Read Progress</strong>
    <span>Stage 2 of 4</span>
  </div>
  <ol class="tlndr-steps">
    <li class="done"><span>1</span><strong>Domain Boundary</strong><em>Locked</em></li>
    <li class="current"><span>2</span><strong>Structure Contract</strong><em>Current</em></li>
    <li><span>3</span><strong>Flow Orchestration</strong><em>Pending</em></li>
    <li><span>4</span><strong>Implementation Decision</strong><em>Pending</em></li>
  </ol>
</section>
```

State snapshot component:

```html
<section class="tlndr-snapshot" aria-label="State Snapshot">
  <div class="tlndr-snapshot-row locked">
    <span class="tlndr-badge locked">LOCKED</span>
    <strong>Domain</strong>
    <span>ProjectName, Windows/Linux</span>
  </div>
  <div class="tlndr-snapshot-row pending">
    <span class="tlndr-badge pending">PENDING</span>
    <strong>Flow</strong>
    <span>Timeout branch awaiting user input</span>
  </div>
</section>
```

Decision status badges:

```html
<span class="tlndr-badge locked">LOCKED</span>
<span class="tlndr-badge pending">PENDING</span>
<span class="tlndr-badge risk">RISK</span>
<span class="tlndr-badge ai">AI</span>
<span class="tlndr-badge manual">Manual</span>
```

If the host or fallback renderer strips HTML, fall back to plain Markdown progress and `[LOCKED]` / `[PENDING]` text blocks, but preserve the HTML-enhanced source whenever the bundled renderer is available.

## Stage Pacing Rule

Render artifacts for one stage at a time. Do not include future-stage artifacts in the same reply or artifact update unless the user explicitly activates Lightning Mode. Later-stage sections may exist as empty placeholders, but their content should remain `Pending`.

## Structured Question Rule

Each active artifact update must create one matching user question. Prefer the host's structured question or user-input API whenever available. The question must reference IDs, node names, row IDs, or function names shown in the preview artifact.

Use one to three questions per turn. Each question should have two or three clear choices when possible, with a recommended default first. If the host cannot show structured questions, place the choices in the preview artifact and ask a concise plain-text question in chat.

Question mapping pattern:

```markdown
Question ID: Q1
Artifact IDs: D1, D2, F1
Prompt: Which decisions should change before locking this stage?
Choices: Accept recommended, Edit listed IDs, Delegate to agent
```

Do not advance the gate until the user answers, delegates the decision, or triggers Lightning Mode.

## Visual Unit Packing Rule

Treat a diagram and its nearby table as one visual decision unit. One preview Markdown file may contain either:

1. One diagram, meaning one Mermaid diagram or one native HTML visual diagram, plus one table with no more than six body rows.
2. No diagram, plus one table with any number of body rows.

Do not put two diagrams in the same preview file. Do not put a diagram plus several decision, scenario, dependency, or open-decision tables in the same preview file. Scenario notes and open decisions are tables for this rule. If a stage needs multiple tables, either merge the rows into one table with compact columns or split the content into more Markdown files.

When splitting files, add a short link explanation near each link:

```markdown
[Open dependency decisions](stage-1-dependencies.md) - review this before changing the boundary diagram.
[Open scenario notes](stage-3-flow-scenarios.md) - branch notes connected to `checkoutFlow`.
```

Progress components, compact state snapshots, and archive/index link panels do not count as the single table, but they must stay short and must not become hidden extra decision tables.

## Preview and Confirmed Archives

Keep Markdown artifacts organized and explicit when the host can write files. Do not require a single Markdown file.

Common patterns:

- Single active preview: `.tlndr/current.md` or `too-long-not-read-current.md`.
- Stage-specific previews: `.tlndr/stage-1-domain.md`, `.tlndr/stage-2-structure.md`, and so on.
- Confirmed archive: `.tlndr/confirmed.md` or `too-long-not-read-confirmed.md`.
- Stage-specific confirmed archives: `.tlndr/confirmed-stage-1-domain.md`, `.tlndr/confirmed-stage-2-structure.md`, and so on.
- Optional index: `.tlndr/index.md` listing the active preview and confirmed archives.

The active preview should contain only:

1. Progress component.
2. Compact state snapshot.
3. One current-stage visual decision unit, following the Visual Unit Packing Rule.
4. Links or paths to sibling preview files and confirmed archives, each with a short explanation.

When a stage is accepted, move its full content to the confirmed archive and remove it from active preview files before rendering the next stage. The chat reply should point to the active preview path or browser URL, not reproduce the diagram.

Archive link block:

```html
<section class="tlndr-panel">
  <strong>Confirmed Archive</strong>
  <p>Locked decisions moved to <code>.tlndr/confirmed.md</code>.</p>
</section>
```

## Diagram Brevity and Scenario Notes

Keep diagrams compact. A stage diagram should usually fit on one screen and use the smallest number of nodes needed to support the current decision. Move explanatory detail into a scenario note block below the diagram.

Scenario note table:

```markdown
| Scenario | Trigger | Expected Path | User Check |
|---|---|---|---|
| Happy path | Valid input | User -> App -> Core -> Adapter -> Result | Confirm |
| Validation failure | Invalid input | Core returns error before Adapter call | Add missing rule? |
| Timeout | External dependency slow | Adapter timeout branch | Keep, change, or delete? |
```

For non-software domains, replace "Expected Path" with "Outcome" or "Deliverable".

## Initial Intake Prompt

Before Stage 1, ask whether the user already has a written target description. Use the host's structured question API when available. Keep this prompt short and localize it to the user's runtime language:

```markdown
Do you already have a target description? If yes, paste it. If not, describe what you want to build, plan, or produce in one paragraph.
```

If the user already provided a clear target, render an intake row in the artifact and proceed:

```html
<section class="tlndr-panel">
  <strong>Intake</strong>
  <p>Target description received. Proceeding to Stage 1.</p>
</section>
```

## Stage 1: Domain Boundary

Goal: define what the system is, what it depends on, and what is out of scope.

Required user-facing artifacts:

- System boundary and dependency diagram.
- Minimum feature list.
- External dependency table.
- Open decisions table.
- Scenario notes for ambiguous boundary cases.

Use Mermaid where available:

````markdown
```mermaid
flowchart LR
  subgraph S["System Boundary"]
    UI["Module: CLI / UI"]
    Core["Module: Core"]
    Store["Module: Storage"]
    UI --> Core
    Core --> Store
  end

  Compiler@{ shape: cloud, label: "External: C++ Compiler" }
  SDK@{ shape: cloud, label: "External: Vendor SDK" }
  OS@{ shape: cloud, label: "External: OS APIs" }

  Core --> Compiler
  Core --> SDK
  Store --> OS
```
````

If the renderer does not support Mermaid shape syntax, use rounded nodes prefixed with `External:` and keep external dependencies outside the system subgraph.

Dependency table:

```markdown
| Dependency | Why It Exists | Required? | Risk | Default Decision | User Decision |
|---|---|---:|---|---|---|
| CMake >= 3.24 | Build generation | Yes | Low | Keep | ? |
| Vendor SDK | Hardware integration | No | Medium | Decide later | ? |
```

Stage 1 gate question:

```markdown
Question ID: Q1
Artifact IDs: D1, D2, feature rows
Please decide only these items: which external dependencies should be removed, kept, or deferred, and which minimum features must enter version one?
```

## Stage 2: Structure Contract

Goal: decide how the project builds and how modules are allowed to depend on each other.

Required user-facing artifacts:

- Project directory tree.
- CMake target dependency diagram.
- Module responsibility table.
- Structure adjustment questions.
- Scenario notes for common layout decisions.

Directory tree:

````markdown
```text
project-root/
|-- CMakeLists.txt
|-- cmake/
|-- include/
|   `-- project_name/
|-- src/
|   |-- core/
|   |-- app/
|   `-- adapters/
|-- tests/
`-- docs/
```
````

CMake dependency hierarchy:

````markdown
```mermaid
flowchart BT
  app["target: project_app"] --> core["target: project_core"]
  tests["target: project_tests"] --> core
  core --> common["target: project_common"]
  adapters["target: project_adapters"] --> core
  adapters --> external_sdk@{ shape: cloud, label: "External SDK" }
```
````

Stage 2 gate question:

```markdown
Question ID: Q2
Artifact IDs: directory names, target names, module rows
Reply by node or directory name: move, split, merge, delete, or say "structure accepted".
```

## Stage 3: Flow Orchestration

Goal: convert behavior into visible runtime flows before locking function declarations.

Required user-facing artifacts:

- Swimlane sequence diagram for each important workflow.
- Branch and exception list.
- Function declaration proposal grouped by module.
- Signature review table.
- Scenario notes below each flow diagram.

Swimlane sequence diagram:

````markdown
```mermaid
sequenceDiagram
  participant User
  participant App
  participant Core
  participant Adapter

  User->>App: Start command
  App->>Core: validateRequest(input)
  alt valid
    Core->>Adapter: execute(action)
    Adapter-->>Core: result
    Core-->>App: success payload
  else invalid
    Core-->>App: validation error
  end
  App-->>User: Render outcome
```
````

Stage 3 gate question:

```markdown
Question ID: Q3
Artifact IDs: branch labels, participant names, function rows
Point to any missing branch, exception, state change, or module interaction in the flow diagram. You can also say "flow accepted, move to function declarations".
```

## Stage 4: Implementation Decision

Goal: let the user choose where to stay involved and where the agent can implement directly.

Required user-facing artifacts:

- Function implementation list as a Markdown table.
- AI/manual/co-author decision column.
- Test expectation column.
- Implementation batch plan after decisions are made.

Implementation table:

```markdown
| Function | Module | Behavior Contract | Tests Needed | AI Implements? | Notes |
|---|---|---|---|---|---|
| parseConfig(path) | core | Load and validate config | Unit: valid/missing/bad format | ? | User decides |
| runPipeline(input) | app | Coordinate validation and execution | Integration: happy path/error path | ? | User decides |
```

Use plain visible markers for uncertain decisions:

- `?` means the user has not decided.
- `AI` means implement automatically.
- `Co-author` means the agent drafts and the user reviews.
- `Manual` means leave a stub, TODO, interface, or documented contract.

Stage 4 gate question:

```markdown
Question ID: Q4
Artifact IDs: function names, implementation rows
Reply by function name: AI, Co-author, or Manual. Functions you do not mention remain `?` and will not be implemented without a decision.
```

## Open Decisions Block

End each gate reply with a small decision block:

```markdown
**Open Decisions**
| ID | Decision | Recommended Default | Your Reply |
|---|---|---|---|
| D1 | Keep Vendor SDK? | Defer | ? |
```

Once a decision is closed, update the diagram/table and remove it from the blocking list.
