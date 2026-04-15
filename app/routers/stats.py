from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.stats import MonthlyStats, YearlySummary
from app.services.stats import get_monthly_stats, get_yearly_summary

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("/monthly", response_model=MonthlyStats)
async def monthly_stats(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_monthly_stats(db, current_user.id, year, month)


@router.get("/yearly", response_model=YearlySummary)
async def yearly_summary(
    year: int = Query(..., ge=2000, le=2100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_yearly_summary(db, current_user.id, year)
