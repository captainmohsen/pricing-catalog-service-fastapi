from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ProductGroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    visible: bool = True

class ProductGroupCreate(ProductGroupBase):
    pass

class ProductGroupUpdate(ProductGroupBase):
    pass

class ProductGroupRead(ProductGroupBase):
    id: UUID
    class Config:
        orm_mode = True
