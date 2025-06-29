from fastapi import APIRouter

router = APIRouter()

@router.get("/check_health/",status_code=200, name="Check Health")
async def check_health():
    return {"status": "ok"}

