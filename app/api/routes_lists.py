from fastapi import APIRouter
from pydantic import BaseModel
router = APIRouter()

class ListEntry(BaseModel):
    entity_type: str  # "card", "email", "ip"
    value: str
    merchant_id: str

@router.post("/whitelist")
async def add_to_whitelist(entry: ListEntry):
    return {"status": "added", "list": "whitelist"}

@router.post("/blacklist")
async def add_to_blacklist(entry: ListEntry):
    return {"status": "added", "list": "blacklist"}
