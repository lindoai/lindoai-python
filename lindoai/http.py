"""
HTTP client for the Lindo SDK.

Provides typed HTTP client wrappers with authentication,
error handling, and request/response serialization.
Supports both synchronous and asynchronous operations.

@satisfies Requirements 6.4, 6.5, 6.7, 6.8
"""

from typing import Any, Dict, Optional, TypeVar, Type
import httpx

from lindoai.errors import (
    LindoError,
    NetworkError,
    TimeoutError,
    create_error_from_status,
)

T = TypeVar("T")


class HttpClient:
    """
    Synchronous HTTP client for making authenticated API requests.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: float = 30.0,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Initialize the HTTP client.

        Args:
            base_url: Base URL for API requests
            api_key: API key for authentication
            timeout: Request timeout in seconds (default: 30.0)
            headers: Custom headers to include in all requests
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            **(headers or {}),
        }
        self._client: Optional[httpx.Client] = None

    @property
    def client(self) -> httpx.Client:
        """Get or create the httpx client."""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=self._build_headers(),
            )
        return self._client

    def _build_headers(
        self,
        additional_headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        """Build the request headers with authentication."""
        return {
            **self.default_headers,
            "Authorization": f"Bearer {self.api_key}",
            **(additional_headers or {}),
        }

    def _build_url(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build the full URL with query parameters."""
        url = path if path.startswith("/") else f"/{path}"
        return url

    def _parse_response(self, response: httpx.Response) -> Any:
        """Parse the response body as JSON."""
        content_type = response.headers.get("content-type", "")

        if "application/json" in content_type:
            try:
                return response.json()
            except Exception:
                return {}

        # For non-JSON responses, try to parse as JSON
        text = response.text
        try:
            import json
            return json.loads(text)
        except Exception:
            return {"message": text}

    def _create_error(self, status_code: int, data: Any) -> LindoError:
        """Create an appropriate error from the response."""
        message = "An error occurred"
        retry_after: Optional[int] = None

        if isinstance(data, dict):
            if "message" in data:
                message = str(data["message"])
            elif "error" in data:
                message = str(data["error"])
            if "retry_after" in data:
                retry_after = int(data["retry_after"])

        return create_error_from_status(status_code, message, retry_after)

    def _request(
        self,
        method: str,
        path: str,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """Make an HTTP request and return the response data."""
        url = self._build_url(path, params)

        # Filter out None values from params
        filtered_params: Optional[Dict[str, Any]] = None
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}

        try:
            response = self.client.request(
                method=method,
                url=url,
                json=body,
                params=filtered_params,
                headers=headers,
                timeout=timeout or self.timeout,
            )

            data = self._parse_response(response)

            if not response.is_success:
                raise self._create_error(response.status_code, data)

            return data

        except httpx.TimeoutException:
            raise TimeoutError("Request timed out")
        except httpx.NetworkError:
            raise NetworkError("Network request failed")
        except LindoError:
            raise
        except Exception as e:
            raise NetworkError(f"An unexpected error occurred: {str(e)}")

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Make a GET request.

        Args:
            path: The API path (relative to base URL)
            params: Query parameters
            headers: Additional headers for this request
            timeout: Request timeout override in seconds

        Returns:
            The response data
        """
        return self._request("GET", path, params=params, headers=headers, timeout=timeout)

    def post(
        self,
        path: str,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Make a POST request.

        Args:
            path: The API path (relative to base URL)
            body: The request body
            params: Query parameters
            headers: Additional headers for this request
            timeout: Request timeout override in seconds

        Returns:
            The response data
        """
        return self._request("POST", path, body=body, params=params, headers=headers, timeout=timeout)

    def put(
        self,
        path: str,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Make a PUT request.

        Args:
            path: The API path (relative to base URL)
            body: The request body
            params: Query parameters
            headers: Additional headers for this request
            timeout: Request timeout override in seconds

        Returns:
            The response data
        """
        return self._request("PUT", path, body=body, params=params, headers=headers, timeout=timeout)

    def patch(
        self,
        path: str,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Make a PATCH request.

        Args:
            path: The API path (relative to base URL)
            body: The request body
            params: Query parameters
            headers: Additional headers for this request
            timeout: Request timeout override in seconds

        Returns:
            The response data
        """
        return self._request("PATCH", path, body=body, params=params, headers=headers, timeout=timeout)

    def delete(
        self,
        path: str,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Make a DELETE request.

        Args:
            path: The API path (relative to base URL)
            body: The request body (optional)
            params: Query parameters
            headers: Additional headers for this request
            timeout: Request timeout override in seconds

        Returns:
            The response data
        """
        return self._request("DELETE", path, body=body, params=params, headers=headers, timeout=timeout)

    def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            self._client.close()
            self._client = None


class AsyncHttpClient:
    """
    Asynchronous HTTP client for making authenticated API requests.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: float = 30.0,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Initialize the async HTTP client.

        Args:
            base_url: Base URL for API requests
            api_key: API key for authentication
            timeout: Request timeout in seconds (default: 30.0)
            headers: Custom headers to include in all requests
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            **(headers or {}),
        }
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def client(self) -> httpx.AsyncClient:
        """Get or create the async httpx client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=self._build_headers(),
            )
        return self._client

    def _build_headers(
        self,
        additional_headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        """Build the request headers with authentication."""
        return {
            **self.default_headers,
            "Authorization": f"Bearer {self.api_key}",
            **(additional_headers or {}),
        }

    def _build_url(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build the full URL with query parameters."""
        url = path if path.startswith("/") else f"/{path}"
        return url

    def _parse_response(self, response: httpx.Response) -> Any:
        """Parse the response body as JSON."""
        content_type = response.headers.get("content-type", "")

        if "application/json" in content_type:
            try:
                return response.json()
            except Exception:
                return {}

        # For non-JSON responses, try to parse as JSON
        text = response.text
        try:
            import json
            return json.loads(text)
        except Exception:
            return {"message": text}

    def _create_error(self, status_code: int, data: Any) -> LindoError:
        """Create an appropriate error from the response."""
        message = "An error occurred"
        retry_after: Optional[int] = None

        if isinstance(data, dict):
            if "message" in data:
                message = str(data["message"])
            elif "error" in data:
                message = str(data["error"])
            if "retry_after" in data:
                retry_after = int(data["retry_after"])

        return create_error_from_status(status_code, message, retry_after)

    async def _request(
        self,
        method: str,
        path: str,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """Make an async HTTP request and return the response data."""
        url = self._build_url(path, params)

        # Filter out None values from params
        filtered_params: Optional[Dict[str, Any]] = None
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}

        try:
            response = await self.client.request(
                method=method,
                url=url,
                json=body,
                params=filtered_params,
                headers=headers,
                timeout=timeout or self.timeout,
            )

            data = self._parse_response(response)

            if not response.is_success:
                raise self._create_error(response.status_code, data)

            return data

        except httpx.TimeoutException:
            raise TimeoutError("Request timed out")
        except httpx.NetworkError:
            raise NetworkError("Network request failed")
        except LindoError:
            raise
        except Exception as e:
            raise NetworkError(f"An unexpected error occurred: {str(e)}")

    async def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Make an async GET request.

        Args:
            path: The API path (relative to base URL)
            params: Query parameters
            headers: Additional headers for this request
            timeout: Request timeout override in seconds

        Returns:
            The response data
        """
        return await self._request("GET", path, params=params, headers=headers, timeout=timeout)

    async def post(
        self,
        path: str,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Make an async POST request.

        Args:
            path: The API path (relative to base URL)
            body: The request body
            params: Query parameters
            headers: Additional headers for this request
            timeout: Request timeout override in seconds

        Returns:
            The response data
        """
        return await self._request("POST", path, body=body, params=params, headers=headers, timeout=timeout)

    async def put(
        self,
        path: str,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Make an async PUT request.

        Args:
            path: The API path (relative to base URL)
            body: The request body
            params: Query parameters
            headers: Additional headers for this request
            timeout: Request timeout override in seconds

        Returns:
            The response data
        """
        return await self._request("PUT", path, body=body, params=params, headers=headers, timeout=timeout)

    async def patch(
        self,
        path: str,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Make an async PATCH request.

        Args:
            path: The API path (relative to base URL)
            body: The request body
            params: Query parameters
            headers: Additional headers for this request
            timeout: Request timeout override in seconds

        Returns:
            The response data
        """
        return await self._request("PATCH", path, body=body, params=params, headers=headers, timeout=timeout)

    async def delete(
        self,
        path: str,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Make an async DELETE request.

        Args:
            path: The API path (relative to base URL)
            body: The request body (optional)
            params: Query parameters
            headers: Additional headers for this request
            timeout: Request timeout override in seconds

        Returns:
            The response data
        """
        return await self._request("DELETE", path, body=body, params=params, headers=headers, timeout=timeout)

    async def close(self) -> None:
        """Close the async HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
