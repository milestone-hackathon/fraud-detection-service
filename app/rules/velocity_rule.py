"""Transaction velocity checking rule."""
from datetime import datetime, timedelta

# In-memory transaction log (would be Redis in production)
_txn_log: dict[str, list[datetime]] = {}

# BUG: No per-merchant exemption support
# Enterprise B2B customers legitimately make 50+ transactions/day
MAX_TRANSACTIONS_PER_DAY = 10  # Global limit, no exceptions


async def check_velocity(txn: dict) -> dict:
    """Check transaction velocity for a card.

    BUG: Uses a single global limit (10 txns/day) with no way
    to configure per-merchant exemptions. B2B customers making
    bulk purchases are blocked after 10 transactions.
    """
    card_key = txn.get("card_bin", "") + "_" + txn.get("transaction_id", "")[:8]
    now = datetime.utcnow()
    cutoff = now - timedelta(days=1)

    if card_key not in _txn_log:
        _txn_log[card_key] = []

    # Clean old entries
    _txn_log[card_key] = [t for t in _txn_log[card_key] if t > cutoff]

    # Record this transaction
    _txn_log[card_key].append(now)

    count = len(_txn_log[card_key])

    # BUG: No merchant-specific override capability
    if count > MAX_TRANSACTIONS_PER_DAY:
        return {
            "risk": True,
            "points": 35,
            "rule": "velocity",
            "reason": f"Velocity exceeded: {count} txns in 24h (limit: {MAX_TRANSACTIONS_PER_DAY})",
        }

    return {"risk": False, "points": 0, "rule": "velocity", "reason": "OK"}
