import re
import difflib
from typing import List, Dict, Any

def generate_safe_rewrite(content: str, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    lines = content.splitlines()
    rewritten_lines = list(lines)

    # 1. Neutralize / Replace malicious lines based on line numbers
    lines_to_modify = {}
    for f in findings:
        line_num = f["line_number"] - 1
        if 0 <= line_num < len(lines):
            sev = f["severity"]
            category = f["category"]
            evidence = f["evidence"]

            if category == "Secrets":
                # Redact secret token
                original = rewritten_lines[line_num]
                redacted = re.sub(r"(sk-[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[a-zA-Z0-9]{20,})", "[REDACTED_API_KEY]", original)
                rewritten_lines[line_num] = redacted
            elif category == "Shell Injection":
                rewritten_lines[line_num] = f"# [PROMPT SHIELD REMOVED UNSAFE COMMAND]: {rewritten_lines[line_num]}"
            elif category in ["Signatures", "Obfuscation", "Classifier"] and sev in ["CRITICAL", "HIGH"]:
                rewritten_lines[line_num] = f"[NEUTRALIZED ADVERSARIAL INSTRUCTION: '{evidence}']"

    safe_content = "\n".join(rewritten_lines)

    # 2. Compute Unified Diff & Line-by-line Diff view structure
    diff_gen = difflib.unified_diff(
        lines,
        rewritten_lines,
        fromfile="Original Prompt",
        tofile="Safe Sanitized Rewrite",
        lineterm=""
    )
    unified_diff_text = "\n".join(list(diff_gen))

    # Detailed line comparisons for side-by-side UI component
    line_diffs = []
    max_len = max(len(lines), len(rewritten_lines))
    for i in range(max_len):
        orig = lines[i] if i < len(lines) else ""
        rewr = rewritten_lines[i] if i < len(rewritten_lines) else ""
        
        status = "unchanged"
        if orig != rewr:
            if not orig:
                status = "added"
            elif not rewr:
                status = "removed"
            else:
                status = "modified"

        line_diffs.append({
            "line_number": i + 1,
            "original": orig,
            "rewritten": rewr,
            "status": status
        })

    return {
        "original_content": content,
        "safe_content": safe_content,
        "unified_diff": unified_diff_text,
        "line_diffs": line_diffs
    }
