from sqlalchemy import Column, String, Integer, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.db.base_class import Base


class FlavorMirror(Base):
    __tablename__ = "flavor_mirrors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    flavor_id = Column(String, unique=True, nullable=False)  # External flavor ID (e.g., OpenStack ID)
    label = Column(String, nullable=False)
    vcpus = Column(Integer)
    ram_mb = Column(Integer)
    disk_gb = Column(Integer)
    tags = Column(ARRAY(String))  # e.g., ["economy", "cpu-optimized"]

    # Relationship to pricing choice
    configurable_option_choice_id = Column(UUID, ForeignKey("configurable_option_choices.id"), nullable=True)
    choice = relationship("ConfigurableOptionChoice", back_populates="flavor_mirror", uselist=False)