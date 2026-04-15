from datetime import datetime

from pydantic import BaseModel, Field

from app.models.category import TransactionType


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: TransactionType


class CategoryRead(BaseModel):
    id: int
    name: str
    type: TransactionType
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    type: TransactionType | None = None
