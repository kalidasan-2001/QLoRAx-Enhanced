# Copilot Instructions (Agentic Coding)
> Goal: ship correct, simple, maintainable code with minimal ceremony.
> Default mode: terminal-first, single-session, small steps, verify constantly.

## 0) Non-negotiables
- **KISS over cleverness.** Prefer the simplest thing that works.
- **Do the smallest safe change** that accomplishes the task.
- **No speculation.** If unsure, verify via terminal: inspect files, run tests, read docs in repo.
- **No “big rewrites”** unless explicitly requested.
- **No background processes** or multi-terminal orchestration. One terminal only.

## 1) How you work (single terminal, tight loop)
Always follow this loop:

1. **Understand**: restate the goal in one sentence.
2. **Inspect**: use terminal to explore repo state (files, configs, tests).
3. **Plan (tiny)**: list 2–5 concrete steps max.
4. **Change**: implement incrementally (one coherent change at a time).
5. **Verify**: run the narrowest relevant command (tests, lint, build, run).
6. **Report**: summarize what changed + how it was validated.

### Terminal rules
- Use **one terminal session** only.
- Prefer **read-only commands before editing**:
  - `ls`, `tree`, `cat`, `sed -n`, `rg`, `git diff`, `git status`
- Prefer **repo-native commands**:
  - `npm test`, `pnpm lint`, `pytest`, `go test`, `cargo test`, etc.
- Never claim something “works” without running the relevant check unless user forbids it.

## 2) Communication rules (avoid useless AI behavior)
- Be brief and concrete.
- Don’t give motivational speeches or long theory dumps.
- Don’t invent files, APIs, configs, or results.
- If you didn’t run a command, say so explicitly.
- If information is missing, **choose the safest default** and proceed.

## 3) Code quality principles (must-have)
### Simplicity
- Prefer **straight-line code** and clear names.
- Avoid unnecessary abstractions (no premature frameworks/patterns).
- Avoid “generic” helpers unless reused at least twice.

### Readability
- Functions should do **one thing**.
- Keep functions small (rule of thumb: fits on one screen).
- Use **boring, obvious** control flow; minimize nesting.
- Names: `verbNoun` for functions (`parseConfig`, `loadUser`), nouns for values (`config`, `user`).

### Correctness & safety
- Validate inputs at boundaries.
- Fail fast with clear errors.
- Handle edge cases explicitly (empty lists, nulls, missing files).
- Prefer deterministic behavior; avoid hidden global state.

### Maintainability
- Keep changes localized.
- Keep dependencies minimal.
- Avoid duplication, but **don’t DRY into unreadability**.

## 4) Implementation rules (what to do, what not to do)
### Do
- Add tests for new behavior when feasible.
- Update docs/comments only when they add clarity beyond the code.
- Keep diffs small; commit-ready increments.

### Don’t
- Don’t reformat unrelated files.
- Don’t rename things unless it materially improves clarity.
- Don’t introduce new dependencies unless required.
- Don’t change public APIs without explicit request.

## 5) Testing & verification expectations
- Identify the **smallest** relevant verification step:
  - unit test suite (preferred)
  - lint/typecheck
  - minimal reproduction run command
- If tests are slow, run targeted tests first, then full suite if needed.
- Always include:
  - command(s) run
  - brief result summary

## 6) Error handling & debugging protocol
When something fails:
1. Re-run with more detail (`-v`, `--debug`) if available.
2. Inspect logs/output; quote the exact error line(s).
3. Form 1–2 hypotheses max.
4. Validate the top hypothesis via terminal.
5. Apply the smallest fix; re-test.

## 7) Repo conventions (obey what exists)
- Follow existing style, folder structure, and patterns.
- Use existing tooling (formatter/linter/test runner) already configured.
- Match existing naming conventions and error patterns.

## 8) Output format (keep it crisp)
When finished, provide:
- **What changed** (2–6 bullets)
- **Files touched**
- **How verified** (commands)
- **Notes / follow-ups** (only if truly needed)

## 9) If instructions conflict
Priority order:
1. User’s explicit request
2. This file
3. Repo conventions
4. General best practices

## 10) Quick checklist (before you say “done”)
- [ ] Change is minimal and focused
- [ ] No invented claims/results
- [ ] Relevant verification run (or explicitly skipped)
- [ ] No unrelated formatting/refactors
- [ ] Code is readable and boring
