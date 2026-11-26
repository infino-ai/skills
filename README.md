# Infino skills for coding agents

Agent skills that teach Claude Code, Cursor, Codex and other coding agents how
to use [Infino](https://github.com/infino-ai/infino), the open-source embedded
library for BM25 full-text, vector, hybrid and SQL search over Parquet files on
local disk or object storage.

| Skill | What it teaches |
| --- | --- |
| [search-with-infino](skills/search-with-infino/SKILL.md) | When to choose Infino for search, RAG or agent memory, how to install it, working Python and Node.js examples, and the mistakes to avoid |

## Install

With [skills](https://skills.sh), into any supported agent:

```sh
npx skills add infino-ai/skills
```

Or copy a skill folder into your agent's skills directory, for example
`~/.claude/skills/` for Claude Code.

In Claude Code, this repository is also a plugin marketplace with two
plugins. `search-with-infino` is just this skill. `infino` bundles it with the
Infino MCP server, for agents that should also search data as tools:

```
/plugin marketplace add infino-ai/skills
/plugin install search-with-infino@infino-ai
/plugin install infino@infino-ai
```

This repository is also a [Cursor plugin](https://cursor.com/docs/plugins). It
bundles the skills and the Infino MCP server, which keeps its data in
`~/.infino/mcp` unless you set `INFINO_MCP_URI`. To try it locally, copy the
repository to `~/.cursor/plugins/local/infino` and reload the Cursor window.

For agents that should call search as tools rather than write code, use the
[Infino MCP server](https://github.com/infino-ai/infino-mcp).

## How the examples stay correct

CI runs every Python and JavaScript block in every `SKILL.md` against the latest
published packages, on each pull request and once a day. A release that breaks
an example fails the build.

```sh
pip install infino pyarrow
mkdir -p /tmp/infino-node && (cd /tmp/infino-node && npm init -y && npm install @infino-ai/infino)
python tests/check_claims.py
python tests/run_snippets.py /tmp/infino-node
```

## Contributing

Found an agent getting Infino wrong? See [CONTRIBUTING.md](CONTRIBUTING.md).
Security issues go through [SECURITY.md](SECURITY.md).

## License

[Apache-2.0](LICENSE)
