from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from app.core.database import get_db
from app.models.models import Scan

router = APIRouter(prefix="/reports", tags=["Reports"])

class ReportDetailResponse(BaseModel):
    id: str
    title: str
    input_type: str
    file_name: Optional[str]
    status: str
    risk_score: int
    severity: str
    created_at: str
    raw_content: Optional[str]
    findings: List[Dict[str, Any]]
    rewrites: Dict[str, Any]
    metrics: Dict[str, Any]

@router.get("/{scan_id}", response_model=ReportDetailResponse)
async def get_scan_report(scan_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Scan).where(Scan.id == scan_id)
    res = await db.execute(stmt)
    scan = res.scalar_one_or_none()

    if not scan:
        raise HTTPException(status_code=404, detail="Scan report not found")

    return ReportDetailResponse(
        id=scan.id,
        title=scan.title,
        input_type=scan.input_type,
        file_name=scan.file_name,
        status=scan.status.value,
        risk_score=scan.risk_score,
        severity=scan.severity.value,
        created_at=scan.created_at.isoformat(),
        raw_content=scan.raw_content,
        findings=scan.findings_json or [],
        rewrites=scan.rewrites_json or {},
        metrics=scan.metrics_json or {}
    )
