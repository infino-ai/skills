# Contributing

Thanks for helping coding agents use Infino well.

## What makes a good change

- **Something an agent got wrong.** If you watched an agent misuse Infino, the
  best fix is usually a line in a skill's "Mistakes to avoid" section. Say in
  the pull request what the agent did.
- **Honest fit.** A skill should say when not to use Infino as clearly as when
  to use it. Agents trust a skill that admits its limits.
- **Short.** An agent reads the whole skill every time it loads. Cut anything
  that does not change what the agent writes.

## Examples must run

CI runs every `python` and `javascript` code block in every `SKILL.md` against
the latest published packages, twice in a fresh directory, so the second run
exercises reopening an existing table. Claims in the mistakes list are checked
in `tests/check_claims.py`. Run both before opening a pull request:

```sh
pip install infino pyarrow
mkdir -p /tmp/infino-node && (cd /tmp/infino-node && npm init -y && npm install @infino-ai/infino)
python tests/check_claims.py
python tests/run_snippets.py /tmp/infino-node
```

A code block that is not meant to run should use a different language tag,
such as `sh` or `text`.

## Adding a skill

Put it in `skills/<name>/SKILL.md` with `name` and `description` frontmatter.
The description is what the agent matches on, so write it as the situations
where the skill applies. Add a row for it to the table in the README.

## Pull requests

Open a pull request against `main`. CI must pass. By contributing you agree
that your contribution is licensed under the Apache License 2.0, and you agree
to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
