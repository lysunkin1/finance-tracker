from decimal import Decimal

from pydantic import BaseModel


class CategoryStat(BaseModel):
    category_id: int | None
    category_name: str | None
    total: Decimal
    count: int


class MonthlyStats(BaseModel):
    year: int
    month: int
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
    income_by_category: list[CategoryStat]
    expense_by_category: list[CategoryStat]


class YearlySummary(BaseModel):
    year: int
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
    months: list[dict]
