# Function Contracts and Implementation Scope

Use this reference during stages 3 and 4.

## Function Declaration Proposal

Do not jump from a flow diagram directly to implementations. First propose function declarations as contracts the user can inspect.

For C++, include:

- Namespace.
- Header path.
- Function or class method signature.
- Ownership and lifetime expectations.
- Error model: return value, exception, `std::expected`-style result, status enum, or callback.
- Test expectation.

Signature review table:

```markdown
| ID | Module | Header | Declaration | Responsibility | Error Model | User Decision |
|---|---|---|---|---|---|---|
| F1 | core | include/app/core/config.hpp | `Config loadConfig(const std::filesystem::path& path);` | Parse and validate config | Throws `ConfigError` | ? |
```

Ask the user to reply with edits by ID:

```markdown
Reply by F ID: accepted, rename, change parameters, change return value, change error model, or let AI decide.
```

## Implementation Scope

After declarations are accepted, classify every function into one of these implementation modes:

- `AI`: agent may implement and test without more design discussion.
- `Co-author`: agent writes a first draft, then asks the user for targeted review before finalizing behavior-sensitive details.
- `Manual`: agent should not implement the function body; create an interface, stub, TODO, or documentation only if useful.
- `?`: undecided; do not implement until resolved unless the user grants autonomy.

Implementation decision table:

```markdown
| ID | Function | Module | Contract Status | Suggested Mode | AI Implements? | Test Plan |
|---|---|---|---|---|---|---|
| F1 | `loadConfig` | core | Accepted | AI | ? | malformed/missing/valid config |
| F2 | `executePayment` | adapters | Needs business rule input | Co-author | ? | timeout/retry/decline/success |
```

Use red text only when the target renderer supports HTML:

```html
<span style="color:#dc2626;font-weight:700">?</span>
```

Otherwise use plain `?` so the table remains portable.

## Implementation Workflow

Once the user has resolved implementation modes:

1. Implement `AI` functions in dependency order.
2. For `Co-author` functions, create a small draft or skeleton and ask for the narrowest useful review question.
3. For `Manual` functions, preserve the contract and avoid filling in behavior.
4. Run tests or build checks after each coherent batch.
5. Report changed files, verification results, and remaining user-owned functions.

If the user changes a declaration after implementation has started, update the implementation table first, then patch code.
