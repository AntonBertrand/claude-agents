# Team Message Drafting

Drafts short Slack or Teams messages that only ask what research can't answer, and checks them for AI tells before you send.

## What it does

Drafts Slack or Teams messages to colleagues that read like you wrote them: short, specific, and only sent when they need to be. It researches before it asks anything, and often concludes that nothing needs sending at all.

## How it works

1. **Reads the whole thread**, up to the latest message, and checks anything new before drafting: a push, a merged PR, a ticket update.
2. **Researches every question first**: the branch your colleague pointed at, git history, infrastructure and pipeline files, vendor and library docs, and decisions already recorded in the repo.
3. **Sorts what is left.** Answered by research: dropped, with the source shown to you. Within your own ticket or branch: your call, not a question. Only the recipient can answer: kept, after checking they are the right person to ask.
4. **Decides what the message should cause.** Leaves out anything that would prompt duplicate work, status they already know, and internal labels from planning docs.
5. **Writes in your voice.** Copies your greeting, capitalisation and sign-off from the thread. Leads with the point, aims for one question, keeps to two or three sentences, and cuts anything over about 80 words.
6. **Checks and presents.** Runs the bundled checker, then shows the draft as plain text you can copy, followed by one line for each thing it left out and the source that settled it.

## Example

A colleague says their branch is untested, then pushes a merge and says to go through the commits. The first instinct is six questions. After research, the latest push answers one, the library docs settle another, three are part of your own ticket, and one is a go-live check rather than a question for this person. What's left:

```
Thanks, I'll branch off yours. I'll be reworking the date parsing into per-locale rules, so shout if you're changing that while you test.
```

## The checker

`scripts/check_message.py` reads a draft and flags:

- em and en dashes, and double hyphens used as dashes
- bold, headings, blockquotes, bullet and numbered lists, and backticks
- more than one exclamation mark
- stock phrases such as "hope this finds you well", "just wanted to reach out", "circle back", "happy to help", "ensure", "leverage", "robust" and "delve"
- drafts over 120 words, or with more than two questions

It exits with an error when it finds something. It can't judge tone, so the skill rereads the draft as the recipient would.

## Requirements

- Python 3 for the checker.
- Works best from inside the repo the conversation is about, so it can check branches and history.

## Example prompts

```
Draft a reply to this thread: <paste>
What should I ask Sam about the release branch?
```

## Install

In Claude Code:

```
/plugin marketplace add AntonBertrand/claude-agents
/plugin install team-message-drafting@claude-agents
```

Without the plugin system, copy the skill folder into `~/.claude/skills/`:

```bash
npx degit --force AntonBertrand/claude-agents/plugins/team-message-drafting/skills/team-message-drafting ~/.claude/skills/team-message-drafting
```
