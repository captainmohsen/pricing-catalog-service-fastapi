from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.deps import get_db
from app.repositories.configurable_option_repository import ConfigurableOptionRepository
from app.schemas.configurable_option import (
    ConfigurableOptionCreate,
    ConfigurableOptionUpdate,
    ConfigurableOptionRead
)
from app.constants.enums import ConfigurableOptionWidget, ConfigurableOptionStatus, CyclePeriods
from app.repositories.currency_repository import CurrencyRepository

router = APIRouter()

@router.get("/admin/configurable-options", response_model=List[ConfigurableOptionRead])
async def list_options(db: AsyncSession = Depends(get_db)):
    repo = ConfigurableOptionRepository(db)
    return await repo.list_all()

@router.post("/admin/configurable-options", response_model=ConfigurableOptionRead)
async def create_option(payload: ConfigurableOptionCreate, db: AsyncSession = Depends(get_db)):
    repo = ConfigurableOptionRepository(db)
    return await repo.create(payload)

@router.put("/admin/configurable-options/{option_id}", response_model=ConfigurableOptionRead)
async def update_option(option_id: str, payload: ConfigurableOptionUpdate, db: AsyncSession = Depends(get_db)):
    repo = ConfigurableOptionRepository(db)
    return await repo.update(option_id, payload)

@router.delete("/admin/configurable-options/{option_id}")
async def delete_option(option_id: str, db: AsyncSession = Depends(get_db)):
    repo = ConfigurableOptionRepository(db)
    return await repo.delete(option_id)

@router.get("/admin/configurable-options/create-options")
async def create_options_metadata(db: AsyncSession = Depends(get_db)):
    currency_repo = CurrencyRepository(db)
    currencies = await currency_repo.list_all()
    default_currency = next((c for c in currencies if c.is_default), None)

    return {
        "widgets": [{"label": label, "value": value} for value, label in ConfigurableOptionWidget.CHOICES],
        "currencies": [c.to_dict() for c in currencies],
        "default_currency": default_currency.to_dict() if default_currency else None,
        "status_choices": [{"label": label, "value": value} for value, label in ConfigurableOptionStatus.CHOICES],
        "cycles": [{"label": label, "value": value} for value, label in CyclePeriods.choices]
    }
