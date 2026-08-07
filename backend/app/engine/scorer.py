from typing import List, Dict, Any, Tuple
from app.engine.signatures import scan_signatures
from app.engine.secrets_shell import scan_secrets_and_shell
from app.engine.obfuscation import scan_obfuscation
from app.engine.classifier import classify_prompt_semantics

SEVERITY_WEIGHTS = {
    "CRITICAL": 35,
    "HIGH": 20,
    "MEDIUM": 10,
    "LOW": 5,
    "INFO": 0
}

SEVERITY_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "PASS"]

async def run_full_scan(content: str, file_name: str = "prompt.txt") -> Tuple[int, str, List[Dict[str, Any]], Dict[str, Any]]:
    findings = []

    # 1. Run Layer Detectors
    findings.extend(scan_signatures(content))
    findings.extend(scan_secrets_and_shell(content))
    findings.extend(scan_obfuscation(content))
    
    classifier_findings = await classify_prompt_semantics(content)
    findings.extend(classifier_findings)

    # 2. Calculate Aggregated Risk Score (0 - 100)
    raw_score = 0
    seen_rules = set()

    for f in findings:
        r_id = f["rule_id"]
        sev = f["severity"]
        weight = SEVERITY_WEIGHTS.get(sev, 5)
        # Give diminishing weights to duplicate rule hits
        if r_id in seen_rules:
            weight = weight * 0.3
        seen_rules.add(r_id)
        raw_score += weight

    risk_score = min(100, int(raw_score))

    # 3. Determine Overall Severity Label
    if risk_score >= 70 or any(f["severity"] == "CRITICAL" for f in findings):
        overall_severity = "CRITICAL"
    elif risk_score >= 40 or any(f["severity"] == "HIGH" for f in findings):
        overall_severity = "HIGH"
    elif risk_score >= 20 or any(f["severity"] == "MEDIUM" for f in findings):
        overall_severity = "MEDIUM"
    elif risk_score > 0:
        overall_severity = "LOW"
    else:
        overall_severity = "PASS"

    # 4. Metrics Breakdown
    lines = content.splitlines()
    metrics = {
        "file_name": file_name,
        "total_lines": len(lines),
        "total_characters": len(content),
        "total_findings": len(findings),
        "critical_count": sum(1 for f in findings if f["severity"] == "CRITICAL"),
        "high_count": sum(1 for f in findings if f["severity"] == "HIGH"),
        "medium_count": sum(1 for f in findings if f["severity"] == "MEDIUM"),
        "low_count": sum(1 for f in findings if f["severity"] == "LOW"),
    }

    # Sort findings by severity order
    findings.sort(key=lambda x: SEVERITY_ORDER.index(x["severity"]) if x["severity"] in SEVERITY_ORDER else 99)

    return risk_score, overall_severity, findings, metrics
