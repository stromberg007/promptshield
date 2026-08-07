# PromptShield AI - Static Analysis Security Scanner for Prompts & AI Configs

**PromptShield AI** is an enterprise-grade static analysis security scanner built to detect security risks in prompts, system instructions, AI agent configs, and LLM application files.

---

## 🌟 Key Features

- **Multi-Input Scanning**:
  - **Text Paste**: Interactive editor with sample presets (DAN jailbreak, secret leaks, benign prompts).
  - **File Upload**: Native scanning for `.md`, `.txt`, `.json`, `.yaml`, `.yml`, and `.py` files.
  - **GitHub Repo Scanner**: Automated cloning & static analysis of prompt templates across entire Git repositories.
- **Multilayer Detection Engine**:
  - **Layer 1: Rule Signatures**: Scans for system prompt overrides, DAN jailbreaks, roleplay tricks, and exfiltration attempts.
  - **Layer 2: Secrets & Shell Injection**: High-entropy regex detector for API keys (OpenAI, Anthropic, AWS, Slack, JWT) and dangerous Unix/PowerShell shell execution (`curl | bash`, `rm -rf`, reverse shells).
  - **Layer 3: Unicode & Obfuscation**: Zero-width character detection (U+200B-U+200D), Cyrillic homoglyph resolution, and Base64 encoded payload decoding & sub-scanning.
  - **Layer 4: Semantic Classifier**: Dual-mode heuristic intent classifier + optional Gemini/OpenAI deep semantic scanning.
- **Actionable Vulnerability Output**:
  - **0-100 Risk Score Gauge**: Unified risk rating with severity badges (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `PASS`).
  - **Line & Column Level Evidence**: Line numbers, character indices, context lines, and remediation guidance.
  - **Safe Rewrite & Diff View**: Side-by-side visual diff showing original vs. sanitized prompt.
- **SaaS Dashboard & Enterprise Controls**:
  - **Scan History**: Full audit logs with filters (severity, score range, input type, search query).
  - **Multi-Format Export**: One-click download of **PDF**, **HTML**, and **JSON** security reports.
  - **Org Settings & RBAC**: Role-Based Access Control (Admin, Security Engineer, Viewer) and API token management.
- **Developer Ecosystem**:
  - **REST API**: Clean FastAPI REST endpoints (`/scan/text`, `/scan/file`, `/scan/github`, `/history`, `/reports`, `/export`).
  - **GitHub Action**: Reusable CI action in `action/action.yml`.
  - **Golden Corpus**: Benchmark dataset in `backend/tests/corpus/samples.json`.
  - **Threat Model**: Comprehensive STRIDE prompt security taxonomy in `THREAT_MODEL.md`.

---

## 🚀 Quick Start (Local & Docker)

### Option 1: Docker Compose (Recommended)

```bash
docker-compose up --build
```
- **Frontend Dashboard**: `http://localhost:3000`
- **Backend API & Swagger Docs**: `http://localhost:8000/docs`

---

### Option 2: Local Python + Next.js Setup

#### 1. Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### 2. Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```
Navigate to `http://localhost:3000`.

---

## 🧪 Running Detector Unit Tests & Golden Corpus Benchmark

```bash
cd backend
pytest tests/ -v
```

---

## 📄 License
MIT License. Developed for enterprise prompt security and AI application safety.
