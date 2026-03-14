"""BIN (Bank Identification Number) fraud rule."""

# Known high-risk BIN ranges
HIGH_RISK_BINS = {
    "4000", "4111",  # Test cards often used in card testing
}

# BUG: Fintech BINs incorrectly classified as "foreign"
# Revolut, Wise, N26 issue US-domiciled cards with unusual BINs
# that are flagged as foreign even for domestic US transactions
FOREIGN_BINS = {
    "4532",  # Actually a Revolut US card
    "5234",  # Actually a Wise US card
    "4023",  # Actually an N26 US card
    "6011",  # Discover - not foreign at all!
}


def check_bin(card_bin: str) -> dict:
    """Check BIN against risk lists.

    BUG: Fintech BINs (Revolut, Wise, N26) are incorrectly
    listed in FOREIGN_BINS, causing domestic US transactions
    from fintech cards to be flagged with cross-border risk
    and charged additional fees.
    """
    bin_prefix = card_bin[:4]

    if bin_prefix in HIGH_RISK_BINS:
        return {
            "risk": True,
            "points": 50,
            "rule": "bin",
            "reason": f"High-risk BIN: {bin_prefix}",
        }

    # BUG: Legitimate fintech cards flagged as foreign
    if bin_prefix in FOREIGN_BINS:
        return {
            "risk": True,
            "points": 25,
            "rule": "bin",
            "reason": f"Foreign BIN detected: {bin_prefix}",
        }

    return {"risk": False, "points": 0, "rule": "bin", "reason": "OK"}
