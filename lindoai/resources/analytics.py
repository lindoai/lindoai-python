"""
Analytics resource for the Lindo SDK.

Provides methods for analytics operations.

@satisfies Requirements 6.2
"""

from typing import Any, Dict, Optional

from lindoai.http import HttpClient, AsyncHttpClient
from lindoai.types import AnalyticsQuery, WorkspaceAnalytics, WebsiteAnalytics


class AnalyticsResource:
    """
    Synchronous resource class for analytics operations.
    """

    def __init__(self, http: HttpClient) -> None:
        """
        Initialize the analytics resource.

        Args:
            http: The HTTP client to use for requests
        """
        self._http = http

    def get_workspace(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> WorkspaceAnalytics:
        """
        Get analytics data for the current workspace.

        Args:
            from_date: Start date for the analytics period (ISO format)
            to_date: End date for the analytics period (ISO format)

        Returns:
            The workspace analytics data

        Example:
            >>> # Get all-time analytics
            >>> analytics = client.analytics.get_workspace()
            >>>
            >>> # Get analytics for a specific period
            >>> period_analytics = client.analytics.get_workspace(
            ...     from_date="2024-01-01",
            ...     to_date="2024-01-31"
            ... )
            >>> print("Total views:", analytics.total_views)
            >>> print("Unique visitors:", analytics.unique_visitors)
        """
        params: Dict[str, Any] = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        data = self._http.get("/v1/ai/analytics/workspace", params=params if params else None)
        return WorkspaceAnalytics.from_dict(data)

    def get_website(
        self,
        website_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> WebsiteAnalytics:
        """
        Get analytics data for a specific website.

        Args:
            website_id: The website ID to get analytics for (required)
            from_date: Start date for the analytics period (ISO format)
            to_date: End date for the analytics period (ISO format)

        Returns:
            The website analytics data

        Example:
            >>> # Get all-time analytics
            >>> analytics = client.analytics.get_website(website_id="website-123")
            >>>
            >>> # Get analytics for a specific period
            >>> period_analytics = client.analytics.get_website(
            ...     website_id="website-123",
            ...     from_date="2024-01-01",
            ...     to_date="2024-01-31"
            ... )
            >>> print("Total views:", analytics.total_views)
            >>> print("Top pages:", analytics.top_pages)
        """
        params: Dict[str, Any] = {"website_id": website_id}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        data = self._http.get("/v1/ai/analytics/website", params=params)
        return WebsiteAnalytics.from_dict(data)


class AsyncAnalyticsResource:
    """
    Asynchronous resource class for analytics operations.
    """

    def __init__(self, http: AsyncHttpClient) -> None:
        """
        Initialize the async analytics resource.

        Args:
            http: The async HTTP client to use for requests
        """
        self._http = http

    async def get_workspace(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> WorkspaceAnalytics:
        """
        Get analytics data for the current workspace.

        Args:
            from_date: Start date for the analytics period (ISO format)
            to_date: End date for the analytics period (ISO format)

        Returns:
            The workspace analytics data

        Example:
            >>> # Get all-time analytics
            >>> analytics = await client.analytics.get_workspace()
            >>>
            >>> # Get analytics for a specific period
            >>> period_analytics = await client.analytics.get_workspace(
            ...     from_date="2024-01-01",
            ...     to_date="2024-01-31"
            ... )
            >>> print("Total views:", analytics.total_views)
            >>> print("Unique visitors:", analytics.unique_visitors)
        """
        params: Dict[str, Any] = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        data = await self._http.get("/v1/ai/analytics/workspace", params=params if params else None)
        return WorkspaceAnalytics.from_dict(data)

    async def get_website(
        self,
        website_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> WebsiteAnalytics:
        """
        Get analytics data for a specific website.

        Args:
            website_id: The website ID to get analytics for (required)
            from_date: Start date for the analytics period (ISO format)
            to_date: End date for the analytics period (ISO format)

        Returns:
            The website analytics data

        Example:
            >>> # Get all-time analytics
            >>> analytics = await client.analytics.get_website(website_id="website-123")
            >>>
            >>> # Get analytics for a specific period
            >>> period_analytics = await client.analytics.get_website(
            ...     website_id="website-123",
            ...     from_date="2024-01-01",
            ...     to_date="2024-01-31"
            ... )
            >>> print("Total views:", analytics.total_views)
            >>> print("Top pages:", analytics.top_pages)
        """
        params: Dict[str, Any] = {"website_id": website_id}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        data = await self._http.get("/v1/ai/analytics/website", params=params)
        return WebsiteAnalytics.from_dict(data)
