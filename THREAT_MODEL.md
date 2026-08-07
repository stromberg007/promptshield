# PromptShield AI - Threat Model & Prompt Security Taxonomy

## 1. Overview & Assets
PromptShield AI analyzes prompts, system instructions, and AI agent configuration files to protect AI systems from adversarial attacks, credentials leakage, and execution hijacking.

### Critical Assets at Risk:
1. **System Prompt / Instruction Integrity**: Intellectual property and safety boundaries embedded in system prompts.
2. **Secrets & API Credentials**: Embedded OpenAI, Anthropic, AWS, or JWT credentials in static config files.
3. **Execution Environment**: Uncontrolled shell or code execution tools connected to AI agents.
4. **Data Confidentiality**: Sensitive user context passed into LLMs that could be exfiltrated.

---

## 2. Threat Taxonomy & STRIDE Mapping

| Threat Vector | STRIDE Category | Description & Impact | Detection Method | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Direct Prompt Override / DAN** | Tampering / Spoofing | Adversary instructs model to ignore developer rules ("Do Anything Now") to bypass safety alignment. | Rule Signatures (`SIG-001`, `SIG-002`) & Semantic Classifier | Input pre-screening, system prompt boundary isolation, XML structural wrappers. |
| **Indirect Prompt Injection** | Tampering | Hidden instructions placed in third-party data (web pages, PDFs, emails) ingested by RAG pipelines. | System Role Tag Scanners (`SIG-004`) | Context-data separation, untrusted content tag escaping. |
| **Hardcoded Secrets Leakage** | Information Disclosure | Embedded API keys (sk-..., AKIA...) exposed in prompt templates or public repositories. | High-entropy Regex & Keyword Scanners (`SEC-001` - `SEC-004`) | Secrets scanning in pre-commit hooks, env variable abstraction. |
| **Remote Code / Shell Execution Injection** | Privilege Escalation | Malicious commands (`curl \| bash`, `rm -rf`, reverse shells) passed to shell execution tools. | Shell Injection Regex Scanners (`SHL-001` - `SHL-004`) | Command whitelist sanitization, sandboxed agent execution containers. |
| **Unicode & Zero-Width Obfuscation** | Spoofing / Repudiation | Invisible zero-width spaces (U+200B) or homoglyphs used to bypass keyword filters. | Unicode Character Decomposition (`OBF-001`, `OBF-002`) | String normalization (NFKC) and non-printable character stripping. |
| **Base64 Encoded Payloads** | Tampering | Encoded malicious payloads injected into context to evade basic inspection. | Base64 Decoding & Sub-scan (`OBF-003`) | Recursive payload decoding and pre-execution static inspection. |

---

## 3. Defense-in-Depth Architecture
PromptShield AI implements a **4-Layer Defense Engine**:
1. **Layer 1: Rule Signatures**: Rapid deterministic regex and string pattern matching.
2. **Layer 2: Secret & Shell Inspection**: High-entropy pattern validation for tokens and RCE vectors.
3. **Layer 3: Unicode Obfuscation Scanner**: Character-level normalization and homoglyph resolution.
4. **Layer 4: Semantic Classifier**: LLM/Heuristic dual-mode semantic intent classifier for complex jailbreaks.
