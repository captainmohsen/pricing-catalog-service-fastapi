from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.currency import CurrencyCreate, CurrencyRead
from app.repositories.currency_repository import CurrencyRepository

router = APIRouter()

@router.get("/admin/currencies", response_model=list[CurrencyRead])
async def list_currencies(db: AsyncSession = Depends(get_db)):
    repo = CurrencyRepository(db)
    return await repo.list()

@router.post("/admin/currencies", response_model=CurrencyRead)
async def create_currency(currency: CurrencyCreate, db: AsyncSession = Depends(get_db)):
    repo = CurrencyRepository(db)
    return await repo.create(currency)

@router.delete("/admin/currencies/{currency_id}")
async def delete_currency(currency_id: str, db: AsyncSession = Depends(get_db)):
    repo = CurrencyRepository(db)
    return await repo.delete(currency_id)

@router.put("/admin/currencies/{currency_id}", response_model=CurrencyRead)
async def update_currency(currency_id: str, data: CurrencyCreate, db: AsyncSession = Depends(get_db)):
    repo = CurrencyRepository(db)
    return await repo.update(currency_id, data)