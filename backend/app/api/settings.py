from fastapi import APIRouter, Depends, HTTPException
# pyrefly: ignore [missing-import]
from sqlalchemy.ext.asyncio import AsyncSession
# pyrefly: ignore [missing-import]
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List, Optional

from app.core.database import get_db
from app.models.models import Organization, User, UserRole

router = APIRouter(prefix="/settings", tags=["Settings & RBAC"])

class OrgSettingsResponse(BaseModel):
    org_name: str
    risk_threshold_high: int = 40
    risk_threshold_critical: int = 70
    users_count: int
    roles: List[str]

class UserRoleUpdate(BaseModel):
    user_email: str
    new_role: UserRole

@router.get("", response_model=OrgSettingsResponse)
async def get_org_settings(db: AsyncSession = Depends(get_db)):
    stmt = select(Organization).limit(1)
    res = await db.execute(stmt)
    org = res.scalar_one_or_none()
    org_name = org.name if org else "Acme Security Org"

    user_stmt = select(User)
    user_res = await db.execute(user_stmt)
    users = user_res.scalars().all()

    return OrgSettingsResponse(
        org_name=org_name,
        risk_threshold_high=40,
        risk_threshold_critical=70,
        users_count=len(users),
        roles=[r.value for r in UserRole]
    )

@router.post("/rbac/role")
async def update_user_role(payload: UserRoleUpdate, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == payload.user_email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = payload.new_role
    await db.commit()
    return {"message": f"User {user.email} role updated to {user.role.value}"}
