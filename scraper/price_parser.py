import re
from decimal import Decimal
from html import unescape


def extract_price_from_html(html: str) -> Decimal:
    text = unescape(html)
    match = re.search(r"\$\s*([0-9]+(?:,[0-9]{3})*(?:\.[0-9]{1,2})?)", text)
    if not match:
        raise ValueError("No price found in HTML")
    normalized = match.group(1).replace(",", "")
    return Decimal(normalized)
