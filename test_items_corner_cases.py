from __future__ import annotations

from api_client import ApiClient
from build_data import build_item_payload


def extract_created_item_id(create_response_json: dict) -> str:
    assert isinstance(create_response_json, dict)
    assert "status" in create_response_json

    StatusText = create_response_json["status"]

    assert isinstance(StatusText, str)
    assert " - " in StatusText

    ItemId = StatusText.split(" - ")[-1].strip()

    assert ItemId

    return ItemId


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


def test_create_same_payload_twice_returns_different_item_ids(
    api_client: ApiClient,
) -> None:
    payload = build_item_payload()

    first_create_response = api_client.create_item(payload)
    second_create_response = api_client.create_item(payload)

    assert first_create_response.status_code == 200, first_create_response.text
    assert second_create_response.status_code == 200, second_create_response.text

    first_item_id = extract_created_item_id(first_create_response.json())
    second_item_id = extract_created_item_id(second_create_response.json())
    assert first_item_id != second_item_id


def test_same_seller_id_contains_two_created_items(api_client: ApiClient) -> None:
    first_payload = build_item_payload()
    seller_id = first_payload.get("sellerID")
    second_payload = build_item_payload(seller_id=seller_id)

    first_create_response = api_client.create_item(first_payload)
    second_create_response = api_client.create_item(second_payload)

    first_item_id = extract_created_item_id(first_create_response.json())
    second_item_id = extract_created_item_id(second_create_response.json())
    assert first_item_id != second_item_id

    get_by_seller_response = api_client.get_items_by_seller_id(seller_id)
    response_json = get_by_seller_response.json()
    assert isinstance(response_json, list)

    created_ids = {Item.get("id") for Item in response_json}
    assert first_item_id in created_ids
    assert second_item_id in created_ids


def test_repeated_get_item_by_id_returns_stable_data(api_client: ApiClient) -> None:
    payload = build_item_payload()
    create_response = api_client.create_item(payload)

    item_id = extract_created_item_id(create_response.json())
    first_get_response = api_client.get_item(item_id)
    second_get_response = api_client.get_item(item_id)

    first_item = extract_item_from_response(first_get_response.json(), item_id)
    second_item = extract_item_from_response(second_get_response.json(), item_id)

    assert first_item["id"] == second_item["id"]
    assert first_item["sellerId"] == second_item["sellerId"]
    assert first_item["name"] == second_item["name"]
    assert first_item["price"] == second_item["price"]
    assert first_item["statistics"] == second_item["statistics"]
    assert first_item["createdAt"] == second_item["createdAt"]


def test_repeated_get_statistics_by_item_id_returns_stable_data(
    api_client: ApiClient,
) -> None:
    payload = build_item_payload()
    create_response = api_client.create_item(payload)

    item_id = extract_created_item_id(create_response.json())
    first_statistics_response = api_client.get_statistics_by_item_id(item_id)
    second_statistics_response = api_client.get_statistics_by_item_id(item_id)

    first_statistic = extract_statistic_from_response(first_statistics_response.json())
    second_statistic = extract_statistic_from_response(
        second_statistics_response.json()
    )

    assert first_statistic["likes"] == second_statistic["likes"]
    assert first_statistic["viewCount"] == second_statistic["viewCount"]
    assert first_statistic["contacts"] == second_statistic["contacts"]
