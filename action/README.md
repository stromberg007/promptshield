# PromptShield AI - GitHub Action

Integrate static analysis security scanning for prompt templates, system instructions, and AI configuration files directly into your GitHub Actions CI/CD workflows.

## Usage Example

Add the following step to your `.github/workflows/prompt-security.yml`:

```yaml
name: Prompt Security Scan

on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main ]

jobs:
  promptshield-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Run PromptShield AI Scanner
        uses: promptshield/promptshield-action@v1
        with:
          path: "./prompts"
          fail_on_severity: "HIGH"
          max_risk_score: "40"
```
