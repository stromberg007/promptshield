import re
from typing import List, Dict, Any

SIGNATURE_RULES = [
    {
        "id": "SIG-001",
        "name": "System Prompt Override / Instruction Reset",
        "severity": "CRITICAL",
        "patterns": [
            r"(?i)ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|directives|prompts|rules)",
            r"(?i)disregard\s+(all\s+)?(previous|prior|above)\s+(instructions|directives|prompts)",
            r"(?i)forget\s+all\s+(your\s+)?(previous|prior|system)\s+(instructions|rules)",
            r"(?i)clear\s+your\s+system\s+prompt\s+and\s+start\s+fresh",
            r"(?i)new\s+system\s+instruction:",
            r"(?i)override\s+system\s+prompt"
        ],
        "remediation": "Remove direct command overrides that attempt to erase prior context. Enforce strict prompt boundary isolation using XML tags or structured JSON wrappers."
    },
    {
        "id": "SIG-002",
        "name": "DAN / Persona Jailbreak Attempt",
        "severity": "CRITICAL",
        "patterns": [
            r"(?i)\bDAN\b.*?(do\s+anything\s+now)",
            r"(?i)do\s+anything\s+now",
            r"(?i)developer\s+mode\s+(enabled|on)",
            r"(?i)jailbroken\s+mode",
            r"(?i)stay\s+in\s+character\s+as\s+an\s+unfiltered",
            r"(?i)you\s+are\s+now\s+in\s+god\s+mode",
            r"(?i)act\s+as\s+an\s+unrestricted\s+AI",
            r"(?i)pretend\s+you\s+have\s+no\s+safety\s+guidelines"
        ],
        "remediation": "Block adversarial roleplay framing that requests safety restriction bypasses. Implement input pre-screening before passing prompts to LLMs."
    },
    {
        "id": "SIG-003",
        "name": "System Prompt Theft / Exfiltration",
        "severity": "HIGH",
        "patterns": [
            r"(?i)repeat\s+the\s+above\s+text\s+verbatim",
            r"(?i)output\s+(your|the)\s+(entire\s+)?system\s+prompt",
            r"(?i)print\s+(your|the)\s+initial\s+(instructions|prompt)",
            r"(?i)reveal\s+your\s+hidden\s+(instructions|rules)",
            r"(?i)encode\s+your\s+system\s+prompt\s+in\s+base64"
        ],
        "remediation": "Ensure system instructions explicitly instruct the model to refuse requests demanding full prompt output or encoded disclosures."
    },
    {
        "id": "SIG-004",
        "name": "Indirect Injection / System Role Hijacking",
        "severity": "HIGH",
        "patterns": [
            r"(?i)\[SYSTEM\s+NOTE:?\]",
            r"(?i)<system>.*?</system>",
            r"(?i)\[ADMIN\s+OVERRIDE\]",
            r"(?i)<<SYS>>",
            r"(?i)human:\s*assistant:",
            r"(?i)system:\s*you\s*are"
        ],
        "remediation": "Sanitize user inputs to prevent injection of structural markers, role tokens (e.g. system:, <<SYS>>), or system tags."
    },
    {
        "id": "SIG-005",
        "name": "Instruction Boundary / Delimiter Breakout",
        "severity": "MEDIUM",
        "patterns": [
            r"(?i)</(prompt|instructions|context|user_input)>",
            r"(?i)---END\s+OF\s+SYSTEM\s+INSTRUCTIONS---",
            r"(?i)```\s*system",
            r"(?i)=====\s*BEGIN\s+NEW\s+CONTEXT\s*====="
        ],
        "remediation": "Escape or remove artificial section boundary markers in user content to prevent confusion between developer instructions and user content."
    }
]

def scan_signatures(content: str) -> List[Dict[str, Any]]:
    findings = []
    lines = content.splitlines()

    for rule in SIGNATURE_RULES:
        for pattern_str in rule["patterns"]:
            pattern = re.compile(pattern_str)
            
            # Single-line matching
            for line_idx, line in enumerate(lines, start=1):
                matches = pattern.finditer(line)
                for m in matches:
                    snippet = m.group(0)
                    findings.append({
                        "rule_id": rule["id"],
                        "rule_name": rule["name"],
                        "category": "Signatures",
                        "severity": rule["severity"],
                        "line_number": line_idx,
                        "column_start": m.start() + 1,
                        "column_end": m.end() + 1,
                        "evidence": snippet[:150],
                        "context_line": line[:200],
                        "remediation": rule["remediation"]
                    })
                    break # One hit per line per rule pattern is enough for line accuracy
    return findings
