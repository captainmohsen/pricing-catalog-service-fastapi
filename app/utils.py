from decimal import Decimal
from datetime import datetime, timedelta
from app.constants.enums import CyclePeriods


def display_name(cycle: str, multiplier: Decimal) -> str:
    if cycle == CyclePeriods.onetime:
        return "One Time"
    elif cycle == CyclePeriods.year:
        if multiplier == Decimal('1.00'):
            return "Yearly"
        elif multiplier == Decimal('2.00'):
            return "Biennial"
        elif multiplier == Decimal('3.00'):
            return "Triennial"
        else:
            return f"Every {multiplier} years"
    elif cycle == CyclePeriods.month:
        if multiplier == Decimal('1.00'):
            return "Monthly"
        elif multiplier == Decimal('3.00'):
            return "Quarterly"
        elif multiplier == Decimal('6.00'):
            return "Semi-Annual"
        else:
            return f"Every {multiplier} months"
    elif cycle == CyclePeriods.hour:
        return "Hourly" if multiplier == Decimal('1.00') else f"Every {multiplier} hours"
    return "Unknown"

def get_next_due_date(start_date: datetime, quantity: int, unit: CyclePeriods) -> datetime:
    if unit == CyclePeriods.onetime:
        return start_date
    elif unit == CyclePeriods.hour:
        return start_date + timedelta(hours=quantity)
    elif unit == CyclePeriods.month:
        new_year = start_date.year + (start_date.month + quantity - 1) // 12
        new_month = (start_date.month + quantity - 1) % 12 + 1
        try:
            return start_date.replace(year=new_year, month=new_month)
        except ValueError:
            return start_date.replace(year=new_year, month=new_month + 1, day=1)
    elif unit == CyclePeriods.year:
        try:
            return start_date.replace(year=start_date.year + quantity)
        except ValueError:
            return start_date + timedelta(days=365 * quantity)
    raise ValueError(f"Unknown cycle unit: {unit}")


def get_price_model_display(price_model: str) -> str:
    PRICING_MODELS = {
        'free': 'Free',
        'fixed_and_dynamic': 'Fixed + Dynamic',
        'dynamic_or_fixed': 'Dynamic with Minimum Fixed'
    }
    return PRICING_MODELS.get(price_model, price_model)

def get_auto_setup_display(auto_setup: str) -> str:
    AUTO_SETUP = {
        'disabled': 'Disabled',
        'on_order': 'On Order',
        'first_payment': 'On First Payment',
        'manual': 'Manual Approval'
    }
    return AUTO_SETUP.get(auto_setup, auto_setup)

def get_plugin_data(product_module_label: str, product: Product) -> Optional[dict]:
    try:
        plugin = PLUGIN_REGISTRY.get(product_module_label)
        if plugin and hasattr(plugin, 'get_product_settings'):
            return plugin.get_product_settings(product)
    except Exception:
        return None
    return None

