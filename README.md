# test-python-package-release

Template repository demonstrating a complete CI/CD pipeline for Python packages
published to PyPI.

## Quick start

```bash
uv sync --group dev
uv run pytest
```

## Project layout

```
.
├── .github/workflows/   # CI, Claude review, release-please, publish
├── src/                 # library code (src/ layout)
├── tests/               # pytest tests
├── pyproject.toml       # single source of truth: build, deps, ruff, pytest, tox
├── .pre-commit-config.yaml
├── commitlint.config.js
└── CHANGELOG.md         # managed by release-please
```

## Development

```bash
# Install hooks (runs ruff + ty pre-commit, conventional commit-msg)
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg

# Run the full test matrix (3.11, 3.12, 3.13)
uv run tox

# Single env
uv run tox -e py313 -- -k calculator

# Lint / format check / type check
uv run ruff check .
uv run ruff format --check .
uv run ty check src
```

## Commits

Every commit MUST follow the
[Conventional Commits](https://www.conventionalcommits.org/) specification.

Examples:
- `feat: add support for negative numbers`
- `fix(calculator): correct divide by zero error`
- `chore(deps): bump ruff to 0.9`
- `feat!: drop Python 3.10 support` (breaking change → major bump)

Enforced locally by `conventional-pre-commit` (commit-msg hook) and in CI by
`commitlint`.

## Release flow

```
PR opened ──▶ ci.yml (lint, ty, pytest matrix, commitlint)
                │
                └─ optional: comment "@claude" ──▶ claude-review.yml

PR merged ──▶ main ──▶ release-please.yml
                          │
                          └─ creates/updates a "Release PR"
                             (bumps version, regenerates CHANGELOG)

Release PR merged ──▶ release-please tags + creates GitHub Release
                          │
                          └─ publish.yml ──▶ uv build
                                            ──▶ TestPyPI (OIDC)
                                            ──▶ PyPI (OIDC, gated env)
```

## First-time setup after cloning the template

1. Rename `name` in `pyproject.toml`, the package directory under `src/`, and
   imports in `tests/`.
2. Configure Trusted Publishers on
   [PyPI](https://docs.pypi.org/trusted-publishers/) and
   [TestPyPI](https://docs.pypi.org/trusted-publishers/) for your repo, pointing
   to the `publish.yml` workflow and the `pypi` / `testpypi` environments.
3. Create two GitHub Environments named `testpypi` and `pypi` (optionally add
   required reviewers on `pypi` as a manual prod gate).
4. Add an `ANTHROPIC_API_KEY` repository secret (for the Claude review
   workflow).
5. Settings → Actions → General → Workflow permissions → "Read and write
   permissions" so release-please can open PRs and push tags.
