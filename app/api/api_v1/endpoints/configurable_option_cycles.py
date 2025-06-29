from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db

from app.schemas.configurable_option_cycle import ConfigurableOptionCycleCreate, ConfigurableOptionCycleRead, ConfigurableOptionCycleUpdate
from app.repositories.configurable_option_cycle_repository import ConfigurableOptionCycleRepository
from uuid import UUID
from typing import List

router = APIRouter()


@router.get("/admin/configurable-option-cycles", response_model=List[ConfigurableOptionCycleRead])
async def list_cycles(db: AsyncSession = Depends(get_db)):
    repo = ConfigurableOptionCycleRepository(db)
    return await repo.list_all()

@router.post("/admin/configurable-option-cycles", response_model=ConfigurableOptionCycleRead)
async def create_cycle(payload: ConfigurableOptionCycleCreate, db: AsyncSession = Depends(get_db)):
    repo = ConfigurableOptionCycleRepository(db)
    return await repo.create(payload)

@router.put("/admin/configurable-option-cycles/{cycle_id}", response_model=ConfigurableOptionCycleRead)
async def update_cycle(cycle_id: str, payload: ConfigurableOptionCycleUpdate, db: AsyncSession = Depends(get_db)):
    repo = ConfigurableOptionCycleRepository(db)
    return await repo.update(cycle_id, payload)

@router.delete("/admin/configurable-option-cycles/{cycle_id}")
async def delete_cycle(cycle_id: str, db: AsyncSession = Depends(get_db)):
    repo = ConfigurableOptionCycleRepository(db)
    return await repo.delete(cycle_id)
