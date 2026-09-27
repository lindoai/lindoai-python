# lindo-sdk

Python SDK for the Lindo API. Provides both synchronous and asynchronous clients for interacting with AI agents, workflows, workspace management, and analytics.

## Installation

```bash
pip install lindo-sdk
```

## Requirements

- Python 3.8 or higher
- httpx

## Quick Start

### Synchronous Client

```python
from lindo_sdk import LindoClient

client = LindoClient(api_key="your-api-key")

# Run an agent
result = client.agents.run(
    agent_id="my-agent",
    input={"prompt": "Hello!"}
)

# Start a workflow
workflow = client.workflows.start(
    workflow_name="publish-page",
    params={"page_id": "page-123"}
)

# Get workspace credits
credits = client.workspace.get_credits()

# Get analytics
analytics = client.analytics.get_workspace(
    from_date="2024-01-01",
    to_date="2024-01-31"
)

# Close the client when done
client.close()
```

### Using Context Manager

```python
from lindo_sdk import LindoClient

with LindoClient(api_key="your-api-key") as client:
    result = client.agents.run(
        agent_id="my-agent",
        input={"prompt": "Hello!"}
    )
```

### Asynchronous Client

```python
import asyncio
from lindo_sdk import AsyncLindoClient

async def main():
    async with AsyncLindoClient(api_key="your-api-key") as client:
        # Run an agent
        result = await client.agents.run(
            agent_id="my-agent",
            input={"prompt": "Hello!"}
        )
        
        # Start a workflow
        workflow = await client.workflows.start(
            workflow_name="publish-page",
            params={"page_id": "page-123"}
        )
        
        # Get workspace credits
        credits = await client.workspace.get_credits()

asyncio.run(main())
```

## Configuration

```python
client = LindoClient(
    api_key="your-api-key",           # Required
    base_url="https://api.lindo.ai",  # Optional, defaults to https://api.lindo.ai
    timeout=30.0,                      # Optional, defaults to 30.0 seconds
)
```

## API Reference

### Agents

Run AI agents with custom inputs.

```python
# Run an agent
result = client.agents.run(
    agent_id="my-agent",
    input={"prompt": "Hello!"},
    stream=False  # Optional: enable streaming
)

print(result.success)       # bool
print(result.output)        # Agent output
print(result.credits_used)  # Credits consumed
```

### Workflows

Manage long-running workflows.

```python
# Start a workflow
workflow = client.workflows.start(
    workflow_name="publish-page",
    params={"page_id": "page-123"}
)
print(workflow.instance_id)  # Workflow instance ID

# Start multiple workflows in batch
batch = client.workflows.batch_start(
    workflow_name="publish-page",
    items=[
        {"params": {"page_id": "page-1"}},
        {"params": {"page_id": "page-2"}},
    ]
)

# Get workflow status
status = client.workflows.get_status("instance-123")
print(status.status)  # 'queued', 'running', 'paused', 'completed', 'failed', 'terminated'

# Pause a workflow
client.workflows.pause("instance-123")

# Resume a workflow
client.workflows.resume("instance-123")

# Terminate a workflow
client.workflows.terminate("instance-123")
```

### Workspace

Manage workspace resources.

```python
# Get credit balance
credits = client.workspace.get_credits()
print(credits.balance)     # Current balance
print(credits.allocated)   # Total allocated
print(credits.used)        # Total used
```

### Analytics

Access workspace and website analytics.

```python
# Get workspace analytics
workspace_analytics = client.analytics.get_workspace(
    from_date="2024-01-01",  # Optional
    to_date="2024-01-31"     # Optional
)
print(workspace_analytics.total_views)
print(workspace_analytics.unique_visitors)

# Get website analytics
website_analytics = client.analytics.get_website(
    from_date="2024-01-01",
    to_date="2024-01-31"
)
print(website_analytics.top_pages)
```

## Error Handling

The SDK provides custom exception classes for common error scenarios:

```python
from lindo_sdk import (
    LindoClient,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ServerError,
)

try:
    result = client.agents.run(
        agent_id="my-agent",
        input={}
    )
except AuthenticationError:
    # Invalid or expired API key (401)
    print("Please check your API key")
except RateLimitError as e:
    # Too many requests (429)
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except NotFoundError:
    # Resource not found (404)
    print("Agent not found")
except ValidationError as e:
    # Invalid request (400)
    print(f"Validation errors: {e.errors}")
except ServerError:
    # Server error (5xx)
    print("Server error, please try again later")
```

### Exception Classes

| Exception | HTTP Status | Description |
|-----------|-------------|-------------|
| `AuthenticationError` | 401 | Invalid or expired API key |
| `ForbiddenError` | 403 | Insufficient permissions |
| `NotFoundError` | 404 | Resource not found |
| `ValidationError` | 400 | Invalid request parameters |
| `RateLimitError` | 429 | Too many requests |
| `ServerError` | 5xx | Internal server error |
| `NetworkError` | - | Network connection failed |
| `TimeoutError` | - | Request timed out |

## Types

The SDK uses dataclasses with type hints for all request and response types:

```python
from lindo_sdk import (
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
    
    # Workspace types
    WorkspaceCredits,
    
    # Analytics types
    AnalyticsQuery,
    WorkspaceAnalytics,
    WebsiteAnalytics,
)
```

### Serialization

All dataclasses support `to_dict()` and `from_dict()` methods:

```python
from lindo_sdk import AgentRunRequest

# Create from dict
request = AgentRunRequest.from_dict({
    "agent_id": "my-agent",
    "input": {"prompt": "Hello!"}
})

# Convert to dict
data = request.to_dict()
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run type checking
mypy lindo_sdk

# Run linting
ruff check lindo_sdk
```

## License

MIT
