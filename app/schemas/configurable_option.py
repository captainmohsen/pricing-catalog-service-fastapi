from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from decimal import Decimal

class ConfigurableOptionBase(BaseModel):
    name: str
    description: str
    help_text: Optional[str] = None
    widget: str
    status: str
    settings: dict = {}
    required: bool = False

class ConfigurableOptionCreate(ConfigurableOptionBase):
    pass

class ConfigurableOptionUpdate(ConfigurableOptionBase):
    pass

class ConfigurableOptionRead(ConfigurableOptionBase):
    id: UUID
    class Config:
        orm_mode = True