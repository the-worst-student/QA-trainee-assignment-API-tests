from __future__ import annotations

import time


def extract_item_from_response(
    response_json: dict | list, expected_item_id: str
) -> dict:
    if isinstance(response_json, dict):
        return response_json

    if isinstance(response_json, list):
        for Item in response_json:
            if Item.get("id") == expected_item_id:
                return Item

    raise AssertionError(
        f"Item with id={expected_item_id} was not found in response: {response_json}"
    )


def extract_statistic_from_response(response_json: dict | list) -> dict:
    if isinstance(response_json, dict):
        return response_json

    if isinstance(response_json, list) and len(response_json) > 0:
        return response_json[0]

    raise AssertionError(
        f"Statistic response has unexpected structure: {response_json}"
    )


def extract_created_item_id(create_response_json: dict) -> str:
    assert isinstance(create_response_json, dict)
    assert "status" in create_response_json

    StatusText = create_response_json["status"]
    assert isinstance(StatusText, str)
    assert " - " in StatusText

    ItemId = StatusText.split(" - ")[-1].strip()

    assert ItemId

    return ItemId


def test_create_item_returns_expected_fields(api_client, item_payload: dict) -> None:
    response = api_client.create_item(item_payload)

    assert response.status_code == 200, response.text

    ResponseJson = response.json()

    assert isinstance(ResponseJson, dict)
    assert "status" in ResponseJson

    ItemId = extract_created_item_id(ResponseJson)

    get_response = api_client.get_item(ItemId)

    assert get_response.status_code == 200, get_response.text

    GetResponseJson = get_response.json()
    Item = extract_item_from_response(GetResponseJson, ItemId)

    assert Item["id"] == ItemId
    assert Item["sellerId"] == item_payload["sellerID"]
    assert Item["name"] == item_payload["name"]
    assert Item["price"] == item_payload["price"]
    assert Item["statistics"]["likes"] == item_payload["statistics"]["likes"]
    assert Item["statistics"]["viewCount"] == item_payload["statistics"]["viewCount"]
    assert Item["statistics"]["contacts"] == item_payload["statistics"]["contacts"]
    assert "createdAt" in Item


def test_get_item_by_id_returns_created_item(api_client, item_payload: dict) -> None:
    create_response = api_client.create_item(item_payload)

    assert create_response.status_code == 200, create_response.text

    created_item_response = create_response.json()
    item_id = extract_created_item_id(created_item_response)

    get_response = api_client.get_item(item_id)

    assert get_response.status_code == 200, get_response.text

    ResponseJson = get_response.json()
    Item = extract_item_from_response(ResponseJson, item_id)

    assert Item["id"] == item_id
    assert Item["sellerId"] == item_payload["sellerID"]
    assert Item["name"] == item_payload["name"]
    assert Item["price"] == item_payload["price"]
    assert Item["statistics"]["likes"] == item_payload["statistics"]["likes"]
    assert Item["statistics"]["viewCount"] == item_payload["statistics"]["viewCount"]
    assert Item["statistics"]["contacts"] == item_payload["statistics"]["contacts"]


def test_get_items_by_seller_id_contains_created_item(
    api_client, item_payload: dict
) -> None:
    create_response = api_client.create_item(item_payload)

    assert create_response.status_code == 200, create_response.text

    created_item_response = create_response.json()
    item_id = extract_created_item_id(created_item_response)
    seller_id = item_payload["sellerID"]

    get_response = api_client.get_items_by_seller_id(seller_id)

    assert get_response.status_code == 200, get_response.text

    ResponseJson = get_response.json()

    assert isinstance(ResponseJson, list)

    matching_items = [Item for Item in ResponseJson if Item.get("id") == item_id]

    assert len(matching_items) == 1

    Item = matching_items[0]

    assert Item["id"] == item_id
    assert Item["sellerId"] == seller_id
    assert Item["name"] == item_payload["name"]
    assert Item["price"] == item_payload["price"]


def test_get_statistic_by_item_id_returns_created_statistics(
    api_client, item_payload: dict
) -> None:
    create_response = api_client.create_item(item_payload)

    assert create_response.status_code == 200, create_response.text

    created_item_response = create_response.json()
    item_id = extract_created_item_id(created_item_response)

    statistic_response = api_client.get_statistics_by_item_id(item_id)

    assert statistic_response.status_code == 200, statistic_response.text

    ResponseJson = statistic_response.json()
    Statistic = extract_statistic_from_response(ResponseJson)

    assert "likes" in Statistic
    assert "viewCount" in Statistic
    assert "contacts" in Statistic

    assert Statistic["likes"] == item_payload["statistics"]["likes"]
    assert Statistic["viewCount"] == item_payload["statistics"]["viewCount"]
    assert Statistic["contacts"] == item_payload["statistics"]["contacts"]


def test_create_get_by_id_get_by_seller_id_get_statistic_e2e(
    api_client, item_payload: dict
) -> None:
    start_time = time.perf_counter()

    create_response = api_client.create_item(item_payload)

    assert create_response.status_code == 200, create_response.text

    created_item_response = create_response.json()
    item_id = extract_created_item_id(created_item_response)
    seller_id = item_payload["sellerID"]

    get_by_id_response = api_client.get_item(item_id)
    assert get_by_id_response.status_code == 200, get_by_id_response.text

    get_by_id_json = get_by_id_response.json()
    ItemById = extract_item_from_response(get_by_id_json, item_id)

    get_by_seller_response = api_client.get_items_by_seller_id(seller_id)
    assert get_by_seller_response.status_code == 200, get_by_seller_response.text

    get_by_seller_json = get_by_seller_response.json()
    matching_items = [Item for Item in get_by_seller_json if Item.get("id") == item_id]

    assert len(matching_items) == 1

    SellerItem = matching_items[0]

    statistic_response = api_client.get_statistics_by_item_id(item_id)
    assert statistic_response.status_code == 200, statistic_response.text

    statistic_json = statistic_response.json()
    Statistic = extract_statistic_from_response(statistic_json)

    total_duration_seconds = time.perf_counter() - start_time

    assert ItemById["id"] == item_id
    assert ItemById["sellerId"] == seller_id
    assert ItemById["name"] == item_payload["name"]
    assert ItemById["price"] == item_payload["price"]

    assert SellerItem["id"] == item_id
    assert SellerItem["sellerId"] == seller_id
    assert SellerItem["name"] == item_payload["name"]
    assert SellerItem["price"] == item_payload["price"]

    assert Statistic["likes"] == item_payload["statistics"]["likes"]
    assert Statistic["viewCount"] == item_payload["statistics"]["viewCount"]
    assert Statistic["contacts"] == item_payload["statistics"]["contacts"]

    assert total_duration_seconds < 10
