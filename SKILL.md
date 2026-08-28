---
name: too-long-not-read
description: Guide greenfield software projects through visual Q&A instead of long agent monologues across agentic coding tools, especially CMake/C++ projects that need boundary, architecture, flow, function-contract, and implementation-scope decisions.
metadata:
  short-description: Visual Q&A project planning and implementation control
---

# Too Long Not Read

Use this skill when the user wants to start, reshape, or deeply plan a software project through guided questions, diagrams, and explicit decision gates rather than open-ended conversational delegation. It is especially suited to CMake/C++ projects, but can be adapted to other compiled or modular projects and to different agentic coding environments.

The skill's product name is "Too Long Not Read". If UI metadata provides a localized display name, use it only when matching the user's language.

## Core Behavior

Every assistant reply while this skill is active must begin with a compact plain-text progress strip:

```markdown
**Too Long Not Read Progress**: [Stage 1 Domain Boundary: Current/Complete/Pending] -> [Stage 2 Structure Contract: Current/Complete/Pending] -> [Stage 3 Flow Orchestration: Current/Complete/Pending] -> [Stage 4 Implementation Decision: Current/Complete/Pending]
```

Keep replies visual and decision-oriented. Prefer Mermaid diagrams, Markdown tables, checklists, and short targeted questions over long prose. The user should be able to answer by editing labels, choosing rows, or saying localized equivalents of "keep", "delete", "move", "AI implements", or "manual decision".

Do not treat a vague project request as approval to implement the whole system. First move through the four gates below unless the user explicitly asks to skip ahead. If the user asks the agent to decide something, make the decision, mark it as agent-decided, and continue.

Proceed stage by stage. A normal reply must advance only the current gate and must not generate artifacts for later gates in the same reply. Do not combine domain boundary, structure, flow, declarations, and implementation decisions into one large answer. Move to the next gate only after the current gate is accepted, explicitly delegated to the agent, or bypassed through Lightning Mode.

## Chat Reply Boundary

The chat reply window is only for brief plain-text guidance. Do not render Mermaid diagrams, native HTML components, Markdown tables, large checklists, or visual decision boards in the chat reply. Put all diagrams, visual tables, progress UI, state snapshots, badges, and scenario notes in Markdown preview artifacts.

Each chat reply should contain only:

1. Plain-text progress strip.
2. One short sentence saying what changed or what needs review.
3. Exact artifact path or local preview URL the user should open.
4. The minimum reply instruction needed for the current decision.

If the host supports rich chat rendering, still keep the chat reply plain and use the artifact preview as the visual surface.

## Initial Intake

At the start of every new workflow, ask whether the user already has a written target description and what they want to build, plan, or produce. If the user has already provided a usable target description in the opening request, briefly acknowledge it and proceed into Stage 1. If the target is missing or too vague, ask one compact intake question before drawing the first boundary diagram:

```markdown
Do you already have a target description? If yes, paste it. If not, describe what you want to build, plan, or produce in one paragraph.
```

Do not start Stage 1 from an empty premise unless the user explicitly asks the agent to invent the target.

## Visual Artifact Delivery

Do not rely on inline chat rendering when presenting diagrams, tables, or decision artifacts. Whenever an active step requires a Mermaid diagram or a visual decision table, create or update Markdown preview artifacts for the user, such as `.tlndr/current.md`, `.tlndr/stage-1-domain.md`, or `too-long-not-read-current.md`, in the current project or task workspace.

Artifacts are not limited to one Markdown file. Use multiple Markdown files when that improves clarity, such as one current file per stage, one confirmed archive per accepted stage, and an optional `.tlndr/index.md`. The chat reply must always guide the user to the exact active preview file or local browser URL.

Maintain confirmed archive Markdown artifacts, such as `.tlndr/confirmed.md`, `.tlndr/confirmed-stage-1-domain.md`, or `too-long-not-read-confirmed.md`. Preview artifacts are for the user's immediate decision only. Confirmed archives are for locked history.

Artifact lifecycle:

1. While a stage is under review, put that stage's diagrams, tables, scenario notes, and open decisions in one or more current-stage preview artifacts.
2. When the user accepts a stage or delegates the current gate to the agent, move the accepted stage content out of active preview artifacts and into confirmed archive artifacts.
3. After moving content, rewrite the active preview artifact so it contains only the progress component, compact state snapshot, links or paths to confirmed archives, and the next current-stage content.
4. Do not keep appending confirmed diagrams below the preview content. Confirmed content must not occupy the user's active preview surface.
5. If the host cannot move or rewrite files, clearly mark archived content as collapsed and keep the current stage at the top.

The artifact is Markdown-first, but it is not limited to Markdown syntax. Use safe native HTML when it improves clarity, especially for progress bars, locked/pending decision snapshots, badges, compact dashboards, and side-by-side decision panels. Prefer the renderer's built-in `.tlndr-*` classes from [assets/markdown-renderer.html](assets/markdown-renderer.html) over inline styles so themes can restyle the same artifact.

After writing the artifact:

1. If the host has a native Markdown preview, document panel, browser panel, or file-opening capability, open or show the artifact automatically and mention the exact path or panel.
2. If the host runs in a CLI or terminal without reliable Markdown rendering, start a local HTML Markdown renderer on an available localhost port and provide the browser URL. The renderer must support full GitHub-flavored Markdown, including headings, tables, task lists, links, images, blockquotes, lists, fenced code, sanitized native HTML, Mermaid code fences, and theme selection. Use [scripts/serve_markdown.py](scripts/serve_markdown.py) with [assets/markdown-renderer.html](assets/markdown-renderer.html) when available.
3. If Mermaid rendering is unavailable, the artifact must still include the Mermaid source and a compact text fallback so the user can locate and inspect the diagram.
4. Keep current-stage preview and confirmed archive files organized under one predictable location when possible, such as `.tlndr/`, and mention the active preview path or URL in every chat reply.
5. If the host cannot write files or open ports, state that limitation explicitly and provide a single Markdown payload that the user can render elsewhere.

## Emergency Bypass

If the user explicitly demands skipping gates with instructions such as "just write the code", "stop asking", or "give me a runnable main file", do not resist. Immediately enter **Lightning Mode**:

1. Compress Stages 1-3 into a single compact Markdown table covering system type, dependencies, main entry point, build/runtime command, and obvious risks.
2. Ask exactly three yes/no questions to close the most dangerous unknowns in that table.
3. Jump directly to Stage 4 with a minimal viable function list inferred from the table.
4. Clearly state: "Skipped detailed flow orchestration. Proceeding with minimal viable contract."

Lightning Mode is a user override, not a default shortcut. Preserve any decisions already locked before the override.

## State Snapshot

Immediately after the progress strip, maintain a hidden or compact state snapshot in task metadata or Markdown artifacts. In the chat reply, mention only the active decision unless the host has no writable artifact surface. In the Markdown artifact, prefer the HTML state snapshot component from [references/artifacts.md](references/artifacts.md) so `[LOCKED]` and `[PENDING]` decisions are visually scannable.

```text
[LOCKED] Domain: {ProjectName}, Platforms: {Windows/macOS/Linux}
[LOCKED] Structure: Core -> Utils -> App
[PENDING] Flow: {branch awaiting user input}
```

Keep the snapshot factual and short. Update it after each user decision so later stages do not contradict earlier locked choices.

## Tool-Agnostic Operation

This workflow is not tied to one agent product. Apply it in any chat-based, IDE-based, terminal-based, or repository-aware agent tool that can display Markdown and maintain task context. Adapt the artifacts to the host's abilities:

- If the host can edit files and run commands, use the gates before changing meaningful project structure or implementation.
- If the host is chat-only, produce the diagrams, tables, contracts, and implementation plan as user-executable artifacts.
- If the host cannot render Mermaid, provide the Mermaid source plus a compact text fallback.
- If the host has its own task, plan, memory, or approval mechanisms, keep those mechanisms subordinate to the four gates.
- Avoid product-specific claims unless the current host actually supports that feature.

## Runtime Language

The skill documentation is written in English, but the agent's runtime replies must match the user's language. If the user writes in Chinese, reply in Chinese. If the user writes in English, reply in English. If the user explicitly requests a different language, follow that request. Localize progress labels, table headers, decision choices, and diagram node labels while preserving stable IDs, function names, target names, paths, and code.

## Length Tyranny

- **Core principle**: Draw an extra line before adding another explanatory sentence.
- **Chinese response limit**: When replying in Chinese, keep core guiding prose, meaning plain narrative sentences, under 200 Chinese characters. Put all remaining content inside Mermaid comments or node labels, Markdown table cells, or numbered list items.
- **Driving mechanism**: While drafting a reply, if the plain prose exceeds 200 Chinese characters, stop and check whether the remaining content can fit inside diagram node labels, Yes/No branches, or a table "Notes" column. Expand to 300 Chinese characters only when diagrams and tables cannot carry the content.
- **Exemptions**: Exact reproduction of user error input, file path diffs, raw build logs, and explicit user requests for detailed error explanation or log analysis are exempt from the length limit. If the user asks why something failed, suspend the limit for that single reply and resume it on the next turn.
- **English response limit**: When replying in English, keep core narrative prose under 150 words. IDs, function names, CMake target names, paths, and code in diagrams or tables do not count.
- **Optional self-check log**: At the end of a reply, outside the rendered decision area, add a line such as `[Length Stats] prose: 142 words, diagram/table cells: 310 words` to verify compliance.

## Four Gates

1. **Domain Boundary**: Turn vague requirements into a bounded system. Identify modules, external dependencies, platforms, minimum features, excluded features, data inputs/outputs, and risk assumptions. Show a "system boundary and dependency diagram" before asking for decisions.
2. **Structure Contract**: Establish compile structure first, then code architecture. Show the project tree and CMake dependency hierarchy before writing files or code.
3. **Flow Orchestration**: Convert module behavior into flows. Start with swimlane sequence diagrams, add exception/branch decisions visibly, then propose function declarations for user review.
4. **Implementation Decision**: Let the user decide which functions should be co-authored with the agent and which can be implemented automatically. Show a function implementation table before making non-trivial implementation edits.

## Reference Routing

- For stage outputs, Mermaid patterns, and required decision questions, read [references/artifacts.md](references/artifacts.md).
- For C/C++ or CMake-specific structure and compile-contract checks, read [references/project-c-c++.md](references/project-c-c++.md).
- For Python projects, read [references/project-python.md](references/project-python.md).
- For Rust projects, read [references/project-rust.md](references/project-rust.md).
- For Go projects, read [references/project-go.md](references/project-go.md).
- For Node.js or TypeScript projects, read [references/project-node-typescript.md](references/project-node-typescript.md).
- For Java projects, read [references/project-java.md](references/project-java.md).
- For function declarations, ownership review, and implementation-scope tables, read [references/function-contracts.md](references/function-contracts.md) during stages 3 and 4.
- For file-backed diagram delivery and CLI rendering, use [scripts/serve_markdown.py](scripts/serve_markdown.py) and the bundled static page [assets/markdown-renderer.html](assets/markdown-renderer.html) when the host environment allows scripts.

## Language/Stack Detection

Before routing to CMake-specific guidance, detect the user's implied stack from language, files, package manifests, and commands:

- If C, C++, `CMakeLists.txt`, or CMake is mentioned, read [references/project-c-c++.md](references/project-c-c++.md).
- If Python, `pyproject.toml`, `setup.py`, or `requirements.txt` is mentioned, read [references/project-python.md](references/project-python.md).
- If Rust or `Cargo.toml` is mentioned, read [references/project-rust.md](references/project-rust.md).
- If Go or `go.mod` is mentioned, read [references/project-go.md](references/project-go.md).
- If Node.js, JavaScript, TypeScript, `package.json`, `tsconfig.json`, `pnpm-lock.yaml`, `yarn.lock`, or `bun.lockb` is mentioned, read [references/project-node-typescript.md](references/project-node-typescript.md).
- If Java, Maven, Gradle, `pom.xml`, `build.gradle`, or `build.gradle.kts` is mentioned, read [references/project-java.md](references/project-java.md).
- For all other stacks, use the generic structure in [references/artifacts.md](references/artifacts.md) and omit CMake-specific target diagrams.
- For all other domains, including documentation, planning, recipes, education, operations, research outlines, travel plans, and other non-software projects, do not load any `project-*.md`. Use only the generic [references/artifacts.md](references/artifacts.md) structure. Replace "CMake target" with "Deliverable" and replace "Compile" with "Produce final output". The four gates still apply: Domain means parts, Structure means table of contents or work breakdown, Flow means timeline or process, and Implementation means who writes, executes, or finalizes each item.

## Operating Rules

- Ask only the minimum question needed to advance the current gate. When there are many open choices, present a table with a recommended default and a "user decides" column.
- After each user decision, update the relevant diagram or table rather than restating the whole conversation.
- Keep a visible "open decisions" list until all blocking decisions for the current gate are closed.
- **Contract Immutability**: Once a gate is marked `[LOCKED]` in the State Snapshot, it cannot be altered unless the user explicitly says "change decision on [ID]" or an equivalent localized override. If a later user request contradicts a locked decision, reply: "Conflict with locked decision [ID]. Please confirm override or adjust request."
- Use Markdown-renderable artifacts as the main communication surface. Diagrams must be concise enough that the user can point to a node, edge, branch, or row. Prefer fewer nodes with clearer labels over exhaustive diagrams. Put necessary explanation below the diagram as a compact scenario table or numbered list instead of expanding the diagram until it becomes unreadable.
- When implementing in a repository, inspect the existing tree first and preserve existing conventions. Do not overwrite user work.
- If the user explicitly asks for agent autonomy, proceed, but still record which decisions were agent-decided.

## Final Handover

When all selected `AI` and `Co-author` functions are implemented and the selected verification checks pass, terminate the active workflow with a **Handover Report**:

1. **Implemented**: files, functions, modules, and generated artifacts completed by the agent.
2. **Verified**: build, test, lint, or runtime commands that were run and passed.
3. **Ownership Transfer**: `Manual` functions, stubs, TODOs, missing credentials, or environment-specific steps the user owns.
4. **Next Command**: the exact next build/test/run command the user should execute locally when appropriate.

After delivering the Handover Report, the skill enters idle mode and stops appending the progress strip unless the user reactivates the workflow.
