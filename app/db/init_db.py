import logging
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import (
    Currency, ProductGroup, Product,
    ConfigurableOption, ConfigurableOptionChoice, ConfigurableOptionCycle,
    ProductConfigurableOption
)
from app.constants.enums import (
    ProductType, PricingModel, ProductAutoSetup,
    PublicStatuses, ProvisioningBackend, ConfigurableOptionWidget,
    CyclePeriods
)
from decimal import Decimal
from app import schemas
from app.core.config import settings

logger = logging.getLogger(__name__)

# Optional: Seed script snippet
from app.models import FlavorMirror

def create_flavor_mirror_entries():
    return [
        FlavorMirror(
            flavor_id="m1.small",
            label="Small (2 vCPU, 4GB RAM)",
            vcpus=2,
            ram_mb=4096,
            disk_gb=20,
            tags=["economy", "balanced"],
            configurable_option_choice_id=choice_id  # attach to correct choice
        ),
        FlavorMirror(
            flavor_id="m1.large",
            label="Large (4 vCPU, 8GB RAM)",
            vcpus=4,
            ram_mb=8192,
            disk_gb=40,
            tags=["performance", "cpu-optimized"],
            configurable_option_choice_id=another_choice_id
        ),
    ]



async def seed_default_pricing_data(db: AsyncSession):
    irr = Currency(id=uuid4(), code="IRR", rate=1, is_default=True)
    db.add(irr)

    compute_group = ProductGroup(id=uuid4(), name="Compute", description="Compute resources")
    db.add(compute_group)

    product = Product(
        id=uuid4(),
        name="IaaS VM Product",
        description="Core compute offering for VMs",
        code="iaas_default",
        group=compute_group,
        product_type=ProductType.openstack,
        price_model=PricingModel.fixed_and_dynamic,
        auto_setup=ProductAutoSetup.on_order,
        provisioning_backend=ProvisioningBackend.openstack,
        status=PublicStatuses.public,
    )
    db.add(product)

    flavor_option = ConfigurableOption(
        id=uuid4(),
        name="Flavor",
        description="Choose your VM flavor",
        widget=ConfigurableOptionWidget.dropdown,
        status=PublicStatuses.public,
        required=True
    )
    db.add(flavor_option)

    ssd_option = ConfigurableOption(
        id=uuid4(),
        name="Storage Type",
        description="Select SSD or HDD",
        widget=ConfigurableOptionWidget.dropdown,
        status=PublicStatuses.public,
        required=True
    )
    db.add(ssd_option)

    disk_option = ConfigurableOption(
        id=uuid4(),
        name="Disk Size",
        description="Choose disk size in GB",
        widget=ConfigurableOptionWidget.number_input,
        status=PublicStatuses.public,
        required=True
    )
    db.add(disk_option)

    # Create Flavor choices and cycles
    flavor_choices = [
        ("m1.small", "Small (2 vCPU, 4GB RAM)", Decimal("5.00"), Decimal("0.10")),
        ("m1.medium", "Medium (4 vCPU, 8GB RAM)", Decimal("10.00"), Decimal("0.20"))
    ]
    for code, label, monthly_price, hourly_price in flavor_choices:
        choice = ConfigurableOptionChoice(
            id=uuid4(), option=flavor_option, choice=code, label=label
        )
        db.add(choice)

        db.add(ConfigurableOptionCycle(
            value=choice, cycle=CyclePeriods.month, cycle_multiplier=1,
            price=monthly_price, setup_fee=Decimal("0.00"),
            setup_fee_entire_quantity=True, currency_id=irr.id, is_relative_price=False
        ))

        db.add(ConfigurableOptionCycle(
            value=choice, cycle=CyclePeriods.hour, cycle_multiplier=1,
            price=hourly_price, setup_fee=Decimal("0.00"),
            setup_fee_entire_quantity=True, currency_id=irr.id, is_relative_price=False
        ))

    # Storage Type
    for code, label, price in [("ssd", "SSD", Decimal("1.00")), ("hdd", "HDD", Decimal("0.50"))]:
        choice = ConfigurableOptionChoice(
            id=uuid4(), option=ssd_option, choice=code, label=label
        )
        db.add(choice)
        db.add(ConfigurableOptionCycle(
            value=choice, cycle=CyclePeriods.month, cycle_multiplier=1,
            price=price, setup_fee=Decimal("0.00"), setup_fee_entire_quantity=True,
            currency_id=irr.id, is_relative_price=False
        ))

    # Disk quantity option
    db.add(ConfigurableOptionCycle(
        option=disk_option, cycle=CyclePeriods.month, cycle_multiplier=1,
        price=Decimal("0.10"), setup_fee=Decimal("0.00"),
        setup_fee_entire_quantity=True, currency_id=irr.id, is_relative_price=False
    ))
    db.add(ConfigurableOptionCycle(
        option=disk_option, cycle=CyclePeriods.hour, cycle_multiplier=1,
        price=Decimal("0.01"), setup_fee=Decimal("0.00"),
        setup_fee_entire_quantity=True, currency_id=irr.id, is_relative_price=False
    ))

    db.add_all([
        ProductConfigurableOption(product=product, configurable_option=flavor_option),
        ProductConfigurableOption(product=product, configurable_option=ssd_option),
        ProductConfigurableOption(product=product, configurable_option=disk_option),
    ])

    await db.commit()


async def init_db(db: AsyncSession) -> None:
    """Initialize the database with default  users"""
    await seed_default_pricing_data(db=db)

    logger.info("✅ Seeded default pricing data.")

    # await db.close()


logger.info("Database initialization complete!")


