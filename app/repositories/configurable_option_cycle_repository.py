from decimal import Decimal
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from sqlalchemy.future import select
from app.models import ConfigurableOptionCycle
from app.schemas.configurable_option_cycle import ConfigurableOptionCycleCreate, ConfigurableOptionCycleUpdate

class ConfigurableOptionCycleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self) -> List[ConfigurableOptionCycle]:
        result = await self.db.execute(select(ConfigurableOptionCycle))
        return result.scalars().all()

    async def create(self, data: ConfigurableOptionCycleCreate) -> ConfigurableOptionCycle:
        cycle = ConfigurableOptionCycle(**data.dict())
        self.db.add(cycle)
        await self.db.commit()
        await self.db.refresh(cycle)
        return cycle

    async def update(self, cycle_id: str, data: ConfigurableOptionCycleUpdate) -> Optional[ConfigurableOptionCycle]:
        stmt = select(ConfigurableOptionCycle).where(ConfigurableOptionCycle.id == cycle_id)
        result = await self.db.execute(stmt)
        cycle = result.scalar_one_or_none()
        if not cycle:
            return None
        for field, value in data.dict().items():
            setattr(cycle, field, value)
        await self.db.commit()
        await self.db.refresh(cycle)
        return cycle

    async def delete(self, cycle_id: str) -> bool:
        stmt = delete(ConfigurableOptionCycle).where(ConfigurableOptionCycle.id == cycle_id)
        await self.db.execute(stmt)
        await self.db.commit()
        return True
