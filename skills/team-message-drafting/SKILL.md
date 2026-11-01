---
name: team-message-drafting
description: Draft Slack or Teams messages to colleagues that read as if a person wrote them, short and plain, carrying only what the recipient needs, and asking only questions that research cannot answer. Use whenever the user asks to draft, write, reword or reply to a message, DM, thread reply or chat to a team member, manager, reviewer or another team ("draft a Slack to X", "what should I ask Y", "reply to this thread", "message the team about Z"), and whenever a pasted Slack or Teams conversation needs a response, even if the user doesn't say "draft".
---

# Drafting messages to team members

The user sends these messages under their own name to people they work with every day. A message that is long, over-formatted or full of questions costs the recipient time and makes the sender look like they did not do their homework. One that reads as AI-written costs the sender credibility. The goal is the message the user would write themselves on a good day: short, specific, and only sent because it needs to be.

## 1. Read the whole thread first

Read every message in the conversation the user pasted, up to the latest one. People answer things between drafts: a colleague may already have pushed a fix, answered the question, or said how they want to work ("go through the commits and ask if anything comes up"). A draft that ignores the latest message reads as if the sender wasn't listening.

If new information has arrived (a push, a merged PR, a ticket update), check it before drafting. In a git repo that means a fetch and a look at the new commits.

## 2. Research every question before asking it

List every question you think the message needs. Then try to answer each one yourself before it goes anywhere near the draft. Most questions to a colleague can be settled in a few minutes:

- **Code and config:** grep the branch they pointed at, not just the local checkout. Does the thing exist, what is it called, what does it do today?
- **Git history:** `git fetch`, `git log`, `git merge-base`. Is it merged, who changed it, what is the branch based on?
- **Infrastructure and secrets layout:** templates, CloudFormation, pipeline files. The names and shapes are usually there.
- **Vendor and library docs:** API limits, field formats, endpoints. Search the official docs and quote them.
- **Tickets, plans and docs in the repo** that already record a decision.

Then sort what's left:

- **Answered by research:** drop it. Mention the finding to the user, with its source, so they can trust the decision.
- **Within the user's own scope:** don't ask permission to do your own job. If the ticket the user owns covers it, or it is a small change on their branch, it's a decision for the user, not a question for the colleague.
- **Only the recipient can answer** (their intentions, unpushed work, a call that is theirs to make, something behind access the user lacks): keep it. Check they're actually the right person to answer it. If the question belongs to someone else (a vendor contact, a product owner), say so to the user rather than sending it to whoever is handy.

Often nothing is left, and the right answer is "you don't need to send anything", or a one-line acknowledgement. Say so plainly; don't manufacture a message.

## 3. Decide what the message should cause

Before writing, ask what the recipient will do after reading it. Every sentence should either give them something they need or ask something only they can answer.

Leave out anything that would prompt them to do work the user is already doing. Telling a colleague about a bug in their code that the user is fixing on their own branch invites them to fix it too, and now it is fixed twice and conflicts. Flag it in the PR instead, or when the work is ready for review, unless they need to know now.

Leave out status the recipient already knows, internal labels from planning docs (C-1, OQ-3, step numbers), and the user's reasoning unless the recipient needs it to answer.

## 4. Write it like a colleague

Match the sender. Read the user's own messages in the thread and copy their register: greeting, capitalisation, punctuation, sign-off or none. If they write "Hey morning, ...", don't open with "Hi Sam, I hope you're well."

- Lead with the point. The ask or the news goes in the first sentence or two.
- One topic per message where possible, and ideally at most one question. If two questions are genuinely both needed, write them as two plain sentences, not a numbered list.
- Plain sentences and short paragraphs. Two or three sentences is normal for Slack. Over about 80 words, cut.
- Be specific where it saves them looking things up (a branch name, a test name, a ticket number they use), and nowhere else. Don't paste SHAs, file paths or line numbers unless they need them to act.
- Name things the way the team names them.

### Formatting

No em dashes or en dashes; use a comma, a full stop or brackets. No headers, bold, italics, bullet or numbered lists, or blockquotes. No backticks either: the user copies the draft from rendered text, so code formatting doesn't survive the paste, and Slack messages between colleagues rarely use it. Emoji only if the user uses them in the thread.

### Phrases that read as AI-written

Avoid these and their cousins: "I hope this message finds you well", "Just wanted to reach out", "Quick question", "I wanted to touch base / circle back", "Great question", "Happy to help", "Thanks in advance!", "Let me know if you have any questions or concerns", "Please don't hesitate", "a few things to flag", "To summarise", "ensure", "leverage", "streamline", "robust", "seamless", "delve". Also avoid lists of three for rhythm, sentences that restate the previous one, and closing offers nobody asked for. Use exclamation marks only if the sender does.

## 5. Check and present

Run the bundled checker on the draft before showing it:

```bash
python3 <skill-dir>/scripts/check_message.py <<'EOF'
<draft text>
EOF
```

It flags dashes, markdown, numbered lists and stock AI phrases. Fix anything it reports. It can't judge tone or relevance, so reread the draft as the recipient would.

Present the draft as plain paragraphs in your reply, not inside a blockquote or a code fence (a blockquote renders as a bar in the terminal and breaks copy-paste). Then, briefly, list what you left out and why, one line each with the source that settled it, so the user can see the research without it being in the message. If nothing needs sending, say that instead of a draft.

## Example

The user pastes a thread where a colleague says their branch is untested, then pushes a merge of the main feature branch and says "best thing is to go through the commits". The first instinct is six numbered questions: is he reworking the date parser, is the timezone handling intended, will he add the new locale to the config, where do the staging keys live, is there a separate sandbox host, how will the branches merge.

After research: the latest push answers the merge question. The library docs settle the timezone behaviour. The locale, the keys and the parser rework are all in the user's own ticket, so the user just does them. The sandbox host is a go-live check in a console, not a question for this colleague. And raising the timezone bug would only prompt him to fix it on his branch too.

What's left is nothing, or at most:

Thanks, I'll branch off yours. I'll be reworking the date parsing into per-locale rules, so shout if you're changing that while you test.
