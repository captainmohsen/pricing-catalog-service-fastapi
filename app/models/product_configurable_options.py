from app.db.base_class import Base
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Numeric, Enum as SAEnum, UniqueConstraint, Table, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy.orm import relationship


class ProductConfigurableOption(Base):
    __tablename__ = 'product_configurable_options'
    __table_args__ = (UniqueConstraint('product_id', 'configurable_option_id', name='uq_product_configurable'),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    product_id = Column(UUID, ForeignKey('products.id'), nullable=False)
    configurable_option_id = Column(UUID, ForeignKey('configurable_options.id'), nullable=False)

    product = relationship("Product", back_populates="product_configurable_options")
    configurable_option = relationship("ConfigurableOption", back_populates="product_configurable_options")
