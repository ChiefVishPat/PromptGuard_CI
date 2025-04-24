# PromptGuard_CI

> Catch prompt regressions **before** they reach prod.  
> YAML → CLI → GitHub Action.

---

## ⚠️ Personal showcase project

This repository is **public read-only** so recruiters can browse the code, but **external pull-requests are disabled**.  
Feel free to open Issues for questions or feedback.

---

## ✨ MVP Feature List

| Status | Feature |
| :---: | --- |
| ☐ | Define prompt tests in plain **YAML** |
| ☐ | Run `promptguard test spec.yml` locally or in **GitHub Actions** |
| ☐ | Output **JUnit XML** so CI fails when tests regress |
| ☐ | Built-in assertions: `contains`, `not_contains`, `json_valid`, `toxicity < 0.2` |
| ☐ | Side-by-side diff viewer (Next.js) for prompt outputs *(stretch goal)* |

*(Tick each box in a future commit as you implement the feature.)*

---

## Quick start (local)

```bash
git clone https://github.com/<your-user>/promptguard-ci
cd promptguard-ci
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# set your key in the shell or .env file
export OPENAI_API_KEY="sk-..."
promptguard test examples/hello.yml
