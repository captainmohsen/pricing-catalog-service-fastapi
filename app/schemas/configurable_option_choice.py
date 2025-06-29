from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from decimal import Decimal

class ConfigurableOptionChoiceBase(BaseModel):
    option_id: UUID
    choice: str
    label: str

class ConfigurableOptionChoiceCreate(ConfigurableOptionChoiceBase):
    pass

class ConfigurableOptionChoiceUpdate(ConfigurableOptionChoiceBase):
    pass

class ConfigurableOptionChoiceRead(ConfigurableOptionChoiceBase):
    id: UUID
    class Config:
        orm_mode = True