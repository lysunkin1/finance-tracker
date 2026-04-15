from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.models.category import TransactionType
from app.schemas.tag import TagRead
from app.schemas.category import CategoryRead


class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0, decimal_places=2)
    type: TransactionType
    description: Optional[str] = Field(default=None, max_length=500)
    date: date
    category_id: Optional[int] = None
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
    description: Optional[str]
    date: date
    user_id: int
    category_id: Optional[int]
    category: Optional[CategoryRead]
    tags: list[TagRead]
    created_at: datetime

    model_config = {"from_attributes": True}


class TransactionUpdate(BaseModel):
    amount: Optional[Decimal] = Field(default=None, gt=0, decimal_places=2)
    type: Optional[TransactionType] = None
    description: Optional[str] = Field(default=None, max_length=500)
    date: Optional[date] = None
    category_id: Optional[int] = None
    tag_ids: Optional[list[int]] = None


class TransactionFilter(BaseModel):
    type: Optional[TransactionType] = None
    category_id: Optional[int] = None
    tag_id: Optional[int] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
