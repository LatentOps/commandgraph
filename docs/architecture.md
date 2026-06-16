# CommandGraph Architecture

CommandGraph is intentionally small.

```text
CLI
 |
 command graph data
 |
 synonym expansion
 |
 lightweight retrieval
 |
 risk rules
 |
 human-readable or JSON output
```

## Why Not Start With RL?

Level 1 is search and ranking. Retrieval, synonyms, and supervised ranking are
better first tools than RL.

RL may fit later when the system has:

- safe sandboxes;
- multi-step task traces;
- human accept/reject feedback;
- clear success metrics;
- constrained action templates.

Even then, use constrained RL over a safe command graph, not free-form shell
generation.

## Project Scope

CommandGraph can review terminal commands locally.

CommandGraph does not provide:

- account management;
- team analytics;
- centralized command governance;
- remote command execution services.

The core system should remain a local Linux command discovery and safety
review tool.

