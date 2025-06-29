from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.models.configurable_option import ConfigurableOption
from app.models.product_configurable_options import ProductConfigurableOption
from app.models.configurable_option_choice import ConfigurableOptionChoice
from app.schemas.product import ProductCreateSchema, ProductUpdateSchema
from app.models import FlavorMirror
from sqlalchemy.orm import selectinload,joinedload
from typing import Optional
from uuid import UUID



class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, product_id: int) -> Product | None:
        stmt = (
            select(Product)
            .options(
                selectinload(Product.group),
                selectinload(Product.cycles),
                selectinload(Product.configurable_options).selectinload(ProductConfigurableOption.configurable_option),
            )
            .where(Product.id == product_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_product_by_code(self, code: str) -> Product | None:
        stmt = (
            select(Product)
            .where(Product.code == code)
            .options(
                selectinload(Product.cycles),
                selectinload(Product.group),
                selectinload(Product.product_configurable_options)
                .joinedload(ProductConfigurableOption.configurable_option)
                .options(
                    selectinload(ConfigurableOption.cycles),
                    selectinload(ConfigurableOption.choices).selectinload(ConfigurableOptionChoice.cycles)
                )
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_openstack_flavors(self, tag: Optional[str] = None):
        stmt = select(FlavorMirror).options(joinedload(FlavorMirror.choice))
        if tag:
            stmt = stmt.where(FlavorMirror.tags.contains([tag]))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_flavors_with_filters(self, vcpus: Optional[int] = None, ram: Optional[int] = None, disk: Optional[int] = None, tag: Optional[str] = None) -> list[FlavorMirror]:
        stmt = select(FlavorMirror)
        if tag:
            stmt = stmt.where(FlavorMirror.tags.contains([tag]))
        if vcpus is not None:
            stmt = stmt.where(FlavorMirror.vcpus == vcpus)
        if ram is not None:
            stmt = stmt.where(FlavorMirror.ram == ram)
        if disk is not None:
            stmt = stmt.where(FlavorMirror.disk == disk)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def sync_flavors_from_openstack(self, flavors: list[dict]) -> list[FlavorMirror]:
        synced_flavors = []
        for flavor in flavors:
            existing = await self.db.execute(
                select(FlavorMirror).where(FlavorMirror.openstack_id == flavor["id"])
            )
            mirror = existing.scalar_one_or_none()
            if mirror:
                mirror.name = flavor["name"]
                mirror.vcpus = flavor["vcpus"]
                mirror.ram = flavor["ram"]
                mirror.disk = flavor["disk"]
                mirror.tag = flavor.get("tag")
            else:
                mirror = FlavorMirror(
                    openstack_id=flavor["id"],
                    name=flavor["name"],
                    vcpus=flavor["vcpus"],
                    ram=flavor["ram"],
                    disk=flavor["disk"],
                    tag=flavor.get("tag"),
                    choice_id=UUID(flavor["choice_id"])
                )
                self.db.add(mirror)
            synced_flavors.append(mirror)
        await self.db.commit()
        return synced_flavors


    async def list_all(self) -> list[Product]:
        result = await self.db.execute(select(Product).options(
                selectinload(Product.group),
                selectinload(Product.cycles),
                selectinload(Product.product_configurable_options).joinedload(ProductConfigurableOption.configurable_option),))
        return result.scalars().all()

    async def create(self, data: ProductCreateSchema) -> Product:
        new_product = Product(**data.dict())
        self.db.add(new_product)
        await self.db.commit()
        await self.db.refresh(new_product)
        return new_product

    async def update(self, product_id: str, data: ProductUpdateSchema) -> Product | None:
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            return None

        for field, value in data.dict(exclude_unset=True).items():
            setattr(product, field, value)

        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete(self, product_id: str) -> bool:
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            return False
        await self.db.delete(product)
        await self.db.commit()
        return True

    async def list_by_group(self, group_id: str) -> list[Product]:
        result = await self.db.execute(select(Product).where(Product.group_id == group_id))
        return result.scalars().all()

    async def get_with_options(self, product_id: str) -> Product | None:
        result = await self.db.execute(
            select(Product).options(
                selectinload(Product.product_configurable_options).selectinload(
                    ProductConfigurableOption.configurable_option)
            ).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def associate_option(self, product: Product, option: ConfigurableOption):
        product.configurable_options.append(option)
        await self.db.commit()

    async def dissociate_option(self, product: Product, option: ConfigurableOption):
        if option in product.configurable_options:
            product.configurable_options.remove(option)
            await self.db.commit()
            return True
        return False

    async def get_available_configurable_options(self, product_id: str) -> list[ConfigurableOption]:
        result = await self.db.execute(
            select(ConfigurableOption).where(ConfigurableOption.products.any(id=product_id)
            )
        )

        return result.scalars().all()

    async def get_product_with_options(self, product_id: str) -> Optional[Product]:
        stmt = (
            select(Product)
            .where(Product.id == product_id)
            .options(
                selectinload(Product.cycles),
                selectinload(Product.group),
                selectinload(Product.product_configurable_options)
                .joinedload(ProductConfigurableOption.configurable_option)
                .options(
                    selectinload(ConfigurableOption.cycles),
                    selectinload(ConfigurableOption.choices).selectinload(ConfigurableOptionChoice.cycles)
                )
            )
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()