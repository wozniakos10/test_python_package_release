# Python Package Release Template — Design

**Date:** 2026-05-30
**Status:** Approved
**Author:** Dawid Wozniak (via brainstorming with Claude)

## Goal

Turn this repo into a reusable template for Python libraries published to PyPI. The template demonstrates a complete CI/CD pipeline:

- On PR: lint, type-check, multi-version tests, conventional commit validation; Claude review on demand (`@claude` comment).
- On merge to `main`: automated version bump, CHANGELOG generation, GitHub Release.
- On GitHub Release: build and publish to TestPyPI then PyPI via Trusted Publishing (OIDC).

## Non-Goals

- Production-grade business logic (the library is intentionally trivial).
- Documentation site (Sphinx/mkdocs) — out of scope.
- Cross-platform CI (Linux only).
- Coverage upload to external service (Codecov etc.).

## High-Level Flow

```
Developer ──▶ PR ──▶ ci.yml (lint + ty + tests matrix + commitlint)
                       │
                       └─ optional: comment "@claude" ──▶ claude-review.yml

Maintainer merges PR ──▶ main ──▶ release-please.yml
                                       │
                                       └─ creates/updates "Release PR"
                                          (bumps version, regenerates CHANGELOG)

Maintainer merges Release PR ──▶ release-please tags + creates GitHub Release
                                       │
                                       └─ publish.yml ──▶ build wheel/sdist
                                                          ──▶ TestPyPI (OIDC)
                                                          ──▶ PyPI (OIDC, gated env)
```

## Repository Structure

```
test_python_package_release/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── claude-review.yml
│   │   ├── release-please.yml
│   │   └── publish.yml
│   ├── dependabot.yml
│   ├── release-please-config.json
│   └── .release-please-manifest.json
├── src/
│   └── test_python_package_release/
│       ├── __init__.py
│       ├── calculator.py
│       └── strings.py
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   └── test_strings.py
├── docs/
│   └── superpowers/specs/2026-05-30-python-package-release-template-design.md
├── .pre-commit-config.yaml
├── .gitignore
├── pyproject.toml
├── commitlint.config.js
├── CHANGELOG.md
├── LICENSE
└── README.md
```

**Rationale:** `src/` layout (PyPA recommended) prevents accidental import of source before install. Single `pyproject.toml` is the source of truth for build, dependencies, ruff, ty, pytest, and tox.

## Library Code

### `src/test_python_package_release/__init__.py`
Exports `__version__` (managed by release-please) and the public API surface (`add`, `subtract`, `multiply`, `divide`, `reverse_string`, `snake_to_camel`).

### `src/test_python_package_release/calculator.py`
Pure functions: `add`, `subtract`, `multiply`, `divide` (raises `ZeroDivisionError` on `b == 0`). All annotated with `float` types.

### `src/test_python_package_release/strings.py`
Pure functions: `reverse_string(s)` (returns `s[::-1]`), `snake_to_camel(s)` (splits on `_`, lowercases first part, title-cases rest).

### Tests
- `tests/test_calculator.py`: positive cases per operation + `pytest.raises(ZeroDivisionError)` for divide.
- `tests/test_strings.py`: `reverse_string("abc") == "cba"`, `snake_to_camel("hello_world_foo") == "helloWorldFoo"`, edge case `snake_to_camel("single") == "single"`.

No mocks needed — pure functions only. Cleanup: remove `main.py` and trim `pandas`/`requests` from default `pyproject.toml`.

## Tooling Configuration

### `pyproject.toml` (single source of truth)

- `[project]`: name, version (release-please managed), description, `requires-python = ">=3.11"`, MIT license, classifiers for 3.11/3.12/3.13, empty `dependencies = []`.
- `[build-system]`: `hatchling` backend.
- `[tool.hatch.build.targets.wheel]`: `packages = ["src/test_python_package_release"]`.
- `[dependency-groups]` dev: `pytest`, `pytest-cov`, `ruff`, `ty`, `tox>=4.21`, `tox-uv`, `pre-commit`.
- `[tool.ruff]`: `line-length = 100`, `target-version = "py311"`, selected lints `E, F, I, B, UP, SIM, RUF`.
- `[tool.ty]`: default configuration.
- `[tool.pytest.ini_options]`: `testpaths = ["tests"]`, `addopts = "-ra --strict-markers"`.
- `[tool.tox]`: envs `py311, py312, py313, lint, type` using `uv-venv-lock-runner`; lint env runs `ruff check` + `ruff format --check`; type env runs `ty check src`.

### `.pre-commit-config.yaml`

Hooks:
- `astral-sh/ruff-pre-commit` — `ruff --fix` + `ruff-format`.
- `astral-sh/ty-pre-commit` — `ty` type check.
- `compilerla/conventional-pre-commit` — validates commit-msg locally (Python-based, no Node required).

### `commitlint.config.js`

```js
module.exports = { extends: ['@commitlint/config-conventional'] };
```

Used by the CI workflow only (`wagoid/commitlint-github-action`) — full validation of all commits in a PR. Pre-commit handles local enforcement via the Python hook.

## GitHub Actions Workflows

### `ci.yml` — PR validation

Triggers: `pull_request` to `main`, `push` to `main`.

Jobs:
- **lint**: install deps via `uv sync --group dev`; run `ruff check`, `ruff format --check`, `ty check src`.
- **test**: matrix on `python-version: ["3.11", "3.12", "3.13"]`; uses `astral-sh/setup-uv@v4` with cache; runs `tox -e py3xx`.
- **commitlint**: only on `pull_request`; uses `wagoid/commitlint-github-action@v6` with `fetch-depth: 0`.

### `claude-review.yml` — on-demand review

Triggers: `issue_comment.created`, `pull_request_review_comment.created`. Gated by `if: contains(github.event.comment.body, '@claude')`. Uses `anthropics/claude-code-action@v1` with `ANTHROPIC_API_KEY` secret. Permissions: `contents: read`, `pull-requests: write`, `issues: write`, `id-token: write`.

### `release-please.yml` — release automation

Trigger: `push` to `main`. Permissions: `contents: write`, `pull-requests: write`. Uses `googleapis/release-please-action@v4` with config + manifest files.

**`.github/release-please-config.json`:**
```json
{
  "packages": {
    ".": {
      "release-type": "python",
      "package-name": "test-python-package-release",
      "changelog-path": "CHANGELOG.md",
      "extra-files": ["src/test_python_package_release/__init__.py"]
    }
  }
}
```

`release-type: python` handles `pyproject.toml` version bumping; `extra-files` keeps `__version__` in `__init__.py` in sync.

**`.github/.release-please-manifest.json`:**
```json
{ ".": "0.1.0" }
```

### `publish.yml` — build + publish

Trigger: `release.published` (fired when release-please creates the GitHub Release after the Release PR is merged).

Jobs:
1. **build**: `uv build`, upload `dist/` artifact.
2. **publish-testpypi**: GitHub environment `testpypi`, `id-token: write`, downloads `dist/`, publishes via `pypa/gh-action-pypi-publish@release/v1` with `repository-url: https://test.pypi.org/legacy/`.
3. **publish-pypi**: `needs: publish-testpypi`, GitHub environment `pypi` (optionally with required reviewers), `id-token: write`, publishes to production PyPI.

No `PYPI_API_TOKEN` — fully OIDC via Trusted Publishers configured on (Test)PyPI side.

## Branch & Merge Strategy

- All commits must follow Conventional Commits (enforced by pre-commit locally + commitlint in CI on every commit in the PR).
- Merge strategy: merge commits (not squash), preserving granular conventional commits for release-please parsing.
- Recommended branch protection (documented in README, not enforced by template): require status checks `lint`, `test`, `commitlint` before merge; require linear history off (merge commits OK).

## Secrets and External Configuration

**Repo secrets required:**
- `ANTHROPIC_API_KEY` — for Claude review workflow.

**No PyPI tokens** — Trusted Publishing on PyPI/TestPyPI side.

**GitHub Environments required:**
- `testpypi` — no protection rules needed.
- `pypi` — optional required reviewers for prod gate.

**Post-clone setup** (README documents):
1. Rename `name` in `pyproject.toml` and package directory under `src/`.
2. Configure Trusted Publishers on PyPI and TestPyPI (link to PyPA docs).
3. Create `testpypi` and `pypi` GitHub Environments.
4. Add `ANTHROPIC_API_KEY` secret.
5. Ensure Actions has write permissions (Settings → Actions → General → Workflow permissions → Read and write).

## Auxiliary Files

### `LICENSE` — MIT, year 2026, holder Dawid Wozniak.

### `.github/dependabot.yml`
Two ecosystems, weekly schedule, grouped PRs:
- `github-actions`: group all actions into one PR.
- `uv`: group dev-dependency updates into one PR.

### `.gitignore` additions
`dist/`, `build/`, `*.egg-info/`, `.tox/`, `.pytest_cache/`, `.ruff_cache/`, `.coverage`, `htmlcov/`, `.ty_cache/`.

### `README.md` sections
- Quick start (`uv sync --group dev`, `uv run pytest`)
- Project layout (tree)
- Development (`pre-commit install`, `uv run tox`, `uv run ruff check .`)
- Commits (link to Conventional Commits, examples)
- Release flow (the diagram from "High-Level Flow")
- First-time setup after cloning the template (the 5 steps above)

## Open Questions / Future Work

- If we later add a real runtime dependency (e.g., HTTP client), revisit test strategy — mock with `responses` or `pytest-mock`.
- Consider adding `pre-commit.ci` for automated pre-commit-hook updates if Dependabot's uv ecosystem coverage proves insufficient.
- Coverage thresholds: currently `pytest-cov` is installed but no threshold enforced — add `--cov-fail-under` in CI if maintainers want to gate on coverage.

## Decisions Log

| # | Decision | Rationale |
|---|---|---|
| 1 | `release-please` over `semantic-release` | Native Python support, Release-PR model, no Node dep beyond commitlint |
| 2 | Calculator + strings library | Trivial code → focus stays on CI/CD demonstration |
| 3 | `ruff + ty + pre-commit` | Astral toolchain consistency with `uv` |
| 4 | `tox + tox-uv` | Fast multi-version test envs reusing uv cache |
| 5 | Python 3.11/3.12/3.13 matrix | Broad support, manageable CI time |
| 6 | TestPyPI → PyPI publish chain | Safe default for a template; prod gated by environment |
| 7 | OIDC / Trusted Publishing | No long-lived tokens to leak |
| 8 | Claude review on `@claude` only | Less noise than auto-review; explicit opt-in |
| 9 | Merge commits + per-commit conventional | Granular history for release-please parsing |
| 10 | commitlint CI + conventional-pre-commit local | Pure-Python local hook (no Node required locally), Node-based commitlint in CI for full validation |
| 11 | Single `pyproject.toml` (incl. tox config) | One file to edit, fewer config sprawl |
| 12 | `hatchling` build backend | Lightweight, plays well with `uv build` |
| 13 | MIT license + Dependabot (actions + uv, grouped weekly) | Standard OSS defaults |
