from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class RegionBase(BaseModel):
    name: str
    note: Optional[str] = None

class RegionCreate(RegionBase):
    pass

class RegionUpdate(BaseModel):
    name: Optional[str] = None
    note: Optional[str] = None

class RegionResponse(RegionBase):
    pk_id: int
    created_at: datetime
    last_modified_at: datetime
    is_deleted: bool

    class Config:
        orm_mode = True