"""Whitelist and blacklist matching logic."""

# In-memory lists (would be database in production)
_whitelist: dict[str, set] = {}  # merchant_id -> set of fingerprints
_blacklist: dict[str, set] = {}


async def check_whitelist(txn: dict) -> bool:
    """Check if a transaction matches a whitelist entry.

    BUG: The whitelist check compares card fingerprint + email,
    but the matching logic uses exact string comparison. If the
    email was stored with different casing (John@Acme.com vs
    john@acme.com), the whitelist won't match and the customer
    remains blocked.
    """
    merchant_id = txn.get("merchant_id", "")
    card_fp = txn.get("card_fingerprint", "")
    email = txn.get("email", "")

    merchant_list = _whitelist.get(merchant_id, set())

    # BUG: case-sensitive email comparison
    key = f"{card_fp}:{email}"  # Should be: f"{card_fp}:{email.lower()}"

    return key in merchant_list


async def add_to_whitelist(merchant_id: str, card_fingerprint: str, email: str):
    """Add an entity to the merchant whitelist."""
    if merchant_id not in _whitelist:
        _whitelist[merchant_id] = set()
    # BUG: email stored as-is, not normalized to lowercase
    _whitelist[merchant_id].add(f"{card_fingerprint}:{email}")
