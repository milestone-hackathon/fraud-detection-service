from fastapi import APIRouter
from pydantic import BaseModel
from app.engine.scorer import score_transaction

router = APIRouter()

class ScoreRequest(BaseModel):
    transaction_id: str
    amount: int
    currency: str
    card_bin: str
    billing_address: dict | None = None
    device_fingerprint: str | None = None
    merchant_id: str | None = None

@router.post("/score")
async def get_risk_score(req: ScoreRequest):
    return await score_transaction(req.model_dump())
