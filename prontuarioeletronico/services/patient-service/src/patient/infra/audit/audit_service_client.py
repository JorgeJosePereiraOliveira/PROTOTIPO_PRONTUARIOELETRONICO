import httpx


class AuditServiceClient:
    def __init__(self, base_url: str, timeout_seconds: float = 5.0):
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    def create_event(self, token: str, payload: dict) -> dict:
        response = self._request(
            method="POST",
            path="/api/v1/audit/events",
            token=token,
            json=payload,
        )
        return response.json()

    def _request(
        self,
        method: str,
        path: str,
        token: str,
        params: dict | None = None,
        json: dict | None = None,
    ) -> httpx.Response:
        url = f"{self._base_url}{path}"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            with httpx.Client(timeout=self._timeout_seconds) as client:
                response = client.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    json=json,
                )
        except httpx.HTTPError as error:
            raise ValueError("audit service unavailable") from error

        if response.status_code >= 400:
            try:
                detail = response.json().get("detail", "audit request failed")
            except ValueError:
                detail = "audit request failed"
            raise ValueError(str(detail))

        return response
