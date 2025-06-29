from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from typing import List, Optional
from app.constants.enums import CyclePeriods

class ConfigurableOptionCycleSchema(BaseModel):
    cycle: CyclePeriods
    cycle_multiplier: Decimal
    price: Decimal
    setup_fee: Decimal

    class Config:
        from_attributes = True


class ConfigurableOptionChoiceSchema(BaseModel):
    id: UUID
    choice: str
    label: str
    cycles: List[ConfigurableOptionCycleSchema]

    class Config:
        from_attributes = True


class ConfigurableOptionSchema(BaseModel):
    id: UUID
    name: str
    description: str
    widget: str
    required: bool
    choices: List[ConfigurableOptionChoiceSchema] = []
    cycles: List[ConfigurableOptionCycleSchema] = []

    class Config:
        from_attributes = True


class ProductExposeSchema(BaseModel):
    id: UUID
    name: str
    code: str
    price_model: str
    configurable_options: List[ConfigurableOptionSchema]

    class Config:
        from_attributes = True

class FlavorMirrorSchema(BaseModel):
    id: UUID
    openstack_id: str
    name: str
    vcpus: int
    ram: int
    disk: int
    tag: Optional[str]
    choice_id: UUID
