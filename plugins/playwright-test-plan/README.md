# Playwright Test Plan

Turns a ticket's test plan into local Playwright tests that run in a visible browser, with screenshots and an acceptance-criteria write-up.

## What it does

The automated version of Bug Walkthrough. It turns a ticket's test plan into a Playwright spec that drives the real app in a browser you can watch, takes a screenshot at every milestone, checks the results in the database, and writes each test up with captioned screenshots and an acceptance-criteria coverage table. It is experimental: it says so up front and asks what worked at the end.

## How it works

1. **Investigate and plan.** Runs Bug Walkthrough's investigation, then records a locator for every element a test touches, preferring role and accessible name, then label, then exact visible text, then a stable id. Locators are confirmed against the live page with the Playwright MCP, or by you clicking through `npx playwright codegen`. Each criterion gets a short ref (AC1, AC2, TN1), and it agrees a milestone table with you before writing any code.
2. **Set up a local workspace** in an `e2e/` folder inside the ticket's git-ignored docs folder: only `@playwright/test` installed, a separate login project, one worker, no retries, headed runs slowed down so you can follow them, page objects for each screen, and a `run.json` holding the seeded ids. Nothing is added to the project's own `package.json`, config or CI.
3. **Write the spec.** One test per milestone, named `M<n> <AC ref>: <description>`. Results use soft assertions so one failed check doesn't hide the rest of the evidence. Screenshots wait for the screen to settle, never for a fixed delay, and setup screenshots outline the fields that matter.
4. **Run and record.** You run the first headed run in your own terminal. It then reads every screenshot, checks the database, writes each caption from what the image actually shows, and updates the write-up and coverage table. Later reruns can be headless, and a failing test can be rerun from that milestone onwards.
5. **Finish.** Runs the coverage check, offers to publish the write-up with full-width screenshots, highlight boxes and a "Scripts for QA" tab as a private page, runs the clean-up script, and deletes session files.

In reproduce mode the tests assert the correct behaviour, so a failing check is the bug being shown.

## What it leaves behind

- The spec, page objects and numbered screenshots.
- A write-up for someone who wasn't there: a summary, the starting values side by side, how to read the tests, one entry per test with expected and shown values and a captioned screenshot, and an id table for reviewers.
- The seed and clean-up scripts from Bug Walkthrough.

## Credentials and evidence

- Passwords stay in your shell, entered with `read -s`. They never go into files, `.env`, or printed output.
- Tracing is off for the login step, because a trace records the text typed into fields.
- Saved login state, test results, reports and Playwright MCP snapshots are deleted at the end. Traces and HTML reports are never published.
- Assertions are never weakened to make a test pass. An unexpected result is reported as a result.

## Requirements

- The Bug Walkthrough skill. Installing through the plugin marketplace adds it automatically.
- Node (an LTS release is safest), and Playwright with Chromium, installed locally in the ticket folder.
- Access to the app's database, and the app running somewhere you can reach.
- The Playwright MCP is optional but lets you watch locators being checked.

## Example

```
Write Playwright tests for ticket 1234's test plan
Run the walkthrough for 1234 in a browser
```

## Install

In Claude Code:

```
/plugin marketplace add AntonBertrand/claude-agents
/plugin install playwright-test-plan@claude-agents
```

Without the plugin system, copy the skill folder into `~/.claude/skills/`:

```bash
npx degit --force AntonBertrand/claude-agents/plugins/bug-walkthrough/skills/bug-walkthrough ~/.claude/skills/bug-walkthrough && npx degit --force AntonBertrand/claude-agents/plugins/playwright-test-plan/skills/playwright-test-plan ~/.claude/skills/playwright-test-plan
```
