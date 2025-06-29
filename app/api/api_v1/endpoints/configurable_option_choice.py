from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.deps import get_db
from app.schemas.configurable_option_choice import ConfigurableOptionChoiceRead
from app.repositories.configurable_option_choice_repository import ConfigurableOptionChoiceRepository
from app.schemas.configurable_option_choice import ConfigurableOptionChoiceCreate, ConfigurableOptionChoiceUpdate
router = APIRouter()

@router.get("/admin/configurable-option-choices", response_model=list[ConfigurableOptionChoiceRead])
async def list_choices(db: AsyncSession = Depends(get_db)):
    repo = ConfigurableOptionChoiceRepository(db)
    return await repo.list_all()


@router.post("/admin/configurable-option-choices", response_model=ConfigurableOptionChoiceRead)
async def create_choice(payload: ConfigurableOptionChoiceCreate, db: AsyncSession = Depends(get_db)):
    repo = ConfigurableOptionChoiceRepository(db)
    return await repo.create(payload)

@router.put("/admin/configurable-option-choices/{choice_id}", response_model=ConfigurableOptionChoiceRead)
async def update_choice(choice_id: str, payload: ConfigurableOptionChoiceUpdate, db: AsyncSession = Depends(get_db)):
    repo = ConfigurableOptionChoiceRepository(db)
    return await repo.update(choice_id, payload)

@router.delete("/admin/configurable-option-choices/{choice_id}")
async def delete_choice(choice_id: str, db: AsyncSession = Depends(get_db)):
    repo = ConfigurableOptionChoiceRepository(db)
    return await repo.delete(choice_id)
