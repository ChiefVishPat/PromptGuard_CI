# PromptGuard CI

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
# run all example specs in the directory
promptguard test examples/ --junit-output results.xml
```

## Features

- Define prompt tests in **YAML**
- Run them locally or in **GitHub Actions**
- Emit **JUnit XML** so CI fails when tests regress
- Built‑in assertions: `contains`, `not_contains`, `json_valid`, `toxicity < 0.2`

See `examples/hello.yml` for a basic example. For more use cases, check additional specs in the `examples/` directory:
```
examples/contains_not_contains.yml
examples/json_valid.yml
examples/toxicity.yml
examples/all_checks.yml
examples/simple.yml
examples/complex.yml
```

## Troubleshooting

### SSL certificate verification failures

On macOS, you may see an error like:

```text
URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate>
```

This indicates your Python environment lacks the necessary root CAs. To fix:

- Run the macOS certificate installer (if using the python.org installer):

  ```bash
  /Applications/Python\ 3.x/Install\ Certificates.command
  ```

- Or ensure you have the `certifi` package installed (it’s a dependency), and set the environment variable:

  ```bash
  export SSL_CERT_FILE=$(python3 -m certifi)
  ```
