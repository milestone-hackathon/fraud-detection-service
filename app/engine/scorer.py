"""Main fraud risk scoring orchestrator."""
from app.rules.avs_rule import check_avs
from app.rules.velocity_rule import check_velocity
from app.rules.bin_rule import check_bin
from app.lists.list_matcher import check_whitelist


async def score_transaction(txn: dict) -> dict:
    """Score a transaction for fraud risk (0-100).

    BUG: Whitelist check happens AFTER rule evaluation.
    Even if a customer is whitelisted, they still get scored
    and potentially blocked before the whitelist is consulted.
    The whitelist should short-circuit all rules.
    """
    score = 0
    signals = []

    # Run all rules first
    avs_result = check_avs(txn.get("billing_address", {}))
    if avs_result["risk"]:
        score += avs_result["points"]
        signals.append(avs_result)

    velocity_result = await check_velocity(txn)
    if velocity_result["risk"]:
        score += velocity_result["points"]
        signals.append(velocity_result)

    bin_result = check_bin(txn.get("card_bin", ""))
    if bin_result["risk"]:
        score += bin_result["points"]
        signals.append(bin_result)

    # BUG: Whitelist checked AFTER scoring - should be BEFORE
    is_whitelisted = await check_whitelist(txn)
    if is_whitelisted:
        score = 0  # Reset score but signals already fired
        # BUG: Even though score is 0, the transaction may have
        # already been declined by a rule with auto_block=True

    # BUG: ECI value from 3DS not passed through to response
    # This prevents liability shift from being applied
    return {
        "transaction_id": txn.get("transaction_id"),
        "risk_score": min(score, 100),
        "signals": signals,
        "decision": "block" if score >= 75 else "review" if score >= 50 else "allow",
        # Missing: "eci": txn.get("eci")  # BUG: 3DS ECI not included
    }
