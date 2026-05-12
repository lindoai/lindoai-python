"""
Main client for the Lindo SDK.

Provides a unified interface for interacting with the Lindo API.
Supports both synchronous and asynchronous operations.

@satisfies Requirements 6.1, 6.2
"""

from typing import Optional
from types import TracebackType

from lindoai.http import HttpClient, AsyncHttpClient
from lindoai.resources import (
    AgentsResource,
    AsyncAgentsResource,
    WorkflowsResource,
    AsyncWorkflowsResource,
    WorkspaceResource,
    AsyncWorkspaceResource,
    AnalyticsResource,
    AsyncAnalyticsResource,
    ClientsResource,
    AsyncClientsResource,
    WebsitesResource,
    AsyncWebsitesResource,
    PagesResource,
    AsyncPagesResource,
    BlogsResource,
    AsyncBlogsResource,
)

# Default base URL for the Lindo API
DEFAULT_BASE_URL = "https://api.lindo.ai"

# Default request timeout in seconds
DEFAULT_TIMEOUT = 30.0


class LindoClient:
    """
    The main Lindo SDK client (synchronous).

    Provides access to all Lindo API resources through typed methods.

    Example:
        >>> from lindoai import LindoClient
        >>>
        >>> client = LindoClient(api_key="your-api-key")
        >>>
        >>> # Run an agent
        >>> result = client.agents.run(
        ...     agent_id="my-agent",
        ...     input={"prompt": "Hello!"}
        ... )
        >>>
        >>> # Start a workflow
        >>> workflow = client.workflows.start(
        ...     workflow_name="publish-page",
        ...     params={"page_id": "page-123"}
        ... )
        >>>
        >>> # Get workspace credits
        >>> credits = client.workspace.get_credits()
        >>>
        >>> # Get analytics
        >>> analytics = client.analytics.get_workspace()
        >>>
        >>> # Close the client when done
        >>> client.close()

    Using context manager:
        >>> with LindoClient(api_key="your-api-key") as client:
        ...     result = client.agents.run(
        ...         agent_id="my-agent",
        ...         input={"prompt": "Hello!"}
        ...     )
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Create a new Lindo client.

        Args:
            api_key: Your Lindo API key. Required for authentication.
            base_url: Base URL for API requests. Defaults to https://api.lindo.ai
            timeout: Request timeout in seconds. Defaults to 30.0

        Raises:
            ValueError: If api_key is not provided

        Example:
            >>> client = LindoClient(
            ...     api_key="your-api-key",
            ...     base_url="https://api.lindo.ai",
            ...     timeout=30.0
            ... )
        """
        if not api_key:
            raise ValueError(
                "API key is required. Please provide an api_key in the configuration."
            )

        self._http = HttpClient(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
        )

        # Initialize resources
        self._agents = AgentsResource(self._http)
        self._workflows = WorkflowsResource(self._http)
        self._workspace = WorkspaceResource(self._http)
        self._analytics = AnalyticsResource(self._http)
        self._clients = ClientsResource(self._http)
        self._websites = WebsitesResource(self._http)
        self._pages = PagesResource(self._http)
        self._blogs = BlogsResource(self._http)

    @property
    def agents(self) -> AgentsResource:
        """
        Resource for AI agent operations.

        Example:
            >>> result = client.agents.run(
            ...     agent_id="my-agent",
            ...     input={"prompt": "Hello!"}
            ... )
        """
        return self._agents

    @property
    def workflows(self) -> WorkflowsResource:
        """
        Resource for workflow operations.

        Example:
            >>> workflow = client.workflows.start(
            ...     workflow_name="publish-page",
            ...     params={"page_id": "page-123"}
            ... )
            >>> status = client.workflows.get_status(workflow.instance_id)
        """
        return self._workflows

    @property
    def workspace(self) -> WorkspaceResource:
        """
        Resource for workspace operations.

        Example:
            >>> credits = client.workspace.get_credits()
            >>> print("Balance:", credits.balance)
        """
        return self._workspace

    @property
    def analytics(self) -> AnalyticsResource:
        """
        Resource for analytics operations.

        Example:
            >>> analytics = client.analytics.get_workspace(
            ...     from_date="2024-01-01",
            ...     to_date="2024-01-31"
            ... )
        """
        return self._analytics

    @property
    def clients(self) -> ClientsResource:
        """
        Resource for client management operations.

        Example:
            >>> clients = client.clients.list()
            >>> new_client = client.clients.create(
            ...     email="user@example.com",
            ...     website_limit=5
            ... )
        """
        return self._clients

    @property
    def websites(self) -> WebsitesResource:
        """
        Resource for website management operations.

        Example:
            >>> websites = client.websites.list()
            >>> client.websites.update(
            ...     website_id="website-123",
            ...     business_name="My Business"
            ... )
        """
        return self._websites

    @property
    def pages(self) -> PagesResource:
        """
        Resource for page management operations.

        Example:
            >>> pages = client.pages.list("website-123")
            >>> client.pages.publish("website-123", "page-456")
        """
        return self._pages

    @property
    def blogs(self) -> BlogsResource:
        """
        Resource for blog management operations.

        Example:
            >>> blogs = client.blogs.list("website-123")
            >>> client.blogs.publish("website-123", "blog-456")
        """
        return self._blogs

    def close(self) -> None:
        """
        Close the client and release resources.

        This should be called when you're done using the client.
        Alternatively, use the client as a context manager.
        """
        self._http.close()

    def __enter__(self) -> "LindoClient":
        """Enter the context manager."""
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Exit the context manager and close the client."""
        self.close()


class AsyncLindoClient:
    """
    The main Lindo SDK client (asynchronous).

    Provides access to all Lindo API resources through typed async methods.

    Example:
        >>> import asyncio
        >>> from lindoai import AsyncLindoClient
        >>>
        >>> async def main():
        ...     async with AsyncLindoClient(api_key="your-api-key") as client:
        ...         # Run an agent
        ...         result = await client.agents.run(
        ...             agent_id="my-agent",
        ...             input={"prompt": "Hello!"}
        ...         )
        ...
        ...         # Start a workflow
        ...         workflow = await client.workflows.start(
        ...             workflow_name="publish-page",
        ...             params={"page_id": "page-123"}
        ...         )
        ...
        ...         # Get workspace credits
        ...         credits = await client.workspace.get_credits()
        ...
        ...         # Get analytics
        ...         analytics = await client.analytics.get_workspace()
        >>>
        >>> asyncio.run(main())
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Create a new async Lindo client.

        Args:
            api_key: Your Lindo API key. Required for authentication.
            base_url: Base URL for API requests. Defaults to https://api.lindo.ai
            timeout: Request timeout in seconds. Defaults to 30.0

        Raises:
            ValueError: If api_key is not provided

        Example:
            >>> client = AsyncLindoClient(
            ...     api_key="your-api-key",
            ...     base_url="https://api.lindo.ai",
            ...     timeout=30.0
            ... )
        """
        if not api_key:
            raise ValueError(
                "API key is required. Please provide an api_key in the configuration."
            )

        self._http = AsyncHttpClient(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
        )

        # Initialize resources
        self._agents = AsyncAgentsResource(self._http)
        self._workflows = AsyncWorkflowsResource(self._http)
        self._workspace = AsyncWorkspaceResource(self._http)
        self._analytics = AsyncAnalyticsResource(self._http)
        self._clients = AsyncClientsResource(self._http)
        self._websites = AsyncWebsitesResource(self._http)
        self._pages = AsyncPagesResource(self._http)
        self._blogs = AsyncBlogsResource(self._http)

    @property
    def agents(self) -> AsyncAgentsResource:
        """
        Resource for AI agent operations.

        Example:
            >>> result = await client.agents.run(
            ...     agent_id="my-agent",
            ...     input={"prompt": "Hello!"}
            ... )
        """
        return self._agents

    @property
    def workflows(self) -> AsyncWorkflowsResource:
        """
        Resource for workflow operations.

        Example:
            >>> workflow = await client.workflows.start(
            ...     workflow_name="publish-page",
            ...     params={"page_id": "page-123"}
            ... )
            >>> status = await client.workflows.get_status(workflow.instance_id)
        """
        return self._workflows

    @property
    def workspace(self) -> AsyncWorkspaceResource:
        """
        Resource for workspace operations.

        Example:
            >>> credits = await client.workspace.get_credits()
            >>> print("Balance:", credits.balance)
        """
        return self._workspace

    @property
    def analytics(self) -> AsyncAnalyticsResource:
        """
        Resource for analytics operations.

        Example:
            >>> analytics = await client.analytics.get_workspace(
            ...     from_date="2024-01-01",
            ...     to_date="2024-01-31"
            ... )
        """
        return self._analytics

    @property
    def clients(self) -> AsyncClientsResource:
        """
        Resource for client management operations.

        Example:
            >>> clients = await client.clients.list()
            >>> new_client = await client.clients.create(
            ...     email="user@example.com",
            ...     website_limit=5
            ... )
        """
        return self._clients

    @property
    def websites(self) -> AsyncWebsitesResource:
        """
        Resource for website management operations.

        Example:
            >>> websites = await client.websites.list()
            >>> await client.websites.update(
            ...     website_id="website-123",
            ...     business_name="My Business"
            ... )
        """
        return self._websites

    @property
    def pages(self) -> AsyncPagesResource:
        """
        Resource for page management operations.

        Example:
            >>> pages = await client.pages.list("website-123")
            >>> await client.pages.publish("website-123", "page-456")
        """
        return self._pages

    @property
    def blogs(self) -> AsyncBlogsResource:
        """
        Resource for blog management operations.

        Example:
            >>> blogs = await client.blogs.list("website-123")
            >>> await client.blogs.publish("website-123", "blog-456")
        """
        return self._blogs

    async def close(self) -> None:
        """
        Close the client and release resources.

        This should be called when you're done using the client.
        Alternatively, use the client as an async context manager.
        """
        await self._http.close()

    async def __aenter__(self) -> "AsyncLindoClient":
        """Enter the async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Exit the async context manager and close the client."""
        await self.close()
