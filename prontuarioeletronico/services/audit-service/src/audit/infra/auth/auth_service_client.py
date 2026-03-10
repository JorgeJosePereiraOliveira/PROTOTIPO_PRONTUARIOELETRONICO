import httpx


class AuthServiceClient:
    def __init__(self, base_url: str, timeout_seconds: float = 5.0):
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    def verify(self, token: str) -> dict:
        response = self._request(
            method="GET",
            path="/api/v1/auth/verify",
            token=token,
        )
        body = response.json()
        if not body.get("valid"):
            raise ValueError("invalid token")
        return body

    def authorize(self, token: str, required_role: str) -> bool:
        response = self._request(
            method="GET",
            path="/api/v1/auth/authorize",
            token=token,
            params={"required_role": required_role},
        )
        body = response.json()
        return bool(body.get("authorized"))

    def _request(
        self,
        method: str,
        path: str,
        token: str,
        params: dict | None = None,
    ) -> httpx.Response:
        url = f"{self._base_url}{path}"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            with httpx.Client(timeout=self._timeout_seconds) as client:
                response = client.request(method, url, headers=headers, params=params)
        except httpx.HTTPError as error:
            raise ValueError("auth service unavailable") from error

        if response.status_code >= 400:
            try:
                detail = response.json().get("detail", "auth request failed")
            except ValueError:
                detail = "auth request failed"
            raise ValueError(str(detail))

        return response
