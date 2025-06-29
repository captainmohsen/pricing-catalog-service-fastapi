import uuid
from sqlalchemy import Column, String, Boolean, Enum, Integer, JSON,Text,Numeric,UniqueConstraint,ForeignKey
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from decimal import Decimal
from app.constants.enums import CyclePeriods,PublicStatuses
from sqlalchemy.dialects.postgresql import UUID


class ProductCycle(Base):
    __tablename__ = 'product_cycles'
    __table_args__ = (
        UniqueConstraint('product_id', 'cycle', 'cycle_multiplier', 'currency_id', name='uq_product_cycle'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    product_id = Column(UUID, ForeignKey('products.id'), nullable=False)
    cycle = Column(Enum(CyclePeriods), nullable=False)
    cycle_multiplier = Column(Numeric(8, 2), default=Decimal('1.00'), nullable=False)
    fixed_price = Column(Numeric(14, 2), default=Decimal('0.00'), nullable=False)
    setup_fee = Column(Numeric(14, 2), default=Decimal('0.00'), nullable=False)
    setup_fee_entire_quantity = Column(Boolean, default=True)
    currency_id = Column(UUID, ForeignKey('currencies.id'), nullable=True)
    is_relative_price = Column(Boolean, default=True)
    status = Column(Enum(PublicStatuses), default=PublicStatuses.public, nullable=False, index=True)

    product = relationship("Product", back_populates="cycles")
    currency = relationship("Currency")
