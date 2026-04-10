import pytest

from api_client import ApiClient
from build_data import build_item_payload


@pytest.fixture
def api_client() -> ApiClient:
    return ApiClient()


@pytest.fixture
def item_payload() -> dict:
    return build_item_payload()


@pytest.fixture
def created_item(api_client: ApiClient, item_payload: dict) -> dict:
    response = api_client.create_item(item_payload)

    assert response.status_code == 200, response.text

    return response.json()
