"""
Lindo SDK for Python

A Python SDK for interacting with the Lindo API.
Provides both synchronous and asynchronous clients.

Example usage:
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
    >>> # Manage clients (API key auth)
    >>> clients = client.clients.list()
    >>>
    >>> # Manage websites (API key auth)
    >>> websites = client.websites.list()

For async usage:
    >>> from lindoai import AsyncLindoClient
    >>>
    >>> async with AsyncLindoClient(api_key="your-api-key") as client:
    ...     result = await client.agents.run(
    ...         agent_id="my-agent",
    ...         input={"prompt": "Hello!"}
    ...     )

@satisfies Requirements 6.1, 6.2
"""

__version__ = "1.0.4"

# Main clients
from lindoai.client import LindoClient, AsyncLindoClient

# Error classes
from lindoai.errors import (
    LindoError,
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
    NetworkError,
    TimeoutError,
)

# Types
from lindoai.types import (
    # Agent types
    AgentRunRequest,
    AgentRunResponse,
    # Workflow types
    WorkflowStartRequest,
    WorkflowStartResponse,
    WorkflowBatchStartRequest,
    WorkflowBatchStartResponse,
    WorkflowStatus,
    WorkflowActionResponse,
    # AI workflow creation & status types
    CreateWorkflowResponse,
    WorkflowEnvelopeStatus,
    PageWorkflowResult,
    BlogWorkflowResult,
    WebsitePageEntry,
    WebsitePagesSummary,
    WebsiteWorkflowResult,
    PageWorkflowStatusResponse,
    BlogWorkflowStatusResponse,
    WebsiteWorkflowStatusResponse,
    # Batch create & batch status
    BatchRollupStatus,
    BatchCreateItemResult,
    BatchCreateResponse,
    BatchStatusSummary,
    BatchWebsiteStatusItem,
    BatchPageStatusItem,
    BatchBlogStatusItem,
    BatchWebsiteStatusResponse,
    BatchPageStatusResponse,
    BatchBlogStatusResponse,
    # Workspace types
    WorkspaceCredits,
    # Analytics types
    AnalyticsQuery,
    WorkspaceAnalytics,
    WebsiteAnalytics,
    # Client management types
    ClientCreateRequest,
    ClientCreateResponse,
    ClientListResponse,
    ClientUpdateRequest,
    ClientUpdateResponse,
    ClientDeleteRequest,
    ClientDeleteResponse,
    ClientInfo,
    # Website management types
    WebsiteListResponse,
    WebsiteUpdateRequest,
    WebsiteUpdateResponse,
    WebsiteDeleteRequest,
    WebsiteDeleteResponse,
    WebsiteAssignRequest,
    WebsiteAssignResponse,
    WebsiteInfo,
    # Magic link types
    MagicLinkCreateRequest,
    MagicLinkCreateResponse,
)

# Resource classes
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
)

__all__ = [
    # Version
    "__version__",
    # Clients
    "LindoClient",
    "AsyncLindoClient",
    # Errors
    "LindoError",
    "AuthenticationError",
    "ForbiddenError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
    "TimeoutError",
    # Types
    "AgentRunRequest",
    "AgentRunResponse",
    "WorkflowStartRequest",
    "WorkflowStartResponse",
    "WorkflowBatchStartRequest",
    "WorkflowBatchStartResponse",
    "WorkflowStatus",
    "WorkflowActionResponse",
    "CreateWorkflowResponse",
    "WorkflowEnvelopeStatus",
    "PageWorkflowResult",
    "BlogWorkflowResult",
    "WebsitePageEntry",
    "WebsitePagesSummary",
    "WebsiteWorkflowResult",
    "PageWorkflowStatusResponse",
    "BlogWorkflowStatusResponse",
    "WebsiteWorkflowStatusResponse",
    "BatchRollupStatus",
    "BatchCreateItemResult",
    "BatchCreateResponse",
    "BatchStatusSummary",
    "BatchWebsiteStatusItem",
    "BatchPageStatusItem",
    "BatchBlogStatusItem",
    "BatchWebsiteStatusResponse",
    "BatchPageStatusResponse",
    "BatchBlogStatusResponse",
    "WorkspaceCredits",
    "AnalyticsQuery",
    "WorkspaceAnalytics",
    "WebsiteAnalytics",
    "ClientCreateRequest",
    "ClientCreateResponse",
    "ClientListResponse",
    "ClientUpdateRequest",
    "ClientUpdateResponse",
    "ClientDeleteRequest",
    "ClientDeleteResponse",
    "ClientInfo",
    "WebsiteListResponse",
    "WebsiteUpdateRequest",
    "WebsiteUpdateResponse",
    "WebsiteDeleteRequest",
    "WebsiteDeleteResponse",
    "WebsiteAssignRequest",
    "WebsiteAssignResponse",
    "WebsiteInfo",
    "MagicLinkCreateRequest",
    "MagicLinkCreateResponse",
    # Resources
    "AgentsResource",
    "AsyncAgentsResource",
    "WorkflowsResource",
    "AsyncWorkflowsResource",
    "WorkspaceResource",
    "AsyncWorkspaceResource",
    "AnalyticsResource",
    "AsyncAnalyticsResource",
    "ClientsResource",
    "AsyncClientsResource",
    "WebsitesResource",
    "AsyncWebsitesResource",
]
