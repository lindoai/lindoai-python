"""
Agents resource for the Lindo SDK.

Provides methods for running AI agents.

@satisfies Requirements 6.2
"""

from typing import Any, Dict, Optional

from lindoai.http import HttpClient, AsyncHttpClient
from lindoai.types import AgentRunRequest, AgentRunResponse


class AgentsResource:
    """
    Synchronous resource class for AI agent operations.
    """

    def __init__(self, http: HttpClient) -> None:
        """
        Initialize the agents resource.

        Args:
            http: The HTTP client to use for requests
        """
        self._http = http

    def run(
        self,
        agent_id: str,
        input: Dict[str, Any],
        stream: Optional[bool] = None,
    ) -> AgentRunResponse:
        """
        Run an AI agent with the specified input.

        Args:
            agent_id: The unique identifier of the agent to run
            input: Input data for the agent
            stream: Whether to stream the response (default: false)

        Returns:
            The agent run response

        Example:
            >>> response = client.agents.run(
            ...     agent_id="my-agent",
            ...     input={"prompt": "Hello, world!"}
            ... )
            >>> if response.success:
            ...     print("Output:", response.output)
        """
        request = AgentRunRequest(agent_id=agent_id, input=input, stream=stream)
        data = self._http.post("/v1/ai/agents/run", request.to_dict())
        return AgentRunResponse.from_dict(data)

    def run_stream(
        self,
        agent_id: str,
        input: Dict[str, Any],
    ) -> AgentRunResponse:
        """
        Run an AI agent with streaming enabled.

        Note: This method returns a promise that resolves when the stream completes.
        For real-time streaming, use the streaming API directly.

        Args:
            agent_id: The unique identifier of the agent to run
            input: Input data for the agent

        Returns:
            The agent run response

        Example:
            >>> response = client.agents.run_stream(
            ...     agent_id="my-agent",
            ...     input={"prompt": "Tell me a story"}
            ... )
        """
        request = AgentRunRequest(agent_id=agent_id, input=input, stream=True)
        data = self._http.post("/v1/ai/agents/run", request.to_dict())
        return AgentRunResponse.from_dict(data)


class AsyncAgentsResource:
    """
    Asynchronous resource class for AI agent operations.
    """

    def __init__(self, http: AsyncHttpClient) -> None:
        """
        Initialize the async agents resource.

        Args:
            http: The async HTTP client to use for requests
        """
        self._http = http

    async def run(
        self,
        agent_id: str,
        input: Dict[str, Any],
        stream: Optional[bool] = None,
    ) -> AgentRunResponse:
        """
        Run an AI agent with the specified input.

        Args:
            agent_id: The unique identifier of the agent to run
            input: Input data for the agent
            stream: Whether to stream the response (default: false)

        Returns:
            The agent run response

        Example:
            >>> response = await client.agents.run(
            ...     agent_id="my-agent",
            ...     input={"prompt": "Hello, world!"}
            ... )
            >>> if response.success:
            ...     print("Output:", response.output)
        """
        request = AgentRunRequest(agent_id=agent_id, input=input, stream=stream)
        data = await self._http.post("/v1/ai/agents/run", request.to_dict())
        return AgentRunResponse.from_dict(data)

    async def run_stream(
        self,
        agent_id: str,
        input: Dict[str, Any],
    ) -> AgentRunResponse:
        """
        Run an AI agent with streaming enabled.

        Note: This method returns a promise that resolves when the stream completes.
        For real-time streaming, use the streaming API directly.

        Args:
            agent_id: The unique identifier of the agent to run
            input: Input data for the agent

        Returns:
            The agent run response

        Example:
            >>> response = await client.agents.run_stream(
            ...     agent_id="my-agent",
            ...     input={"prompt": "Tell me a story"}
            ... )
        """
        request = AgentRunRequest(agent_id=agent_id, input=input, stream=True)
        data = await self._http.post("/v1/ai/agents/run", request.to_dict())
        return AgentRunResponse.from_dict(data)
