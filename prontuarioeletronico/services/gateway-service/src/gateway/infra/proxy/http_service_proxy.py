from __future__ import annotations

import httpx


class HttpServiceProxy:
    def __init__(self, base_url: str, timeout_seconds: float = 10.0):
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    def request(
        self,
        method: str,
        path: str,
        authorization: str | None = None,
        json_body: dict | None = None,
        params: dict | None = None,
    ) -> tuple[int, object]:
        url = f"{self._base_url}{path}"
        headers = {"Content-Type": "application/json"}
        if authorization:
            headers["Authorization"] = authorization

        try:
            with httpx.Client(timeout=self._timeout_seconds) as client:
                response = client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=json_body,
                    params=params,
                )
        except httpx.HTTPError:
            return 503, {"detail": "downstream service unavailable"}

        try:
            body: object = response.json()
        except ValueError:
            body = {"detail": response.text}

        return response.status_code, body