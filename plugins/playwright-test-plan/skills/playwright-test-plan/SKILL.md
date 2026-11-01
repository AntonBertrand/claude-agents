---
name: playwright-test-plan
description: EXPERIMENTAL. Turn a ticket's test plan (reproduce a bug, or verify a fix) into local, per-ticket Playwright tests that drive the real app in a visible browser, take a screenshot at every milestone, and document each test in the ticket's write-up with captioned screenshots and an acceptance-criteria coverage table. Prepares data with a seed script, learns the UI from the source and the live page, and checks results in the database after each run. Tests stay in the ticket's git-ignored docs folder and are never committed. Use only when the user asks for Playwright or for a ticket's test plan to be automated, e.g. "write Playwright tests for this ticket" or "run the walkthrough in a browser". Not for committed test suites, unit or integration tests (use a testing skill), a manual step-by-step walkthrough (use bug-walkthrough), or a quick look at a change in the browser (use the project's run skill).
---

# Playwright test plan (experimental)

You turn a ticket's test plan into a Playwright spec, run it in a browser the user can watch, and record the
evidence. This skill is **experimental**: say so in your first message, and at the end ask the user what
worked and what did not, then add the lessons to the matching file in `references/`.

It builds on the `bug-walkthrough` skill (its own plugin, installed alongside this one). Read its SKILL.md
and follow its Ground
rules, Phase 1 (Investigate), Phase 3 (Coverage check), "The living write-up" and "Seed and clean-up
scripts". Never edit that skill.

**Overrides of bug-walkthrough for an automated run:**

- Skip its "one milestone per message" rule and its Phase 2. The whole spec runs at once; you report each
  milestone afterwards in its What-this-proves / What-it-showed form.
- Its Phase 1 step 6 list of milestones becomes the plan table below.
- Its Phase 1 step 7 stops once the write-up is created; it does not start milestone 1.
- Screenshot numbering follows its Ground rule, without the 📸 markers.
- The Tests section below replaces its per-milestone entries in the living write-up, and the write-up is
  updated after each run rather than after each milestone.

## Ground rules (in addition to bug-walkthrough's)

- **Local and per ticket.** Everything lives in `<ticket docs folder>/e2e/`. Check it is git-ignored
  (`git check-ignore`) before creating anything. Never add Playwright to the project's own `package.json`,
  configs or CI.
- **Credentials stay in the user's shell.** Test passwords and AWS profiles are set by the user as
  environment variables in their own terminal. Never ask for a password value, never write one to a file
  (no `.env` files), never print environment variables. Saved login state (`.auth/`), `test-results/` and
  `playwright-report/` hold session cookies and are deleted at the end. Never attach or publish a trace or
  the HTML report. Never pass `--trace` on the command line: it overrides the setup project's
  `trace: 'off'`.
- **The user runs headed tests.** A visible browser and the user's credentials live in the user's terminal,
  so give them the exact command to run. You may run headless re-runs yourself, from the `e2e/` folder, with
  `E2E_HEADLESS=true npx playwright test --project=chromium --no-deps` and the non-secret variables set
  inline, while `.auth/` is still valid. A run that lands on the login page means the session expired:
  hand it back to the user.
- **Never weaken an assertion to make a test pass.** If the app does something unexpected, that is a
  result: report it.
- **Playwright MCP output.** The MCP saves page snapshots to `.playwright-mcp/` in the session's working
  folder, which may be inside the repo. Tell the user it is untracked, never commit it, and delete it in
  Phase 5.
- **Database work.** Seed and clean-up writes follow bug-walkthrough's dry-run and commit-switch rules.
  Everything else you do in the database is read-only and done by you between runs. Test code holds no
  database credentials.

## Phase 1: Investigate and plan

Do bug-walkthrough's Phase 1 (with the overrides above). Then, for this skill:

1. **Learn the UI for automation.** For every element a test touches, record a locator, preferring in
   order: `getByRole` with an accessible name, `getByLabel`, `getByText` with exact visible text, then a
   stable id. Avoid generated ids, positions (`nth`), and minified class names. Confirm each locator against
   the live page with the Playwright MCP if it is available (it shows a visible browser, so tell the user
   they can watch). Otherwise have the user run `npx playwright codegen <base URL>` and click through: it
   records locators in a window they can watch. Use the source templates to resolve labels. Note custom
   labels per tenant: the locator must use the label the test tenant actually shows.
2. **Number the criteria.** Give each acceptance criterion a short ref (AC1, AC2, ...) and each testing note
   one too (TN, or TN1, TN2). Every test names exactly which ref it covers, in its name and in the write-up;
   a test that only shows a negative case or a variation of an AC still names that AC.
3. **Plan the setup evidence.** Readers need to see the starting values before they can judge a result.
   Plan read-only capture tests (`evidence.spec.ts`) that screenshot each setting the plan depends on (for
   example account-level defaults and each user's own defaults), with the relevant fields outlined.
4. **Plan the spec.** One spec per test plan, one test per milestone. Show the user a table before writing
   any code:

   | Milestone | What it does | What it proves | AC ref |
   |---|---|---|---|

   "What it proves" is one plain sentence. Wait for the user to agree, or adjust.

## Phase 2: Set up the workspace

In `<ticket docs folder>/e2e/`:

- `package.json` with only `@playwright/test`. Install with `npm install -D -E @playwright/test@<version>`
  (match the version another project in the repo already uses, if any), then `npx playwright install
  chromium`. The browser goes to the user's Playwright cache, outside the repo. Specs are `.ts` and need no
  tsconfig. If the installed Node misbehaves, use an LTS Node. Say these are local-only packages.
- `playwright.config.ts`:
  - `baseURL` from `E2E_BASE_URL`;
  - two projects: `setup` (`testMatch: /auth\.setup\.ts/`, `use: { trace: 'off' }`) and `chromium`
    (`dependencies: ['setup']`);
  - `workers: 1`, `fullyParallel: false`, `retries: 0`, because the tests share data and run in order;
  - `use.headless` from `E2E_HEADLESS` (default false), `launchOptions.slowMo` from `E2E_SLOWMO` (default 400);
  - `trace: 'on'` when headless, `'retain-on-failure'` when headed; `screenshot: 'only-on-failure'`;
  - `timeout: 10 * 60_000`, `expect: { timeout: 15_000 }`, and under `use`, `actionTimeout: 15_000` and
    `navigationTimeout: 30_000`;
  - reporters `list`, `['html', { open: 'never' }]` and `['json', { outputFile: 'results/last-run.json' }]`.
- `.gitignore` covering `node_modules/`, `.auth/`, `test-results/`, `playwright-report/`, `results/`, as a
  second guard.
- `pages/`: small page objects holding the locators from Phase 1, one file per screen.
- `auth.setup.ts`: logs in once per role from `E2E_USER_<ROLE>` and `E2E_PASSWORD_<ROLE>` and saves
  `.auth/<role>.json`. Tracing is off in the setup project because a trace records the value passed to
  `fill()`, including the password. Tests pick a role with `test.use({ storageState: '.auth/<role>.json' })`
  per describe; a test that switches user opens `browser.newContext({ storageState })`.
- `run.json`: the ids and run marker for the current run, written by you from the seed's final SELECT (see
  Phase 4). The spec reads it; it never hard-codes ids. Never rewrite it while the user's run is in progress.
- `steps/` or helpers for anything the UI cannot trigger: shell out to the ticket's driver with
  `execFileSync(process.execPath, [driver, ...args], { cwd: <repro folder>, env, timeout: 120_000,
  encoding: 'utf8' })`, where `env` is `process.env` without the `E2E_PASSWORD_*` variables. The driver's own npm installs live in its folder. Check its
  output for the expected transaction id, and attach the output only if it holds no secret values.

## Phase 3: Write the spec

- A plain `test.describe` (not `.serial`), one `test` per milestone named `M<n> <AC ref>: <short description>`,
  using `test.step` for the actions inside it. `workers: 1` and `fullyParallel: false` already keep the
  order. Do not use serial mode: a soft assertion failure still fails the test, and serial mode then skips
  every later test, hiding the rest of the evidence. Each test starts on a fresh page, so it navigates to
  its own screen. Data created earlier is found by its marker, not by page state.
- For custom widgets (dropdowns, date pickers), assert on the element that holds the displayed value, not
  the whole widget: widget text often includes hidden icon labels.
- Build every file path (`.auth/`, `screenshots/`, `run.json`) from `__dirname`, not the working directory.
- Each test: act through page objects and wait on a visible outcome, never on fixed timeouts. Then, in this
  order:
  1. take the milestone screenshot to `screenshots/<NN>-<short-name>.png` and attach it to the report with a
     draft caption as its title (`testInfo.attach(caption, { path })`). The draft says what the screenshot
     is meant to show; the final caption is written after you have looked at the image (Phase 4);
  2. assert the AC values with `expect.soft`, so the milestone records everything it saw even when a check
     fails. Keep hard `expect` for navigation and set-up only, where carrying on is meaningless.
- Before any screenshot, wait for the screen to settle: animated panels (fades, expanding tabs) must have
  finished, or the image shows a half-drawn page. Wait on the panel's computed opacity and size, not on a
  fixed delay. In capture tests, outline the fields that matter (a yellow `outline` set from the page)
  so readers see at a glance what to look at.
- **In reproduce mode, assert the correct behaviour.** A failing AC check is the bug being shown and is
  reported as Proven; a passing one means the bug did not reproduce.
- Keep the spec free of explanatory comments: the test names and the write-up are the documentation.
- Assert what the AC is about (the field values, the prompt and its buttons, what was imported), using the
  expected values from the plan table. Do not assert incidental layout.
- Read back the spec in two lines per test before the first run: what it does, what it checks.

## Phase 4: Run and record

0. **Before every full run:** run the seed (dry run, then its commit switch) and confirm its ids. Write them and a
   fresh run marker to `run.json`. Each run uses a fresh marker (e.g. a description suffix `-r<n>`) and a
   fresh driver transaction id, so text locators never match rows from an earlier run.
1. **First run, headed and slowed down**, run by the user in their own terminal:
   ```
   cd <ticket docs folder>/e2e
   read -s "E2E_PASSWORD_<ROLE>?Password for <role>: " && export E2E_PASSWORD_<ROLE>; echo
   export E2E_BASE_URL=... E2E_USER_<ROLE>=...
   npx playwright test
   ```
   `read -s` keeps the password out of shell history (that form is zsh; in bash use
   `read -s -p "Password for <role>: " E2E_PASSWORD_<ROLE> && export E2E_PASSWORD_<ROLE>; echo`). Tell them what they should see in the
   browser, test by test, in two or three lines, and that they only need to say "done" afterwards.
2. **After the run**, read `results/last-run.json` for the counts, each test's status and any errors, then
   for each milestone:
   - read its screenshot yourself, and check the result in the database;
   - give **What it showed** in a short paragraph or bullets, tied to the AC, saying plainly whether it
     passed, failed, or only partly proved the AC;
   - write the final caption for each screenshot from what the image actually shows (see "Documenting
     the tests"), and correct the draft if they differ;
   - update the living write-up: result, ids, screenshots with captions, and the AC coverage table.
   Report how many tests actually ran. A green run with no test count is not a pass.
3. **When a test fails**, open its trace, or give the user a command to rerun with `--ui` (leave the setup
   project unticked; `.auth/` must be valid, otherwise do a normal headed run first) or
   `--debug --project=chromium --no-deps`. Both need a screen, so the user runs them. Decide whether it is
   the test (locator, timing, data) or the app. If it is the test, fix it and rerun from that milestone with
   `--grep` matching it and later ones (e.g. `-g "M([3-9]|1[0-9]) "`), keeping the same `run.json` and
   marker, unless the failed milestone consumed or changed the seeded data: then re-seed and run in full.
   If it is the app, stop and report.
4. **Later re-runs** (after a code change, or to re-check the fix): re-seed per step 0, then headless. The
   user runs `E2E_HEADLESS=true npx playwright test`; you run the form in the Ground rules. Replay with
   `npx playwright show-trace test-results/<test folder>/trace.zip`, or `npx playwright show-report` for
   the HTML report. `test-results/` is wiped at the start of every run, and `screenshots/` is overwritten,
   so the write-up always shows the latest run. After a `--grep` rerun, earlier screenshots are from the
   previous run; say so in their entries.

## Documenting the tests

Write for a reader who was not in the session and does not know the data: plain names, never database ids
or internal markers, in the main text.

1. **Summary:** what was wrong and what the fix does (two short paragraphs), then the AC table with refs.
2. **Before the tests:** a table of the starting values that matter (for example account default vs each
   user's own default, side by side) and the setup screenshots from the evidence tests. Every expected value
   later is one of these names.
3. **How to read the tests:** one short box explaining the label each test transaction carries (e.g.
   "E2E r2 M1 = run 2, test 1"), the highlight boxes, and any fixture (such as an order with special header
   values) the reader must know about.
4. **One entry per test**, in this shape:

```
### Test 4 (AC2): on an order with a delivery address saved on its header, Yes only changes the address

Covers AC2: the line item keeps the buyer's default warehouse and takes the address from the order header.

<one line on why this case matters>

**What we did**
1. Added another item to Order 2 as the buyer.
2. Answered Yes to "Use the order's delivery address?".

**What you should see**

| Field | Expected | Why | Shown |
|---|---|---|---|
| Warehouse | Test Warehouse B | buyer's default, kept | Test Warehouse B |
| Delivery address | Test Office North | from the order header, because of Yes | Test Office North |

![Test 4, after Yes](e2e/screenshots/05-header-prompt-yes-item.png)
*Order 2, after Yes. Warehouse Test Warehouse B is still the buyer's. Delivery address changed to
Test Office North, from the order header.*
```

5. **How it was tested:** what ran, what was stubbed and why it does not matter, any earlier failed run in one
   line, and how test data is cleaned up.
6. **Database check, for reviewers:** a collapsed or final table of record ids and value ids, with a key from
   id to name. This is the only place ids appear.

Captions:

- One or two plain sentences: which screen, the values that matter by name, and what that shows for the AC.
- Describe what is in the image, not what was expected. If they differ, the caption says so and the test
  is not a pass.
- Refer to the test transaction as "the new transaction" and give its label once, so readers can find it.
- Use relative paths so the doc renders from the docs folder. Never caption with data from outside the test
  tenant.

Keep entries in milestone order, mark skipped ones as skipped with the reason, and keep the latest run's
result (note earlier failed runs in one line if they taught something).

## Phase 5: Finish

- Run the coverage check from bug-walkthrough Phase 3.
- Offer to publish the write-up with its screenshots as a private Artifact if the user wants to share it.
  Screenshots must come from test tenants only; traces and the HTML report are never published. The page:
  - follows "Documenting the tests" and the user's brand or design system, if any;
  - shows every screenshot full width (side by side is too small to read) and overlays yellow highlight
    boxes on the fields that matter, positioned in percentages of the image; clicking a screenshot opens it
    full size;
  - has a second tab, **Scripts for QA**, with the seed, run-prep, clean-up and driver scripts, each with a
    one-line purpose, how to run it, and a copy button. Before publishing them, remove machine-specific paths
    (resolve paths relative to the script) and check they hold no secret values;
  - sets `[hidden] { display: none !important; }` itself, since its own layout rules can otherwise override
    the `hidden` attribute used by the tabs.
  Render it once locally before publishing to check the highlight boxes land on the right fields and the
  tabs switch. Keep the Markdown write-up in step with the page.
- Run the clean-up script (dry run first, then its commit switch on the user's go-ahead). Write its deletes
  as `DELETE ... WHERE id IN (...)`: some database tools refuse `DELETE ... JOIN` without a `WHERE`. Delete
  `.auth/`, `test-results/`, `playwright-report/`, `results/` and the MCP's `.playwright-mcp/` folder. Keep
  the screenshots the write-up links to.
- Ask what to change in this skill, and record lessons in `references/`.

## Project notes

Keep project-specific notes (how to log in locally, where ticket docs live, database quirks) in
`references/<project>.md`, and load only the one for the project you are in.
