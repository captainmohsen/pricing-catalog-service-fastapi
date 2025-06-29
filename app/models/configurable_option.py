from datetime import datetime
from app.db.base_class import Base
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Numeric, Enum as SAEnum, UniqueConstraint, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.associationproxy import association_proxy



class ConfigurableOption(Base):
    __tablename__ = 'configurable_options'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(64), nullable=False, index=True)
    description = Column(String(128), nullable=False)
    help_text = Column(String(255), nullable=True)
    widget = Column(String(12), nullable=False, index=True)
    status = Column(String(8), nullable=False, index=True)
    settings = Column(JSONB, default=dict)
    required = Column(Boolean, default=False)

    choices = relationship("ConfigurableOptionChoice", back_populates="option")
    cycles = relationship("ConfigurableOptionCycle", back_populates="option")

    product_configurable_options = relationship(
        "ProductConfigurableOption", back_populates="configurable_option", cascade="all, delete-orphan"
    )

    products = association_proxy(
        "product_configurable_options", "product"
    )
