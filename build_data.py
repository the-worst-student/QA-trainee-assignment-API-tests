from __future__ import annotations

import uuid


def generate_unique_seller_id() -> int:
    raw_number = uuid.uuid4().int % 888889
    return raw_number + 111111


def generate_product_id() -> str:
    return f"qa-autotest-{uuid.uuid4().hex[:10]}"


def build_item_payload(
    seller_id: int | None = None,
    name: str | None = None,
    price: int = 1000,
    likes: int = 1,
    view_count: int = 1,
    contacts: int = 1,
) -> dict:
    if seller_id is None:
        seller_id = generate_unique_seller_id()

    if name is None:
        name = generate_product_id()

    return {
        "sellerID": seller_id,
        "name": name,
        "price": price,
        "statistics": {
            "likes": likes,
            "viewCount": view_count,
            "contacts": contacts,
        },
    }
