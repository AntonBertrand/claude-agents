# Bug Walkthrough

Guides you through reproducing a bug or verifying a fix in the real app, one milestone at a time, checking each result in the database.

## What it does

Guides you through the real application one milestone at a time, in one of two modes:

- **Reproduce**, before a fix: shows the bug happening, with expected and actual values at each step.
- **Verify**, after a fix: proves each acceptance criterion, plus regression, fallback and edge cases and an unchanged path as a control.

You click and report back. It does the investigation, prepares the data and tooling, and checks every result in the database itself.

## Before the first step

- Confirms the mode, and that the running build matches it (reproduce needs a build without the fix, verify needs one with it), from the build output rather than the branch name.
- Lists the acceptance criteria and testing notes from the ticket and plan.
- Traces the code path end to end: where the data is created, read and shown.
- Maps every screen you will touch: menu path, page title, tabs, and button and field labels as they actually render (resolving translation keys and per-tenant custom labels), plus the roles and feature flags that gate them, with file and line references.
- Picks accounts and data from the database where the bug is unambiguous: the right flags on, values that visibly differ so you can tell where each one came from, and no leftover records to confuse the screen.
- If the trigger can't come from the UI (webhooks, queues, scheduled jobs, external providers), builds a small driver that runs the real code path with the fewest possible stubs, and tests it before handing it to you.
- Shows you the milestone plan, each milestone mapped to a criterion.

## Each milestone

1. **What this proves**: which criterion it covers and why it matters.
2. **Steps**: exact clicks and labels, which account to use, complete copy-paste commands, and the expected values.
3. **Screenshot points**, numbered across the whole walkthrough.

When you report back, it confirms the result in the database, says plainly whether the milestone passed, failed or only partly proved its criterion, and updates the write-up before giving you the next one. If something fails, it diagnoses the real cause before asking you to retry.

## What it leaves behind

In the ticket's git-ignored docs folder:

- **`bug-reproduction.md`** or **`fix-verification.md`**, with a coverage table (Not yet run, Proven, Partly, Failed) updated after every milestone, so an interrupted session can pick up where it stopped.
- **`repro/seed-<ticket>.sql`**: parameterised, idempotent and transactional, a dry run by default with an explicit commit switch, and every row it creates marked so it can be found later.
- **`repro/cleanup-<ticket>.sql`**: removes only what the seed and the walkthrough created, children before parents, restores any settings the seed changed, with the same dry-run safety.
- Any driver script used to trigger the bug.

## Guardrails

- One milestone per message. Every label, account and value comes from the code or the database, not from memory.
- Never asks for, looks up or prints passwords, tokens or secret values.
- Never edits tracked files to make a repro work.
- Uses counts rather than listings to judge totals, because some database tools silently cap result rows.
- Before finishing, reads the coverage table back and offers one more milestone for anything not fully proven.

## Requirements

- Claude Code with access to the app's database, through an MCP server or a command-line client.
- The app running locally or in a test environment.
- Optional per-project notes (how to log in, where ticket docs live, database quirks) in `references/<project>.md`.

## Example

```
Walk me through reproducing ticket 1234
Verify the fix for 1234 end to end
```

## Works well with

Playwright Test Plan, which automates the same walkthrough in a browser, and Dev Planning, whose plan supplies the acceptance criteria.

## Install

In Claude Code:

```
/plugin marketplace add AntonBertrand/claude-agents
/plugin install bug-walkthrough@claude-agents
```

Without the plugin system, copy the skill folder into `~/.claude/skills/`:

```bash
npx degit --force AntonBertrand/claude-agents/plugins/bug-walkthrough/skills/bug-walkthrough ~/.claude/skills/bug-walkthrough
```
