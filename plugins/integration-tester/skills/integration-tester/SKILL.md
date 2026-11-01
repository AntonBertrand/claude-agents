---
name: integration-tester
description: Write and run unit or integration tests the way the project you are in already tests. Works out its framework version, mocking idiom, assertion library, harness, run command and CI treatment from existing tests and build files rather than guessing by analogy, writes tests that match, confirms they really ran, and checks they will also pass in CI. Use when asked to add, fix or run tests, unit tests, integration tests or ITs.
---

# Testing a project the way it already tests

Projects, even in one repo, differ in test framework major version, mocking idiom, assertion
library, whether an integration tier exists at all, how tests are invoked, and whether CI runs
them. **Do not generalise from one project to another.**

## Step 1: Establish project and tier

**Project**: from the path the user names, the current directory, or by asking.

**Tier**: unit or integration. Usually obvious from the request. If not:

- "test this service/class/function" with mocked collaborators: **unit**
- "test this endpoint end to end", "against the database", "with the real container":
  **integration**
- Genuinely ambiguous, and the two would mean materially different work: ask. One line.

## Step 2: Learn the conventions

- Read the testing section of `CLAUDE.md` and the README, if there is one.
- Find two or three recent tests of the same tier near the code under test. Note the framework
  and its version (from the build file, not the imports alone), class and method naming, the
  mocking idiom, the assertion library, fixture helpers and base classes.
- Read the build config that runs them: surefire and failsafe in Maven, test tasks in Gradle,
  the Jest or Vitest config. Note any profile that has to be active for a tier to run.
- If you keep per-project notes, put them in `references/<project>.md` and read only the one
  for the project you are in.

## Step 3: Check the tier exists

Some projects will not simply accept a new test: no integration tier, no failsafe wiring, no
test convention at all. Where adding one would set new precedent, present it as a proposal,
not as the convention.

## Step 4: Write it

Copy the project's actual conventions: framework version, naming (class **and** method),
mocking idiom, assertion library, fixture helpers. Start from a real test file and name the
file you based it on.

### Unit tests must be concurrency-safe when CI runs them in parallel

Check the CI flags (surefire `parallel` and `threadCount`, Maven `-T`, Gradle
`maxParallelForks`, Jest workers). If classes or methods run concurrently, a new unit test must
not rely on mutable static fields, shared mutable fixtures, fixed ports, mutation of system
properties, `Locale`, `TimeZone` or the default clock, un-closed static mocks, or execution
order.

### Integration tests must be named so the right plugin runs them

In Maven, failsafe picks up `IT*`, `*IT` and `*ITCase`; surefire picks up `Test*`, `*Test`,
`*Tests` and `*TestCase`. A name both claim runs in the wrong phase or twice, and a name
neither claims never runs. Prefer `*IT`.

## Step 5: Run it, and let the output arbitrate

Take the exact command from the project's docs. Several commands report `BUILD SUCCESS` while
running zero tests, for example `mvn verify` when the failsafe plugin is bound inside a profile
that is not active.

Always confirm from the output that tests actually **ran**, and say how many. A passing build
with no test count is a failure to verify, not a pass, and it is the exact symptom of a wrong
invocation.

If a doc's command and the output disagree, trust the output, try the alternative, and say
which one worked. Integration tests that use Testcontainers need Docker running.

## Step 6: CI check, when it matters

Read the pipeline config only when:

- the project's tests are not run in CI, and the user should know what that means;
- the test needs a credential, external service, network egress, or coverage output;
- you are adding a module to the pipeline or changing a template;
- something passes locally and fails in CI, and you need to find the divergence.
