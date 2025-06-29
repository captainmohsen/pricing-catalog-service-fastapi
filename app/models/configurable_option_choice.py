from app.db.base_class import Base
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Numeric, Enum as SAEnum, UniqueConstraint, Table, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid


class ConfigurableOptionChoice(Base):
    __tablename__ = 'configurable_option_choices'
    __table_args__ = (UniqueConstraint('option_id', 'choice', name='uq_option_choice'),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    option_id = Column(UUID, ForeignKey('configurable_options.id'), nullable=False)
    choice = Column(String(64), nullable=False)
    label = Column(String(128), nullable=False)

    option = relationship("ConfigurableOption", back_populates="choices")
    cycles = relationship("ConfigurableOptionCycle", back_populates="value")
    flavor_mirror = relationship("FlavorMirror", back_populates="choice", uselist=False)
