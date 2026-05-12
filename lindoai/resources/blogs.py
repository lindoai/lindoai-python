"""
Blogs resource for the Lindo SDK.

Provides methods for managing website blogs (API key authentication).
"""

from typing import Optional, Dict, Any, List

from lindoai.http import HttpClient, AsyncHttpClient


class BlogsResource:
    """
    Synchronous resource class for blog management operations.
    
    These endpoints require API key authentication.
    """

    def __init__(self, http: HttpClient) -> None:
        """
        Initialize the blogs resource.

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
        List all blogs for a website.

        Args:
            website_id: The website ID
            page: Page number for pagination
            search: Search term to filter blogs

        Returns:
            The blog list response

        Example:
            >>> response = client.blogs.list("website-123", page=1)
            >>> for b in response["result"]["list"]:
            ...     print(b["name"])
        """
        params = {}
        if page is not None:
            params["page"] = str(page)
        if search is not None:
            params["search"] = search
        
        return self._http.get(
            f"/v1/workspace/website/{website_id}/blogs/list",
            params=params if params else None
        )

    def get(self, website_id: str, blog_id: str) -> Dict[str, Any]:
        """
        Get details of a specific blog.

        Args:
            website_id: The website ID
            blog_id: The blog ID

        Returns:
            The blog details response

        Example:
            >>> response = client.blogs.get("website-123", "blog-456")
            >>> print(response["result"]["name"])
        """
        return self._http.get(f"/v1/workspace/website/{website_id}/blogs/{blog_id}")

    def update(
        self,
        website_id: str,
        blog_id: str,
        name: Optional[str] = None,
        path: Optional[str] = None,
        seo: Optional[Dict[str, Any]] = None,
        blog_settings: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update a blog using PATCH semantics.

        Args:
            website_id: The website ID
            blog_id: The blog ID
            name: Blog name (optional)
            path: URL path (optional)
            seo: SEO metadata (optional)
            blog_settings: Blog settings (optional)
            data: Blog data (optional)
            language: Language code (optional)

        Returns:
            The update response

        Example:
            >>> response = client.blogs.update(
            ...     "website-123",
            ...     "blog-456",
            ...     name="Updated Blog",
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
        if blog_settings is not None:
            body["blog_settings"] = blog_settings
        if data is not None:
            body["data"] = data
        if language is not None:
            body["language"] = language
        return self._http.patch(f"/v1/workspace/website/{website_id}/blogs/{blog_id}", body)

    def unpublish(self, website_id: str, blog_id: str) -> Dict[str, Any]:
        """
        Unpublish a blog.

        Args:
            website_id: The website ID
            blog_id: The blog ID

        Returns:
            The unpublish response

        Example:
            >>> response = client.blogs.unpublish("website-123", "blog-456")
            >>> print(response["result"]["message"])
        """
        return self._http.post(f"/v1/workspace/website/{website_id}/blogs/{blog_id}/unpublish")

    def delete(self, website_id: str, blog_id: str) -> Dict[str, Any]:
        """
        Delete a blog.

        Permanently deletes a blog. If the blog was published, also removes
        the HTML file from storage and purges the cache.

        Args:
            website_id: The website ID
            blog_id: The blog ID

        Returns:
            The delete response

        Example:
            >>> response = client.blogs.delete("website-123", "blog-456")
            >>> print(response["result"]["message"])
        """
        return self._http.delete(f"/v1/workspace/website/{website_id}/blogs/{blog_id}")


class AsyncBlogsResource:
    """
    Asynchronous resource class for blog management operations.
    
    These endpoints require API key authentication.
    """

    def __init__(self, http: AsyncHttpClient) -> None:
        """
        Initialize the async blogs resource.

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
        List all blogs for a website.

        Args:
            website_id: The website ID
            page: Page number for pagination
            search: Search term to filter blogs

        Returns:
            The blog list response
        """
        params = {}
        if page is not None:
            params["page"] = str(page)
        if search is not None:
            params["search"] = search
        
        return await self._http.get(
            f"/v1/workspace/website/{website_id}/blogs/list",
            params=params if params else None
        )

    async def get(self, website_id: str, blog_id: str) -> Dict[str, Any]:
        """
        Get details of a specific blog.

        Args:
            website_id: The website ID
            blog_id: The blog ID

        Returns:
            The blog details response
        """
        return await self._http.get(f"/v1/workspace/website/{website_id}/blogs/{blog_id}")

    async def update(
        self,
        website_id: str,
        blog_id: str,
        name: Optional[str] = None,
        path: Optional[str] = None,
        seo: Optional[Dict[str, Any]] = None,
        blog_settings: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update a blog using PATCH semantics.

        Args:
            website_id: The website ID
            blog_id: The blog ID
            name: Blog name (optional)
            path: URL path (optional)
            seo: SEO metadata (optional)
            blog_settings: Blog settings (optional)
            data: Blog data (optional)
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
        if blog_settings is not None:
            body["blog_settings"] = blog_settings
        if data is not None:
            body["data"] = data
        if language is not None:
            body["language"] = language
        return await self._http.patch(f"/v1/workspace/website/{website_id}/blogs/{blog_id}", body)

    async def unpublish(self, website_id: str, blog_id: str) -> Dict[str, Any]:
        """
        Unpublish a blog.

        Args:
            website_id: The website ID
            blog_id: The blog ID

        Returns:
            The unpublish response
        """
        return await self._http.post(f"/v1/workspace/website/{website_id}/blogs/{blog_id}/unpublish")

    async def delete(self, website_id: str, blog_id: str) -> Dict[str, Any]:
        """
        Delete a blog.

        Permanently deletes a blog. If the blog was published, also removes
        the HTML file from storage and purges the cache.

        Args:
            website_id: The website ID
            blog_id: The blog ID

        Returns:
            The delete response
        """
        return await self._http.delete(f"/v1/workspace/website/{website_id}/blogs/{blog_id}")
