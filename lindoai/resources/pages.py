"""
Pages resource for the Lindo SDK.

Provides methods for managing website pages (API key authentication).
"""

from typing import Optional, Dict, Any, List

from lindoai.http import HttpClient, AsyncHttpClient


class PagesResource:
    """
    Synchronous resource class for page management operations.
    
    These endpoints require API key authentication.
    """

    def __init__(self, http: HttpClient) -> None:
        """
        Initialize the pages resource.

        Args:
            http: The HTTP client to use for requests
        """
        self._http = http

    def list(
        self,
        website_id: str,
        page: Optional[int] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List all pages for a website.

        Args:
            website_id: The website ID
            page: Page number for pagination
            search: Search term to filter pages

        Returns:
            The page list response

        Example:
            >>> response = client.pages.list("website-123", page=1)
            >>> for p in response["result"]["list"]:
            ...     print(p["name"])
        """
        params = {}
        if page is not None:
            params["page"] = str(page)
        if search is not None:
            params["search"] = search
        
        return self._http.get(
            f"/v1/workspace/website/{website_id}/pages/list",
            params=params if params else None
        )

    def get(self, website_id: str, page_id: str) -> Dict[str, Any]:
        """
        Get details of a specific page.

        Args:
            website_id: The website ID
            page_id: The page ID

        Returns:
            The page details response

        Example:
            >>> response = client.pages.get("website-123", "page-456")
            >>> print(response["result"]["name"])
        """
        return self._http.get(f"/v1/workspace/website/{website_id}/pages/{page_id}")

    def update(
        self,
        website_id: str,
        page_id: str,
        name: Optional[str] = None,
        path: Optional[str] = None,
        seo: Optional[Dict[str, Any]] = None,
        settings: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update a page using PATCH semantics.

        Args:
            website_id: The website ID
            page_id: The page ID
            name: Page name (optional)
            path: URL path (optional)
            seo: SEO metadata (optional)
            settings: Page settings (optional)
            data: Page data (optional)
            language: Language code (optional)

        Returns:
            The update response

        Example:
            >>> response = client.pages.update(
            ...     "website-123",
            ...     "page-456",
            ...     name="Updated Page",
            ...     language="en"
            ... )
            >>> print(response["result"]["message"])
        """
        body = {}
        if name is not None:
            body["name"] = name
        if path is not None:
            body["path"] = path
        if seo is not None:
            body["seo"] = seo
        if settings is not None:
            body["settings"] = settings
        if data is not None:
            body["data"] = data
        if language is not None:
            body["language"] = language
        return self._http.patch(f"/v1/workspace/website/{website_id}/pages/{page_id}", body)

    def unpublish(self, website_id: str, page_id: str) -> Dict[str, Any]:
        """
        Unpublish a page.

        Args:
            website_id: The website ID
            page_id: The page ID

        Returns:
            The unpublish response

        Example:
            >>> response = client.pages.unpublish("website-123", "page-456")
            >>> print(response["result"]["message"])
        """
        return self._http.post(f"/v1/workspace/website/{website_id}/pages/{page_id}/unpublish")

    def delete(self, website_id: str, page_id: str) -> Dict[str, Any]:
        """
        Delete a page.

        Permanently deletes a page. If the page was published, also removes
        the HTML file from storage and purges the cache.

        Args:
            website_id: The website ID
            page_id: The page ID

        Returns:
            The delete response

        Example:
            >>> response = client.pages.delete("website-123", "page-456")
            >>> print(response["result"]["message"])
        """
        return self._http.delete(f"/v1/workspace/website/{website_id}/pages/{page_id}")


class AsyncPagesResource:
    """
    Asynchronous resource class for page management operations.
    
    These endpoints require API key authentication.
    """

    def __init__(self, http: AsyncHttpClient) -> None:
        """
        Initialize the async pages resource.

        Args:
            http: The async HTTP client to use for requests
        """
        self._http = http

    async def list(
        self,
        website_id: str,
        page: Optional[int] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List all pages for a website.

        Args:
            website_id: The website ID
            page: Page number for pagination
            search: Search term to filter pages

        Returns:
            The page list response
        """
        params = {}
        if page is not None:
            params["page"] = str(page)
        if search is not None:
            params["search"] = search
        
        return await self._http.get(
            f"/v1/workspace/website/{website_id}/pages/list",
            params=params if params else None
        )

    async def get(self, website_id: str, page_id: str) -> Dict[str, Any]:
        """
        Get details of a specific page.

        Args:
            website_id: The website ID
            page_id: The page ID

        Returns:
            The page details response
        """
        return await self._http.get(f"/v1/workspace/website/{website_id}/pages/{page_id}")

    async def update(
        self,
        website_id: str,
        page_id: str,
        name: Optional[str] = None,
        path: Optional[str] = None,
        seo: Optional[Dict[str, Any]] = None,
        settings: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update a page using PATCH semantics.

        Args:
            website_id: The website ID
            page_id: The page ID
            name: Page name (optional)
            path: URL path (optional)
            seo: SEO metadata (optional)
            settings: Page settings (optional)
            data: Page data (optional)
            language: Language code (optional)

        Returns:
            The update response
        """
        body = {}
        if name is not None:
            body["name"] = name
        if path is not None:
            body["path"] = path
        if seo is not None:
            body["seo"] = seo
        if settings is not None:
            body["settings"] = settings
        if data is not None:
            body["data"] = data
        if language is not None:
            body["language"] = language
        return await self._http.patch(f"/v1/workspace/website/{website_id}/pages/{page_id}", body)

    async def unpublish(self, website_id: str, page_id: str) -> Dict[str, Any]:
        """
        Unpublish a page.

        Args:
            website_id: The website ID
            page_id: The page ID

        Returns:
            The unpublish response
        """
        return await self._http.post(f"/v1/workspace/website/{website_id}/pages/{page_id}/unpublish")

    async def delete(self, website_id: str, page_id: str) -> Dict[str, Any]:
        """
        Delete a page.

        Permanently deletes a page. If the page was published, also removes
        the HTML file from storage and purges the cache.

        Args:
            website_id: The website ID
            page_id: The page ID

        Returns:
            The delete response
        """
        return await self._http.delete(f"/v1/workspace/website/{website_id}/pages/{page_id}")
