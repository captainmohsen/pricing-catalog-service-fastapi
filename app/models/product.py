import uuid
from sqlalchemy import Column, String, Boolean, Enum, Integer, JSON,Text,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.constants.enums import ProductType,PricingModel,ProductAutoSetup,ProvisioningBackend
from app.db.base_class import Base
# from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from app.models.product_configurable_options import ProductConfigurableOption



class Product(Base):
    """
    Defines billable service product. It includes web hosting products, but also domain registration pricing and
    cloud services with utility priced model.
    """
    __tablename__ = 'products'


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    code = Column(String(255), unique=True, index=True, nullable=False)

    group_id = Column(UUID(as_uuid=True), ForeignKey("product_groups.id"), nullable=False)

    product_type = Column(Enum(ProductType), nullable=False)
    price_model = Column(Enum(PricingModel), nullable=False)
    auto_setup = Column(Enum(ProductAutoSetup), default=ProductAutoSetup.disabled, nullable=False)
    provisioning_backend = Column(Enum(ProvisioningBackend), nullable=False)

    status = Column(String(20), default="private", index=True)

    has_quantity = Column(Boolean, default=False)
    available_quantity = Column(Integer, default=0)

    taxable = Column(Boolean, default=False)

    group = relationship("ProductGroup", back_populates="products")
    product_configurable_options = relationship(
        "ProductConfigurableOption", back_populates="product", cascade="all, delete-orphan"
    )

    configurable_options = association_proxy(
        'product_configurable_options',
        'configurable_option',
        creator=lambda option: ProductConfigurableOption(configurable_option=option)
        )
    cycles = relationship("ProductCycle", back_populates="product", cascade="all, delete-orphan")
