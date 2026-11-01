# Dev Planning

Turns a ticket into an investigated, test-baselined implementation plan, reviewed by subagents before any code is written.

## What it does

Dev Planning takes a ticket, feature or bug, and turns it into an implementation plan you can trust before anyone writes code. It investigates the real codebase, records a test baseline, writes the plan, then has independent reviewers try to break it. It never edits application code, configuration or tests.

## What you get

Two Markdown files in `docs/<ticket number>/`, kept out of git:

- **`ticket-context.md`**: the ticket copied in full and structured for later reading, with no detail dropped or reworded.
- **`implementation-plan.md`**, in eight sections:
  1. **Summary** of what is being built or fixed, and why.
  2. **Root cause** for bugs, or each acceptance criterion mapped to the change that meets it for features.
  3. **Prerequisites**: services that must be running, seed data to insert, feature flags and config to set.
  4. **Implementation steps**, ordered, each traceable to a requirement or the root cause, preferring the smallest correct change.
  5. **Testing plan**: the unit and integration tests to add or change, and the fixtures each one needs.
  6. **Compliance and acceptance**: a criterion-by-criterion checklist, and a check against the repo's coding standards.
  7. **Risks and assumptions**, including anything it could not verify and the blast radius of the change.
  8. **Ticket sub-tasks**: 6 to 11 short names ready to paste into Jira or similar, starting with Planning and ending with Code Review, plus Testing when the ticket goes through QA.

## How it works

1. **Capture.** Reads `CLAUDE.md` files first, takes the ticket number from the title (or asks for it), saves the ticket context, and adds the folder to `.git/info/exclude` if docs aren't already ignored.
2. **Investigate.** Traces the code paths the ticket touches: entry points, services, persistence, authorisation, config and downstream calls. Searching is handed to Sonnet subagents; it reads files itself only to confirm high-risk claims such as a root cause or a security path. Docs are treated as leads and checked against the code.
3. **Baseline.** Runs the affected service's unit and integration tests with the commands in `CLAUDE.md` and records the result. A failing baseline is reported prominently rather than fixed.
4. **Plan.** Writes the eight-section plan.
5. **Review.** Three reviewer subagents check the plan against the code in parallel, one lens each: correctness against the root cause or criteria, test adequacy and missed prerequisites, and unnecessary or risky changes. It verifies every finding itself, fixes the valid ones and notes the dismissed ones. Two rounds at most; anything still open goes under Risks.

## When it finishes

A short report with the two file paths, the baseline result, a plan synopsis, the acceptance checklist, open risks, how many review rounds it took, and the sub-task list copied verbatim. The full plan stays in the file.

## Guardrails

- Writes only the two Markdown files, plus the git exclude entry if needed.
- The code is the source of truth. When a doc disagrees, it trusts the code and records the discrepancy.
- Never invents service names, tables or flags. Anything unverified is flagged as an assumption to confirm.

## Requirements

- Claude Code with subagents. The planner runs on Opus and sends subagents to Sonnet to keep cost down.
- Tools: Read, Grep, Glob, Bash, Write, Edit, WebFetch, WebSearch, TodoWrite, Agent.
- A git repository, with test commands documented in `CLAUDE.md` so the baseline can run.

## Example

```
Use dev-planning on this ticket:
1234 Add currency validation to checkout
<description and acceptance criteria>
```

## Works well with

Bug Walkthrough, to reproduce the bug before planning or verify the fix afterwards, and PR Code Reviewer once the change is built.

## Install

In Claude Code:

```
/plugin marketplace add AntonBertrand/claude-agents
/plugin install dev-planning@claude-agents
```

Without the plugin system, copy an agent file into `~/.claude/agents/`:

```bash
mkdir -p ~/.claude/agents && curl -fsSL https://raw.githubusercontent.com/AntonBertrand/claude-agents/main/plugins/dev-planning/agents/dev-planning.md -o ~/.claude/agents/dev-planning.md
```
