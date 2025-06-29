from sqlalchemy.future import select
from app.models.currency import Currency
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException


class CurrencyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self):
        result = await self.db.execute(select(Currency))
        return result.scalars().all()

    async def create(self, data):
        currency = Currency(**data.dict())
        self.db.add(currency)
        await self.db.commit()
        await self.db.refresh(currency)
        return currency

    async def delete(self, currency_id:str):
        currency = await self.db.get(Currency, currency_id)
        if currency.is_default:
            raise HTTPException(status_code=403, detail="Cannot delete the default currency")
        await self.db.delete(currency)
        await self.db.commit()
        return True

    async def update(self, currency_id:str, data):
        currency = await self.db.get(Currency, currency_id)
        if not currency:
            raise HTTPException(status_code=404, detail="Currency not found")

        if data.is_default and not currency.is_default:
            rate_to_old_default = currency.rate
            currencies = await self.db.execute(select(Currency))
            for c in currencies.scalars():
                c.rate = c.rate / rate_to_old_default
                c.is_default = (c.code == currency.code)
                self.db.add(c)

        for field, value in data.dict().items():
            setattr(currency, field, value)

        await self.db.commit()
        await self.db.refresh(currency)
        return currency