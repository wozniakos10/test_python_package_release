# Python Package Release Template — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn this empty `uv init` repo into a reusable template that demonstrates a complete CI/CD pipeline for Python packages published to PyPI.

**Architecture:** `src/`-layout library with trivial pure-function code (calculator + strings), `pyproject.toml` as single source of truth for build/lint/type/test config, tox-uv matrix testing on Python 3.11/3.12/3.13, GitHub Actions workflows for PR validation (lint/type/tests/commitlint), on-demand Claude review, release-please for automated versioning + CHANGELOG, and OIDC-based TestPyPI → PyPI publish on release.

**Tech Stack:** Python 3.11/3.12/3.13, uv, hatchling, ruff, ty, pytest, tox + tox-uv, pre-commit, conventional-pre-commit, commitlint, release-please, claude-code-action, Dependabot.

**Spec:** `docs/superpowers/specs/2026-05-30-python-package-release-template-design.md`

---

## File Structure Overview

**Files to create:**
- `src/test_python_package_release/__init__.py` — public API + `__version__`
- `src/test_python_package_release/calculator.py` — `add`, `subtract`, `multiply`, `divide`
- `src/test_python_package_release/strings.py` — `reverse_string`, `snake_to_camel`
- `tests/__init__.py`
- `tests/test_calculator.py`
- `tests/test_strings.py`
- `.pre-commit-config.yaml`
- `commitlint.config.js`
- `CHANGELOG.md`
- `LICENSE`
- `.github/workflows/ci.yml`
- `.github/workflows/claude-review.yml`
- `.github/workflows/release-please.yml`
- `.github/workflows/publish.yml`
- `.github/dependabot.yml`
- `.github/release-please-config.json`
- `.github/.release-please-manifest.json`

**Files to modify:**
- `pyproject.toml` — full rewrite (build backend, deps, tool configs, tox)
- `.gitignore` — add Python build/cache directories
- `README.md` — full content (template usage docs)

**Files to delete:**
- `main.py` — leftover from `uv init`, not needed for a library template

---

## Task 1: Repository scaffolding (delete cruft, restructure)

**Files:**
- Delete: `main.py`
- Modify: `.gitignore`

- [ ] **Step 1: Delete `main.py`**

```bash
rm main.py
```

- [ ] **Step 2: Append Python build/cache patterns to `.gitignore`**

Append the following to `.gitignore`:

```
# Build artifacts
dist/
build/
*.egg-info/

# Test / lint caches
.tox/
.pytest_cache/
.ruff_cache/
.ty_cache/
.coverage
htmlcov/
```

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "chore: remove uv init leftovers and extend gitignore"
```

---

## Task 2: Library source — package init + calculator module

**Files:**
- Create: `src/test_python_package_release/__init__.py`
- Create: `src/test_python_package_release/calculator.py`
- Create: `tests/__init__.py`
- Create: `tests/test_calculator.py`

- [ ] **Step 1: Create `tests/__init__.py` (empty)**

```bash
mkdir -p tests
touch tests/__init__.py
```

- [ ] **Step 2: Write failing test `tests/test_calculator.py`**

```python
import pytest

from test_python_package_release import add, divide, multiply, subtract


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(3, 4) == 12


def test_divide():
    assert divide(10, 2) == 5.0


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
```

- [ ] **Step 3: Run the test — it must fail**

```bash
uv run pytest tests/test_calculator.py -v
```

Expected: ImportError / ModuleNotFoundError on `test_python_package_release` (package does not exist yet).

- [ ] **Step 4: Create `src/test_python_package_release/calculator.py`**

```python
def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
```

- [ ] **Step 5: Create `src/test_python_package_release/__init__.py`**

```python
"""Test Python package release — template library."""

__version__ = "0.1.0"  # managed by release-please

from test_python_package_release.calculator import add, divide, multiply, subtract

__all__ = ["add", "divide", "multiply", "subtract"]
```

- [ ] **Step 6: Tests cannot pass yet — `pyproject.toml` must be configured first.**

Skip running pytest. The test will pass after Task 4 sets up the build system.

- [ ] **Step 7: Commit**

```bash
git add src/ tests/
git commit -m "feat: add calculator module with tests"
```

---

## Task 3: Library source — strings module

**Files:**
- Create: `src/test_python_package_release/strings.py`
- Create: `tests/test_strings.py`
- Modify: `src/test_python_package_release/__init__.py`

- [ ] **Step 1: Write failing test `tests/test_strings.py`**

```python
from test_python_package_release import reverse_string, snake_to_camel


def test_reverse_string():
    assert reverse_string("abc") == "cba"


def test_reverse_string_empty():
    assert reverse_string("") == ""


def test_snake_to_camel():
    assert snake_to_camel("hello_world_foo") == "helloWorldFoo"


def test_snake_to_camel_single_word():
    assert snake_to_camel("single") == "single"
```

- [ ] **Step 2: Create `src/test_python_package_release/strings.py`**

```python
def reverse_string(s: str) -> str:
    return s[::-1]


def snake_to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])
```

- [ ] **Step 3: Update `src/test_python_package_release/__init__.py`** to export the new symbols

Replace the file contents with:

```python
"""Test Python package release — template library."""

__version__ = "0.1.0"  # managed by release-please

from test_python_package_release.calculator import add, divide, multiply, subtract
from test_python_package_release.strings import reverse_string, snake_to_camel

__all__ = [
    "add",
    "divide",
    "multiply",
    "reverse_string",
    "snake_to_camel",
    "subtract",
]
```

- [ ] **Step 4: Skip running tests — still blocked on `pyproject.toml` setup (Task 4).**

- [ ] **Step 5: Commit**

```bash
git add src/ tests/
git commit -m "feat: add strings module with tests"
```

---

## Task 4: pyproject.toml — full configuration (build, deps, tool configs, tox)

**Files:**
- Modify: `pyproject.toml` (full replacement)

- [ ] **Step 1: Replace `pyproject.toml` content with the following**

```toml
[project]
name = "test-python-package-release"
version = "0.1.0"
description = "Template library demonstrating Python package release CI/CD"
readme = "README.md"
requires-python = ">=3.11"
license = { file = "LICENSE" }
authors = [{ name = "Dawid Wozniak", email = "wozniakos10@gmail.com" }]
classifiers = [
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "License :: OSI Approved :: MIT License",
]
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/test_python_package_release"]

[dependency-groups]
dev = [
    "pytest>=8",
    "pytest-cov>=5",
    "ruff>=0.8",
    "ty>=0.0.1a1",
    "tox>=4.21",
    "tox-uv>=1.16",
    "pre-commit>=4",
]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "RUF"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --strict-markers"

[tool.tox]
env_list = ["py311", "py312", "py313", "lint", "type"]
requires = ["tox>=4.21", "tox-uv>=1.16"]

[tool.tox.env_run_base]
runner = "uv-venv-lock-runner"
dependency_groups = ["dev"]
commands = [["pytest", "{posargs}"]]

[tool.tox.env.lint]
commands = [
    ["ruff", "check", "."],
    ["ruff", "format", "--check", "."],
]

[tool.tox.env.type]
commands = [["ty", "check", "src"]]
```

- [ ] **Step 2: Sync dependencies**

```bash
uv sync --group dev
```

Expected: lockfile updated, dev deps installed.

- [ ] **Step 3: Run all tests — they must pass now**

```bash
uv run pytest -v
```

Expected: 9 tests pass (5 calculator + 4 strings).

- [ ] **Step 4: Verify ruff and ty are clean**

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check src
```

Expected: all three exit 0 (no issues). If `ruff format --check` fails, run `uv run ruff format .` then commit the formatting fix as part of step 5.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "chore: configure pyproject.toml as single source of truth"
```

---

## Task 5: Pre-commit hooks (ruff, ty, conventional commits)

**Files:**
- Create: `.pre-commit-config.yaml`

- [ ] **Step 1: Create `.pre-commit-config.yaml`**

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/astral-sh/ty-pre-commit
    rev: 0.0.1a1
    hooks:
      - id: ty

  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.6.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
```

- [ ] **Step 2: Install hooks and verify they run**

```bash
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
uv run pre-commit run --all-files
```

Expected: ruff check + format + ty all pass. (Commit-msg hook is not exercised by `run --all-files`.)

- [ ] **Step 3: Commit**

```bash
git add .pre-commit-config.yaml
git commit -m "chore: add pre-commit hooks for ruff, ty, conventional commits"
```

If the commit-msg hook complains, the message above is already conventional — should pass.

---

## Task 6: LICENSE, README, commitlint config, CHANGELOG

**Files:**
- Create: `LICENSE`
- Create: `commitlint.config.js`
- Create: `CHANGELOG.md`
- Modify: `README.md`

- [ ] **Step 1: Create `LICENSE` (MIT)**

```
MIT License

Copyright (c) 2026 Dawid Wozniak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 2: Create `commitlint.config.js`**

```js
module.exports = { extends: ['@commitlint/config-conventional'] };
```

- [ ] **Step 3: Create empty `CHANGELOG.md`** (release-please will manage from now on)

```markdown
# Changelog

All notable changes to this project will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
and the changelog is generated automatically by
[release-please](https://github.com/googleapis/release-please).
```

- [ ] **Step 4: Replace `README.md` with template documentation**

```markdown
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
```

- [ ] **Step 5: Commit**

```bash
git add LICENSE commitlint.config.js CHANGELOG.md README.md
git commit -m "docs: add LICENSE, README, commitlint config, CHANGELOG"
```

---

## Task 7: CI workflow (lint, tests matrix, commitlint)

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Create `.github/workflows/ci.yml`**

```yaml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true
      - run: uv sync --group dev
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run ty check src

  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true
      - run: uv python install ${{ matrix.python-version }}
      - name: Run tox env
        run: |
          env_name="py$(echo ${{ matrix.python-version }} | tr -d .)"
          uv run tox -e "${env_name}"

  commitlint:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: wagoid/commitlint-github-action@v6
```

- [ ] **Step 2: Validate YAML syntax locally**

```bash
uv run --with pyyaml python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"
```

Expected: no output, no error.

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: add lint, test matrix, and commitlint workflow"
```

---

## Task 8: Claude review workflow (`@claude` trigger)

**Files:**
- Create: `.github/workflows/claude-review.yml`

- [ ] **Step 1: Create `.github/workflows/claude-review.yml`**

```yaml
name: Claude Review

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      issues: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

- [ ] **Step 2: Validate YAML syntax locally**

```bash
uv run --with pyyaml python -c "import yaml; yaml.safe_load(open('.github/workflows/claude-review.yml'))"
```

Expected: no output, no error.

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/claude-review.yml
git commit -m "ci: add on-demand Claude review workflow triggered by @claude"
```

---

## Task 9: Release-please workflow + config

**Files:**
- Create: `.github/release-please-config.json`
- Create: `.github/.release-please-manifest.json`
- Create: `.github/workflows/release-please.yml`

- [ ] **Step 1: Create `.github/release-please-config.json`**

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

- [ ] **Step 2: Create `.github/.release-please-manifest.json`**

```json
{
  ".": "0.1.0"
}
```

- [ ] **Step 3: Create `.github/workflows/release-please.yml`**

```yaml
name: Release Please

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v4
        with:
          config-file: .github/release-please-config.json
          manifest-file: .github/.release-please-manifest.json
```

- [ ] **Step 4: Validate JSON + YAML syntax locally**

```bash
uv run python -c "import json; json.load(open('.github/release-please-config.json'))"
uv run python -c "import json; json.load(open('.github/.release-please-manifest.json'))"
uv run --with pyyaml python -c "import yaml; yaml.safe_load(open('.github/workflows/release-please.yml'))"
```

Expected: no output, no error.

- [ ] **Step 5: Commit**

```bash
git add .github/release-please-config.json .github/.release-please-manifest.json .github/workflows/release-please.yml
git commit -m "ci: add release-please workflow and configuration"
```

---

## Task 10: Publish workflow (TestPyPI → PyPI via OIDC)

**Files:**
- Create: `.github/workflows/publish.yml`

- [ ] **Step 1: Create `.github/workflows/publish.yml`**

```yaml
name: Publish

on:
  release:
    types: [published]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  publish-testpypi:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: testpypi
      url: https://test.pypi.org/p/test-python-package-release
    permissions:
      id-token: write
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - uses: pypa/gh-action-pypi-publish@release/v1
        with:
          repository-url: https://test.pypi.org/legacy/

  publish-pypi:
    needs: publish-testpypi
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/test-python-package-release
    permissions:
      id-token: write
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - uses: pypa/gh-action-pypi-publish@release/v1
```

- [ ] **Step 2: Validate YAML syntax locally**

```bash
uv run --with pyyaml python -c "import yaml; yaml.safe_load(open('.github/workflows/publish.yml'))"
```

Expected: no output, no error.

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/publish.yml
git commit -m "ci: add OIDC-based publish workflow for TestPyPI and PyPI"
```

---

## Task 11: Dependabot configuration

**Files:**
- Create: `.github/dependabot.yml`

- [ ] **Step 1: Create `.github/dependabot.yml`**

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      actions:
        patterns: ["*"]

  - package-ecosystem: "uv"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      dev-dependencies:
        dependency-type: "development"
```

- [ ] **Step 2: Validate YAML syntax locally**

```bash
uv run --with pyyaml python -c "import yaml; yaml.safe_load(open('.github/dependabot.yml'))"
```

Expected: no output, no error.

- [ ] **Step 3: Commit**

```bash
git add .github/dependabot.yml
git commit -m "chore: add Dependabot config for actions and uv dev deps"
```

---

## Task 12: Final end-to-end verification

**Files:** none (verification only)

- [ ] **Step 1: Run full local validation**

```bash
uv sync --group dev
uv run pytest -v
uv run ruff check .
uv run ruff format --check .
uv run ty check src
```

Expected: 9 tests pass, all linters clean.

- [ ] **Step 2: Build the package locally**

```bash
uv build
ls dist/
```

Expected: `dist/` contains a `.whl` and a `.tar.gz` named
`test_python_package_release-0.1.0-*`.

- [ ] **Step 3: Inspect built wheel — sanity check that `src/` layout produced a correct wheel**

```bash
uv run python -c "import zipfile; z = zipfile.ZipFile(next(__import__('pathlib').Path('dist').glob('*.whl'))); print('\n'.join(z.namelist()))"
```

Expected output contains:
```
test_python_package_release/__init__.py
test_python_package_release/calculator.py
test_python_package_release/strings.py
```

- [ ] **Step 4: Clean up build artifacts (they're gitignored, but tidy up the worktree)**

```bash
rm -rf dist/ build/
```

- [ ] **Step 5: Confirm git state is clean**

```bash
git status
```

Expected: `nothing to commit, working tree clean`.

- [ ] **Step 6: No commit for this task — verification only.**

---

## Notes for the executing agent

- **Tasks 2 and 3** intentionally defer running tests until Task 4 completes the `pyproject.toml` setup, because the package isn't importable without a build backend declaration. The TDD red-step is "tests can't even import the package" — captured implicitly by the missing `pyproject.toml` config.
- **All commit messages** in this plan are conventional and will pass both `conventional-pre-commit` and `commitlint`.
- **No secrets** are needed for local verification. The OIDC-based publishing and `ANTHROPIC_API_KEY` only matter once the template is cloned and deployed to GitHub.
- **`ty` version** uses an alpha (`0.0.1a1`) — it's the current state of the tool. If `uv sync` fails to resolve, fall back to the latest pre-release matching the `0.0.x` series; this is a known characteristic of the tool, not a plan defect.
