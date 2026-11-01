# PR Code Reviewer

Reviews a branch against its target and returns approve or block, with paste-ready comments that read like a colleague wrote them.

## What it does

Acts as the approver on a pull request. You name the branch and the branch it merges into; it reviews only what the branch adds and answers the question you asked, whether it can be approved, with comments you can paste straight into the PR.

## What you get

A one-line verdict, then the comments in two sections. The format looks like this:

```
VERDICT: BLOCK, 1 mandatory change(s)

## Mandatory before approval

`src/orders/OrderService.java:142`
orderIds can be empty here, and findAllByIds returns everything when it is.

## Recommendations (non-blocking)

`src/orders/OrderMapper.java:31`
Was dropping the null check here deliberate?
```

Empty sections are left out. There is no PR summary, no description of its process and no list of rejected findings. Ask if you want the reasoning behind a comment.

## How it works

1. **Branches.** If either branch is missing or ambiguous, it asks once before doing any work. It fetches, resolves both names to real refs, and never reviews a near-miss.
2. **Scope.** Diffs from the merge-base (`git diff target...source`), reading `--stat` and the commit log first to find where the risk is. For a large diff it tells you which areas it prioritised.
3. **Investigate in parallel.** Sonnet subagents each take one lane: correctness, refactor fidelity (does a consolidated method behave the same for every caller it replaced), callers and blast radius (including reflection, DI wiring and string references), tests, data and queries, and coding standards. Each must report file, line and a concrete failure scenario, or say "no findings".
4. **Adjudicate.** It opens every cited line, walks the failure scenario and checks for guards elsewhere. Anything it can't confirm, anything already prevented, and anything the PR didn't introduce is dropped. Rejecting most leads is normal.
5. **Classify.** Blockers are defects, regressions, weakened or broken tests, and data or security risks. Everything else is a recommendation. If it is unsure, it is a recommendation.

## Coding standards

Reviews against the repo's own standards (`docs/coding-standards.md`, `CONTRIBUTING.md`, or a guide linked from `CLAUDE.md`). Rules the standards mark mandatory, and anything with runtime, data or security risk such as secrets in logs or a rethrow that loses the cause, block. Formatting, naming, missing docs and similar are recommendations. Standards findings only count on lines the PR adds or changes. If the repo has no standards, it says so instead of inventing them.

## How the comments read

Like a colleague wrote them: one or two plain sentences about this specific code, leading with what is wrong and naming the fix when it is obvious. No hedging, no praise before the criticism, no bullets or bold inside a comment, no severity tags, and none of the stock phrases that make review comments easy to ignore.

## Guardrails

Strictly read-only. No edits, commits, pushes, branch switching, or posting comments to the PR. You decide what to post.

## Requirements

- Claude Code with subagents. Runs on Opus with Sonnet subagents.
- Tools: Read, Grep, Glob, Bash, TodoWrite, Agent.
- A git repository with both branches available locally or on `origin`.

## Example

```
Review feature/checkout-validation into main
Is this PR good to approve? fix/rounding into release/2.4
```

## Install

In Claude Code:

```
/plugin marketplace add AntonBertrand/claude-agents
/plugin install pr-codereviewer@claude-agents
```

Without the plugin system, copy an agent file into `~/.claude/agents/`:

```bash
mkdir -p ~/.claude/agents && curl -fsSL https://raw.githubusercontent.com/AntonBertrand/claude-agents/main/plugins/pr-codereviewer/agents/pr-codereviewer.md -o ~/.claude/agents/pr-codereviewer.md
```
