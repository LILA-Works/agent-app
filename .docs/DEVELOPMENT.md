# Development Guide

## Conventions

### Static Checks

Use the following commands after making changes to make sure there aren't code style errors introduced in the changes.

```bash
make format  # formatting the code to match style guidelines
make typecheck  # make sure there aren't type errors
```

### Coding

- Always use absolute imports.
- Always specify explicit types on function inputs and outputs. See [Typing](#typing) for more information.
- Do not add comments to top of source files.

### Package Organization

- Common commands and scripts should be encapsulated in submodule Makefile.
- Never pin or bound dependency versions in `pyproject.toml`, and rely on uv.lock instead.
- Declare dependencies in the `pyproject.toml` of the package that uses them, not the root.

### Typing

- Be explicit, a reader should never have to guess what a `str` holds. Use alias, e.g. `ID = str`.

### Tests

#### Unit Tests

- Live in `tst/`, and the structure should mirror `src`.
- Name each test case `test_<method>__<should-happen-when-scenario>`, so a failure reads as a sentence.
- Keep each case small and targeted: one scenario, one behavior, a small sets of asserts.
- Structure every case in three sections, marked with `# prepare`, `# act`, `# verify`.
- Group cases by method under test, wrapped in `# region <name>` / `# endregion <name>` markers.
- Shared fixtures go at the top of the file, in its own `# region fixture` section, if the fixtures is only shared in the test file. Fixtures shared across multiple files should be extracted into its own file.

#### Integration Tests

- Live in `integ/`. Should target top-level modules with public APIs (any APIs used by other top-level modules) and exercise code across submodule boundaries.
- Keep integration tests minimal - enough to prove wiring works, but not enough to re-cover unit tested branching.

## Scratchpad

A scratchpad is a space for brainstorming between the developer and the agent. The documents are stored under `.docs/scratchpad`.

Each document should conform to the following rules,

- Name should follow the format `YYYYMMDD-<topic>.md`.
- The title should clearly and concisely reflect the topic.
- The first sentence should be a `Status: ` sentence, using one or two sentences to maintain the latest TL;DR on the topic.
- The first subsection for each scratchpad should contain a `Goal` section, describing the goal of this scratchpad, i.e. what we are hoping to achieve, and when that is achieved, this scratchpad is no longer relevant and can be archived.

Scratchpads are not meant to be long-living documents. Any important decisions coming out of a scratchpad will be recorded manually elsewhere upon archival. DO NOT ATTEMPT TO RECORD ANY DECISIONS ELSEWHERE WITHOUT ASKING FIRST.