from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional

from app.models import Product, ProductCycle, ConfigurableOption, ConfigurableOptionCycle, ConfigurableOptionChoice

class PricingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_product_base_price(self, product_id: int, currency_id: int, cycle: str, multiplier: Decimal) -> Optional[Decimal]:
        query = select(ProductCycle).where(
            ProductCycle.product_id == product_id,
            ProductCycle.currency_id == currency_id,
            ProductCycle.cycle == cycle,
            ProductCycle.cycle_multiplier == multiplier
        )
        result = await self.session.execute(query)
        cycle_row = result.scalars().first()
        return cycle_row.fixed_price if cycle_row else None

    async def get_configurable_option_price(self, option_id: int, currency_id: int, cycle: str, multiplier: Decimal, quantity: int = 1, choice_value: Optional[str] = None) -> Decimal:
        total_price = Decimal('0.00')
        setup_fee = Decimal('0.00')

        option = await self.session.get(ConfigurableOption, option_id)

        if option.widget in ("num_in", "text_in", "yesno"):
            query = select(ConfigurableOptionCycle).where(
                ConfigurableOptionCycle.option_id == option_id,
                ConfigurableOptionCycle.currency_id == currency_id,
                ConfigurableOptionCycle.cycle == cycle,
                ConfigurableOptionCycle.cycle_multiplier == multiplier
            )
            result = await self.session.execute(query)
            cycle_price = result.scalars().first()
            if cycle_price:
                total_price = cycle_price.price * quantity
                setup_fee = cycle_price.setup_fee * (quantity if not cycle_price.setup_fee_entire_quantity else 1)
        elif option.widget in ("drop", "radio") and choice_value:
            subq = select(ConfigurableOptionChoice.id).where(
                ConfigurableOptionChoice.option_id == option_id,
                ConfigurableOptionChoice.choice == choice_value
            )
            choice_result = await self.session.execute(subq)
            choice_id = choice_result.scalars().first()
            if choice_id:
                cycle_q = select(ConfigurableOptionCycle).where(
                    ConfigurableOptionCycle.value_id == choice_id,
                    ConfigurableOptionCycle.currency_id == currency_id,
                    ConfigurableOptionCycle.cycle == cycle,
                    ConfigurableOptionCycle.cycle_multiplier == multiplier
                )
                result = await self.session.execute(cycle_q)
                cycle_price = result.scalars().first()
                if cycle_price:
                    total_price = cycle_price.price * quantity
                    setup_fee = cycle_price.setup_fee * (quantity if not cycle_price.setup_fee_entire_quantity else 1)

        return total_price + setup_fee