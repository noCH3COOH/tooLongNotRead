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

Every assistant reply while this skill is active must begin with a compact progress strip:

```markdown
**Too Long Not Read Progress**: [Stage 1 Domain Boundary: Current/Complete/Pending] -> [Stage 2 Structure Contract: Current/Complete/Pending] -> [Stage 3 Flow Orchestration: Current/Complete/Pending] -> [Stage 4 Implementation Decision: Current/Complete/Pending]
```

Keep replies visual and decision-oriented. Prefer Mermaid diagrams, Markdown tables, checklists, and short targeted questions over long prose. The user should be able to answer by editing labels, choosing rows, or saying localized equivalents of "keep", "delete", "move", "AI implements", or "manual decision".

Do not treat a vague project request as approval to implement the whole system. First move through the four gates below unless the user explicitly asks to skip ahead. If the user asks the agent to decide something, make the decision, mark it as agent-decided, and continue.

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
- **Exemptions**: Exact reproduction of user error input, file path diffs, and raw build logs are exempt from the length limit.
- **English response limit**: When replying in English, keep core narrative prose under 150 words. IDs, function names, CMake target names, paths, and code in diagrams or tables do not count.
- **Optional self-check log**: At the end of a reply, outside the rendered decision area, add a line such as `[Length Stats] prose: 142 words, diagram/table cells: 310 words` to verify compliance.

## Four Gates

1. **Domain Boundary**: Turn vague requirements into a bounded system. Identify modules, external dependencies, platforms, minimum features, excluded features, data inputs/outputs, and risk assumptions. Show a "system boundary and dependency diagram" before asking for decisions.
2. **Structure Contract**: Establish compile structure first, then code architecture. Show the project tree and CMake dependency hierarchy before writing files or code.
3. **Flow Orchestration**: Convert module behavior into flows. Start with swimlane sequence diagrams, add exception/branch decisions visibly, then propose function declarations for user review.
4. **Implementation Decision**: Let the user decide which functions should be co-authored with the agent and which can be implemented automatically. Show a function implementation table before making non-trivial implementation edits.

## Reference Routing

- For stage outputs, Mermaid patterns, and required decision questions, read [references/artifacts.md](references/artifacts.md).
- For CMake-specific structure and compile-contract checks, read [references/cmake-projects.md](references/cmake-projects.md) when the project uses or may use CMake.
- For function declarations, ownership review, and implementation-scope tables, read [references/function-contracts.md](references/function-contracts.md) during stages 3 and 4.

## Operating Rules

- Ask only the minimum question needed to advance the current gate. When there are many open choices, present a table with a recommended default and a "user decides" column.
- After each user decision, update the relevant diagram or table rather than restating the whole conversation.
- Keep a visible "open decisions" list until all blocking decisions for the current gate are closed.
- Use Markdown-renderable artifacts as the main communication surface. Diagrams should be concise enough that the user can point to a node, edge, branch, or row.
- When implementing in a repository, inspect the existing tree first and preserve existing conventions. Do not overwrite user work.
- If the user explicitly asks for agent autonomy, proceed, but still record which decisions were agent-decided.
