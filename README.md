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
├── commitlint.config.cjs
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

1. **Rename the package**: update `name` in `pyproject.toml`, the directory
   under `src/`, and imports in `tests/`. Also update the `package-name` and
   `extra-files` paths in `.github/release-please-config.json`.

2. **Workflow permissions**: Settings → Actions → General → Workflow
   permissions. Enable:
   - "Read and write permissions"
   - "Allow GitHub Actions to create and approve pull requests"

3. **Personal Access Token for release-please**: create a fine-grained PAT
   ([generate here](https://github.com/settings/personal-access-tokens/new))
   scoped to this repo with `Contents: read+write`, `Pull requests: read+write`,
   `Workflows: read+write`. Add as repository secret `RELEASE_PLEASE_TOKEN`.
   (Required so the GitHub Release created by release-please triggers the
   `publish.yml` workflow — events from the default `GITHUB_TOKEN` do not
   trigger other workflows.)

4. **Install the Claude Code GitHub App** at
   [github.com/apps/claude](https://github.com/apps/claude) and grant access to
   this repo. Add `ANTHROPIC_API_KEY` repository secret.

5. **Configure Trusted Publishers** on
   [PyPI](https://docs.pypi.org/trusted-publishers/) and
   [TestPyPI](https://docs.pypi.org/trusted-publishers/) for your repo. Use
   "pending publisher" if the project doesn't exist yet. Point each to:
   - Workflow name: `publish.yml`
   - Environment name: `pypi` (production) and `testpypi` respectively

6. **Create GitHub Environments** `testpypi` and `pypi` under Settings →
   Environments. For each, under **Deployment branches and tags**:
   - Select "Selected branches and tags"
   - Add a **branch** rule: `main`
   - Add a **tag** rule (toggle ref type to "Tag" in the modal): use the tag
     pattern that release-please produces — by default
     `<package-name>-v*` (e.g. `test-python-package-release-v*`)

7. **(Optional) Branch protection ruleset** for `main`:
   - Require a PR before merging
   - Require status checks: `lint`, `test (3.11)`, `test (3.12)`,
     `test (3.13)`, `commitlint`
   - Block force pushes, restrict deletions
   - Add yourself to the bypass list so you can merge release-please PRs

8. **(Optional) Production gate** for PyPI publishing — on Pro/Team/Enterprise
   plans only: add a Required reviewer on the `pypi` environment to require
   manual approval before production publish.
