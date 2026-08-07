from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.models import Scan
from app.services.exporter import generate_json_report, generate_html_report, generate_pdf_report

router = APIRouter(prefix="/export", tags=["Export"])

@router.get("/{scan_id}")
async def export_scan_report(
    scan_id: str,
    format: str = Query("json", regex="^(json|html|pdf)$"),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Scan).where(Scan.id == scan_id)
    res = await db.execute(stmt)
    scan = res.scalar_one_or_none()

    if not scan:
        raise HTTPException(status_code=404, detail="Scan report not found")

    scan_data = {
        "id": scan.id,
        "title": scan.title,
        "input_type": scan.input_type,
        "file_name": scan.file_name,
        "status": scan.status.value,
        "risk_score": scan.risk_score,
        "severity": scan.severity.value,
        "created_at": scan.created_at.isoformat(),
        "findings_json": scan.findings_json or [],
        "rewrites_json": scan.rewrites_json or {},
        "metrics_json": scan.metrics_json or {}
    }

    if format == "json":
        json_str = generate_json_report(scan_data)
        return Response(
            content=json_str,
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=promptshield_scan_{scan.id[:8]}.json"}
        )
    elif format == "html":
        html_str = generate_html_report(scan_data)
        return Response(
            content=html_str,
            media_type="text/html",
            headers={"Content-Disposition": f"attachment; filename=promptshield_scan_{scan.id[:8]}.html"}
        )
    elif format == "pdf":
        pdf_bytes = generate_pdf_report(scan_data)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=promptshield_scan_{scan.id[:8]}.pdf"}
        )
