"""
Workflows resource for the Lindo SDK.

Provides methods for managing workflows.

@satisfies Requirements 6.2
"""

from typing import Any, Dict, List, Optional

from lindoai.http import HttpClient, AsyncHttpClient
from lindoai.types import (
    WorkflowStartRequest,
    WorkflowStartResponse,
    WorkflowBatchStartRequest,
    WorkflowBatchStartResponse,
    WorkflowStatus,
    WorkflowActionResponse,
    CreateWorkflowResponse,
    PageWorkflowStatusResponse,
    BlogWorkflowStatusResponse,
    WebsiteWorkflowStatusResponse,
    BatchCreateResponse,
    BatchWebsiteStatusResponse,
    BatchPageStatusResponse,
    BatchBlogStatusResponse,
)


class WorkflowsResource:
    """
    Synchronous resource class for workflow operations.
    """

    def __init__(self, http: HttpClient) -> None:
        """
        Initialize the workflows resource.

        Args:
            http: The HTTP client to use for requests
        """
        self._http = http

    def start(
        self,
        workflow_name: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> WorkflowStartResponse:
        """
        Start a new workflow instance.

        Args:
            workflow_name: The name of the workflow to start
            params: Parameters for the workflow

        Returns:
            The workflow start response with instance ID

        Example:
            >>> response = client.workflows.start(
            ...     workflow_name="publish-page",
            ...     params={"page_id": "page-123"}
            ... )
            >>> print("Workflow started:", response.instance_id)
        """
        request = WorkflowStartRequest(workflow_name=workflow_name, params=params)
        data = self._http.post("/v1/ai/workflows/start", request.to_dict())
        return WorkflowStartResponse.from_dict(data)

    def batch_start(
        self,
        workflows: List[Dict[str, Any]],
    ) -> WorkflowBatchStartResponse:
        """
        Start multiple workflow instances in a batch.

        Args:
            workflows: Array of workflows to start

        Returns:
            The batch start response with results for each workflow

        Example:
            >>> response = client.workflows.batch_start(
            ...     workflows=[
            ...         {"workflow_name": "publish-page", "page_id": "page-1"},
            ...         {"workflow_name": "publish-page", "page_id": "page-2"},
            ...     ]
            ... )
            >>> print("Started", response.total, "workflows")
        """
        request = WorkflowBatchStartRequest(workflows=workflows)
        data = self._http.post("/v1/ai/workflows/batch", request.to_dict())
        return WorkflowBatchStartResponse.from_dict(data)

    def get_status(self, instance_id: str) -> WorkflowStatus:
        """
        Get the status of a workflow instance.

        Args:
            instance_id: The workflow instance ID

        Returns:
            The workflow status

        Example:
            >>> status = client.workflows.get_status("instance-123")
            >>> if status.status == "completed":
            ...     print("Output:", status.output)
        """
        data = self._http.get(f"/v1/ai/workflows/{instance_id}")
        return WorkflowStatus.from_dict(data)

    def pause(self, instance_id: str) -> WorkflowActionResponse:
        """
        Pause a running workflow instance.

        Args:
            instance_id: The workflow instance ID

        Returns:
            The action response

        Example:
            >>> client.workflows.pause("instance-123")
            >>> print("Workflow paused")
        """
        data = self._http.post(f"/ai/workflows/pause/{instance_id}")
        return WorkflowActionResponse.from_dict(data)

    def resume(self, instance_id: str) -> WorkflowActionResponse:
        """
        Resume a paused workflow instance.

        Args:
            instance_id: The workflow instance ID

        Returns:
            The action response

        Example:
            >>> client.workflows.resume("instance-123")
            >>> print("Workflow resumed")
        """
        data = self._http.post(f"/ai/workflows/resume/{instance_id}")
        return WorkflowActionResponse.from_dict(data)

    def terminate(self, instance_id: str) -> WorkflowActionResponse:
        """
        Terminate a workflow instance.

        Args:
            instance_id: The workflow instance ID

        Returns:
            The action response

        Example:
            >>> client.workflows.terminate("instance-123")
            >>> print("Workflow terminated")
        """
        data = self._http.post(f"/ai/workflows/terminate/{instance_id}")
        return WorkflowActionResponse.from_dict(data)

    def create_website(
        self,
        prompt: str,
        schedule_at: Optional[str] = None,
        client: Optional[Dict[str, str]] = None,
    ) -> CreateWorkflowResponse:
        """
        Create a website using AI.

        Starts an asynchronous workflow that generates a website from the prompt.
        Returns a ``record_id`` immediately — poll :meth:`get_website_status` with
        that id to track progress and get the final result.

        Args:
            prompt: AI prompt describing the website (min 10 chars).
            schedule_at: Optional ISO 8601 timestamp to schedule creation for later.
            client: Optional client assignment. Dict may contain ``client_id``
                (existing client) or ``email`` + optional ``name`` (lookup or create).

        Returns:
            :class:`CreateWorkflowResponse`. Use ``response.record_id`` to poll.

        Example:
            >>> resp = client.workflows.create_website(
            ...     prompt="Create a website for a coffee shop",
            ...     client={"email": "hello@beanthere.coffee", "name": "Bean There"},
            ... )
            >>> # Poll until done
            >>> import time
            >>> while True:
            ...     status = client.workflows.get_website_status(resp.record_id)
            ...     if status.done:
            ...         print(status.message)
            ...         break
            ...     time.sleep((status.poll_after_ms or 5000) / 1000)
        """
        body: Dict[str, Any] = {"prompt": prompt}
        if schedule_at is not None:
            body["schedule_at"] = schedule_at
        if client is not None:
            body["client"] = client
        data = self._http.post("/v1/ai/workspace/website", body)
        return CreateWorkflowResponse.from_dict(data)

    def create_page(
        self,
        website_id: str,
        prompt: str,
        schedule_at: Optional[str] = None,
    ) -> CreateWorkflowResponse:
        """
        Create a page on an existing website using AI.

        Starts an asynchronous workflow. Poll :meth:`get_page_status` with the
        returned ``record_id`` to track progress.

        Args:
            website_id: The website to add the page to.
            prompt: AI prompt describing the page (min 10 chars).
            schedule_at: Optional ISO 8601 timestamp to schedule creation for later.

        Returns:
            :class:`CreateWorkflowResponse`. Use ``response.record_id`` to poll.
        """
        body: Dict[str, Any] = {"prompt": prompt}
        if schedule_at is not None:
            body["schedule_at"] = schedule_at
        data = self._http.post(
            f"/v1/ai/workspace/website/{website_id}/page", body
        )
        return CreateWorkflowResponse.from_dict(data)

    def create_blog(
        self,
        website_id: str,
        prompt: str,
        schedule_at: Optional[str] = None,
    ) -> CreateWorkflowResponse:
        """
        Create a blog post on an existing website using AI.

        Starts an asynchronous workflow. Poll :meth:`get_blog_status` with the
        returned ``record_id`` to track progress.

        Args:
            website_id: The website to add the blog post to.
            prompt: AI prompt describing the blog post (min 10 chars).
            schedule_at: Optional ISO 8601 timestamp to schedule creation for later.

        Returns:
            :class:`CreateWorkflowResponse`. Use ``response.record_id`` to poll.
        """
        body: Dict[str, Any] = {"prompt": prompt}
        if schedule_at is not None:
            body["schedule_at"] = schedule_at
        data = self._http.post(
            f"/v1/ai/workspace/website/{website_id}/blog", body
        )
        return CreateWorkflowResponse.from_dict(data)

    def get_website_status(
        self, record_id: str
    ) -> WebsiteWorkflowStatusResponse:
        """
        Poll the status of a website-creation workflow started via
        :meth:`create_website`.

        ``status`` is ``"complete"`` only when every page (home + additional)
        has succeeded, ``"partial"`` if some failed, ``"running"`` while in
        flight.

        Args:
            record_id: The ``record_id`` returned by :meth:`create_website`.

        Returns:
            :class:`WebsiteWorkflowStatusResponse`.
        """
        data = self._http.get(f"/v1/ai/workspace/website/status/{record_id}")
        return WebsiteWorkflowStatusResponse.from_dict(data)

    def get_page_status(self, record_id: str) -> PageWorkflowStatusResponse:
        """
        Poll the status of a page-creation workflow started via :meth:`create_page`.

        Args:
            record_id: The ``record_id`` returned by :meth:`create_page`.

        Returns:
            :class:`PageWorkflowStatusResponse`.
        """
        data = self._http.get(f"/v1/ai/workspace/page/status/{record_id}")
        return PageWorkflowStatusResponse.from_dict(data)

    def get_blog_status(self, record_id: str) -> BlogWorkflowStatusResponse:
        """
        Poll the status of a blog-creation workflow started via :meth:`create_blog`.

        Args:
            record_id: The ``record_id`` returned by :meth:`create_blog`.

        Returns:
            :class:`BlogWorkflowStatusResponse`.
        """
        data = self._http.get(f"/v1/ai/workspace/blog/status/{record_id}")
        return BlogWorkflowStatusResponse.from_dict(data)

    # ------------------------------------------------------------------
    # Batch Create
    # ------------------------------------------------------------------

    def batch_create_websites(
        self, items: List[Dict[str, Any]]
    ) -> BatchCreateResponse:
        """
        Start up to 25 website-creation workflows in one request.

        Args:
            items: Between 1 and 25 dicts, each with ``prompt`` and optional
                ``schedule_at`` / ``client``.

        Returns:
            :class:`BatchCreateResponse` with per-item ``record_id`` / ``error``.

        Example:
            >>> batch = client.workflows.batch_create_websites([
            ...     {"prompt": "Website for a coffee shop"},
            ...     {"prompt": "Photography portfolio for Maria Chen"},
            ... ])
            >>> ok_ids = [i.record_id for i in batch.items if i.success and i.record_id]
            >>> status = client.workflows.batch_check_website_status(ok_ids)
        """
        data = self._http.post(
            "/v1/ai/workspace/website/batch", {"items": items}
        )
        return BatchCreateResponse.from_dict(data)

    def batch_create_pages(
        self, website_id: str, items: List[Dict[str, Any]]
    ) -> BatchCreateResponse:
        """Start up to 25 page-creation workflows on a single website."""
        data = self._http.post(
            f"/v1/ai/workspace/website/{website_id}/page/batch",
            {"items": items},
        )
        return BatchCreateResponse.from_dict(data)

    def batch_create_blogs(
        self, website_id: str, items: List[Dict[str, Any]]
    ) -> BatchCreateResponse:
        """Start up to 25 blog-creation workflows on a single website."""
        data = self._http.post(
            f"/v1/ai/workspace/website/{website_id}/blog/batch",
            {"items": items},
        )
        return BatchCreateResponse.from_dict(data)

    # ------------------------------------------------------------------
    # Batch Status
    # ------------------------------------------------------------------

    def batch_check_website_status(
        self, record_ids: List[str]
    ) -> BatchWebsiteStatusResponse:
        """
        Poll up to 25 website-creation workflows at once.

        Returns a rollup ``status`` (``scheduled`` / ``running`` / ``complete``
        / ``partial`` / ``errored``) plus per-item envelopes and a summary with
        counts.
        """
        data = self._http.post(
            "/v1/ai/workspace/website/status/batch",
            {"record_ids": record_ids},
        )
        return BatchWebsiteStatusResponse.from_dict(data)

    def batch_check_page_status(
        self, record_ids: List[str]
    ) -> BatchPageStatusResponse:
        """Poll up to 25 page-creation workflows at once."""
        data = self._http.post(
            "/v1/ai/workspace/page/status/batch",
            {"record_ids": record_ids},
        )
        return BatchPageStatusResponse.from_dict(data)

    def batch_check_blog_status(
        self, record_ids: List[str]
    ) -> BatchBlogStatusResponse:
        """Poll up to 25 blog-creation workflows at once."""
        data = self._http.post(
            "/v1/ai/workspace/blog/status/batch",
            {"record_ids": record_ids},
        )
        return BatchBlogStatusResponse.from_dict(data)


class AsyncWorkflowsResource:
    """
    Asynchronous resource class for workflow operations.
    """

    def __init__(self, http: AsyncHttpClient) -> None:
        """
        Initialize the async workflows resource.

        Args:
            http: The async HTTP client to use for requests
        """
        self._http = http

    async def start(
        self,
        workflow_name: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> WorkflowStartResponse:
        """
        Start a new workflow instance.

        Args:
            workflow_name: The name of the workflow to start
            params: Parameters for the workflow

        Returns:
            The workflow start response with instance ID

        Example:
            >>> response = await client.workflows.start(
            ...     workflow_name="publish-page",
            ...     params={"page_id": "page-123"}
            ... )
            >>> print("Workflow started:", response.instance_id)
        """
        request = WorkflowStartRequest(workflow_name=workflow_name, params=params)
        data = await self._http.post("/v1/ai/workflows/start", request.to_dict())
        return WorkflowStartResponse.from_dict(data)

    async def batch_start(
        self,
        workflows: List[Dict[str, Any]],
    ) -> WorkflowBatchStartResponse:
        """
        Start multiple workflow instances in a batch.

        Args:
            workflows: Array of workflows to start

        Returns:
            The batch start response with results for each workflow

        Example:
            >>> response = await client.workflows.batch_start(
            ...     workflows=[
            ...         {"workflow_name": "publish-page", "page_id": "page-1"},
            ...         {"workflow_name": "publish-page", "page_id": "page-2"},
            ...     ]
            ... )
            >>> print("Started", response.total, "workflows")
        """
        request = WorkflowBatchStartRequest(workflows=workflows)
        data = await self._http.post("/v1/ai/workflows/batch", request.to_dict())
        return WorkflowBatchStartResponse.from_dict(data)

    async def get_status(self, instance_id: str) -> WorkflowStatus:
        """
        Get the status of a workflow instance.

        Args:
            instance_id: The workflow instance ID

        Returns:
            The workflow status

        Example:
            >>> status = await client.workflows.get_status("instance-123")
            >>> if status.status == "completed":
            ...     print("Output:", status.output)
        """
        data = await self._http.get(f"/v1/ai/workflows/{instance_id}")
        return WorkflowStatus.from_dict(data)

    async def pause(self, instance_id: str) -> WorkflowActionResponse:
        """
        Pause a running workflow instance.

        Args:
            instance_id: The workflow instance ID

        Returns:
            The action response

        Example:
            >>> await client.workflows.pause("instance-123")
            >>> print("Workflow paused")
        """
        data = await self._http.post(f"/ai/workflows/pause/{instance_id}")
        return WorkflowActionResponse.from_dict(data)

    async def resume(self, instance_id: str) -> WorkflowActionResponse:
        """
        Resume a paused workflow instance.

        Args:
            instance_id: The workflow instance ID

        Returns:
            The action response

        Example:
            >>> await client.workflows.resume("instance-123")
            >>> print("Workflow resumed")
        """
        data = await self._http.post(f"/ai/workflows/resume/{instance_id}")
        return WorkflowActionResponse.from_dict(data)

    async def terminate(self, instance_id: str) -> WorkflowActionResponse:
        """
        Terminate a workflow instance.

        Args:
            instance_id: The workflow instance ID

        Returns:
            The action response

        Example:
            >>> await client.workflows.terminate("instance-123")
            >>> print("Workflow terminated")
        """
        data = await self._http.post(f"/ai/workflows/terminate/{instance_id}")
        return WorkflowActionResponse.from_dict(data)

    async def create_website(
        self,
        prompt: str,
        schedule_at: Optional[str] = None,
        client: Optional[Dict[str, str]] = None,
    ) -> CreateWorkflowResponse:
        """
        Create a website using AI (async).

        Starts an asynchronous workflow that generates a website from the prompt.
        Returns a ``record_id`` immediately — poll :meth:`get_website_status` with
        that id to track progress and get the final result.

        Args:
            prompt: AI prompt describing the website (min 10 chars).
            schedule_at: Optional ISO 8601 timestamp to schedule creation for later.
            client: Optional client assignment. Dict may contain ``client_id``
                (existing client) or ``email`` + optional ``name`` (lookup or create).

        Returns:
            :class:`CreateWorkflowResponse`. Use ``response.record_id`` to poll.
        """
        body: Dict[str, Any] = {"prompt": prompt}
        if schedule_at is not None:
            body["schedule_at"] = schedule_at
        if client is not None:
            body["client"] = client
        data = await self._http.post("/v1/ai/workspace/website", body)
        return CreateWorkflowResponse.from_dict(data)

    async def create_page(
        self,
        website_id: str,
        prompt: str,
        schedule_at: Optional[str] = None,
    ) -> CreateWorkflowResponse:
        """
        Create a page on an existing website using AI (async).

        Poll :meth:`get_page_status` with the returned ``record_id``.
        """
        body: Dict[str, Any] = {"prompt": prompt}
        if schedule_at is not None:
            body["schedule_at"] = schedule_at
        data = await self._http.post(
            f"/v1/ai/workspace/website/{website_id}/page", body
        )
        return CreateWorkflowResponse.from_dict(data)

    async def create_blog(
        self,
        website_id: str,
        prompt: str,
        schedule_at: Optional[str] = None,
    ) -> CreateWorkflowResponse:
        """
        Create a blog post on an existing website using AI (async).

        Poll :meth:`get_blog_status` with the returned ``record_id``.
        """
        body: Dict[str, Any] = {"prompt": prompt}
        if schedule_at is not None:
            body["schedule_at"] = schedule_at
        data = await self._http.post(
            f"/v1/ai/workspace/website/{website_id}/blog", body
        )
        return CreateWorkflowResponse.from_dict(data)

    async def get_website_status(
        self, record_id: str
    ) -> WebsiteWorkflowStatusResponse:
        """
        Poll the status of a website-creation workflow (async).

        ``status`` is ``"complete"`` only when every page has succeeded.
        """
        data = await self._http.get(
            f"/v1/ai/workspace/website/status/{record_id}"
        )
        return WebsiteWorkflowStatusResponse.from_dict(data)

    async def get_page_status(
        self, record_id: str
    ) -> PageWorkflowStatusResponse:
        """Poll the status of a page-creation workflow (async)."""
        data = await self._http.get(
            f"/v1/ai/workspace/page/status/{record_id}"
        )
        return PageWorkflowStatusResponse.from_dict(data)

    async def get_blog_status(
        self, record_id: str
    ) -> BlogWorkflowStatusResponse:
        """Poll the status of a blog-creation workflow (async)."""
        data = await self._http.get(
            f"/v1/ai/workspace/blog/status/{record_id}"
        )
        return BlogWorkflowStatusResponse.from_dict(data)

    # ------------------------------------------------------------------
    # Batch Create (async)
    # ------------------------------------------------------------------

    async def batch_create_websites(
        self, items: List[Dict[str, Any]]
    ) -> BatchCreateResponse:
        """Start up to 25 website-creation workflows in one request (async)."""
        data = await self._http.post(
            "/v1/ai/workspace/website/batch", {"items": items}
        )
        return BatchCreateResponse.from_dict(data)

    async def batch_create_pages(
        self, website_id: str, items: List[Dict[str, Any]]
    ) -> BatchCreateResponse:
        """Start up to 25 page-creation workflows on a single website (async)."""
        data = await self._http.post(
            f"/v1/ai/workspace/website/{website_id}/page/batch",
            {"items": items},
        )
        return BatchCreateResponse.from_dict(data)

    async def batch_create_blogs(
        self, website_id: str, items: List[Dict[str, Any]]
    ) -> BatchCreateResponse:
        """Start up to 25 blog-creation workflows on a single website (async)."""
        data = await self._http.post(
            f"/v1/ai/workspace/website/{website_id}/blog/batch",
            {"items": items},
        )
        return BatchCreateResponse.from_dict(data)

    # ------------------------------------------------------------------
    # Batch Status (async)
    # ------------------------------------------------------------------

    async def batch_check_website_status(
        self, record_ids: List[str]
    ) -> BatchWebsiteStatusResponse:
        """Poll up to 25 website-creation workflows at once (async)."""
        data = await self._http.post(
            "/v1/ai/workspace/website/status/batch",
            {"record_ids": record_ids},
        )
        return BatchWebsiteStatusResponse.from_dict(data)

    async def batch_check_page_status(
        self, record_ids: List[str]
    ) -> BatchPageStatusResponse:
        """Poll up to 25 page-creation workflows at once (async)."""
        data = await self._http.post(
            "/v1/ai/workspace/page/status/batch",
            {"record_ids": record_ids},
        )
        return BatchPageStatusResponse.from_dict(data)

    async def batch_check_blog_status(
        self, record_ids: List[str]
    ) -> BatchBlogStatusResponse:
        """Poll up to 25 blog-creation workflows at once (async)."""
        data = await self._http.post(
            "/v1/ai/workspace/blog/status/batch",
            {"record_ids": record_ids},
        )
        return BatchBlogStatusResponse.from_dict(data)
