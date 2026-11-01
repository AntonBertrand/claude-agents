# claude-agents

Agents and skills I use with Claude Code.

## Agents

| Name | What it does |
|------|--------------|
| [dev-planning](plugins/dev-planning/agents/dev-planning.md) | Turns a ticket into an investigated, reviewed implementation plan without writing code |
| [pr-codereviewer](plugins/pr-codereviewer/agents/pr-codereviewer.md) | Reviews a branch against its target and returns an approve or block verdict with paste-ready PR comments |

## Skills

| Name | What it does |
|------|--------------|
| [integration-tester](plugins/integration-tester/skills/integration-tester/SKILL.md) | Writes and runs tests that follow the project's own conventions, and checks they actually ran |
| [bug-walkthrough](plugins/bug-walkthrough/skills/bug-walkthrough/SKILL.md) | Walks you through reproducing a bug or verifying a fix in the real app, one milestone at a time |
| [playwright-test-plan](plugins/playwright-test-plan/skills/playwright-test-plan/SKILL.md) | Turns a ticket's test plan into local Playwright tests with screenshots and a write-up (experimental) |
| [team-message-drafting](plugins/team-message-drafting/skills/team-message-drafting/SKILL.md) | Drafts short Slack or Teams messages that read like you wrote them |

## Install

In Claude Code, add the marketplace once:

```
/plugin marketplace add AntonBertrand/claude-agents
```

Then install whatever you want by name:

```
/plugin install team-message-drafting@claude-agents
```

`playwright-test-plan` depends on `bug-walkthrough`, which is installed with it. Run `/plugin marketplace update claude-agents` to pick up changes.

### Without the plugin system

Copy a skill folder into `~/.claude/skills/`:

```bash
npx degit AntonBertrand/claude-agents/plugins/bug-walkthrough/skills/bug-walkthrough ~/.claude/skills/bug-walkthrough
```

Or an agent file into `~/.claude/agents/`:

```bash
mkdir -p ~/.claude/agents && curl -fsSL https://raw.githubusercontent.com/AntonBertrand/claude-agents/main/plugins/dev-planning/agents/dev-planning.md -o ~/.claude/agents/dev-planning.md
```
