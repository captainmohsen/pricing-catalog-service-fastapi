from sqlalchemy import Column, String, Boolean, Numeric,text
from sqlalchemy.orm import validates
from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Currency(Base):
    __tablename__ = "currencies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    code = Column(String(3), unique=True, nullable=False, index=True)
    rate = Column(Numeric(12, 6), default=1)
    is_default = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "code": self.code,
            "rate": str(self.rate),
            "is_default": self.is_default,
        }
    ##TODO: remove this validator from here and put in better place
    @validates("is_default")
    def ensure_only_one_default(self, key, value):
        if value:
            from app.db.session import SessionLocal
            import asyncio

            async def unset_others():
                async with SessionLocal() as session:
                    await session.execute(
                        text("UPDATE currencies SET is_default = false WHERE code != :code"),
                        {"code": self.code}
                    )
                    await session.commit()

            asyncio.create_task(unset_others())
        return value

    configurable_option_cycles = relationship("ConfigurableOptionCycle", back_populates="currency")

    def __str__(self):
        return self.code

