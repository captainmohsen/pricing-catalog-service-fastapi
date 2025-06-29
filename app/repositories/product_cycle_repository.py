from decimal import Decimal
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.product_cycle import ProductCycle


class ProductCycleRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def list_all(self) -> list[ProductCycle]:
        result = await self.db.execute(select(ProductCycle).order_by(ProductCycle.id))
        return result.scalars().all()

    async def get_by_id(self, cycle_id: int) -> Optional[ProductCycle]:
        return await self.db.get(ProductCycle, cycle_id)

    async def create(self, payload: dict) -> ProductCycle:
        new_cycle = ProductCycle(**payload)
        self.db.add(new_cycle)
        await self.db.commit()
        await self.db.refresh(new_cycle)
        return new_cycle

    async def delete(self, cycle_id: int) -> bool:
        cycle = await self.db.get(ProductCycle, cycle_id)
        if not cycle:
            return False
        await self.db.delete(cycle)
        await self.db.commit()
        return True