from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.deps import get_db
from app.schemas.product_cycle import ProductCycleCreateSchema, ProductCycleReadSchema
from app.repositories.product_cycle_repository import ProductCycleRepository

router = APIRouter()

@router.get("/admin/product-cycles", response_model=List[ProductCycleReadSchema])
async def list_product_cycles(db: AsyncSession = Depends(get_db)):
    repo = ProductCycleRepository(db)
    return await repo.list_all()

@router.get("/admin/product-cycles/{cycle_id}", response_model=ProductCycleReadSchema)
async def get_product_cycle(cycle_id: int, db: AsyncSession = Depends(get_db)):
    repo = ProductCycleRepository(db)
    cycle = await repo.get_by_id(cycle_id)
    if not cycle:
        raise HTTPException(status_code=404, detail="Product cycle not found")
    return cycle

@router.post("/admin/product-cycles", response_model=ProductCycleReadSchema)
async def create_product_cycle(payload: ProductCycleCreateSchema, db: AsyncSession = Depends(get_db)):
    repo = ProductCycleRepository(db)
    return await repo.create(payload.dict())

@router.delete("/admin/product-cycles/{cycle_id}")
async def delete_product_cycle(cycle_id: int, db: AsyncSession = Depends(get_db)):
    repo = ProductCycleRepository(db)
    deleted = await repo.delete(cycle_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product cycle not found or already deleted")
    return {"detail": "Product cycle deleted"}
