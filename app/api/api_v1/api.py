from fastapi import APIRouter

from app.api.api_v1.endpoints import (health,product,product_cycle,currency,configurable_option,
                                      configurable_option_cycles,configurable_option_choice,product_group)

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(product.router,prefix="/products", tags=["Product"])

api_router.include_router(product_group.router,prefix="/product_group", tags=["Product_Groups"])


api_router.include_router(product_cycle.router,prefix="/product_cycle", tags=["Product_Cycle"])

api_router.include_router(currency.router,prefix="/currency", tags=["Currency"])

api_router.include_router(configurable_option.router,prefix="/configurable_option", tags=["Configurable_Options"])


api_router.include_router(configurable_option_cycles.router,prefix="/configurable_option_cycles", tags=["Configurable_Option_Cycles"])

api_router.include_router(configurable_option_choice.router,prefix="/configurable_option_choices", tags=["Configurable_Option_Choices"])
