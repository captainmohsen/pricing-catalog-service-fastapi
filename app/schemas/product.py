from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from app.constants.enums import ProvisioningBackend
from .product_group import ProductGroupRead
from .configurable_option import ConfigurableOptionRead
from .product_cycle import ProductCycleBase
from uuid import UUID


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    code: str
    group_id: UUID
    product_type: str
    status: str
    price_model: str
    auto_setup: str
    has_quantity: bool = False
    available_quantity: int = 0
    taxable: bool = False
    provisioning_backend: ProvisioningBackend


class ProductCreateSchema(ProductBase):
    configurable_options: Optional[list[str]] = []


class ProductUpdateSchema(ProductBase):
    configurable_options: Optional[list[str]] = []


class ProductAdminSchema(ProductBase):
    id: UUID
    #TODO:chedck this part for lazy load
    # group: ProductGroupRead
    # configurable_options: list[ConfigurableOptionRead] = []
    # cycles: list[ProductCycleBase] = []

    class Config:
        orm_mode = True

