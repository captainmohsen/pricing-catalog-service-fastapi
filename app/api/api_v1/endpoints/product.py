from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import get_db
from app.models import Product
# from app.schemas import ProductOut
from app.repositories.product_repository import ProductRepository
from app.repositories.product_group_repository import ProductGroupRepository
from app.repositories.configurable_option_repository import ConfigurableOptionRepository
# from app.services.currency import get_currency_for_user
from app.schemas.product import ProductAdminSchema, ProductCreateSchema, ProductUpdateSchema
from app.schemas.product_expose import ProductExposeSchema,FlavorMirrorSchema

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.product import ProductAdminSchema, ProductCreateSchema, ProductUpdateSchema
from app.schemas.product_expose import ProductExposeSchema,FlavorMirrorSchema


router = APIRouter()
#TODO: this is for client we can ignore it
# @router.get("/products", response_model=List[ProductOut])
# async def list_products(
#     group: Optional[int] = Query(None),
#     product_type: Optional[str] = Query(None),
#     status: Optional[str] = Query(None),
#     price_model: Optional[str] = Query(None),
#     auto_setup: Optional[str] = Query(None),
#     taxable: Optional[bool] = Query(None),
#     search: Optional[str] = Query(None),
#     db: AsyncSession = Depends(get_db),
#     current_user = Depends(get_current_user_optional)
# ):
#     repo = ProductRepository(db)
#     currency = await get_currency_for_user(current_user, db)
#
#     products = await repo.available_for_order(
#         currency=currency,
#         group=group,
#         product_type=product_type,
#         status=status,
#         price_model=price_model,
#         auto_setup=auto_setup,
#         taxable=taxable,
#         search=search
#     )
#     return products

@router.get("/admin/products", response_model=List[ProductAdminSchema])
async def list_products(db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    return await repo.list_all()

@router.post("/admin/products", response_model=ProductAdminSchema)
async def create_product(payload: ProductCreateSchema, db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    return await repo.create(payload)

@router.get("/admin/products/{product_id}", response_model=ProductAdminSchema)
async def retrieve_product(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    product = await repo.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/admin/products/{product_id}", response_model=ProductAdminSchema)
async def update_product(product_id: int, payload: ProductUpdateSchema, db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    updated = await repo.update(product_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/admin/products/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    deleted = await repo.delete(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}



@router.post("/admin/products/{product_id}/associate-option")
async def associate_option(product_id: str, option_id: str, db: AsyncSession = Depends(get_db)):
    product_repo = ProductRepository(db)
    option_repo = ConfigurableOptionRepository(db)
    option = await option_repo.get_option_by_id(option_id=option_id)
    product = await product_repo.get_with_options(product_id)
    if not product or not option:
        raise HTTPException(status_code=404, detail="Product or option not found")
    await product_repo.associate_option(product=product, option=option)
    return {"detail": "Option associated"}

@router.post("/admin/products/{product_id}/dissociate-option")
async def dissociate_option(product_id: str, option_id: str, db: AsyncSession = Depends(get_db)):
    product_repo = ProductRepository(db)
    option_repo = ConfigurableOptionRepository(db)
    option = await option_repo.get_option_by_id(option_id=option_id)
    product = await product_repo.get_with_options(product_id)
    if not product or not option:
        raise HTTPException(status_code=404, detail="Product or option not found")
    removed = await product_repo.dissociate_option(product, option)
    if removed:
        return {"detail": "Option dissociated"}
    raise HTTPException(status_code=400, detail="Option not associated")

@router.get("/admin/product-groups")
async def list_product_groups(db: AsyncSession = Depends(get_db)):
    repo = ProductGroupRepository(db)
    return await repo.list_visible()

@router.get("/admin/products/{product_id}/configurable-options")
async def list_configurable_options(product_id: str, db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)

    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    associated = product.configurable_options
    available = await repo.get_available_configurable_options(product_id)

    return {
        "configurable_options": associated,
        "available_options": available
    }

@router.get("/{product_id}/public", response_model=ProductExposeSchema)
async def get_product_details(product_id: str, db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    product = await repo.get_product_with_options(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductExposeSchema.from_orm(product)

@router.get("/default-iaas", response_model=ProductExposeSchema)
async def get_default_iaas_product(db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    product = await repo.get_product_by_code("iaas_default")
    if not product:
        raise HTTPException(status_code=404, detail="Default IaaS product not found")
    return ProductExposeSchema.from_orm(product)

@router.get("/products/flavors", response_model=List[FlavorMirrorSchema])
async def list_flavors(
    tag: Optional[str] = Query(None),
    vcpus: Optional[int] = Query(None),
    ram: Optional[int] = Query(None),
    disk: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    repo = ProductRepository(db)
    flavors = await repo.list_flavors_with_filters(tag=tag, vcpus=vcpus, ram=ram, disk=disk)
    return flavors


@router.post("/products/flavors/sync", response_model=list[FlavorMirrorSchema])
async def sync_flavors_from_compute(flavors: List[dict], db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    return await repo.sync_flavors_from_openstack(flavors)

@router.get("/plans", response_model=List[Plan])
async def list_plans(db: AsyncSession = Depends(get_db)):
    result = []
    products = await db.execute(
        select(Product).options(
            selectinload(Product.product_configurable_options)
            .selectinload(ProductConfigurableOption.configurable_option)
            .selectinload(ConfigurableOption.choices)
            .selectinload(ConfigurableOptionChoice.flavor_mirror),
            selectinload(Product.product_configurable_options)
            .selectinload(ProductConfigurableOption.configurable_option)
            .selectinload(ConfigurableOption.choices)
            .selectinload(ConfigurableOptionChoice.cycles)
        )
    )

    for product in products.scalars():
        for pco in product.product_configurable_options:
            for choice in pco.configurable_option.choices:
                flavor = choice.flavor_mirror
                if not flavor:
                    continue
                cycles = {c.cycle.name: float(c.price) for c in choice.cycles}

                result.append(
                    Plan(
                        name=product.name,
                        vcpus=flavor.vcpus,
                        ram_mb=flavor.ram_mb,
                        disk_gb=flavor.disk_gb,
                        price_per_hour=cycles.get("hour"),
                        price_per_month=cycles.get("month")
                    )
                )

    return result


@router.get("/backups", response_model=list[BackupItem])
async def list_backups(db: AsyncSession = Depends(get_db)):
    backups = []

    result = await db.execute(
        select(ConfigurableOption)
        .where(ConfigurableOption.name.ilike("backup"))  # or .contains("backup") if more generic
        .options(
            selectinload(ConfigurableOption.choices)
            .selectinload(ConfigurableOptionChoice.cycles)
        )
    )

    for option in result.scalars():
        for choice in option.choices:
            monthly_cycle = next((c for c in choice.cycles if c.cycle == CyclePeriods.month), None)
            backups.append(BackupItem(
                id=choice.id,
                title=choice.label,
                price_per_month=float(monthly_cycle.price) if monthly_cycle else None
            ))

    return backups
