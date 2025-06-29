from pydantic import BaseModel, Field
from decimal import Decimal
from uuid import UUID


class ProductCycleBase(BaseModel):
    product_id: UUID
    cycle: str
    cycle_multiplier: Decimal
    fixed_price: Decimal
    setup_fee: Decimal
    setup_fee_entire_quantity: bool = True
    currency_id: UUID
    is_relative_price: bool = True
    status: str

class ProductCycleCreateSchema(ProductCycleBase):
    pass

class ProductCycleReadSchema(ProductCycleBase):
    id: UUID

    class Config:
        orm_mode = True
