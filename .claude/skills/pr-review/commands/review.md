---
description: Review a pull request for code smells, best practices, test coverage, and scope alignment
argument-hint: [GitHub PR number, URL, commit range, or branch — e.g. "42", "https://github.com/owner/repo/pull/42", "abc123..def456"]
---

@../SKILL.md

Review the following pull request:

$ARGUMENTS

## Execution Steps

### Step 1 — Parse Arguments & Fetch PR

Extract from the arguments:
- **GitHub PR number or URL** — run `gh pr view {number|url} --json number,title,author,headRefName,baseRefName,body,state,url`
- **Commit range** — use directly if in `{sha1}..{sha2}` format
- **Branch name** — resolve via `git log main..{branch} --oneline --no-merges`

Determine the commit range (`{baseRef}..{headRef}`) for the diff commands.

### Step 2 — Read Project Conventions

Read `CLAUDE.md` at the project root before analyzing the diff.

### Step 2b — Fetch Scope

Follow Phase 3b of the SKILL definition:
1. Parse the PR body for scope description or task references (e.g., `T2.1`)
2. If a GitHub issue is linked (`closes #N`), run `gh issue view {N} --json title,body`
3. If no issue and no description scope, find the matching task doc in `docs/implementation_plan/` based on branch name and read its **Goal** and **Deliverables Checklist**
4. Extract expected scope to verify against the diff

### Step 3 — Collect Diff

Follow Phase 2 of the SKILL definition:
1. Run `git log`, `git diff --stat`, `git diff --shortstat` for the commit range
2. Run `git diff` filtered to `*.py`, `*.sql`, `*.yaml`, `*.yml`, `*.toml`, `*.txt`, `*.json`
3. If diff >3000 lines, use stat summaries and read key files selectively

### Step 4 — Analyze & Report

Follow Phases 4–5 of the SKILL definition:
1. Read the full diff carefully
2. Identify: summary, code smells, best-practice alignment, test coverage, security, simpler alternatives, scope coverage
3. Present the review as markdown following the output template — do NOT save to a file
