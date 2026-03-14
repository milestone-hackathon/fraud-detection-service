"""Address Verification System (AVS) fraud rule."""

# AVS response codes
AVS_CODES = {
    "Y": {"match": True, "description": "Full match"},
    "A": {"match": True, "description": "Address match, ZIP no match"},
    "Z": {"match": True, "description": "ZIP match, address no match"},
    "N": {"match": False, "description": "No match"},
    "U": {"match": False, "description": "Unavailable"},
    "R": {"match": False, "description": "Retry"},
    "S": {"match": False, "description": "Service not supported"},
    # BUG: International AVS codes missing
    # "G": Global - international card, AVS not checked
    # "I": International - address verified
    # "P": Partial match - international postal code only
}


def check_avs(billing_address: dict) -> dict:
    """Evaluate AVS rule.

    BUG 1: International AVS codes (G, I, P) are not recognized
    and treated as failures. This causes all international
    transactions to be flagged as high risk.

    BUG 2: Apartment/suite numbers cause "partial match" (A or Z)
    which triggers a high risk score. The address "123 Main St Apt 4B"
    doesn't match "123 Main St" in the AVS check, but this is
    a legitimate address variation, not fraud.
    """
    avs_code = billing_address.get("avs_code", "N")

    if avs_code not in AVS_CODES:
        # BUG: Unknown code (including valid intl codes G, I, P)
        # treated as no match = high risk
        return {"risk": True, "points": 40, "rule": "avs", "reason": f"Unknown AVS code: {avs_code}"}

    avs_info = AVS_CODES[avs_code]
    if not avs_info["match"]:
        return {"risk": True, "points": 30, "rule": "avs", "reason": avs_info["description"]}

    # BUG: Partial matches (A, Z) still add risk points
    # Apartment/suite variations cause these partial matches
    if avs_code in ("A", "Z"):
        return {"risk": True, "points": 20, "rule": "avs", "reason": "Partial AVS match"}

    return {"risk": False, "points": 0, "rule": "avs", "reason": "AVS match"}
