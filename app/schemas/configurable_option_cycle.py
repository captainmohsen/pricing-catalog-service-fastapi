from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from decimal import Decimal

class ConfigurableOptionCycleBase(BaseModel):
    option_id: Optional[UUID] = None
    value_id: Optional[UUID] = None
    cycle: str
    cycle_multiplier: Decimal
    price: Decimal
    setup_fee: Decimal
    setup_fee_entire_quantity: bool
    is_relative_price: bool
    currency_id: UUID

# class ConfigurableOptionCycle(ConfigurableOptionCycleBase):
#     pass

class ConfigurableOptionCycleCreate(ConfigurableOptionCycleBase):
    pass

class ConfigurableOptionCycleUpdate(ConfigurableOptionCycleBase):
    pass

class ConfigurableOptionCycleRead(ConfigurableOptionCycleBase):
    id: UUID
    class Config:
        orm_mode = True
