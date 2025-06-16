# PromptGuard CI

[![CI](https://github.com/example/promptguard-ci/actions/workflows/ci.yml/badge.svg)](https://github.com/example/promptguard-ci/actions)
[![PyPI version](https://img.shields.io/pypi/v/promptguard-ci.svg)](https://pypi.org/project/promptguard-ci/)

Catch prompt regressions **before** they reach production.

```
YAML -> CLI -> GitHub Action
```

## Quick start

```bash
pip install promptguard-ci
# or from sources
# git clone https://github.com/<your-user>/promptguard-ci && cd promptguard-ci
# pip install -e .

# configure API keys in .env
cp .env.example .env
# edit OPENAI_API_KEY and PERSPECTIVE_API_KEY

# run the example spec
promptguard test examples/hello.yml --junit-output results.xml
```

## Features

- Define prompt tests in **YAML**
- Run them locally or in **GitHub Actions**
- Emit **JUnit XML** so CI fails when tests regress
- Built‑in assertions: `contains`, `not_contains`, `json_valid`, `toxicity < 0.2`

See `examples/hello.yml` for a starting point.

