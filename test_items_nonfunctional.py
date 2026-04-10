import time
import uuid

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


def generate_nonexistent_item_id() -> str:
    return f"nonexistent-{uuid.uuid4()}"


def test_create_item_response_time_is_less_than_timeout(api_client: ApiClient) -> None:
    payload = build_item_payload()

    start_time = time.perf_counter()
    response = api_client.create_item(payload)
    duration_seconds = time.perf_counter() - start_time

    assert response.status_code == 200, response.text
    assert duration_seconds < api_client.Request_timeout_seconds


def test_get_item_response_time_is_less_than_timeout(api_client: ApiClient) -> None:
    payload = build_item_payload()

    create_response = api_client.create_item(payload)

    assert create_response.status_code == 200, create_response.text

    item_id = extract_created_item_id(create_response.json())

    start_time = time.perf_counter()
    get_response = api_client.get_item(item_id)
    duration_seconds = time.perf_counter() - start_time

    assert get_response.status_code == 200, get_response.text
    assert duration_seconds < api_client.Request_timeout_seconds


def test_valid_scenarios_do_not_return_5xx(api_client: ApiClient) -> None:
    payload = build_item_payload()

    create_response = api_client.create_item(payload)
    assert create_response.status_code < 500, create_response.text
    assert create_response.status_code == 200, create_response.text

    item_id = extract_created_item_id(create_response.json())
    seller_id = payload["sellerID"]

    get_item_response = api_client.get_item(item_id)
    assert get_item_response.status_code < 500, get_item_response.text
    assert get_item_response.status_code == 200, get_item_response.text

    get_seller_items_response = api_client.get_items_by_seller_id(seller_id)
    assert get_seller_items_response.status_code < 500, get_seller_items_response.text
    assert get_seller_items_response.status_code == 200, get_seller_items_response.text

    get_statistics_response = api_client.get_statistics_by_item_id(item_id)
    assert get_statistics_response.status_code < 500, get_statistics_response.text
    assert get_statistics_response.status_code == 200, get_statistics_response.text


def test_invalid_requests_do_not_return_5xx(api_client: ApiClient) -> None:
    invalid_payload = {}
    create_response = api_client.create_item(invalid_payload)

    assert create_response.status_code < 500, create_response.text

    nonexistent_item_id = generate_nonexistent_item_id()

    get_item_response = api_client.get_item(nonexistent_item_id)
    assert get_item_response.status_code < 500, get_item_response.text

    get_statistics_response = api_client.get_statistics_by_item_id(nonexistent_item_id)
    assert get_statistics_response.status_code < 500, get_statistics_response.text

    invalid_seller_id = "invalid-seller-id"
    get_seller_items_response = api_client.Session.get(
        url=f"{api_client.Base_url}/api/1/{invalid_seller_id}/item",
        timeout=api_client.Request_timeout_seconds,
    )

    assert get_seller_items_response.status_code < 500, get_seller_items_response.text
