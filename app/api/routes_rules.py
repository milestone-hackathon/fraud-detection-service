from fastapi import APIRouter
router = APIRouter()

@router.get("/rules")
async def list_rules(merchant_id: str):
    return {"rules": []}

@router.put("/rules/{rule_id}")
async def update_rule(rule_id: str, enabled: bool = True):
    return {"rule_id": rule_id, "enabled": enabled}
