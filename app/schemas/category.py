from datetime import datetime
from typing import Optional

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
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    type: Optional[TransactionType] = None
