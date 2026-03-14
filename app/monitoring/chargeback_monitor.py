"""Chargeback ratio monitoring and alerting."""
from datetime import datetime, timedelta

# Visa Dispute Monitoring Program thresholds
VDMP_THRESHOLD = 0.009  # 0.9%
VDMP_COUNT_THRESHOLD = 100  # minimum 100 disputes


async def calculate_chargeback_ratio(
    merchant_id: str,
    month: int,
    year: int,
) -> dict:
    """Calculate the chargeback ratio for a merchant.

    BUG: Window calculation has off-by-one error.
    When calculating the ratio for March, it queries
    Feb 1 - Feb 28 instead of Mar 1 - Mar 31.
    This means the current month's chargebacks are never
    counted, and the alert fires a month late.
    """
    # BUG: off-by-one in month calculation
    start_date = datetime(year, month - 1, 1)  # Should be month, not month-1
    if month == 1:
        start_date = datetime(year - 1, 12, 1)

    end_date = datetime(year, month, 1)  # End is exclusive

    # Simulated data
    total_transactions = 5000
    total_chargebacks = 60
    ratio = total_chargebacks / total_transactions

    in_vdmp = ratio >= VDMP_THRESHOLD and total_chargebacks >= VDMP_COUNT_THRESHOLD

    return {
        "merchant_id": merchant_id,
        "period": f"{year}-{month:02d}",
        "total_transactions": total_transactions,
        "total_chargebacks": total_chargebacks,
        "ratio": ratio,
        "in_vdmp": in_vdmp,
        "window_start": start_date.isoformat(),  # BUG: wrong month
        "window_end": end_date.isoformat(),
    }
