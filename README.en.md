# Too Long Not Read

[中文](README.md)

**Too Long Not Read** is a visual, question-driven project-building workflow for agent tools. Its goal is not to make one agent write more, but to make chat-based, IDE-based, terminal-based, and repository-aware agents clarify project boundaries, structure, flows, function contracts, and implementation scope before writing substantial code.

This repository is currently packaged in a Codex-compatible skill format, but the method is not tied to Codex. Any agent tool that can keep context, output Markdown, and render Mermaid or at least provide Mermaid source can adapt the workflow.

## What It Solves

| Common Problem | Too Long Not Read Approach |
|---|---|
| The user gives one broad request and the agent writes too much code | Pass four decision gates before implementation |
| The user returns later and finds the architecture wrong | Use diagrams and explicit decisions at every stage |
| Structure, dependencies, and module boundaries are unclear | Show boundary diagrams, directory trees, and dependency graphs |
| Function responsibilities and exception paths appear too late | Draw swimlane flows before reviewing declarations |
| The user has to read long replies | Use Length Tyranny to move information into diagrams, tables, and numbered items |
| The user says "stop asking, just write it" | Enter Lightning Mode and compress decisions into three yes/no questions |
| Long conversations make the agent forget earlier choices | Maintain a locked decision snapshot in every active reply |
| The user cannot find the diagram | Create a Markdown artifact file; CLI agents serve a full Markdown local HTML preview |

## Four Stages

| Stage | Name | Main Artifact | User Action |
|---|---|---|---|
| 1 | Domain Boundary | System boundary and dependency diagram | Keep, remove, or defer dependencies and minimum features |
| 2 | Structure Contract | Project tree and CMake target hierarchy | Move, split, merge, delete, or accept modules |
| 3 | Flow Orchestration | Swimlane sequence diagrams and function declaration tables | Add branches, revise signatures, or accept contracts |
| 4 | Implementation Decision | Function implementation table | Mark functions as `AI`, `Co-author`, or `Manual` |

## Agent Compatibility

| Agent Type | How To Use It |
|---|---|
| Chat-based agent | Produce diagrams, tables, contracts, and implementation plans for manual execution |
| IDE agent | Complete the four decision gates before editing files |
| Terminal agent | Confirm structure and command boundaries before generating, building, and testing |
| Repository-aware agent | Treat trees, dependency graphs, and function lists as pre-change review artifacts |
| Agent without Mermaid rendering | Output Mermaid source and a compact text fallback |
| Non-software project | Replace target with deliverable and compile with produce final output |

## Stack Adaptation

| Stack | Structure Contract Mapping |
|---|---|
| C / C++ / CMake | `CMakeLists.txt`, targets, `target_link_libraries` |
| Python | `pyproject.toml`, `setup.py`, packages, modules, dependency sections |
| Rust | `Cargo.toml`, crates, features, workspaces |
| Go | `go.mod`, packages, `cmd/`, `internal/` |
| Node.js / TypeScript | `package.json`, `tsconfig.json`, scripts, packages |
| Java | Maven/Gradle, packages, modules, JUnit |
| Other | Use generic module diagrams, trees, and flows; omit CMake-specific graphs |
| Non-software domains | Use generic `artifacts.md`; map the four gates to parts, outline/work breakdown, timeline, and delivery ownership |

## Core Rules

1. Every active reply starts with a visible progress strip.
2. Runtime replies match the user's language.
3. English guiding prose is limited to 150 words by default.
4. Diagrams, tables, and numbered lists carry most of the information.
5. The agent does not implement the whole project until boundary, structure, flow, declaration, and scope decisions are explicit.
6. Native planning, memory, approval, and execution features of the host agent remain subordinate to the four gates.
7. If the user explicitly overrides the gates, enter Lightning Mode instead of resisting.
8. Finish with a Handover Report listing implemented work, verified checks, and user-owned items.
9. Locked decisions cannot be implicitly rolled back; conflicting requests require explicit override confirmation.
10. Any diagram or decision table must be written to a dedicated Markdown artifact; CLI agents must provide a local browser preview URL with full GitHub Flavored Markdown support.

## Repository Layout

```text
too-long-not-read/
|-- SKILL.md
|-- README.md
|-- README.en.md
|-- agents/
|   `-- openai.yaml
|-- assets/
|   `-- markdown-renderer.html
|-- scripts/
|   `-- serve_markdown.py
`-- references/
    |-- artifacts.md
    |-- function-contracts.md
    |-- project-c-c++.md
    |-- project-go.md
    |-- project-java.md
    |-- project-node-typescript.md
    |-- project-python.md
    `-- project-rust.md
```

## Install In Codex

If you use Codex, copy this repository into the Codex skills directory and make sure the target directory is named `too-long-not-read`.

Windows PowerShell:

```powershell
Copy-Item -Recurse -Force . "$env:USERPROFILE\.codex\skills\too-long-not-read"
```

macOS / Linux:

```bash
mkdir -p ~/.codex/skills/too-long-not-read
cp -R ./* ~/.codex/skills/too-long-not-read/
```

## Port To Other Agents

Use [SKILL.md](SKILL.md) as the main instruction file and the files under `references/` as stage-specific references. Each host agent has its own integration path, but the core requirements stay the same:

1. Show progress first.
2. Prefer diagrams before explanation.
3. Ask the user to decide before implementation.
4. Propose function declarations before writing bodies.
5. Keep undecided implementation scope as `?`.
6. Write diagrams and tables into one Markdown artifact file; when no Markdown renderer is available, use `scripts/serve_markdown.py` to launch the `assets/markdown-renderer.html` static page and preview full Markdown on a local port.

Local preview example:

```bash
python scripts/serve_markdown.py too-long-not-read-artifacts.md --port 8765
```

The renderer supports GitHub Flavored Markdown, tables, task lists, fenced code, highlighting, links, images, blockquotes, sanitized HTML, and Mermaid diagram rendering from source fences.

## Usage Example

```text
Use the too-long-not-read workflow to plan a CMake/C++ project from scratch. Start by defining boundaries, structure, flows, and implementation scope through visual Q&A.
```

In Codex, you can invoke it as:

```text
Use $too-long-not-read to turn this project idea into a guided Q&A build plan with diagrams and implementation choices.
```

## Validate

For the Codex-compatible skill package, run:

```powershell
python -X utf8 C:\Users\<you>\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
```

Expected output:

```text
Skill is valid!
```
