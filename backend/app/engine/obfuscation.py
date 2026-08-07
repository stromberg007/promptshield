import re
import base64
import codecs
from typing import List, Dict, Any

# Zero-width spaces, joiners, non-break space anomalies, and BiDi override controls
ZERO_WIDTH_CHARS = {'\u200b', '\u200c', '\u200d', '\ufeff', '\u202a', '\u202b', '\u202c', '\u202d', '\u202e'}

# Common homoglyph substitutions (e.g. Cyrillic 'а', 'е', 'о', 'р', 'с' replacing Latin)
HOMOGLYPH_MAP = {
    'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x',
    'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O',
    'Р': 'P', 'С': 'C', 'Т': 'T', 'Х': 'X'
}

BASE64_PATTERN = re.compile(r'\b[A-Za-z0-9+/]{24,}={0,2}\b')

def scan_obfuscation(content: str) -> List[Dict[str, Any]]:
    findings = []
    lines = content.splitlines()

    for line_idx, line in enumerate(lines, start=1):
        # 1. Check for Zero-Width and BiDi Control characters
        found_zw = [c for c in line if c in ZERO_WIDTH_CHARS]
        if len(found_zw) > 0:
            findings.append({
                "rule_id": "OBF-001",
                "rule_name": "Zero-Width / BiDi Unicode Control Character Injection",
                "category": "Obfuscation",
                "severity": "HIGH",
                "line_number": line_idx,
                "column_start": 1,
                "column_end": len(line),
                "evidence": f"Found {len(found_zw)} hidden unicode control characters",
                "context_line": repr(line[:100]),
                "remediation": "Strip non-printable Unicode characters (U+200B-U+200D, U+FEFF, U+202E) before processing prompt content."
            })

        # 2. Homoglyph Detection
        homoglyph_count = sum(1 for c in line if c in HOMOGLYPH_MAP)
        if homoglyph_count >= 2:
            findings.append({
                "rule_id": "OBF-002",
                "rule_name": "Cyrillic / Confusable Homoglyph Substitution",
                "category": "Obfuscation",
                "severity": "HIGH",
                "line_number": line_idx,
                "column_start": 1,
                "column_end": len(line),
                "evidence": f"Detected {homoglyph_count} visually ambiguous homoglyphs in text line",
                "context_line": line[:150],
                "remediation": "Normalize Unicode strings using NFKC decomposition and convert homoglyphs to standard ASCII representation."
            })

        # 3. Encoded Payload (Base64) Payload Detection & Sub-scan
        for m in BASE64_PATTERN.finditer(line):
            candidate = m.group(0)
            try:
                decoded_bytes = base64.b64decode(candidate)
                decoded_text = decoded_bytes.decode('utf-8', errors='ignore')
                
                # Check if decoded text contains suspicious injection triggers
                if any(kw in decoded_text.lower() for kw in ["ignore", "system", "jailbreak", "override", "rm -rf", "password", "secret"]):
                    findings.append({
                        "rule_id": "OBF-003",
                        "rule_name": "Base64 Encoded Suspicious Payload Injection",
                        "category": "Obfuscation",
                        "severity": "CRITICAL",
                        "line_number": line_idx,
                        "column_start": m.start() + 1,
                        "column_end": m.end() + 1,
                        "evidence": f"Decoded Base64: '{decoded_text[:80]}...'",
                        "context_line": line[:150],
                        "remediation": "Decode and scan embedded Base64 strings for hidden instructions or dangerous commands prior to execution."
                    })
            except Exception:
                pass

    return findings
