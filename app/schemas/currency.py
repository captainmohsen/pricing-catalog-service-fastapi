from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal

class CurrencyBase(BaseModel):
    code: str
    rate: Decimal
    is_default: bool

class CurrencyCreate(CurrencyBase):
    pass

class CurrencyUpdate(CurrencyBase):
    pass

class CurrencyRead(CurrencyBase):
    id: UUID

    class Config:
        orm_mode = True
