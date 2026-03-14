"""Card testing / BIN attack detection."""
from datetime import datetime, timedelta

_small_txn_log: list[dict] = []

# BUG: Threshold set too low - $0.50 instead of $5.00
# Many legitimate micro-transactions (e.g., in-app purchases) are $0.99-$2.99
SMALL_TXN_THRESHOLD = 0.50  # Should be 5.00

CARD_TESTING_VELOCITY = 20  # 20 small txns in 1 hour = card testing


async def detect_card_testing(merchant_id: str, amount: float) -> bool:
    """Detect potential card testing attacks.

    BUG: The small transaction threshold is $0.50 which catches
    many legitimate small purchases (games, stickers, etc.).
    Should be $5.00 to focus on actual card testing patterns
    which typically use $0.01-$1.00 transactions.
    """
    if amount > SMALL_TXN_THRESHOLD:
        return False

    now = datetime.utcnow()
    cutoff = now - timedelta(hours=1)

    _small_txn_log.append({"merchant_id": merchant_id, "time": now})

    # Count recent small transactions for this merchant
    recent = [
        t for t in _small_txn_log
        if t["merchant_id"] == merchant_id and t["time"] > cutoff
    ]

    return len(recent) >= CARD_TESTING_VELOCITY
