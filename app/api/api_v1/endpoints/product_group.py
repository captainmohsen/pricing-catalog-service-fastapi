from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.api.deps import get_db
from app.repositories.product_group_repository import ProductGroupRepository
from app.schemas.product_group import ProductGroupCreate, ProductGroupUpdate, ProductGroupRead

router = APIRouter()

@router.get("/admin/product-groups", response_model=List[ProductGroupRead])
async def list_groups(db: AsyncSession = Depends(get_db)):
    repo = ProductGroupRepository(db)
    return await repo.list_all()

@router.post("/admin/product-groups", response_model=ProductGroupRead)
async def create_group(payload: ProductGroupCreate, db: AsyncSession = Depends(get_db)):
    repo = ProductGroupRepository(db)
    return await repo.create(payload)

@router.get("/admin/product-groups/{group_id}", response_model=ProductGroupRead)
async def get_group(group_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = ProductGroupRepository(db)
    group = await repo.get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.put("/admin/product-groups/{group_id}", response_model=ProductGroupRead)
async def update_group(group_id: UUID, payload: ProductGroupUpdate, db: AsyncSession = Depends(get_db)):
    repo = ProductGroupRepository(db)
    return await repo.update(group_id, payload)

@router.delete("/admin/product-groups/{group_id}")
async def delete_group(group_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = ProductGroupRepository(db)
    return await repo.delete(group_id)
