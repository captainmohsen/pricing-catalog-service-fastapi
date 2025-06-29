from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from typing import List, Optional
from uuid import UUID

from app.models import ProductGroup
from app.schemas.product_group import ProductGroupCreate, ProductGroupUpdate

class ProductGroupRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self) -> List[ProductGroup]:
        result = await self.db.execute(select(ProductGroup))
        return result.scalars().all()

    async def get(self, group_id: UUID) -> Optional[ProductGroup]:
        result = await self.db.execute(select(ProductGroup).where(ProductGroup.id == group_id))
        return result.scalar_one_or_none()

    async def create(self, payload: ProductGroupCreate) -> ProductGroup:
        new_group = ProductGroup(**payload.dict())
        self.db.add(new_group)
        await self.db.commit()
        await self.db.refresh(new_group)
        return new_group

    async def update(self, group_id: UUID, payload: ProductGroupUpdate) -> Optional[ProductGroup]:
        group = await self.get(group_id)
        if not group:
            return None
        for field, value in payload.dict(exclude_unset=True).items():
            setattr(group, field, value)
        await self.db.commit()
        await self.db.refresh(group)
        return group

    async def delete(self, group_id: UUID) -> bool:
        group = await self.get(group_id)
        if not group:
            return False
        await self.db.delete(group)
        await self.db.commit()
        return True

    async def list_visible(self) -> list[ProductGroup]:
        result = await self.db.execute(
            select(ProductGroup).where(ProductGroup.visible == True)
        )

        return result.scalars().all()