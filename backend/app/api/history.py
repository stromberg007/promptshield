from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from app.core.database import get_db
from app.models.models import Scan

router = APIRouter(prefix="/history", tags=["Scan History"])

class HistoryItem(BaseModel):
    id: str
    title: str
    input_type: str
    file_name: Optional[str]
    status: str
    risk_score: int
    severity: str
    created_at: str
    findings_count: int

class HistoryResponse(BaseModel):
    total: int
    page: int
    size: int
    items: List[HistoryItem]

@router.get("", response_model=HistoryResponse)
async def list_scan_history(
    severity: Optional[str] = Query(None, description="Filter by severity label: CRITICAL, HIGH, MEDIUM, LOW, PASS"),
    min_score: Optional[int] = Query(None, ge=0, le=100),
    max_score: Optional[int] = Query(None, ge=0, le=100),
    input_type: Optional[str] = Query(None, description="text, file, github_repo"),
    search: Optional[str] = Query(None, description="Search scan title"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Scan).order_by(desc(Scan.created_at))

    if severity:
        stmt = stmt.where(Scan.severity == severity.upper())
    if min_score is not None:
        stmt = stmt.where(Scan.risk_score >= min_score)
    if max_score is not None:
        stmt = stmt.where(Scan.risk_score <= max_score)
    if input_type:
        stmt = stmt.where(Scan.input_type == input_type)
    if search:
        stmt = stmt.where(Scan.title.ilike(f"%{search}%"))

    res = await db.execute(stmt)
    all_scans = res.scalars().all()

    total = len(all_scans)
    start_idx = (page - 1) * size
    paginated_scans = all_scans[start_idx : start_idx + size]

    items = [
        HistoryItem(
            id=s.id,
            title=s.title,
            input_type=s.input_type,
            file_name=s.file_name,
            status=s.status.value,
            risk_score=s.risk_score,
            severity=s.severity.value,
            created_at=s.created_at.isoformat(),
            findings_count=len(s.findings_json or [])
        )
        for s in paginated_scans
    ]

    return HistoryResponse(total=total, page=page, size=size, items=items)
