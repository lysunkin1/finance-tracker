from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.models.category import TransactionType
from app.schemas.tag import TagRead
from app.schemas.category import CategoryRead


class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0, decimal_places=2)
    type: TransactionType
    description: str | None = Field(default=None, max_length=500)
    date: date
    category_id: int | None = None
    tag_ids: list[int] = Field(default_factory=list)

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v


class TransactionRead(BaseModel):
    id: int
    amount: Decimal
    type: TransactionType
    description: str | None
    date: date
    user_id: int
    category_id: int | None
    category: CategoryRead | None
    tags: list[TagRead]
    created_at: datetime

    model_config = {"from_attributes": True}


class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    type: TransactionType | None = None
    description: str | None = Field(default=None, max_length=500)
    date: date | None = None
    category_id: int | None = None
    tag_ids: list[int] | None = None


class TransactionFilter(BaseModel):
    type: TransactionType | None = None
    category_id: int | None = None
    tag_id: int | None = None
    date_from: date | None = None
    date_to: date | None = None
