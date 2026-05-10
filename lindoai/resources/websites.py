"""
Websites resource for the Lindo SDK.

Provides methods for managing workspace websites (API key authentication).

@satisfies Requirements 6.2, 25.3
"""

from typing import Optional, Dict, Any

from lindoai.http import HttpClient, AsyncHttpClient
from lindoai.types import (
    WebsiteListResponse,
    WebsiteUpdateRequest,
    WebsiteUpdateResponse,
    WebsiteDeleteRequest,
    WebsiteDeleteResponse,
    WebsiteAssignRequest,
    WebsiteAssignResponse,
)


class WebsitesResource:
    """
    Synchronous resource class for website management operations.
    
    These endpoints require API key authentication.
    """

    def __init__(self, http: HttpClient) -> None:
        """
        Initialize the websites resource.

        Args:
            http: The HTTP client to use for requests
        """
        self._http = http

    def list(
        self,
        page: Optional[int] = None,
        search: Optional[str] = None,
    ) -> WebsiteListResponse:
        """
        List all workspace websites.

        Args:
            page: Page number for pagination
            search: Search term to filter websites

        Returns:
            The website list response

        Example:
            >>> response = client.websites.list(page=1)
            >>> for w in response.websites:
            ...     print(w.business_name)
        """
        params = {}
        if page is not None:
            params["page"] = str(page)
        if search is not None:
            params["search"] = search
        
        data = self._http.get("/v1/workspace/website/list", params=params if params else None)
        return WebsiteListResponse.from_dict(data)

    def get(self, website_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific website.

        Args:
            website_id: The website ID to retrieve details for

        Returns:
            The website details response
        """
        return self._http.get(f"/v1/workspace/website/{website_id}")

    def update(
        self,
        website_id: str,
        business_name: Optional[str] = None,
        activated: Optional[bool] = None,
    ) -> WebsiteUpdateResponse:
        """
        Update a website.

        Args:
            website_id: The website ID to update
            business_name: New business name
            activated: Whether to activate the website

        Returns:
            The website update response
        """
        request = WebsiteUpdateRequest(
            website_id=website_id,
            business_name=business_name,
            activated=activated,
        )
        data = self._http.put("/v1/workspace/website/update", request.to_dict())
        return WebsiteUpdateResponse.from_dict(data)

    def update_settings(self, website_id: str, **settings) -> Dict[str, Any]:
        """
        Update website settings.

        Args:
            website_id: The website ID to update
            **settings: Settings to update (business_name, language, theme, etc.)

        Returns:
            The settings update response
        """
        return self._http.put(f"/v1/workspace/website/{website_id}/settings", settings)

    def delete(self, website_id: str) -> WebsiteDeleteResponse:
        """
        Delete a website.

        Args:
            website_id: The website ID to delete

        Returns:
            The website deletion response
        """
        request = WebsiteDeleteRequest(website_id=website_id)
        data = self._http.delete("/v1/workspace/website/delete", body=request.to_dict())
        return WebsiteDeleteResponse.from_dict(data)

    def assign(self, website_id: str, client_id: str) -> WebsiteAssignResponse:
        """
        Assign a website to a client.

        Args:
            website_id: The website ID to assign
            client_id: The client ID to assign the website to

        Returns:
            The website assignment response
        """
        request = WebsiteAssignRequest(website_id=website_id, client_id=client_id)
        data = self._http.post("/v1/workspace/website/assign", request.to_dict())
        return WebsiteAssignResponse.from_dict(data)

    def add_domain(self, website_id: str, domain: str) -> Dict[str, Any]:
        """
        Add a custom domain to a website.

        Args:
            website_id: The website ID
            domain: The custom domain to add

        Returns:
            The domain add response with DNS records
        """
        return self._http.post(f"/v1/workspace/website/{website_id}/domain", {"domain": domain})

    def remove_domain(self, website_id: str) -> Dict[str, Any]:
        """
        Remove a custom domain from a website.

        Args:
            website_id: The website ID

        Returns:
            The domain remove response
        """
        return self._http.delete(f"/v1/workspace/website/{website_id}/domain")

    def add_integration(self, website_id: str, integration_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add an integration to a website.

        Args:
            website_id: The website ID
            integration_type: The type of integration (e.g., 'matomo')
            config: The integration configuration

        Returns:
            The integration add response
        """
        return self._http.post(f"/v1/workspace/website/{website_id}/integration", {
            "integration_type": integration_type,
            "config": config
        })

    def remove_integration(self, website_id: str, integration_type: str) -> Dict[str, Any]:
        """
        Remove an integration from a website.

        Args:
            website_id: The website ID
            integration_type: The type of integration to remove

        Returns:
            The integration remove response
        """
        return self._http.delete(f"/v1/workspace/website/{website_id}/integration/{integration_type}")

    def add_team_member(self, website_id: str, email: str, role: str) -> Dict[str, Any]:
        """
        Add a team member to a website.

        Args:
            website_id: The website ID
            email: The email address of the team member
            role: The role to assign ('Editor' or 'Commenter')

        Returns:
            The team member add response
        """
        return self._http.post(f"/v1/workspace/website/{website_id}/team", {"email": email, "role": role})

    def remove_team_member(self, website_id: str, member_id: str) -> Dict[str, Any]:
        """
        Remove a team member from a website.

        Args:
            website_id: The website ID
            member_id: The member ID to remove

        Returns:
            The team member remove response
        """
        return self._http.delete(f"/v1/workspace/website/{website_id}/team/{member_id}")

    def get_team(self, website_id: str) -> Dict[str, Any]:
        """
        Get the list of team members for a website.

        Args:
            website_id: The website ID

        Returns:
            The team list response

        Example:
            >>> response = client.websites.get_team("website-123")
            >>> for member in response["result"]["list"]:
            ...     print(member["email"], member["role"])
        """
        return self._http.get(f"/v1/workspace/website/{website_id}/team")

    def get_analytics(
        self,
        website_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get analytics data for a website.

        Args:
            website_id: The website ID
            from_date: Start date for analytics (ISO format)
            to_date: End date for analytics (ISO format)

        Returns:
            The website analytics response

        Example:
            >>> response = client.websites.get_analytics("website-123")
            >>> print("Total requests:", response["result"]["total_requests"])
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        return self._http.get(f"/v1/workspace/website/{website_id}/analytics", params=params if params else None)


class AsyncWebsitesResource:
    """
    Asynchronous resource class for website management operations.
    
    These endpoints require API key authentication.
    """

    def __init__(self, http: AsyncHttpClient) -> None:
        """
        Initialize the async websites resource.

        Args:
            http: The async HTTP client to use for requests
        """
        self._http = http

    async def list(
        self,
        page: Optional[int] = None,
        search: Optional[str] = None,
    ) -> WebsiteListResponse:
        """
        List all workspace websites.

        Args:
            page: Page number for pagination
            search: Search term to filter websites

        Returns:
            The website list response
        """
        params = {}
        if page is not None:
            params["page"] = str(page)
        if search is not None:
            params["search"] = search
        
        data = await self._http.get("/v1/workspace/website/list", params=params if params else None)
        return WebsiteListResponse.from_dict(data)

    async def get(self, website_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific website.

        Args:
            website_id: The website ID to retrieve details for

        Returns:
            The website details response
        """
        return await self._http.get(f"/v1/workspace/website/{website_id}")

    async def update(
        self,
        website_id: str,
        business_name: Optional[str] = None,
        activated: Optional[bool] = None,
    ) -> WebsiteUpdateResponse:
        """
        Update a website.

        Args:
            website_id: The website ID to update
            business_name: New business name
            activated: Whether to activate the website

        Returns:
            The website update response
        """
        request = WebsiteUpdateRequest(
            website_id=website_id,
            business_name=business_name,
            activated=activated,
        )
        data = await self._http.put("/v1/workspace/website/update", request.to_dict())
        return WebsiteUpdateResponse.from_dict(data)

    async def update_settings(self, website_id: str, **settings) -> Dict[str, Any]:
        """
        Update website settings.

        Args:
            website_id: The website ID to update
            **settings: Settings to update (business_name, language, theme, etc.)

        Returns:
            The settings update response
        """
        return await self._http.put(f"/v1/workspace/website/{website_id}/settings", settings)

    async def delete(self, website_id: str) -> WebsiteDeleteResponse:
        """
        Delete a website.

        Args:
            website_id: The website ID to delete

        Returns:
            The website deletion response
        """
        request = WebsiteDeleteRequest(website_id=website_id)
        data = await self._http.delete("/v1/workspace/website/delete", body=request.to_dict())
        return WebsiteDeleteResponse.from_dict(data)

    async def assign(self, website_id: str, client_id: str) -> WebsiteAssignResponse:
        """
        Assign a website to a client.

        Args:
            website_id: The website ID to assign
            client_id: The client ID to assign the website to

        Returns:
            The website assignment response
        """
        request = WebsiteAssignRequest(website_id=website_id, client_id=client_id)
        data = await self._http.post("/v1/workspace/website/assign", request.to_dict())
        return WebsiteAssignResponse.from_dict(data)

    async def add_domain(self, website_id: str, domain: str) -> Dict[str, Any]:
        """
        Add a custom domain to a website.

        Args:
            website_id: The website ID
            domain: The custom domain to add

        Returns:
            The domain add response with DNS records
        """
        return await self._http.post(f"/v1/workspace/website/{website_id}/domain", {"domain": domain})

    async def remove_domain(self, website_id: str) -> Dict[str, Any]:
        """
        Remove a custom domain from a website.

        Args:
            website_id: The website ID

        Returns:
            The domain remove response
        """
        return await self._http.delete(f"/v1/workspace/website/{website_id}/domain")

    async def add_integration(self, website_id: str, integration_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add an integration to a website.

        Args:
            website_id: The website ID
            integration_type: The type of integration (e.g., 'matomo')
            config: The integration configuration

        Returns:
            The integration add response
        """
        return await self._http.post(f"/v1/workspace/website/{website_id}/integration", {
            "integration_type": integration_type,
            "config": config
        })

    async def remove_integration(self, website_id: str, integration_type: str) -> Dict[str, Any]:
        """
        Remove an integration from a website.

        Args:
            website_id: The website ID
            integration_type: The type of integration to remove

        Returns:
            The integration remove response
        """
        return await self._http.delete(f"/v1/workspace/website/{website_id}/integration/{integration_type}")

    async def add_team_member(self, website_id: str, email: str, role: str) -> Dict[str, Any]:
        """
        Add a team member to a website.

        Args:
            website_id: The website ID
            email: The email address of the team member
            role: The role to assign ('Editor' or 'Commenter')

        Returns:
            The team member add response
        """
        return await self._http.post(f"/v1/workspace/website/{website_id}/team", {"email": email, "role": role})

    async def remove_team_member(self, website_id: str, member_id: str) -> Dict[str, Any]:
        """
        Remove a team member from a website.

        Args:
            website_id: The website ID
            member_id: The member ID to remove

        Returns:
            The team member remove response
        """
        return await self._http.delete(f"/v1/workspace/website/{website_id}/team/{member_id}")

    async def get_team(self, website_id: str) -> Dict[str, Any]:
        """
        Get the list of team members for a website.

        Args:
            website_id: The website ID

        Returns:
            The team list response
        """
        return await self._http.get(f"/v1/workspace/website/{website_id}/team")

    async def get_analytics(
        self,
        website_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get analytics data for a website.

        Args:
            website_id: The website ID
            from_date: Start date for analytics (ISO format)
            to_date: End date for analytics (ISO format)

        Returns:
            The website analytics response
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        return await self._http.get(f"/v1/workspace/website/{website_id}/analytics", params=params if params else None)
