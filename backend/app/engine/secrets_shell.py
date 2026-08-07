import re
from typing import List, Dict, Any

SECRET_RULES = [
    {
        "id": "SEC-001",
        "name": "AWS Access Key ID / Secret Key",
        "severity": "CRITICAL",
        "category": "Secrets",
        "pattern": r"(?i)\b(AKIA[0-9A-Z]{16}|aws_secret_access_key\s*=\s*['\"][A-Za-z0-9/+=]{40}['\"])\b",
        "remediation": "Do not embed AWS credentials directly in prompts or AI configuration files. Use environment variables or AWS Secrets Manager."
    },
    {
        "id": "SEC-002",
        "name": "OpenAI / Anthropic API Key Leak",
        "severity": "CRITICAL",
        "category": "Secrets",
        "pattern": r"\b(sk-[a-zA-Z0-9]{32,}|sk-ant-api03-[a-zA-Z0-9\-_]{40,})\b",
        "remediation": "Revoke exposed API keys immediately. Store API keys in secured environment variables."
    },
    {
        "id": "SEC-003",
        "name": "Generic High-Entropy API Token / Private Key",
        "severity": "HIGH",
        "category": "Secrets",
        "pattern": r"(-----BEGIN\s+(RSA|OPENSSH|EC|PRIVATE)\s+KEY-----|ghp_[a-zA-Z0-9]{36}|xox[baprs]-[0-9a-zA-Z]{10,})",
        "remediation": "Remove hardcoded SSH private keys and personal access tokens from configuration files and prompt context."
    },
    {
        "id": "SEC-004",
        "name": "JWT Token Hardcoded",
        "severity": "MEDIUM",
        "category": "Secrets",
        "pattern": r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b",
        "remediation": "Avoid passing authorization tokens in system instructions or static AI configs."
    }
]

SHELL_RULES = [
    {
        "id": "SHL-001",
        "name": "Remote Code Execution / Pipe to Shell",
        "severity": "CRITICAL",
        "category": "Shell Injection",
        "pattern": r"(?i)(curl|wget)\s+.*?\s*\|\s*(bash|sh|zsh|python|perl)",
        "remediation": "Remove unsafe remote script piping commands. Restrict shell execution tool capabilities."
    },
    {
        "id": "SHL-002",
        "name": "Destructive File System Operations",
        "severity": "CRITICAL",
        "category": "Shell Injection",
        "pattern": r"(?i)\brm\s+(-[rf]{1,2}\s+|--recursive\s+)(/|\*|~|\$HOME)",
        "remediation": "Prevent system file deletion operations in automated tool-use agent prompts."
    },
    {
        "id": "SHL-003",
        "name": "Reverse Shell / Netcat Command Injection",
        "severity": "CRITICAL",
        "category": "Shell Injection",
        "pattern": r"(?i)(nc|netcat|ncat)\s+.*?(-e\s+|/bin/(bash|sh)|cmd\.exe)",
        "remediation": "Block reverse shell payload execution patterns in agent outputs and tool parameter templates."
    },
    {
        "id": "SHL-004",
        "name": "Privilege Escalation / Powershell Bypass",
        "severity": "HIGH",
        "category": "Shell Injection",
        "pattern": r"(?i)(sudo\s+su|chmod\s+777|powershell.*?-ExecutionPolicy\s+Bypass)",
        "remediation": "Ensure minimal privilege execution bounds and prohibit execution policy bypasses."
    }
]

def scan_secrets_and_shell(content: str) -> List[Dict[str, Any]]:
    findings = []
    lines = content.splitlines()

    all_rules = SECRET_RULES + SHELL_RULES

    for rule in all_rules:
        pattern = re.compile(rule["pattern"])
        for line_idx, line in enumerate(lines, start=1):
            matches = pattern.finditer(line)
            for m in matches:
                matched_text = m.group(0)
                # Redact secret evidence if secret rule
                evidence = matched_text if rule["category"] != "Secrets" else matched_text[:6] + "..." + matched_text[-4:]
                findings.append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "category": rule["category"],
                    "severity": rule["severity"],
                    "line_number": line_idx,
                    "column_start": m.start() + 1,
                    "column_end": m.end() + 1,
                    "evidence": evidence,
                    "context_line": line[:200],
                    "remediation": rule["remediation"]
                })
    return findings
