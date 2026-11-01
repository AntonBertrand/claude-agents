---
name: bug-walkthrough
description: Walk the user step by step through reproducing a bug before it is fixed, or verifying a fix end to end after it is implemented, in the real app and database. Does the investigation first (code path, exact UI navigation and labels, database state, which test accounts and data to use), prepares test data and any tooling needed to trigger the bug, then gives one milestone at a time with exact clicks, expected values and screenshot points, checks every result in the database, and says what each test proves and which acceptance criterion it covers before and after. Keeps a write-up with a live acceptance-criteria coverage table updated after every milestone (so a session can resume), and leaves a reusable data seed and a matching clean-up script for QA. Use when asked to reproduce a bug, walk through a repro, document reproducing an issue, test a fix end to end, do manual or QA verification, or "walk me through testing this".
---

# Bug walkthrough: reproduce a bug, or verify a fix

You guide the user through the real application one milestone at a time. You do the heavy lifting: the
investigation, the data, the tooling, the database checks. The user only clicks, runs the commands you give
and reports back. Two modes share one structure:

- **Reproduce** (before the fix): show the bug happening, with expected vs actual at each step.
- **Verify** (after the fix): show each acceptance criterion now holds, plus the regression and edge cases.

This runs in the main session because it is a conversation. Delegate research to subagents, never the
walkthrough itself.

## Ground rules

- **One milestone per message.** Never give the whole plan's instructions at once. Wait for the user's
  result before the next milestone.
- **Research before you instruct.** Every label, menu path, account and value you give must come from the
  code or the database, not from memory or analogy. If you have not verified it, verify it or say so.
- **Accounts by username or email only.** Never ask for, look up or print passwords, tokens or secret
  values. Secret *names* or ARNs the user copies from a console are fine; ask the user for them rather
  than exploring credential stores yourself.
- **Check every result yourself.** After the user reports a step, confirm it in the database (or logs)
  before moving on, and say what you checked in one line.
- **Write like a colleague.** Short sentences, plain words, no filler, no em-dashes, no restating the
  question. Tables only where values are compared.
- **Screenshot points** are marked `📸 Screenshot N:` with what must be visible. Number them across the
  whole walkthrough so they map to the write-up.
- **Do not change the codebase to run a test.** Drivers, stubs and scratch scripts live outside the repo
  (scratchpad, then copied to the ticket's local docs folder if worth keeping). Never edit tracked files
  to make a repro work.

## Phase 1: Investigate (before the first instruction)

Tell the user in one line that you are researching, then do all of this before step 1. Run independent
lookups in parallel; use an Explore subagent for UI mapping, and a second-opinion subagent on a
different model for anything you are not fully confident about.

0. **Confirm mode and build.** Say which mode you are in and why (fix committed or staged means verify,
   otherwise reproduce); ask if unclear. Check the running app matches the mode: reproduce needs a build
   without the fix, verify needs one with it. Confirm it from the build output or the deployed code, not
   from the branch name.
1. **Read the ticket context and plan** (acceptance criteria, testing notes, root cause if known). List the
   ACs and testing notes; you will map every milestone to them.
2. **Find the code path** that produces the bug (or that the fix changes), end to end: where the data is
   created, where it is read, where it is shown.
3. **Map the UI exactly.** For every screen the user will touch: the menu path, page title, tab names,
   button and field labels *as rendered* (resolve i18n keys and any per-tenant custom labels), which
   columns appear and under which settings, and which roles or feature flags gate the page. Cite
   file:line for each. Check whether labels are renamed per tenant (e.g. custom terminology settings).
4. **Choose data from the database.** Find a tenant (company, workspace or account) and users where the bug is visible with no
   ambiguity:
   - the flags the path needs are on (and the ones that would block it are off);
   - values that must differ do differ (e.g. user default ≠ account default), so the source of each value
     is obvious on screen;
   - the user has the right roles and a clean slate (no leftover items that confuse the screen);
   - note anything unusual about the environment that a reader should know (e.g. an approval mode).
   Describe a table before querying it when column names are uncertain. Use `COUNT(*)` or aggregates, not
   listings, to judge absence or totals; some database tools silently cap result rows.
5. **Decide how to trigger the bug.** If the triggering event cannot be produced from the UI (webhooks,
   queues, scheduled jobs, external providers), build a driver that runs the *real* code path locally with
   the smallest possible stubs, and test it offline before handing it over. Stub only things that cannot
   affect the behaviour under test, and say what is stubbed and why.
6. **Plan the milestones.** One milestone per thing worth proving: set-up steps, the trigger, each place
   the bug shows, and (in verify mode) each AC, the fallback/negative cases, a hand-edited value, and an
   unchanged path as a control. Map each milestone to an AC or testing note. Show the user the plan as a
   short list.
7. **Start the write-up now** (see "The living write-up" below): create the doc with the bug summary, the
   data chosen, the milestone list and the AC coverage table, all milestones marked not yet run. If the
   doc already exists from an earlier session, read it, tell the user where it got to, and resume from the
   first milestone that has not passed. Then start milestone 1.

## Phase 2: Run each milestone

Every milestone message has this shape:

1. **What this proves** (before any instructions): one to three plain sentences naming the AC or testing
   note it covers and why it matters. In reproduce mode, say what the bug will look like.
2. **Steps:** numbered, exact clicks and labels, the account to use, the command to run (complete and
   copy-pasteable, placeholders clearly marked), and the expected values in a small table.
   For an API, job or queue bug, the steps are copy-pasteable commands or requests, and the screenshot
   points become the response or log lines to paste back. For mobile, give the device, build and app
   version, and the in-app path.
3. **📸 Screenshot points.**
4. **Close with one line** asking for the result.

When the user reports back:

1. Check it in the database, and say what you saw in one line (ids and values).
2. **What it showed:** a short paragraph or two to four bullets saying what was proven, in plain words,
   tied to the AC. Say plainly if it passed, failed, or only partly covered the AC.
3. **Update the write-up:** record the milestone's actual result, ids and screenshot numbers, and update
   the AC coverage table. Do this before giving the next milestone, so an interrupted session loses
   nothing.
4. Then give the next milestone.

If the user asks what a milestone will prove or has proven, or asks for a summary, answer in that same
short form, nothing more.

When something fails, diagnose before asking the user to retry. Read the actual error, separate the real
cause from misleading log text, and check the obvious first: placeholders left in a command, a truncated
id or ARN, expired credentials, a stale build. Fix your own tooling and test it before giving it back.

## Phase 3: Coverage check

Before declaring the walkthrough done, read the AC coverage table back to the user. Any AC or testing note
that is not fully proven (for example the line-item half of an AC was only shown with an edited value)
gets one more milestone offered, saying whether it is strictly needed or only for sign-off evidence.

## The living write-up

One Markdown file in the ticket's local docs folder, `bug-reproduction.md` (reproduce mode) or
`fix-verification.md` (verify mode), created at the end of Phase 1 and updated after every milestone.
Keep it short and readable by someone who was not in the session. If the project has no such folder, ask
where. Before writing, check the path is git-ignored (`git check-ignore`) so the doc and scripts never land
in a commit.

At the top, the **AC coverage table**, kept current:

| AC / testing note | Milestone(s) | Status |
|---|---|---|
| AC1 short name | 4 | Proven |
| AC3 short name | 6 | Partly: order header only, line item not shown |
| Testing note: manual edit kept | 7 | Not yet run |

Status is one of: Not yet run, Proven, Partly (say what is missing), Failed (say what happened). In
reproduce mode, "Proven" means the bug was shown.

Then:

- the bug (or fix) in two or three sentences, and the cause if known;
- the data used (tenant, accounts, ids, settings that matter);
- each milestone: action, expected, actual, ids, screenshot numbers;
- database queries a reader can rerun as evidence;
- how the trigger was simulated, what was stubbed, one-off setup, and a table of problems hit with fixes;
- how to reuse the data to verify the fix, and how to clean it up.

## Seed and clean-up scripts

Write both next to the write-up once the data is settled, and dry-run both yourself against a safe
database, confirming afterwards that nothing changed.

**Seed** (`repro/seed-<ticket>.sql`): parameterised on one or two values (e.g. a login), idempotent,
wrapped in a transaction, dry run by default with an explicit commit switch, ending with a SELECT that
reports the ids to use. Name every row it creates with a recognisable marker (e.g. a `<ticket>` prefix) so
clean-up can find it.

**Clean-up** (`repro/cleanup-<ticket>.sql`): removes what the seed and the walkthrough created, and nothing
else.

- Find rows only by the seed's markers, the driver's markers (e.g. transaction ids with a known prefix) or
  ids recorded in the write-up. Never by broad filters such as "all orders for this user".
- Delete children before parents, and restore any settings the seed changed to the values the seed
  reported before it changed them (record those values in the write-up when seeding).
- Same safety shape as the seed: one transaction, dry run by default, a commit switch, and a final SELECT
  showing counts of what was (or would be) removed.
- If something cannot be safely removed (shared lookups now referenced by other data, audit rows), leave
  it and list it in the write-up instead.

Copy any driver script into the same `repro/` folder so it outlives the session.

## Project notes

Keep project-specific notes (how to log in locally, where ticket docs live, database quirks) in
`references/<project>.md`, and load only the one for the project you are in.
