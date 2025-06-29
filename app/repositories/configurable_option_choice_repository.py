from decimal import Decimal
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import ConfigurableOption, Product, ConfigurableOptionChoice
from app.constants.enums import ConfigurableOptionWidget, CyclePeriods
from app.schemas.configurable_option_choice import ConfigurableOptionChoiceCreate, ConfigurableOptionChoiceUpdate

class ConfigurableOptionChoiceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self) -> List[ConfigurableOptionChoice]:
        result = await self.db.execute(select(ConfigurableOptionChoice))
        return result.scalars().all()

    async def create(self, data: ConfigurableOptionChoiceCreate) -> ConfigurableOptionChoice:
        choice = ConfigurableOptionChoice(**data.dict())
        self.db.add(choice)
        await self.db.commit()
        await self.db.refresh(choice)
        return choice

    async def update(self, choice_id: str, data: ConfigurableOptionChoiceUpdate) -> Optional[ConfigurableOptionChoice]:
        stmt = select(ConfigurableOptionChoice).where(ConfigurableOptionChoice.id == choice_id)
        result = await self.db.execute(stmt)
        choice = result.scalar_one_or_none()
        if not choice:
            return None
        for field, value in data.dict().items():
            setattr(choice, field, value)
        await self.db.commit()
        await self.db.refresh(choice)
        return choice

    async def delete(self, choice_id: str) -> bool:
        stmt = delete(ConfigurableOptionChoice).where(ConfigurableOptionChoice.id == choice_id)
        await self.db.execute(stmt)
        await self.db.commit()
        return True