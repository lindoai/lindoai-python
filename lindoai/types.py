"""
Type definitions for the Lindo SDK.

Defines all request and response types for the Lindo API using dataclasses.
These types are generated from the unified OpenAPI specification.

@satisfies Requirements 6.3, 6.7, 6.8
"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Literal, TypeVar, Type

T = TypeVar("T")

# Workflow status type
WorkflowStatusType = Literal[
    "queued", "running", "paused", "completed", "failed", "terminated"
]


# ============================================================================
# Agent Types
# ============================================================================


@dataclass
class AgentRunRequest:
    """
    Request to run an AI agent.
    """

    agent_id: str
    """The unique identifier of the agent to run."""

    input: Dict[str, Any]
    """Input data for the agent."""

    stream: Optional[bool] = None
    """Whether to stream the response (default: false)."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: Dict[str, Any] = {
            "agent_id": self.agent_id,
            "input": self.input,
        }
        if self.stream is not None:
            result["stream"] = self.stream
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentRunRequest":
        """Create an instance from a dictionary."""
        return cls(
            agent_id=data["agent_id"],
            input=data.get("input", {}),
            stream=data.get("stream"),
        )


@dataclass
class AgentRunResponse:
    """
    Response from running an AI agent.
    """

    success: bool
    """Whether the agent run was successful."""

    output: Optional[Dict[str, Any]] = None
    """Output data from the agent."""

    credits_used: Optional[float] = None
    """Number of credits used for this run."""

    error: Optional[str] = None
    """Error message if the run failed."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: Dict[str, Any] = {"success": self.success}
        if self.output is not None:
            result["output"] = self.output
        if self.credits_used is not None:
            result["credits_used"] = self.credits_used
        if self.error is not None:
            result["error"] = self.error
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentRunResponse":
        """Create an instance from a dictionary."""
        return cls(
            success=data.get("success", False),
            output=data.get("output"),
            credits_used=data.get("credits_used"),
            error=data.get("error"),
        )


# ============================================================================
# Workflow Types
# ============================================================================


@dataclass
class WorkflowStartRequest:
    """
    Request to start a workflow.
    """

    workflow_name: str
    """The name of the workflow to start."""

    params: Optional[Dict[str, Any]] = None
    """Parameters for the workflow."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: Dict[str, Any] = {"workflow_name": self.workflow_name}
        if self.params is not None:
            # Store params under a dedicated key to avoid conflicts
            result["params"] = self.params
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowStartRequest":
        """Create an instance from a dictionary."""
        workflow_name = data.get("workflow_name", "")
        params = data.get("params")
        return cls(
            workflow_name=workflow_name,
            params=params,
        )


@dataclass
class WorkflowStartResponse:
    """
    Response from starting a workflow.
    """

    success: bool
    """Whether the workflow was started successfully."""

    instance_id: str
    """The unique identifier of the workflow instance."""

    status: WorkflowStatusType
    """Current status of the workflow."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "success": self.success,
            "instance_id": self.instance_id,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowStartResponse":
        """Create an instance from a dictionary."""
        return cls(
            success=data.get("success", False),
            instance_id=data.get("instance_id", ""),
            status=data.get("status", "queued"),
        )


@dataclass
class WorkflowBatchStartRequest:
    """
    Request to start multiple workflows in a batch.
    """

    workflows: List[Dict[str, Any]]
    """Array of workflows to start."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {"workflows": self.workflows}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowBatchStartRequest":
        """Create an instance from a dictionary."""
        return cls(workflows=data.get("workflows", []))


@dataclass
class WorkflowBatchStartResponse:
    """
    Response from starting a batch of workflows.
    """

    success: bool
    """Whether the batch was started successfully."""

    total: int
    """Total number of workflows in the batch."""

    results: List["WorkflowStartResponse"]
    """Results for each workflow."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "success": self.success,
            "total": self.total,
            "results": [r.to_dict() for r in self.results],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowBatchStartResponse":
        """Create an instance from a dictionary."""
        return cls(
            success=data.get("success", False),
            total=data.get("total", 0),
            results=[
                WorkflowStartResponse.from_dict(r)
                for r in data.get("results", [])
            ],
        )


@dataclass
class WorkflowStatus:
    """
    Status information for a workflow instance.
    """

    instance_id: str
    """The unique identifier of the workflow instance."""

    workflow_name: str
    """The name of the workflow."""

    status: WorkflowStatusType
    """Current status of the workflow."""

    created_at: str
    """ISO timestamp when the workflow was created."""

    updated_at: str
    """ISO timestamp when the workflow was last updated."""

    output: Optional[Dict[str, Any]] = None
    """Output data from the workflow (if completed)."""

    error: Optional[str] = None
    """Error message (if failed)."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: Dict[str, Any] = {
            "instance_id": self.instance_id,
            "workflow_name": self.workflow_name,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        if self.output is not None:
            result["output"] = self.output
        if self.error is not None:
            result["error"] = self.error
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowStatus":
        """Create an instance from a dictionary."""
        return cls(
            instance_id=data.get("instance_id", ""),
            workflow_name=data.get("workflow_name", ""),
            status=data.get("status", "queued"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            output=data.get("output"),
            error=data.get("error"),
        )


@dataclass
class WorkflowActionResponse:
    """
    Response from a workflow action (pause, resume, terminate).
    """

    success: bool
    """Whether the action was successful."""

    message: str
    """Message describing the result."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "success": self.success,
            "message": self.message,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowActionResponse":
        """Create an instance from a dictionary."""
        return cls(
            success=data.get("success", False),
            message=data.get("message", ""),
        )


# ============================================================================
# AI Workflow Creation & Status Types
# ----------------------------------------------------------------------------
# Used by client.workflows.create_website / create_page / create_blog and the
# matching get_website_status / get_page_status / get_blog_status pollers.
# All three create endpoints return the same shape; the three status endpoints
# share an envelope but differ in the shape of `result`.
# ============================================================================

# Normalized status used across all three status endpoints.
#   - "scheduled": queued to run in the future
#   - "running":   currently executing
#   - "complete":  fully finished with no errors
#   - "partial":   finished, but some sub-steps failed (e.g. individual pages)
#   - "errored":   the workflow itself failed
WorkflowEnvelopeStatus = Literal[
    "scheduled", "running", "complete", "partial", "errored"
]


@dataclass
class CreateWorkflowResult:
    """
    Inner result payload for workflow creation responses.
    """

    workflow_id: str
    """
    Unique identifier for this workflow. Pass it to ``get_website_status`` /
    ``get_page_status`` / ``get_blog_status`` to poll.
    """

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "workflow_id": self.workflow_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CreateWorkflowResult":
        """Create an instance from a dictionary."""
        return cls(
            workflow_id=data.get("workflow_id", ""),
        )


@dataclass
class CreateWorkflowResponse:
    """
    Response returned by ``create_website``, ``create_page``, and ``create_blog``.

    Deliberately minimal: pass ``result.workflow_id`` to the matching status endpoint
    to poll progress. No alternate identifiers — agents have exactly one id
    to remember.
    """

    success: bool
    """True when the workflow was accepted."""

    result: Optional[CreateWorkflowResult] = None
    """Inner result containing the workflow_id."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        out: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            out["result"] = self.result.to_dict()
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CreateWorkflowResponse":
        """Create an instance from a dictionary."""
        raw_result = data.get("result")
        return cls(
            success=data.get("success", False),
            result=CreateWorkflowResult.from_dict(raw_result) if raw_result else None,
        )


@dataclass
class PageWorkflowResult:
    """Result payload for a single-page workflow."""

    website_id: str
    page_id: str
    slug: str
    """Path without the leading slash, e.g. ``"about"``."""
    path: str
    """Full URL path on the website, e.g. ``"/about"``."""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "website_id": self.website_id,
            "page_id": self.page_id,
            "slug": self.slug,
            "path": self.path,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PageWorkflowResult":
        return cls(
            website_id=data.get("website_id", ""),
            page_id=data.get("page_id", ""),
            slug=data.get("slug", ""),
            path=data.get("path", ""),
        )


@dataclass
class BlogWorkflowResult:
    """Result payload for a single-blog workflow."""

    website_id: str
    blog_id: str
    slug: str
    """Path without the leading slash, e.g. ``"hello-world"``."""
    path: str
    """Full URL path on the website, e.g. ``"/blog/hello-world"``."""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "website_id": self.website_id,
            "blog_id": self.blog_id,
            "slug": self.slug,
            "path": self.path,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BlogWorkflowResult":
        return cls(
            website_id=data.get("website_id", ""),
            blog_id=data.get("blog_id", ""),
            slug=data.get("slug", ""),
            path=data.get("path", ""),
        )


@dataclass
class WebsitePageEntry:
    """A single page within a website workflow's ``result.pages`` array."""

    slug: str
    path: str
    status: Literal["running", "complete", "errored"]
    page_id: Optional[str] = None
    """Page ID once published. Absent while running or if it errored before publish."""
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "slug": self.slug,
            "path": self.path,
            "status": self.status,
        }
        if self.page_id is not None:
            result["page_id"] = self.page_id
        if self.error_message is not None:
            result["error_message"] = self.error_message
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebsitePageEntry":
        return cls(
            slug=data.get("slug", ""),
            path=data.get("path", ""),
            status=data.get("status", "running"),
            page_id=data.get("page_id"),
            error_message=data.get("error_message"),
        )


@dataclass
class WebsitePagesSummary:
    """Aggregate progress across every page of a website workflow."""

    total: int
    complete: int
    running: int
    errored: int

    def to_dict(self) -> Dict[str, int]:
        return {
            "total": self.total,
            "complete": self.complete,
            "running": self.running,
            "errored": self.errored,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebsitePagesSummary":
        return cls(
            total=data.get("total", 0),
            complete=data.get("complete", 0),
            running=data.get("running", 0),
            errored=data.get("errored", 0),
        )


@dataclass
class WebsiteWorkflowResult:
    """
    Result payload for a website-creation workflow. Includes aggregate progress
    plus per-page details for the home page and every additional page.
    """

    website_id: str
    pages_summary: WebsitePagesSummary
    pages: List[WebsitePageEntry] = field(default_factory=list)
    home_page_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "website_id": self.website_id,
            "pages_summary": self.pages_summary.to_dict(),
            "pages": [p.to_dict() for p in self.pages],
        }
        if self.home_page_id is not None:
            result["home_page_id"] = self.home_page_id
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebsiteWorkflowResult":
        return cls(
            website_id=data.get("website_id", ""),
            home_page_id=data.get("home_page_id"),
            pages_summary=WebsitePagesSummary.from_dict(
                data.get("pages_summary", {})
            ),
            pages=[
                WebsitePageEntry.from_dict(p) for p in data.get("pages", [])
            ],
        )


@dataclass
class PageWorkflowStatusResult:
    """Inner result payload for page workflow status responses."""

    done: bool
    status: WorkflowEnvelopeStatus
    workflow_id: str
    message: str
    poll_after_ms: Optional[int] = None
    result: Optional[PageWorkflowResult] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "done": self.done,
            "status": self.status,
            "workflow_id": self.workflow_id,
            "message": self.message,
        }
        if self.poll_after_ms is not None:
            out["poll_after_ms"] = self.poll_after_ms
        if self.result is not None:
            out["result"] = self.result.to_dict()
        if self.error is not None:
            out["error"] = self.error
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PageWorkflowStatusResult":
        raw_result = data.get("result")
        return cls(
            done=data.get("done", False),
            status=data.get("status", "running"),
            workflow_id=data.get("workflow_id", ""),
            message=data.get("message", ""),
            poll_after_ms=data.get("poll_after_ms"),
            result=PageWorkflowResult.from_dict(raw_result) if raw_result else None,
            error=data.get("error"),
        )


@dataclass
class PageWorkflowStatusResponse:
    """Response shape for GET /v1/ai/workspace/page/status/{workflow_id}."""

    success: bool
    result: Optional[PageWorkflowStatusResult] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            out["result"] = self.result.to_dict()
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PageWorkflowStatusResponse":
        raw_result = data.get("result")
        return cls(
            success=data.get("success", False),
            result=PageWorkflowStatusResult.from_dict(raw_result) if raw_result else None,
        )


@dataclass
class BlogWorkflowStatusResult:
    """Inner result payload for blog workflow status responses."""

    done: bool
    status: WorkflowEnvelopeStatus
    workflow_id: str
    message: str
    poll_after_ms: Optional[int] = None
    result: Optional[BlogWorkflowResult] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "done": self.done,
            "status": self.status,
            "workflow_id": self.workflow_id,
            "message": self.message,
        }
        if self.poll_after_ms is not None:
            out["poll_after_ms"] = self.poll_after_ms
        if self.result is not None:
            out["result"] = self.result.to_dict()
        if self.error is not None:
            out["error"] = self.error
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BlogWorkflowStatusResult":
        raw_result = data.get("result")
        return cls(
            done=data.get("done", False),
            status=data.get("status", "running"),
            workflow_id=data.get("workflow_id", ""),
            message=data.get("message", ""),
            poll_after_ms=data.get("poll_after_ms"),
            result=BlogWorkflowResult.from_dict(raw_result) if raw_result else None,
            error=data.get("error"),
        )


@dataclass
class BlogWorkflowStatusResponse:
    """Response shape for GET /v1/ai/workspace/blog/status/{workflow_id}."""

    success: bool
    result: Optional[BlogWorkflowStatusResult] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            out["result"] = self.result.to_dict()
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BlogWorkflowStatusResponse":
        raw_result = data.get("result")
        return cls(
            success=data.get("success", False),
            result=BlogWorkflowStatusResult.from_dict(raw_result) if raw_result else None,
        )


@dataclass
class WebsiteWorkflowStatusResult:
    """Inner result payload for website workflow status responses."""

    done: bool
    status: WorkflowEnvelopeStatus
    workflow_id: str
    message: str
    poll_after_ms: Optional[int] = None
    result: Optional[WebsiteWorkflowResult] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "done": self.done,
            "status": self.status,
            "workflow_id": self.workflow_id,
            "message": self.message,
        }
        if self.poll_after_ms is not None:
            out["poll_after_ms"] = self.poll_after_ms
        if self.result is not None:
            out["result"] = self.result.to_dict()
        if self.error is not None:
            out["error"] = self.error
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebsiteWorkflowStatusResult":
        raw_result = data.get("result")
        return cls(
            done=data.get("done", False),
            status=data.get("status", "running"),
            workflow_id=data.get("workflow_id", ""),
            message=data.get("message", ""),
            poll_after_ms=data.get("poll_after_ms"),
            result=WebsiteWorkflowResult.from_dict(raw_result) if raw_result else None,
            error=data.get("error"),
        )


@dataclass
class WebsiteWorkflowStatusResponse:
    """Response shape for GET /v1/ai/workspace/website/status/{workflow_id}."""

    success: bool
    result: Optional[WebsiteWorkflowStatusResult] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            out["result"] = self.result.to_dict()
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebsiteWorkflowStatusResponse":
        raw_result = data.get("result")
        return cls(
            success=data.get("success", False),
            result=WebsiteWorkflowStatusResult.from_dict(raw_result) if raw_result else None,
        )


# ============================================================================
# Batch Create & Batch Status Types
# ----------------------------------------------------------------------------
# Used by client.workflows.batch_create_websites / batch_create_pages /
# batch_create_blogs and the matching batch_check_*_status pollers.
# Max 25 items per batch.
# ============================================================================

# Rollup status for a batch: same vocabulary as the singular envelope status.
BatchRollupStatus = Literal[
    "scheduled", "running", "complete", "partial", "errored"
]


@dataclass
class BatchCreateItemResult:
    """Per-item result in a batch-create response."""

    success: bool
    """True if this item was accepted and scheduled."""
    workflow_id: Optional[str] = None
    """Workflow id (present when success)."""
    error: Optional[str] = None
    """Error message (present when not success)."""

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"success": self.success}
        if self.workflow_id is not None:
            out["workflow_id"] = self.workflow_id
        if self.error is not None:
            out["error"] = self.error
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchCreateItemResult":
        return cls(
            success=data.get("success", False),
            workflow_id=data.get("workflow_id"),
            error=data.get("error"),
        )


@dataclass
class BatchCreateResult:
    """Inner result payload for batch-create responses."""

    total: int
    succeeded: int
    failed: int
    items: List[BatchCreateItemResult] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.total,
            "succeeded": self.succeeded,
            "failed": self.failed,
            "items": [i.to_dict() for i in self.items],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchCreateResult":
        return cls(
            total=data.get("total", 0),
            succeeded=data.get("succeeded", 0),
            failed=data.get("failed", 0),
            items=[
                BatchCreateItemResult.from_dict(i) for i in data.get("items", [])
            ],
        )


@dataclass
class BatchCreateResponse:
    """Response shape shared by all three batch-create endpoints."""

    success: bool
    result: Optional[BatchCreateResult] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            out["result"] = self.result.to_dict()
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchCreateResponse":
        raw_result = data.get("result")
        return cls(
            success=data.get("success", False),
            result=BatchCreateResult.from_dict(raw_result) if raw_result else None,
        )


@dataclass
class BatchStatusSummary:
    """Summary counts returned with every batch-status response."""

    total: int
    complete: int
    running: int
    """Includes both running and scheduled per-item statuses."""
    partial: int
    """Items with partial outcome (website-only)."""
    errored: int
    not_found: int
    """workflow_ids that could not be found (or were the wrong workflow type)."""

    def to_dict(self) -> Dict[str, int]:
        return {
            "total": self.total,
            "complete": self.complete,
            "running": self.running,
            "partial": self.partial,
            "errored": self.errored,
            "not_found": self.not_found,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchStatusSummary":
        return cls(
            total=data.get("total", 0),
            complete=data.get("complete", 0),
            running=data.get("running", 0),
            partial=data.get("partial", 0),
            errored=data.get("errored", 0),
            not_found=data.get("not_found", 0),
        )


@dataclass
class BatchWebsiteStatusItem:
    """Per-record entry in a batch website-status response."""

    success: bool
    workflow_id: str
    done: Optional[bool] = None
    status: Optional[WorkflowEnvelopeStatus] = None
    message: Optional[str] = None
    result: Optional[WebsiteWorkflowResult] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"success": self.success, "workflow_id": self.workflow_id}
        if self.done is not None:
            out["done"] = self.done
        if self.status is not None:
            out["status"] = self.status
        if self.message is not None:
            out["message"] = self.message
        if self.result is not None:
            out["result"] = self.result.to_dict()
        if self.error is not None:
            out["error"] = self.error
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchWebsiteStatusItem":
        raw = data.get("result")
        return cls(
            success=data.get("success", False),
            workflow_id=data.get("workflow_id", ""),
            done=data.get("done"),
            status=data.get("status"),
            message=data.get("message"),
            result=WebsiteWorkflowResult.from_dict(raw) if raw else None,
            error=data.get("error"),
        )


@dataclass
class BatchPageStatusItem:
    """Per-record entry in a batch page-status response."""

    success: bool
    workflow_id: str
    done: Optional[bool] = None
    status: Optional[WorkflowEnvelopeStatus] = None
    message: Optional[str] = None
    result: Optional[PageWorkflowResult] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"success": self.success, "workflow_id": self.workflow_id}
        if self.done is not None:
            out["done"] = self.done
        if self.status is not None:
            out["status"] = self.status
        if self.message is not None:
            out["message"] = self.message
        if self.result is not None:
            out["result"] = self.result.to_dict()
        if self.error is not None:
            out["error"] = self.error
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchPageStatusItem":
        raw = data.get("result")
        return cls(
            success=data.get("success", False),
            workflow_id=data.get("workflow_id", ""),
            done=data.get("done"),
            status=data.get("status"),
            message=data.get("message"),
            result=PageWorkflowResult.from_dict(raw) if raw else None,
            error=data.get("error"),
        )


@dataclass
class BatchBlogStatusItem:
    """Per-record entry in a batch blog-status response."""

    success: bool
    workflow_id: str
    done: Optional[bool] = None
    status: Optional[WorkflowEnvelopeStatus] = None
    message: Optional[str] = None
    result: Optional[BlogWorkflowResult] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"success": self.success, "workflow_id": self.workflow_id}
        if self.done is not None:
            out["done"] = self.done
        if self.status is not None:
            out["status"] = self.status
        if self.message is not None:
            out["message"] = self.message
        if self.result is not None:
            out["result"] = self.result.to_dict()
        if self.error is not None:
            out["error"] = self.error
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchBlogStatusItem":
        raw = data.get("result")
        return cls(
            success=data.get("success", False),
            workflow_id=data.get("workflow_id", ""),
            done=data.get("done"),
            status=data.get("status"),
            message=data.get("message"),
            result=BlogWorkflowResult.from_dict(raw) if raw else None,
            error=data.get("error"),
        )


@dataclass
class BatchWebsiteStatusResult:
    """Inner result payload for batch website-status responses."""

    done: bool
    status: BatchRollupStatus
    message: str
    summary: BatchStatusSummary
    items: List[BatchWebsiteStatusItem] = field(default_factory=list)
    poll_after_ms: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "done": self.done,
            "status": self.status,
            "message": self.message,
            "summary": self.summary.to_dict(),
            "items": [i.to_dict() for i in self.items],
        }
        if self.poll_after_ms is not None:
            out["poll_after_ms"] = self.poll_after_ms
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchWebsiteStatusResult":
        return cls(
            done=data.get("done", False),
            status=data.get("status", "running"),
            message=data.get("message", ""),
            summary=BatchStatusSummary.from_dict(data.get("summary", {})),
            items=[
                BatchWebsiteStatusItem.from_dict(i) for i in data.get("items", [])
            ],
            poll_after_ms=data.get("poll_after_ms"),
        )


@dataclass
class BatchWebsiteStatusResponse:
    """Response shape for POST /v1/ai/workspace/website/status/batch."""

    success: bool
    result: Optional[BatchWebsiteStatusResult] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            out["result"] = self.result.to_dict()
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchWebsiteStatusResponse":
        raw_result = data.get("result")
        return cls(
            success=data.get("success", False),
            result=BatchWebsiteStatusResult.from_dict(raw_result) if raw_result else None,
        )


@dataclass
class BatchPageStatusResult:
    """Inner result payload for batch page-status responses."""

    done: bool
    status: BatchRollupStatus
    message: str
    summary: BatchStatusSummary
    items: List[BatchPageStatusItem] = field(default_factory=list)
    poll_after_ms: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "done": self.done,
            "status": self.status,
            "message": self.message,
            "summary": self.summary.to_dict(),
            "items": [i.to_dict() for i in self.items],
        }
        if self.poll_after_ms is not None:
            out["poll_after_ms"] = self.poll_after_ms
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchPageStatusResult":
        return cls(
            done=data.get("done", False),
            status=data.get("status", "running"),
            message=data.get("message", ""),
            summary=BatchStatusSummary.from_dict(data.get("summary", {})),
            items=[
                BatchPageStatusItem.from_dict(i) for i in data.get("items", [])
            ],
            poll_after_ms=data.get("poll_after_ms"),
        )


@dataclass
class BatchPageStatusResponse:
    """Response shape for POST /v1/ai/workspace/page/status/batch."""

    success: bool
    result: Optional[BatchPageStatusResult] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            out["result"] = self.result.to_dict()
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchPageStatusResponse":
        raw_result = data.get("result")
        return cls(
            success=data.get("success", False),
            result=BatchPageStatusResult.from_dict(raw_result) if raw_result else None,
        )


@dataclass
class BatchBlogStatusResult:
    """Inner result payload for batch blog-status responses."""

    done: bool
    status: BatchRollupStatus
    message: str
    summary: BatchStatusSummary
    items: List[BatchBlogStatusItem] = field(default_factory=list)
    poll_after_ms: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "done": self.done,
            "status": self.status,
            "message": self.message,
            "summary": self.summary.to_dict(),
            "items": [i.to_dict() for i in self.items],
        }
        if self.poll_after_ms is not None:
            out["poll_after_ms"] = self.poll_after_ms
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchBlogStatusResult":
        return cls(
            done=data.get("done", False),
            status=data.get("status", "running"),
            message=data.get("message", ""),
            summary=BatchStatusSummary.from_dict(data.get("summary", {})),
            items=[
                BatchBlogStatusItem.from_dict(i) for i in data.get("items", [])
            ],
            poll_after_ms=data.get("poll_after_ms"),
        )


@dataclass
class BatchBlogStatusResponse:
    """Response shape for POST /v1/ai/workspace/blog/status/batch."""

    success: bool
    result: Optional[BatchBlogStatusResult] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            out["result"] = self.result.to_dict()
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchBlogStatusResponse":
        raw_result = data.get("result")
        return cls(
            success=data.get("success", False),
            result=BatchBlogStatusResult.from_dict(raw_result) if raw_result else None,
        )


# ============================================================================
# Workspace Types
# ============================================================================


@dataclass
class CreditBucket:
    available: int
    used: int
    # monthly/daily have limit; purchased has total_allocated
    limit: Optional[int] = None
    utilization_percentage: Optional[float] = None
    total_allocated: Optional[int] = None
    resets_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"available": self.available, "used": self.used}
        if self.limit is not None:
            out["limit"] = self.limit
        if self.utilization_percentage is not None:
            out["utilization_percentage"] = self.utilization_percentage
        if self.total_allocated is not None:
            out["total_allocated"] = self.total_allocated
        if self.resets_at is not None:
            out["resets_at"] = self.resets_at
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CreditBucket":
        return cls(
            available=data.get("available", 0),
            used=data.get("used", 0),
            limit=data.get("limit"),
            utilization_percentage=data.get("utilization_percentage"),
            total_allocated=data.get("total_allocated"),
            resets_at=data.get("resets_at"),
        )


@dataclass
class CreditBalanceDetails:
    """Full credit balance breakdown."""

    workspace_id: Optional[str]
    monthly: CreditBucket
    purchased: CreditBucket
    daily: CreditBucket
    total_available: int
    current_plan: Optional[str]
    monthly_limit: int
    daily_limit: int
    next_monthly_reset: str
    next_daily_reset: str
    last_updated: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workspace_id": self.workspace_id,
            "current_balance": {
                "monthly": self.monthly.to_dict(),
                "purchased": self.purchased.to_dict(),
                "daily": self.daily.to_dict(),
                "total_available": self.total_available,
            },
            "plan_details": {
                "current_plan": self.current_plan,
                "monthly_limit": self.monthly_limit,
                "daily_limit": self.daily_limit,
            },
            "reset_dates": {
                "next_monthly_reset": self.next_monthly_reset,
                "next_daily_reset": self.next_daily_reset,
            },
            "last_updated": self.last_updated,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CreditBalanceDetails":
        cb = data.get("current_balance", {})
        pd = data.get("plan_details", {})
        rd = data.get("reset_dates", {})
        return cls(
            workspace_id=data.get("workspace_id"),
            monthly=CreditBucket.from_dict(cb.get("monthly", {})),
            purchased=CreditBucket.from_dict(cb.get("purchased", {})),
            daily=CreditBucket.from_dict(cb.get("daily", {})),
            total_available=cb.get("total_available", 0),
            current_plan=pd.get("current_plan"),
            monthly_limit=pd.get("monthly_limit", 0),
            daily_limit=pd.get("daily_limit", 0),
            next_monthly_reset=rd.get("next_monthly_reset", ""),
            next_daily_reset=rd.get("next_daily_reset", ""),
            last_updated=data.get("last_updated", ""),
        )


@dataclass
class WorkspaceCreditsResult:
    type: str  # "workspace"
    workspace_id: str
    balance: CreditBalanceDetails

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "workspace_id": self.workspace_id,
            "balance": self.balance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkspaceCreditsResult":
        return cls(
            type=data.get("type", "workspace"),
            workspace_id=data.get("workspace_id", ""),
            balance=CreditBalanceDetails.from_dict(data.get("balance", {})),
        )


@dataclass
class WorkspaceCreditsResponse:
    """Response from GET /v1/ai/credits."""

    success: bool
    result: Optional[WorkspaceCreditsResult] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            out["result"] = self.result.to_dict()
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkspaceCreditsResponse":
        raw = data.get("result")
        return cls(
            success=data.get("success", False),
            result=WorkspaceCreditsResult.from_dict(raw) if raw else None,
        )


@dataclass
class ClientCreditsResult:
    type: str  # "client"
    workspace_id: str
    client_id: str
    balance: CreditBalanceDetails

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "workspace_id": self.workspace_id,
            "client_id": self.client_id,
            "balance": self.balance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientCreditsResult":
        return cls(
            type=data.get("type", "client"),
            workspace_id=data.get("workspace_id", ""),
            client_id=data.get("client_id", ""),
            balance=CreditBalanceDetails.from_dict(data.get("balance", {})),
        )


@dataclass
class ClientCreditsResponse:
    """Response from GET /v1/ai/credits/client."""

    success: bool
    result: Optional[ClientCreditsResult] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            out["result"] = self.result.to_dict()
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientCreditsResponse":
        raw = data.get("result")
        return cls(
            success=data.get("success", False),
            result=ClientCreditsResult.from_dict(raw) if raw else None,
        )


@dataclass
class CreditAllocation:
    id: str
    client_id: str
    credit_type: str
    amount: int
    remaining: int
    source: str
    status: str
    created_at: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "client_id": self.client_id,
            "credit_type": self.credit_type,
            "amount": self.amount,
            "remaining": self.remaining,
            "source": self.source,
            "status": self.status,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CreditAllocation":
        return cls(
            id=data.get("id", ""),
            client_id=data.get("client_id", ""),
            credit_type=data.get("credit_type", ""),
            amount=data.get("amount", 0),
            remaining=data.get("remaining", 0),
            source=data.get("source", ""),
            status=data.get("status", ""),
            created_at=data.get("created_at", ""),
        )


@dataclass
class SimpleCreditBalance:
    monthly: int
    purchased: int
    daily: int
    total: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "monthly": self.monthly,
            "purchased": self.purchased,
            "daily": self.daily,
            "total": self.total,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SimpleCreditBalance":
        return cls(
            monthly=data.get("monthly", 0),
            purchased=data.get("purchased", 0),
            daily=data.get("daily", 0),
            total=data.get("total", 0),
        )


@dataclass
class AllocateClientCreditsResult:
    allocation: Optional[CreditAllocation] = None
    message: Optional[str] = None
    balance: Optional[SimpleCreditBalance] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        if self.allocation is not None:
            out["allocation"] = self.allocation.to_dict()
        if self.message is not None:
            out["message"] = self.message
        if self.balance is not None:
            out["balance"] = self.balance.to_dict()
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AllocateClientCreditsResult":
        raw_alloc = data.get("allocation")
        raw_bal = data.get("balance")
        return cls(
            allocation=CreditAllocation.from_dict(raw_alloc) if raw_alloc else None,
            message=data.get("message"),
            balance=SimpleCreditBalance.from_dict(raw_bal) if raw_bal else None,
        )


@dataclass
class AllocateClientCreditsResponse:
    """Response from POST /v1/ai/credits/client/allocate."""

    success: bool
    result: Optional[AllocateClientCreditsResult] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            out["result"] = self.result.to_dict()
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AllocateClientCreditsResponse":
        raw = data.get("result")
        return cls(
            success=data.get("success", False),
            result=AllocateClientCreditsResult.from_dict(raw) if raw else None,
        )


# ============================================================================
# Analytics Types
# ============================================================================


@dataclass
class AnalyticsQuery:
    """
    Query parameters for analytics requests.
    """

    from_date: Optional[str] = None
    """Start date for the analytics period (ISO format)."""

    to_date: Optional[str] = None
    """End date for the analytics period (ISO format)."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: Dict[str, Any] = {}
        if self.from_date is not None:
            result["from"] = self.from_date
        if self.to_date is not None:
            result["to"] = self.to_date
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AnalyticsQuery":
        """Create an instance from a dictionary."""
        return cls(
            from_date=data.get("from"),
            to_date=data.get("to"),
        )


@dataclass
class AnalyticsPeriod:
    """
    The analytics period.
    """

    from_date: str
    """Start date of the period (ISO format)."""

    to_date: str
    """End date of the period (ISO format)."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "from": self.from_date,
            "to": self.to_date,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AnalyticsPeriod":
        """Create an instance from a dictionary."""
        return cls(
            from_date=data.get("from", ""),
            to_date=data.get("to", ""),
        )


@dataclass
class WorkspaceAnalytics:
    """
    Analytics data for a workspace.
    """

    total_requests: int
    """Total API requests."""

    total_visitors: int
    """Total unique visitors."""

    avg_response_time: float
    """Average response time in ms."""

    total_pages: int
    """Total pages count."""

    total_blogs: int
    """Total blogs count."""

    raw_data: Optional[Dict[str, Any]] = None
    """Raw response data for additional fields."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "total_requests": self.total_requests,
            "total_visitors": self.total_visitors,
            "avg_response_time": self.avg_response_time,
            "total_pages": self.total_pages,
            "total_blogs": self.total_blogs,
        }
        if self.raw_data:
            result.update(self.raw_data)
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkspaceAnalytics":
        """Create an instance from a dictionary."""
        return cls(
            total_requests=int(data.get("total_requests", 0)),
            total_visitors=int(data.get("total_visitors", 0)),
            avg_response_time=float(data.get("avg_response_time", 0)),
            total_pages=int(data.get("total_pages", 0)),
            total_blogs=int(data.get("total_blogs", 0)),
            raw_data=data,
        )


@dataclass
class WebsiteAnalytics:
    """
    Analytics data for a website.
    """

    total_requests: int
    """Total API requests."""

    total_visitors: int
    """Total unique visitors."""

    avg_response_time: float
    """Average response time in ms."""

    total_pages: int
    """Total pages count."""

    total_blogs: int
    """Total blogs count."""

    raw_data: Optional[Dict[str, Any]] = None
    """Raw response data for additional fields."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "total_requests": self.total_requests,
            "total_visitors": self.total_visitors,
            "avg_response_time": self.avg_response_time,
            "total_pages": self.total_pages,
            "total_blogs": self.total_blogs,
        }
        if self.raw_data:
            result.update(self.raw_data)
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebsiteAnalytics":
        """Create an instance from a dictionary."""
        return cls(
            total_requests=int(data.get("total_requests", 0)),
            total_visitors=int(data.get("total_visitors", 0)),
            avg_response_time=float(data.get("avg_response_time", 0)),
            total_pages=int(data.get("total_pages", 0)),
            total_blogs=int(data.get("total_blogs", 0)),
            raw_data=data,
        )


# ============================================================================
# Client Management Types (API Key Auth)
# ============================================================================


@dataclass
class ClientInfo:
    """
    Information about a workspace client.
    """

    client_id: str
    """The unique identifier of the client."""

    email: str
    """Client email address."""

    full_name: Optional[str] = None
    """Client full name."""

    website_limit: Optional[int] = None
    """Maximum number of websites the client can have."""

    suspended: Optional[bool] = None
    """Whether the client is suspended."""

    created_date: Optional[str] = None
    """ISO timestamp when the client was created."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: Dict[str, Any] = {
            "client_id": self.client_id,
            "email": self.email,
        }
        if self.full_name is not None:
            result["full_name"] = self.full_name
        if self.website_limit is not None:
            result["website_limit"] = self.website_limit
        if self.suspended is not None:
            result["suspended"] = self.suspended
        if self.created_date is not None:
            result["created_date"] = self.created_date
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientInfo":
        """Create an instance from a dictionary."""
        return cls(
            client_id=data.get("client_id", ""),
            email=data.get("email", ""),
            full_name=data.get("full_name"),
            website_limit=data.get("website_limit"),
            suspended=data.get("suspended"),
            created_date=data.get("created_date"),
        )


@dataclass
class ClientCreateRequest:
    """
    Request to create a new workspace client.
    """

    email: str
    """Client email address."""

    website_limit: Optional[int] = None
    """Maximum number of websites the client can have."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: Dict[str, Any] = {"email": self.email}
        if self.website_limit is not None:
            result["website_limit"] = self.website_limit
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientCreateRequest":
        """Create an instance from a dictionary."""
        return cls(
            email=data.get("email", ""),
            website_limit=data.get("website_limit"),
        )


@dataclass
class ClientCreateResponse:
    """
    Response from creating a workspace client.
    """

    success: bool
    """Whether the client was created successfully."""

    result: Optional[ClientInfo] = None
    """The created client information."""

    errors: Optional[List[str]] = None
    """Error messages if creation failed."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result_dict: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            result_dict["result"] = self.result.to_dict()
        if self.errors is not None:
            result_dict["errors"] = self.errors
        return result_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientCreateResponse":
        """Create an instance from a dictionary."""
        result_data = data.get("result")
        return cls(
            success=data.get("success", False),
            result=ClientInfo.from_dict(result_data) if result_data else None,
            errors=data.get("errors"),
        )


@dataclass
class ClientListResponse:
    """
    Response from listing workspace clients.
    """

    success: bool
    """Whether the request was successful."""

    result: Optional[Dict[str, Any]] = None
    """Result containing list and total."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result_dict: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            result_dict["result"] = self.result
        return result_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientListResponse":
        """Create an instance from a dictionary."""
        return cls(
            success=data.get("success", False),
            result=data.get("result"),
        )

    @property
    def clients(self) -> List[ClientInfo]:
        """Get list of clients."""
        if self.result and "list" in self.result:
            return [ClientInfo.from_dict(c) for c in self.result["list"]]
        return []

    @property
    def total(self) -> int:
        """Get total count."""
        if self.result and "total" in self.result:
            return self.result["total"]
        return 0


@dataclass
class ClientUpdateRequest:
    """
    Request to update a workspace client.
    """

    client_id: str
    """The client ID to update."""

    website_limit: Optional[int] = None
    """New website limit."""

    suspended: Optional[bool] = None
    """Whether to suspend the client."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: Dict[str, Any] = {"client_id": self.client_id}
        if self.website_limit is not None:
            result["website_limit"] = self.website_limit
        if self.suspended is not None:
            result["suspended"] = self.suspended
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientUpdateRequest":
        """Create an instance from a dictionary."""
        return cls(
            client_id=data.get("client_id", ""),
            website_limit=data.get("website_limit"),
            suspended=data.get("suspended"),
        )


@dataclass
class ClientUpdateResponse:
    """
    Response from updating a workspace client.
    """

    success: bool
    """Whether the update was successful."""

    result: Optional[ClientInfo] = None
    """The updated client information."""

    errors: Optional[List[str]] = None
    """Error messages if update failed."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result_dict: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            result_dict["result"] = self.result.to_dict()
        if self.errors is not None:
            result_dict["errors"] = self.errors
        return result_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientUpdateResponse":
        """Create an instance from a dictionary."""
        result_data = data.get("result")
        return cls(
            success=data.get("success", False),
            result=ClientInfo.from_dict(result_data) if result_data else None,
            errors=data.get("errors"),
        )


@dataclass
class ClientDeleteRequest:
    """
    Request to delete a workspace client.
    """

    client_id: str
    """The client ID to delete."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {"client_id": self.client_id}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientDeleteRequest":
        """Create an instance from a dictionary."""
        return cls(client_id=data.get("client_id", ""))


@dataclass
class ClientDeleteResponse:
    """
    Response from deleting a workspace client.
    """

    success: bool
    """Whether the deletion was successful."""

    errors: Optional[List[str]] = None
    """Error messages if deletion failed."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: Dict[str, Any] = {"success": self.success}
        if self.errors is not None:
            result["errors"] = self.errors
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientDeleteResponse":
        """Create an instance from a dictionary."""
        return cls(
            success=data.get("success", False),
            errors=data.get("errors"),
        )


# ============================================================================
# Website Management Types (API Key Auth)
# ============================================================================


@dataclass
class WebsiteInfo:
    """
    Information about a website.
    """

    website_id: str
    """The unique identifier of the website."""

    website_name: Optional[str] = None
    """Website name."""

    domain: Optional[str] = None
    """Website domain URL."""

    activated: Optional[bool] = None
    """Whether the website is activated."""

    created_date: Optional[str] = None
    """ISO timestamp when the website was created."""

    language: Optional[str] = None
    """Website language."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: Dict[str, Any] = {"website_id": self.website_id}
        if self.website_name is not None:
            result["website_name"] = self.website_name
        if self.domain is not None:
            result["domain"] = self.domain
        if self.activated is not None:
            result["activated"] = self.activated
        if self.created_date is not None:
            result["created_date"] = self.created_date
        if self.language is not None:
            result["language"] = self.language
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebsiteInfo":
        """Create an instance from a dictionary."""
        return cls(
            website_id=data.get("website_id", ""),
            website_name=data.get("website_name"),
            domain=data.get("domain"),
            activated=data.get("activated"),
            created_date=data.get("created_date"),
            language=data.get("language"),
        )


@dataclass
class WebsiteListResponse:
    """
    Response from listing workspace websites.
    """

    success: bool
    """Whether the request was successful."""

    result: Optional[Dict[str, Any]] = None
    """Result containing list and total."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result_dict: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            result_dict["result"] = self.result
        return result_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebsiteListResponse":
        """Create an instance from a dictionary."""
        return cls(
            success=data.get("success", False),
            result=data.get("result"),
        )

    @property
    def websites(self) -> List[WebsiteInfo]:
        """Get list of websites."""
        if self.result and "list" in self.result:
            return [WebsiteInfo.from_dict(w) for w in self.result["list"]]
        return []

    @property
    def total(self) -> int:
        """Get total count."""
        if self.result and "total" in self.result:
            return self.result["total"]
        return 0


@dataclass
class WebsiteUpdateRequest:
    """
    Request to update a website.
    """

    website_id: str
    """The website ID to update."""

    business_name: Optional[str] = None
    """New business name."""

    activated: Optional[bool] = None
    """Whether to activate the website."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: Dict[str, Any] = {"website_id": self.website_id}
        if self.business_name is not None:
            result["business_name"] = self.business_name
        if self.activated is not None:
            result["activated"] = self.activated
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebsiteUpdateRequest":
        """Create an instance from a dictionary."""
        return cls(
            website_id=data.get("website_id", ""),
            business_name=data.get("business_name"),
            activated=data.get("activated"),
        )


@dataclass
class WebsiteUpdateResponse:
    """
    Response from updating a website.
    """

    success: bool
    """Whether the update was successful."""

    result: Optional[WebsiteInfo] = None
    """The updated website information."""

    errors: Optional[List[str]] = None
    """Error messages if update failed."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result_dict: Dict[str, Any] = {"success": self.success}
        if self.result is not None:
            result_dict["result"] = self.result.to_dict()
        if self.errors is not None:
            result_dict["errors"] = self.errors
        return result_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebsiteUpdateResponse":
        """Create an instance from a dictionary."""
        result_data = data.get("result")
        return cls(
            success=data.get("success", False),
            result=WebsiteInfo.from_dict(result_data) if result_data else None,
            errors=data.get("errors"),
        )


@dataclass
class WebsiteDeleteRequest:
    """
    Request to delete a website.
    """

    website_id: str
    """The website ID to delete."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {"website_id": self.website_id}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebsiteDeleteRequest":
        """Create an instance from a dictionary."""
        return cls(website_id=data.get("website_id", ""))


@dataclass
class WebsiteDeleteResponse:
    """
    Response from deleting a website.
    """

    success: bool
    """Whether the deletion was successful."""

    errors: Optional[List[str]] = None
    """Error messages if deletion failed."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: Dict[str, Any] = {"success": self.success}
        if self.errors is not None:
            result["errors"] = self.errors
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebsiteDeleteResponse":
        """Create an instance from a dictionary."""
        return cls(
            success=data.get("success", False),
            errors=data.get("errors"),
        )


@dataclass
class WebsiteAssignRequest:
    """
    Request to assign a website to a client.
    """

    website_id: str
    """The website ID to assign."""

    client_id: str
    """The client ID to assign the website to."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "website_id": self.website_id,
            "client_id": self.client_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebsiteAssignRequest":
        """Create an instance from a dictionary."""
        return cls(
            website_id=data.get("website_id", ""),
            client_id=data.get("client_id", ""),
        )


@dataclass
class WebsiteAssignResponse:
    """
    Response from assigning a website to a client.
    """

    success: bool
    """Whether the assignment was successful."""

    errors: Optional[List[str]] = None
    """Error messages if assignment failed."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: Dict[str, Any] = {"success": self.success}
        if self.errors is not None:
            result["errors"] = self.errors
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebsiteAssignResponse":
        """Create an instance from a dictionary."""
        return cls(
            success=data.get("success", False),
            errors=data.get("errors"),
        )


# ============================================================================
# Magic Link Types (API Key Auth)
# ============================================================================


@dataclass
class MagicLinkCreateRequest:
    """
    Request to create a magic link for authentication.
    """

    email: str
    """Email address to send the magic link to."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {"email": self.email}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MagicLinkCreateRequest":
        """Create an instance from a dictionary."""
        return cls(email=data.get("email", ""))


@dataclass
class MagicLinkCreateResponse:
    """
    Response from creating a magic link.
    """

    success: bool
    """Whether the magic link was created successfully."""

    magic_link: Optional[str] = None
    """The magic link URL."""

    verification_code: Optional[str] = None
    """The verification code."""

    errors: Optional[List[str]] = None
    """Error messages if creation failed."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: Dict[str, Any] = {"success": self.success}
        if self.magic_link is not None:
            result["magic_link"] = self.magic_link
        if self.verification_code is not None:
            result["verification_code"] = self.verification_code
        if self.errors is not None:
            result["errors"] = self.errors
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MagicLinkCreateResponse":
        """Create an instance from a dictionary."""
        return cls(
            success=data.get("success", False),
            magic_link=data.get("magic_link"),
            verification_code=data.get("verification_code"),
            errors=data.get("errors"),
        )
