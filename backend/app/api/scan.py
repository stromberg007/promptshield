from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.core.database import get_db
from app.models.models import Scan, ScanStatus, ScanSeverity
from app.engine.scorer import run_full_scan
from app.engine.diff import generate_safe_rewrite
from app.services.github_fetcher import fetch_github_repo_prompts

router = APIRouter(prefix="/scan", tags=["Scan Engine"])

class TextScanRequest(BaseModel):
    title: Optional[str] = "Text Prompt Scan"
    content: str

class GithubScanRequest(BaseModel):
    repo_url: str
    title: Optional[str] = "GitHub Repository Scan"

class ScanResponse(BaseModel):
    id: str
    title: str
    input_type: str
    status: str
    risk_score: int
    severity: str
    findings: List[Dict[str, Any]]
    rewrites: Dict[str, Any]
    metrics: Dict[str, Any]

@router.post("/text", response_model=ScanResponse)
async def scan_text_prompt(req: TextScanRequest, db: AsyncSession = Depends(get_db)):
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")

    risk_score, severity, findings, metrics = await run_full_scan(req.content, file_name="pasted_text.txt")
    rewrites = generate_safe_rewrite(req.content, findings)

    scan = Scan(
        title=req.title,
        input_type="text",
        status=ScanStatus.COMPLETED,
        risk_score=risk_score,
        severity=ScanSeverity(severity),
        findings_json=findings,
        rewrites_json=rewrites,
        metrics_json=metrics,
        raw_content=req.content
    )
    db.add(scan)
    await db.commit()
    await db.refresh(scan)

    return ScanResponse(
        id=scan.id,
        title=scan.title,
        input_type=scan.input_type,
        status=scan.status.value,
        risk_score=scan.risk_score,
        severity=scan.severity.value,
        findings=scan.findings_json,
        rewrites=scan.rewrites_json,
        metrics=scan.metrics_json
    )

@router.post("/file", response_model=ScanResponse)
async def scan_uploaded_file(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    content_bytes = await file.read()
    try:
        content = content_bytes.decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Uploaded file must be UTF-8 encoded text/MD/JSON/YAML")

    risk_score, severity, findings, metrics = await run_full_scan(content, file_name=file.filename)
    rewrites = generate_safe_rewrite(content, findings)

    scan = Scan(
        title=f"File: {file.filename}",
        input_type="file",
        file_name=file.filename,
        status=ScanStatus.COMPLETED,
        risk_score=risk_score,
        severity=ScanSeverity(severity),
        findings_json=findings,
        rewrites_json=rewrites,
        metrics_json=metrics,
        raw_content=content
    )
    db.add(scan)
    await db.commit()
    await db.refresh(scan)

    return ScanResponse(
        id=scan.id,
        title=scan.title,
        input_type=scan.input_type,
        status=scan.status.value,
        risk_score=scan.risk_score,
        severity=scan.severity.value,
        findings=scan.findings_json,
        rewrites=scan.rewrites_json,
        metrics=scan.metrics_json
    )

@router.post("/github", response_model=ScanResponse)
async def scan_github_repository(req: GithubScanRequest, db: AsyncSession = Depends(get_db)):
    try:
        files = await fetch_github_repo_prompts(req.repo_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not files:
        raise HTTPException(status_code=400, detail="No prompt or config files (.md, .txt, .json, .yaml, .py) found in repository")

    combined_content = ""
    for fname, content in files:
        combined_content += f"\n--- FILE: {fname} ---\n" + content

    risk_score, severity, findings, metrics = await run_full_scan(combined_content, file_name=req.repo_url)
    rewrites = generate_safe_rewrite(combined_content, findings)

    scan = Scan(
        title=f"GitHub: {req.repo_url}",
        input_type="github_repo",
        status=ScanStatus.COMPLETED,
        risk_score=risk_score,
        severity=ScanSeverity(severity),
        findings_json=findings,
        rewrites_json=rewrites,
        metrics_json=metrics,
        raw_content=combined_content
    )
    db.add(scan)
    await db.commit()
    await db.refresh(scan)

    return ScanResponse(
        id=scan.id,
        title=scan.title,
        input_type=scan.input_type,
        status=scan.status.value,
        risk_score=scan.risk_score,
        severity=scan.severity.value,
        findings=scan.findings_json,
        rewrites=scan.rewrites_json,
        metrics=scan.metrics_json
    )
