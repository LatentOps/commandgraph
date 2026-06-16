# CommandGraph Plan

CommandGraph is the open-source terminal intelligence module for LatentOps.

It is not the enterprise LatentOps product. The open-source scope should stay local-first, lightweight, explainable, and useful to developers without requiring a cloud account or managed policy system.

## Positioning

CommandGraph starts as a semantic upgrade to `apropos`:

- Users describe what they want in natural language.
- CommandGraph maps that intent to relevant commands, flags, examples, and risks.
- It can also review proposed shell commands before humans or AI agents run them.

The larger idea:

> Intent-aware command discovery and command safety for humans and AI agents.

This gives LatentOps an open-source wedge without open-sourcing the enterprise runtime control product.

## What Stays Open Source

Open-source CommandGraph should include:

- Semantic command search.
- Local command graph data.
- Command examples and safe usage notes.
- Basic risk labels.
- Basic command review API and CLI.
- Local-first indexing from curated data and eventually local man pages.
- Agent-friendly JSON output.
- Test fixtures and benchmarks for command search and risk review.

## Product Boundary

CommandGraph open source:

- Understands terminal command intent.
- Finds useful commands.
- Explains command risks.
- Gives local safety review for shell commands.
- Provides a clean integration surface for agents.

CommandGraph should be useful on its own while keeping a clean integration path for broader LatentOps workflows later.

## Level 1: Semantic Apropos

Goal:

Help developers find commands even when they do not know the command name.

Examples:

- `make file runnable` -> `chmod`
- `what is using port 3000` -> `lsof`, `ss`, `fuser`
- `show biggest folders` -> `du`
- `undo last git commit but keep changes` -> `git reset --soft`

Implementation:

- Hybrid keyword and semantic search.
- Synonym graph.
- Command popularity boost.
- Exact command-name and alias boost.
- Weak-term filtering for words like `is`, `the`, `to`, `for`.
- Curated command cards in JSON.
- Deterministic scoring before adding heavier ML.

Do not use RL here. This is a retrieval and ranking problem.

## Level 2: Command Graph

Goal:

Move from command search to task understanding.

Data model:

- intent
- command
- flags
- examples
- slots
- risks
- safe order
- related commands
- recovery notes

Example skill:

```yaml
intent: debug_port_conflict
queries:
  - what is using port
  - address already in use
  - port already busy
slots:
  - port
commands:
  - lsof
  - ss
  - fuser
  - kill
safe_order:
  - inspect
  - identify
  - confirm
  - act
risks:
  - killing the wrong process
  - stopping a system service
```

Implementation:

- Add command templates.
- Add slot extraction.
- Add intent categories.
- Add structured recipes.
- Add safe first-step recommendations.
- Add command-specific risk notes.

This is the main moat. The graph matters more than the model.

## Level 3: Command Guard

Goal:

Review a proposed shell command before execution.

Input:

```json
{
  "intent": "clean project dependencies",
  "command": "rm -rf node_modules",
  "context": {
    "cwd": "/project/app"
  }
}
```

Output:

```json
{
  "decision": "warn",
  "risk": "medium",
  "reasons": [
    "Deletes a local dependency directory"
  ],
  "safer_next_step": "Confirm the target path before deletion"
}
```

Implementation:

- Risk taxonomy.
- Command parser.
- Rules for destructive operations.
- Rules for permission changes.
- Rules for process killing.
- Rules for secret exposure.
- Rules for network access.
- Rules for package install and system mutation.
- JSON schema for agent integrations.

This is the strongest bridge into LatentOps.

## Level 4: Agent Integration

Goal:

Make it easy for AI coding agents and terminal agents to call CommandGraph before running shell commands.

Interfaces:

- CLI: `commandgraph review --intent ... --command ... --json`
- Python API.
- JSON stdin/stdout mode.
- Optional MCP server later.
- Optional shell hook later.

Design principle:

CommandGraph should review and explain. It should not auto-execute commands by default.

## Level 5: Learning Layer

Do this only after the deterministic version works.

Good early ML:

- Embeddings for semantic search.
- Learning-to-rank from accepted results.
- Intent classifier.
- Slot extraction.
- Risk classifier.

Avoid early:

- Full RL.
- Free-form shell generation.
- Auto-execution agents.
- Cloud-only model dependency.

Where RL may fit later:

- Multi-step command planning.
- Learning which safe next step works best.
- Offline training from expert traces.
- Contextual bandits for recommendation ranking.

Important constraint:

If RL is ever used, it should operate over a constrained command graph, not free-form shell text.

## Immediate Implementation Priorities

1. Improve search quality.

   Add a real BM25-style scorer, exact-intent boosts, command-name boosts, synonym expansion weights, and weak-token filtering.

2. Add man-page ingestion.

   Build an indexer that can read local `apropos` or `man -k` output and merge it with curated command cards.

3. Expand command coverage.

   Grow from the current small seed set to 30-50 high-value commands:

   - files: `ls`, `find`, `cp`, `mv`, `rm`, `mkdir`, `touch`
   - permissions: `chmod`, `chown`
   - disk: `df`, `du`
   - processes: `ps`, `top`, `kill`, `pgrep`, `pkill`
   - network: `curl`, `ping`, `ss`, `lsof`, `dig`
   - archives: `tar`, `gzip`, `zip`, `unzip`
   - git: `git status`, `git log`, `git reset`, `git restore`
   - package managers: `npm`, `pip`, `apt`, `brew`
   - containers: `docker`, `docker compose`

4. Add command templates.

   Examples:

   - `chmod +x {file}`
   - `lsof -i :{port}`
   - `du -h --max-depth={depth} {path}`
   - `find {path} -name {pattern}`

5. Add slot extraction.

   Extract simple values from user queries:

   - port numbers
   - file paths
   - package names
   - process names
   - branch names
   - depth values

6. Improve risk review.

   Add categories:

   - read-only
   - file write
   - recursive delete
   - permission change
   - process termination
   - network request
   - package install
   - secret exposure
   - production or infrastructure mutation

7. Add fixtures and tests.

   Test against common queries:

   - `make file runnable`
   - `what is using port 3000`
   - `delete node_modules`
   - `show biggest folders`
   - `undo last commit keep changes`
   - `find files named config`
   - `download url`

8. Add a small evaluation set.

   Track:

   - top-1 command accuracy
   - top-3 command accuracy
   - risk classification accuracy
   - false safe rate for dangerous commands
   - false block rate for normal commands

9. Polish CLI.

   Commands:

   - `commandgraph search "make file runnable"`
   - `commandgraph explain chmod`
   - `commandgraph check "chmod -R 777 ."`
   - `commandgraph review --intent "clean dependencies" --command "rm -rf node_modules" --json`
   - `commandgraph index`
   - `commandgraph doctor`

10. Keep the repo separable.

   Avoid importing from the main LatentOps app.
   Keep package metadata, tests, examples, and docs self-contained inside `commandgraph/`.

## Open Source Requirements

Before separating CommandGraph into its own repository, define the public project rules clearly.

### License

Use a permissive open-source license unless there is a clear reason not to.

Recommended options:

- Apache-2.0 if patent protection and enterprise-friendly adoption matter.
- MIT if maximum simplicity matters.

Current recommendation:

Use Apache-2.0 for CommandGraph because it is enterprise-friendly and gives clearer patent protections while still being permissive.

### Contribution Model

Add contributor documentation before public launch:

- `CONTRIBUTING.md`
- command-card schema documentation
- test requirements for new command cards
- review rules for risk labels
- issue templates for command coverage, search quality, and safety bugs
- pull request template with safety checklist

New command contributions should include:

- command metadata
- common intents
- examples
- risk labels
- safer alternatives when relevant
- tests for at least one search query and one risk case

### Data Governance

Curated command data is part of the product, so it needs review rules.

Requirements:

- Every command card should be source-reviewable.
- Risk labels should be conservative.
- Dangerous examples should be marked clearly or avoided.
- Generated data should not be merged without human review.
- Command cards should include platform notes when behavior differs by OS.
- Changes to risk rules should include tests.

The public repo should treat incorrect "safe" ratings as high-priority safety bugs.

### Security Policy

Add `SECURITY.md`.

Security-sensitive issues include:

- dangerous commands marked safe
- command review bypasses
- shell parsing bugs that hide risky behavior
- examples that could leak secrets
- examples that encourage destructive operations without warning
- package or dependency vulnerabilities

The security policy should explain how to report private safety bugs before opening a public issue.

### Platform Support

Start narrow and be explicit.

Initial support:

- Linux first.
- macOS second.
- Windows/PowerShell later.

Reason:

`apropos`, `man -k`, command flags, paths, permissions, and process tools vary by platform. Linux gives the cleanest first target and best alignment with traditional `apropos`.

Platform-specific behavior should be represented in command metadata instead of hidden in code.

### Package And Distribution

Early distribution:

- Python package.
- `pipx install commandgraph` target.
- local source install for contributors.

Later distribution:

- Homebrew formula.
- GitHub releases.
- standalone binaries if needed.

The CLI should remain the primary surface:

```powershell
commandgraph search "make file runnable"
commandgraph check "chmod -R 777 ."
commandgraph review --intent "clean dependencies" --command "rm -rf node_modules" --json
```

### Privacy Promise

CommandGraph should be local-first.

Default behavior:

- no telemetry
- no cloud calls
- no command upload
- no shell history upload
- no hidden analytics

If optional remote models or analytics are ever added, they must be opt-in and clearly documented.

### Compatibility With Existing Tools

CommandGraph should build on existing Unix tooling instead of replacing it.

Integrations to support:

- `apropos`
- `man -k`
- `whatis`
- local man-db output
- local command availability checks

The first version should work with curated data alone, then enrich results when local man-page tools are available.

### Open-Core Boundary

Keep the boundary clear.

Open-source CommandGraph can include:

- local search
- local command graph
- local command review
- basic risk taxonomy
- agent-friendly JSON
- simple local policy hooks

Do not include:

- hosted policy dashboard
- organization approval workflows
- tenant administration
- enterprise audit exports
- managed integrations
- team analytics
- centralized agent governance

This prevents the open-source project from becoming the enterprise LatentOps product while still making it useful and credible.

### Community Standards

Add a standard `CODE_OF_CONDUCT.md` before public launch.

The goal is not to over-formalize the project early, but a public safety-oriented tool should have clear expectations for contributor behavior, issue discussion, and maintainer decisions.

### Maintainer Policy

Document who can approve sensitive changes.

Sensitive changes include:

- risk taxonomy updates
- shell parsing changes
- command review decision logic
- dangerous-command examples
- command cards for destructive tools
- schema changes
- security fixes

Risk rules and safety decisions should require stricter review than ordinary documentation or command metadata changes.

### Versioning Policy

Use semantic versioning.

Versioning matters because agents and other tools may depend on stable CLI and JSON behavior.

Guidelines:

- Patch releases: bug fixes, command-card additions, safe scoring improvements.
- Minor releases: new commands, new fields, new CLI options that are backward compatible.
- Major releases: breaking CLI behavior, breaking JSON schema changes, major risk taxonomy changes.

### Schema Versioning

Every stable machine-readable object should include a schema version.

This includes:

- command cards
- command templates
- search results
- risk check results
- agent review responses
- evaluation fixtures

Example:

```json
{
  "schema_version": "commandgraph.review.v1",
  "decision": "warn",
  "risk": "medium"
}
```

Agent-facing schemas should be treated as public contracts.

### Threat Model

Add a `docs/threat-model.md`.

It should explain what CommandGraph tries to protect against:

- accidental destructive shell commands
- commands that do not match the user's intent
- risky commands proposed by AI agents
- unsafe examples copied from search results
- obvious secret exposure patterns
- permission changes and recursive deletion mistakes

It should also explain what CommandGraph does not guarantee:

- it is not a sandbox
- it is not a malware detector
- it is not a complete shell parser at first
- it cannot prove a command is safe
- it cannot replace human review for high-risk operations

### Evaluation Transparency

Publish a small evaluation set with expected behavior.

Include:

- natural-language queries
- expected top commands
- acceptable alternate commands
- dangerous command examples
- expected risk labels
- known failure cases

Metrics:

- top-1 command accuracy
- top-3 command accuracy
- risk classification accuracy
- false safe rate
- false block rate
- latency

Known failures should be documented instead of hidden.

### False-Safety Policy

Treat false-safe results as the highest-priority bug class.

Definition:

A false-safe result is when CommandGraph marks or presents a risky command as safer than it is.

Examples:

- `rm -rf /` marked low risk
- recursive permission broadening marked safe
- secret-printing commands shown without warning
- destructive commands recommended before inspection

The project should prefer conservative warnings over unsafe silence.

### Dependency Policy

Keep dependencies small and understandable.

Requirements:

- no heavy ML dependency in the default install
- no network-required dependency for core behavior
- pin or constrain dependencies where stability matters
- avoid dependency chains that make the CLI slow to install
- keep optional ML dependencies behind extras

Possible extras later:

```toml
[project.optional-dependencies]
ml = ["sentence-transformers", "numpy"]
dev = ["pytest", "ruff"]
```

### Offline Mode Guarantee

Core behavior must work offline.

Tests should verify:

- search works from bundled/curated command cards
- risk review works without network access
- CLI help works without external services
- JSON output does not require cloud calls

Local man-page enrichment should be optional. If `apropos` or `man -k` is unavailable, CommandGraph should still work with curated data.

### Model And Provider Boundary

If embeddings or models are added later:

- local/offline should be the default
- remote providers should be opt-in
- users should know exactly what text is sent remotely
- shell history should never be uploaded by default
- remote provider configuration should be explicit
- tests should cover the no-network default path

CommandGraph should not depend on a hosted LLM to be useful.

### Release Checklist

Each release should check:

- tests pass
- CLI smoke tests pass
- JSON schema compatibility is reviewed
- changelog is updated
- risky command examples are reviewed
- false-safe regressions are checked
- dependency changes are reviewed
- package build works
- install from a clean environment works

Before `v1.0`, every release can be marked experimental, but the safety claims should still be conservative and accurate.

### Public Roadmap

Create a public `ROADMAP.md` later.

The public roadmap should be cleaner than this internal plan and should focus on:

- current milestone
- next milestone
- planned command coverage
- planned integrations
- known limitations
- contribution areas

Keep enterprise LatentOps roadmap items out of the open-source roadmap unless they are already public.

### Naming And Branding

Decide the public repo name before launch.

Options:

- `commandgraph`
- `latentops-commandgraph`
- `semantic-apropos`
- `aproposx`

Recommended:

Use `commandgraph` for the project name and mention LatentOps in the description:

> CommandGraph by LatentOps: intent-aware command discovery and safety review for humans and AI agents.

This keeps the project standalone while still connecting it to LatentOps.

## First Milestone

The first milestone should be a useful local CLI:

```powershell
commandgraph search "make file runnable"
commandgraph check "chmod -R 777 ."
commandgraph review --intent "clean dependencies" --command "rm -rf node_modules" --json
```

Success criteria:

- Works locally without cloud services.
- Returns useful command matches.
- Explains why a command matched.
- Flags obviously risky commands.
- Produces stable JSON for agent integrations.
- Has tests for search, templates, and risk review.

## Second Milestone

Add a real command graph:

- 30-50 curated commands.
- Intent recipes.
- Slots and templates.
- Safe execution order.
- Recovery notes.
- Local man-page enrichment.

Success criteria:

- Handles common developer/admin terminal tasks.
- Can explain commands, flags, risks, and safer next steps.
- Provides better results than plain `apropos` for beginner-style queries.

## Third Milestone

Make it agent-ready:

- Stable review schema.
- MCP or stdio integration.
- Agent examples.
- Safety-focused evaluation set.
- Basic policy hooks without enterprise features.

Success criteria:

- A coding agent can call CommandGraph before shell execution.
- CommandGraph can warn or block dangerous terminal actions locally.
- The open-source module clearly supports the broader LatentOps runtime safety thesis.

## Research Direction

CommandGraph can support a technical report later:

Working title:

> CommandGraph: Intent-Aware Command Discovery and Safety Review for Tool-Using AI Agents

Potential research questions:

- Can intent-based command graphs outperform traditional `apropos` on natural language command discovery?
- Can constrained command templates reduce unsafe command generation compared with free-form generation?
- Can local command risk review reduce dangerous terminal actions from AI agents?
- Which risk categories are most important for terminal-based AI agents?
- How often do agents propose commands that do not match the user's stated intent?

This research should connect to LatentOps without exposing enterprise code.
