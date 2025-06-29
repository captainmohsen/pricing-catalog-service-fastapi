import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Integer, JSON,Text,Numeric
from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship



class ProductGroup(Base):
    __tablename__ = 'product_groups'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(64), unique=True, nullable=False, index=True)
    description = Column(String(2048), nullable=False)
    visible = Column(Boolean, default=True)

    products = relationship("Product", back_populates="group")