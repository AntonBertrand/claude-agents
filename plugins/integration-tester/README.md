# Integration Tester

Writes and runs unit or integration tests that follow the project's own conventions, and won't call a build with no test count a pass.

## What it does

Adds, fixes or runs tests the way the project you are in already tests. Projects, even inside one repo, differ in framework version, mocking style, assertion library, whether an integration tier exists and how tests are run, so it works these out from the project instead of guessing from another one.

## How it works

1. **Project and tier.** Takes the project from the path you name or the current directory, and unit or integration from your request. If that is genuinely ambiguous and the two would mean different work, it asks in one line.
2. **Learn the conventions.** Reads the testing notes in `CLAUDE.md` and the README, two or three recent tests of the same tier near the code under test, and the build config that runs them: Maven surefire and failsafe, Gradle test tasks, or the Jest or Vitest config, including any profile a tier needs.
3. **Check the tier exists.** If the project has no integration tier, or nothing wired to run one, it proposes adding it rather than presenting new precedent as the convention.
4. **Write.** Starts from a real test in the project and tells you which file it based the new one on.
5. **Run.** Uses the project's documented command and reports how many tests actually ran.
6. **CI check, when it matters.** Reads the pipeline config if the project's tests don't run in CI, the test needs credentials, an external service or network access, you are adding a module to the pipeline, or something passes locally and fails in CI.

## Checks it applies

- **No false greens.** A build that passes with no test count is treated as a failure to verify. A common case: `mvn verify` runs zero integration tests when failsafe is bound inside a profile that isn't active.
- **Parallel-safe unit tests.** When CI runs tests in parallel, new unit tests avoid mutable static fields, shared fixtures, fixed ports, changing system properties, locale, time zone or the default clock, unclosed static mocks, and any reliance on execution order.
- **Integration test naming.** In Maven, failsafe runs `IT*`, `*IT` and `*ITCase`, and surefire runs `Test*`, `*Test`, `*Tests` and `*TestCase`. A name both claim runs in the wrong phase, and a name neither claims never runs, so it prefers `*IT`.
- **Output over docs.** When a documented command and the real output disagree, it trusts the output and tells you which command worked.

## Requirements

- Works with any stack; most detailed for Maven and JUnit.
- Docker running for integration tests that use Testcontainers.
- Optional per-project notes in `references/<project>.md` inside the skill folder. It loads only the one for the project you are in.

## Example

```
Add an integration test for the order export endpoint
Fix the flaky PricingServiceTest
Why does mvn verify pass but run no tests?
```

## Install

In Claude Code:

```
/plugin marketplace add AntonBertrand/claude-agents
/plugin install integration-tester@claude-agents
```

Without the plugin system, copy the skill folder into `~/.claude/skills/`:

```bash
npx degit --force AntonBertrand/claude-agents/plugins/integration-tester/skills/integration-tester ~/.claude/skills/integration-tester
```
