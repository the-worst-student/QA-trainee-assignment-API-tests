import requests

from config import BASE_URL, RequestTimeOutSeconds


class ApiClient:
    def __init__(
        self,
        base_url: str = BASE_URL,
        request_timeout_seconds: int = RequestTimeOutSeconds,
    ) -> None:
        self.Base_url = base_url.rstrip("/")
        self.Request_timeout_seconds = request_timeout_seconds
        self.Session = requests.Session()
        self.Session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def create_item(self, payload: dict) -> requests.Response:
        return self.Session.post(
            url=f"{self.Base_url}/api/1/item",
            json=payload,
            timeout=self.Request_timeout_seconds,
        )

    def get_item(self, item_id: str) -> requests.Response:
        return self.Session.get(
            url=f"{self.Base_url}/api/1/item/{item_id}",
            timeout=self.Request_timeout_seconds,
        )

    def get_items_by_seller_id(self, seller_id: int) -> requests.Response:
        return self.Session.get(
            url=f"{self.Base_url}/api/1/{seller_id}/item",
            timeout=self.Request_timeout_seconds,
        )

    def get_statistics_by_item_id(self, item_id: str) -> requests.Response:
        return self.Session.get(
            url=f"{self.Base_url}/api/1/statistic/{item_id}",
            timeout=self.Request_timeout_seconds,
        )
