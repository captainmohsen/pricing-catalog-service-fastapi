from sqlalchemy import delete
from decimal import Decimal
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import ConfigurableOption, Product, ConfigurableOptionChoice
from app.constants.enums import ConfigurableOptionWidget, CyclePeriods
from app.schemas.configurable_option import ConfigurableOptionCreate, ConfigurableOptionUpdate

class ConfigurableOptionRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def list_all(self) -> List[ConfigurableOption]:
        result = await self.db.execute(select(ConfigurableOption))
        return result.scalars().all()

    async def create(self, data: ConfigurableOptionCreate) -> ConfigurableOption:
        option = ConfigurableOption(**data.dict())
        self.db.add(option)
        await self.db.commit()
        await self.db.refresh(option)
        return option

    async def update(self, option_id: str, data: ConfigurableOptionUpdate) -> Optional[ConfigurableOption]:
        stmt = select(ConfigurableOption).where(ConfigurableOption.id == option_id)
        result = await self.db.execute(stmt)
        option = result.scalar_one_or_none()
        if not option:
            return None
        for field, value in data.dict().items():
            setattr(option, field, value)
        await self.db.commit()
        await self.db.refresh(option)
        return option

    async def delete(self, option_id: str) -> bool:
        stmt = delete(ConfigurableOption).where(ConfigurableOption.id == option_id)
        await self.db.execute(stmt)
        await self.db.commit()
        return True

    async def get_option_by_id(self, option_id: str):
        stmt = select(ConfigurableOption).where(ConfigurableOption.id == option_id).options(
            selectinload(ConfigurableOption.choices),
            selectinload(ConfigurableOption.cycles)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_option_price(
        self,
        option_id: int,
        cycle_name: str,
        cycle_multiplier: Decimal,
        quantity: int,
        currency_id: int,
        choice_value: Optional[str] = None
    ) -> tuple[Decimal, Decimal, Decimal]:
        zero = Decimal('0.00')
        option = await self.get_option_by_id(option_id)
        if option is None:
            return zero, zero, zero

        if option.widget in ConfigurableOptionWidget.WITHOUT_CHOICES:
            cycle = next((
                c for c in option.cycles
                if c.cycle == cycle_name and
                   c.cycle_multiplier == cycle_multiplier and
                   c.currency_id == currency_id
            ), None)
            if cycle:
                unit_price = cycle.price
                total_price = cycle.price * quantity
                setup_fee = cycle.setup_fee if cycle.setup_fee_entire_quantity else quantity * cycle.setup_fee
                return unit_price, total_price, setup_fee

        elif option.widget in ConfigurableOptionWidget.WITH_CHOICES:
            choice = next((ch for ch in option.choices if ch.choice == choice_value), None)
            if choice:
                cycle = next((
                    c for c in choice.cycles
                    if c.cycle == cycle_name and
                       c.cycle_multiplier == cycle_multiplier and
                       c.currency_id == currency_id
                ), None)
                if cycle:
                    unit_price = cycle.price
                    total_price = cycle.price * quantity
                    setup_fee = cycle.setup_fee if cycle.setup_fee_entire_quantity else quantity * cycle.setup_fee
                    return unit_price, total_price, setup_fee

        return zero, zero, zero

    async def option_has_cycle(
        self,
        option_id: int,
        cycle: str,
        multiplier: Decimal,
        currency_id: int,
        choice_value: Optional[str] = None
    ) -> bool:
        option = await self.get_option_by_id(option_id)
        if not option:
            return False

        if option.widget in ConfigurableOptionWidget.WITH_CHOICES:
            return any(
                c.cycle == cycle and c.cycle_multiplier == multiplier and c.currency_id == currency_id
                for choice in option.choices
                if choice.choice == choice_value
                for c in choice.cycles
            )
        else:
            return any(
                c.cycle == cycle and c.cycle_multiplier == multiplier and c.currency_id == currency_id
                for c in option.cycles
            )

    async def get_available_options_for_product(self, product_id: int) -> List[ConfigurableOption]:
        stmt = select(ConfigurableOption).where(~ConfigurableOption.products.any(id=product_id))
        result = await self.db.execute(stmt)
        return result.scalars().all()