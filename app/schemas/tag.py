from datetime import datetime

from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)


class TagRead(BaseModel):
    id: int
    name: str
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TagUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
