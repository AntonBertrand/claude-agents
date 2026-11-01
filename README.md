# claude-agents

Agents and skills I use with Claude Code.

## Agents

| Name | What it does |
|------|--------------|
| [dev-planning](agents/dev-planning.md) | Turns a ticket into an investigated, reviewed implementation plan without writing code |
| [pr-codereviewer](agents/pr-codereviewer.md) | Reviews a branch against its target and returns an approve or block verdict with paste-ready PR comments |

## Skills

| Name | What it does |
|------|--------------|
| [integration-tester](skills/integration-tester/SKILL.md) | Writes and runs tests that follow the project's own conventions, and checks they actually ran |
| [bug-walkthrough](skills/bug-walkthrough/SKILL.md) | Walks you through reproducing a bug or verifying a fix in the real app, one milestone at a time |
| [playwright-test-plan](skills/playwright-test-plan/SKILL.md) | Turns a ticket's test plan into local Playwright tests with screenshots and a write-up (experimental) |
| [team-message-drafting](skills/team-message-drafting/SKILL.md) | Drafts short Slack or Teams messages that read like you wrote them |

## Install

An agent is a single file in `~/.claude/agents/`:

```bash
mkdir -p ~/.claude/agents && curl -fsSL https://raw.githubusercontent.com/AntonBertrand/claude-agents/main/agents/dev-planning.md -o ~/.claude/agents/dev-planning.md
```

A skill is a folder in `~/.claude/skills/`:

```bash
tmp=$(mktemp -d) && git clone -q --depth 1 https://github.com/AntonBertrand/claude-agents "$tmp" && mkdir -p ~/.claude/skills && cp -R "$tmp/skills/bug-walkthrough" ~/.claude/skills/
```

`playwright-test-plan` builds on `bug-walkthrough`, so install both.
