from app.constants.enums import CyclePeriods
from sqlalchemy.ext.hybrid import hybrid_property
from app.db.base_class import Base
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Numeric, Enum , Table, DateTime
from sqlalchemy.orm import relationship
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID
import uuid


class ConfigurableOptionCycle(Base):
    __tablename__ = 'configurable_option_cycles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    value_id = Column(UUID, ForeignKey('configurable_option_choices.id'), nullable=True)
    option_id = Column(UUID, ForeignKey('configurable_options.id'), nullable=True)
    cycle = Column(Enum(CyclePeriods), nullable=False, index=True)
    cycle_multiplier = Column(Numeric(8, 2), default=Decimal('1.00'), nullable=False, index=True)
    price = Column(Numeric(14, 2), default=Decimal('0.00'), nullable=False)
    currency_id = Column(UUID, ForeignKey('currencies.id'), nullable=True)
    setup_fee = Column(Numeric(14, 2), default=Decimal('0.00'), nullable=False)
    setup_fee_entire_quantity = Column(Boolean, default=True)
    is_relative_price = Column(Boolean, default=True)

    value = relationship("ConfigurableOptionChoice", back_populates="cycles")
    option = relationship("ConfigurableOption", back_populates="cycles")
    currency = relationship("Currency", back_populates="configurable_option_cycles")
