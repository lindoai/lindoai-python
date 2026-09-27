"""
Clients resource for the Lindo SDK.

Provides methods for managing workspace clients (API key authentication).

@satisfies Requirements 6.2
"""

from typing import Optional

from lindoai.http import HttpClient, AsyncHttpClient
from lindoai.types import (
    ClientCreateRequest,
    ClientCreateResponse,
    ClientListResponse,
    ClientUpdateRequest,
    ClientUpdateResponse,
    ClientDeleteRequest,
    ClientDeleteResponse,
    MagicLinkCreateRequest,
    MagicLinkCreateResponse,
)


class ClientsResource:
    """
    Synchronous resource class for client management operations.
    
    These endpoints require API key authentication.
    """

    def __init__(self, http: HttpClient) -> None:
        """
        Initialize the clients resource.

        Args:
            http: The HTTP client to use for requests
        """
        self._http = http

    def create(
        self,
        email: str,
        website_limit: Optional[int] = None,
    ) -> ClientCreateResponse:
        """
        Create a new workspace client.

        Args:
            email: Client email address
            website_limit: Maximum number of websites the client can have

        Returns:
            The client creation response

        Example:
            >>> response = client.clients.create(
            ...     email="user@example.com",
            ...     website_limit=5
            ... )
            >>> if response.success:
            ...     print("Created client:", response.client.record_id)
        """
        request = ClientCreateRequest(email=email, website_limit=website_limit)
        data = self._http.post("/v1/workspace/client/create", request.to_dict())
        return ClientCreateResponse.from_dict(data)

    def list(
        self,
        page: Optional[int] = None,
        search: Optional[str] = None,
    ) -> ClientListResponse:
        """
        List all workspace clients.

        Args:
            page: Page number for pagination
            search: Search term to filter clients

        Returns:
            The client list response

        Example:
            >>> response = client.clients.list(page=1)
            >>> for c in response.clients:
            ...     print(c.email)
        """
        params = {}
        if page is not None:
            params["page"] = str(page)
        if search is not None:
            params["search"] = search
        
        data = self._http.get("/v1/workspace/client/list", params=params if params else None)
        return ClientListResponse.from_dict(data)

    def update(
        self,
        client_id: str,
        website_limit: Optional[int] = None,
        suspended: Optional[bool] = None,
    ) -> ClientUpdateResponse:
        """
        Update a workspace client.

        Args:
            client_id: The client ID to update
            website_limit: New website limit
            suspended: Whether to suspend the client

        Returns:
            The client update response

        Example:
            >>> response = client.clients.update(
            ...     client_id="client-123",
            ...     website_limit=10
            ... )
        """
        request = ClientUpdateRequest(
            client_id=client_id,
            website_limit=website_limit,
            suspended=suspended,
        )
        data = self._http.put("/v1/workspace/client/update", request.to_dict())
        return ClientUpdateResponse.from_dict(data)

    def delete(self, client_id: str) -> ClientDeleteResponse:
        """
        Delete a workspace client.

        Args:
            client_id: The client ID to delete

        Returns:
            The client deletion response

        Example:
            >>> response = client.clients.delete("client-123")
            >>> if response.success:
            ...     print("Client deleted")
        """
        request = ClientDeleteRequest(client_id=client_id)
        data = self._http.delete("/v1/workspace/client/delete", body=request.to_dict())
        return ClientDeleteResponse.from_dict(data)

    def create_magic_link(self, email: str) -> MagicLinkCreateResponse:
        """
        Create a magic link for client authentication.

        Args:
            email: Email address to send the magic link to

        Returns:
            The magic link creation response

        Example:
            >>> response = client.clients.create_magic_link("user@example.com")
            >>> if response.success:
            ...     print("Magic link:", response.magic_link)
        """
        request = MagicLinkCreateRequest(email=email)
        data = self._http.post("/v1/workspace/client/magic-link", request.to_dict())
        return MagicLinkCreateResponse.from_dict(data)


class AsyncClientsResource:
    """
    Asynchronous resource class for client management operations.
    
    These endpoints require API key authentication.
    """

    def __init__(self, http: AsyncHttpClient) -> None:
        """
        Initialize the async clients resource.

        Args:
            http: The async HTTP client to use for requests
        """
        self._http = http

    async def create(
        self,
        email: str,
        website_limit: Optional[int] = None,
    ) -> ClientCreateResponse:
        """
        Create a new workspace client.

        Args:
            email: Client email address
            website_limit: Maximum number of websites the client can have

        Returns:
            The client creation response
        """
        request = ClientCreateRequest(email=email, website_limit=website_limit)
        data = await self._http.post("/v1/workspace/client/create", request.to_dict())
        return ClientCreateResponse.from_dict(data)

    async def list(
        self,
        page: Optional[int] = None,
        search: Optional[str] = None,
    ) -> ClientListResponse:
        """
        List all workspace clients.

        Args:
            page: Page number for pagination
            search: Search term to filter clients

        Returns:
            The client list response
        """
        params = {}
        if page is not None:
            params["page"] = str(page)
        if search is not None:
            params["search"] = search
        
        data = await self._http.get("/v1/workspace/client/list", params=params if params else None)
        return ClientListResponse.from_dict(data)

    async def update(
        self,
        client_id: str,
        website_limit: Optional[int] = None,
        suspended: Optional[bool] = None,
    ) -> ClientUpdateResponse:
        """
        Update a workspace client.

        Args:
            client_id: The client ID to update
            website_limit: New website limit
            suspended: Whether to suspend the client

        Returns:
            The client update response
        """
        request = ClientUpdateRequest(
            client_id=client_id,
            website_limit=website_limit,
            suspended=suspended,
        )
        data = await self._http.put("/v1/workspace/client/update", request.to_dict())
        return ClientUpdateResponse.from_dict(data)

    async def delete(self, client_id: str) -> ClientDeleteResponse:
        """
        Delete a workspace client.

        Args:
            client_id: The client ID to delete

        Returns:
            The client deletion response
        """
        request = ClientDeleteRequest(client_id=client_id)
        data = await self._http.delete("/v1/workspace/client/delete", body=request.to_dict())
        return ClientDeleteResponse.from_dict(data)

    async def create_magic_link(self, email: str) -> MagicLinkCreateResponse:
        """
        Create a magic link for client authentication.

        Args:
            email: Email address to send the magic link to

        Returns:
            The magic link creation response
        """
        request = MagicLinkCreateRequest(email=email)
        data = await self._http.post("/v1/workspace/client/magic-link", request.to_dict())
        return MagicLinkCreateResponse.from_dict(data)
