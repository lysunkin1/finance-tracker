from decimal import Decimal

from sqlalchemy import extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category, TransactionType
from app.models.transaction import Transaction
from app.schemas.stats import CategoryStat, MonthlyStats, YearlySummary


async def get_monthly_stats(db: AsyncSession, user_id: int, year: int, month: int) -> MonthlyStats:
    base_query = (
        select(
            Transaction.category_id,
            Category.name.label("category_name"),
            func.sum(Transaction.amount).label("total"),
            func.count(Transaction.id).label("count"),
            Transaction.type,
        )
        .outerjoin(Category, Transaction.category_id == Category.id)
        .where(
            Transaction.user_id == user_id,
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month,
        )
        .group_by(Transaction.category_id, Category.name, Transaction.type)
    )

    result = await db.execute(base_query)
    rows = result.all()

    total_income = Decimal("0")
    total_expense = Decimal("0")
    income_by_category: list[CategoryStat] = []
    expense_by_category: list[CategoryStat] = []

    for row in rows:
        stat = CategoryStat(
            category_id=row.category_id,
            category_name=row.category_name,
            total=Decimal(str(row.total)),
            count=row.count,
        )
        if row.type == TransactionType.income:
            total_income += stat.total
            income_by_category.append(stat)
        else:
            total_expense += stat.total
            expense_by_category.append(stat)

    return MonthlyStats(
        year=year,
        month=month,
        total_income=total_income,
        total_expense=total_expense,
        balance=total_income - total_expense,
        income_by_category=income_by_category,
        expense_by_category=expense_by_category,
    )


async def get_yearly_summary(db: AsyncSession, user_id: int, year: int) -> YearlySummary:
    query = (
        select(
            extract("month", Transaction.date).label("month"),
            Transaction.type,
            func.sum(Transaction.amount).label("total"),
        )
        .where(
            Transaction.user_id == user_id,
            extract("year", Transaction.date) == year,
        )
        .group_by(extract("month", Transaction.date), Transaction.type)
        .order_by(extract("month", Transaction.date))
    )

    result = await db.execute(query)
    rows = result.all()

    monthly_data: dict[int, dict] = {
        m: {"month": m, "income": Decimal("0"), "expense": Decimal("0")} for m in range(1, 13)
    }

    for row in rows:
        m = int(row.month)
        if row.type == TransactionType.income:
            monthly_data[m]["income"] += Decimal(str(row.total))
        else:
            monthly_data[m]["expense"] += Decimal(str(row.total))

    total_income = sum(v["income"] for v in monthly_data.values())
    total_expense = sum(v["expense"] for v in monthly_data.values())

    months = [
        {
            "month": v["month"],
            "income": v["income"],
            "expense": v["expense"],
            "balance": v["income"] - v["expense"],
        }
        for v in monthly_data.values()
    ]

    return YearlySummary(
        year=year,
        total_income=total_income,
        total_expense=total_expense,
        balance=total_income - total_expense,
        months=months,
    )
