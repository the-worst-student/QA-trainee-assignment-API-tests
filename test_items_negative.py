import uuid

from api_client import ApiClient
from build_data import build_item_payload


def assert_client_error(response) -> None:
    assert 400 <= response.status_code < 500, (
        f"Expected 4xx status code, got {response.status_code}. Response text: {response.text}"
    )


def generate_nonexistent_item_id() -> str:
    return f"nonexistent-{uuid.uuid4()}"


def test_create_item_without_seller_id_returns_client_error(api_client: ApiClient) -> None:
    payload = build_item_payload()
    payload.pop("sellerID")

    response = api_client.create_item(payload)

    assert_client_error(response)


def test_create_item_without_name_returns_client_error(api_client: ApiClient) -> None:
    payload = build_item_payload()
    payload.pop("name")

    response = api_client.create_item(payload)

    assert_client_error(response)


def test_create_item_without_price_returns_client_error(api_client: ApiClient) -> None:
    payload = build_item_payload()
    payload.pop("price")

    response = api_client.create_item(payload)

    assert_client_error(response)


def test_create_item_without_statistics_returns_client_error(api_client: ApiClient) -> None:
    payload = build_item_payload()
    payload.pop("statistics")

    response = api_client.create_item(payload)

    assert_client_error(response)


def test_create_item_with_string_seller_id_returns_client_error(api_client: ApiClient) -> None:
    payload = build_item_payload()
    payload["sellerID"] = "invalid-seller-id"

    response = api_client.create_item(payload)

    assert_client_error(response)


def test_create_item_with_string_price_returns_client_error(api_client: ApiClient) -> None:
    payload = build_item_payload()
    payload["price"] = "invalid-price"

    response = api_client.create_item(payload)

    assert_client_error(response)


def test_create_item_with_invalid_statistics_type_returns_client_error(api_client: ApiClient) -> None:
    payload = build_item_payload()
    payload["statistics"] = "invalid-statistics"

    response = api_client.create_item(payload)

    assert_client_error(response)


def test_create_item_with_empty_body_returns_client_error(api_client: ApiClient) -> None:
    response = api_client.create_item({})

    assert_client_error(response)


def test_get_item_by_nonexistent_id_returns_client_error(api_client: ApiClient) -> None:
    nonexistent_item_id = generate_nonexistent_item_id()

    response = api_client.get_item(nonexistent_item_id)

    assert_client_error(response)


def test_get_statistics_by_nonexistent_id_returns_client_error(api_client: ApiClient) -> None:
    nonexistent_item_id = generate_nonexistent_item_id()

    response = api_client.get_statistics_by_item_id(nonexistent_item_id)

    assert_client_error(response)


def test_get_items_by_invalid_seller_id_returns_client_error(api_client: ApiClient) -> None:
    invalid_seller_id = "invalid-seller-id"

    response = api_client.Session.get(
        url=f"{api_client.Base_url}/api/1/{invalid_seller_id}/item",
        timeout=api_client.Request_timeout_seconds,
    )

    assert_client_error(response)