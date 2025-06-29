from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.constants.enums import  ConfigurableOptionWidget, CyclePeriods
from app.repositories.configurable_option_repository import ConfigurableOptionRepository



class PricingService:
    def __init__(self, option_repo: ConfigurableOptionRepository):
        self.option_repo = option_repo

    async def calculate_total_for_options(
        self,
        selected_options: list[dict],
        cycle_name: str,
        cycle_multiplier: Decimal,
        currency_id: int
    ) -> dict:
        """
        Calculate total price for a list of configurable options
        Each item must include: option_id, quantity, choice (if applicable)
        """
        total_price = Decimal('0.00')
        total_setup = Decimal('0.00')
        detailed = []

        for item in selected_options:
            option_id = item['option_id']
            quantity = item.get('quantity', 1)
            choice = item.get('choice')

            unit, total, setup = await self.option_repo.get_option_price(
                option_id=option_id,
                cycle_name=cycle_name,
                cycle_multiplier=cycle_multiplier,
                quantity=quantity,
                currency_id=currency_id,
                choice_value=choice
            )

            total_price += total
            total_setup += setup

            detailed.append({
                'option_id': option_id,
                'unit_price': str(unit),
                'total_price': str(total),
                'setup_fee': str(setup)
            })

        return {
            'total_price': str(total_price),
            'total_setup_fee': str(total_setup),
            'details': detailed
        }
