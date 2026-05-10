"""
Workspace resource for the Lindo SDK.

Provides methods for workspace operations.

@satisfies Requirements 6.2, 25.4
"""

from typing import Optional, Dict, Any

from lindoai.http import HttpClient, AsyncHttpClient
from lindoai.types import WorkspaceCredits


class WorkspaceResource:
    """
    Synchronous resource class for workspace operations.
    """

    def __init__(self, http: HttpClient) -> None:
        """
        Initialize the workspace resource.

        Args:
            http: The HTTP client to use for requests
        """
        self._http = http

    def get(self) -> Dict[str, Any]:
        """
        Get detailed information about the current workspace.

        Returns:
            The workspace details response

        Example:
            >>> response = client.workspace.get()
            >>> print("Workspace:", response["result"]["workspace_name"])
        """
        return self._http.get("/v1/workspace")

    def get_credits(self) -> WorkspaceCredits:
        """
        Get the credit balance for the current workspace.

        Returns:
            The workspace credits information

        Example:
            >>> credits = client.workspace.get_credits()
            >>> print("Balance:", credits.balance)
        """
        data = self._http.get("/v1/ai/credits")
        return WorkspaceCredits.from_dict(data)

    def get_client_credits(self, client_id: str) -> Dict[str, Any]:
        """
        Get the credit balance for a specific client.

        Args:
            client_id: The client ID to get credits for

        Returns:
            The client credits information
        """
        return self._http.get("/v1/ai/credits/client", params={"client_id": client_id})

    def update(
        self,
        workspace_name: Optional[str] = None,
        workspace_language: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update workspace settings.

        Args:
            workspace_name: New workspace name
            workspace_language: New workspace language
            webhook_url: New webhook URL

        Returns:
            The workspace update response
        """
        body = {}
        if workspace_name is not None:
            body["workspace_name"] = workspace_name
        if workspace_language is not None:
            body["workspace_language"] = workspace_language
        if webhook_url is not None:
            body["webhook_url"] = webhook_url
        return self._http.put("/v1/workspace", body)

    def add_team_member(self, email: str, role: str = "Team") -> Dict[str, Any]:
        """
        Add a team member to the workspace.

        Args:
            email: The email address of the team member
            role: The role to assign (default: 'Team')

        Returns:
            The team member add response
        """
        return self._http.post("/v1/workspace/team", {"email": email, "role": role})

    def remove_team_member(self, member_id: str) -> Dict[str, Any]:
        """
        Remove a team member from the workspace.

        Args:
            member_id: The member ID to remove

        Returns:
            The team member remove response
        """
        return self._http.delete(f"/v1/workspace/team/{member_id}")

    def get_team(self) -> Dict[str, Any]:
        """
        Get the list of team members in the workspace.

        Returns:
            The team list response

        Example:
            >>> response = client.workspace.get_team()
            >>> for member in response["result"]["list"]:
            ...     print(member["email"], member["role"])
        """
        return self._http.get("/v1/workspace/team")

    def get_analytics(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get analytics data for the workspace.

        Args:
            from_date: Start date for analytics (ISO format)
            to_date: End date for analytics (ISO format)

        Returns:
            The workspace analytics response

        Example:
            >>> response = client.workspace.get_analytics()
            >>> print("Total requests:", response["result"]["total_requests"])
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        return self._http.get("/v1/workspace/analytics", params=params if params else None)

    def add_integration(self, integration_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add an integration to the workspace.

        Args:
            integration_type: The type of integration (e.g., 'matomo')
            config: The integration configuration

        Returns:
            The integration add response
        """
        return self._http.post("/v1/workspace/integration", {
            "integration_type": integration_type,
            "config": config
        })

    def remove_integration(self, integration_type: str) -> Dict[str, Any]:
        """
        Remove an integration from the workspace.

        Args:
            integration_type: The type of integration to remove

        Returns:
            The integration remove response
        """
        return self._http.delete(f"/v1/workspace/integration/{integration_type}")

    def setup_whitelabel(
        self,
        domain: Optional[str] = None,
        subdomain_domain: Optional[str] = None,
        email_sender: Optional[str] = None,
        wl_client_register: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Setup or update workspace whitelabel settings.

        Args:
            domain: Custom domain
            subdomain_domain: Subdomain domain
            email_sender: Email sender address
            wl_client_register: Enable client registration

        Returns:
            The whitelabel update response
        """
        body = {}
        if domain is not None:
            body["domain"] = domain
        if subdomain_domain is not None:
            body["subdomain_domain"] = subdomain_domain
        if email_sender is not None:
            body["email_sender"] = email_sender
        if wl_client_register is not None:
            body["wl_client_register"] = wl_client_register
        return self._http.put("/v1/workspace/whitelabel", body)

    def update_appearance(
        self,
        primary_color: Optional[str] = None,
        secondary_color: Optional[str] = None,
        theme_mode: Optional[str] = None,
        custom_code_header: Optional[str] = None,
        custom_code_footer: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update workspace appearance settings.

        Args:
            primary_color: Primary color (hex)
            secondary_color: Secondary color (hex)
            theme_mode: Theme mode ('light' or 'dark')
            custom_code_header: Custom header code
            custom_code_footer: Custom footer code

        Returns:
            The appearance update response
        """
        body = {}
        if primary_color is not None:
            body["primary_color"] = primary_color
        if secondary_color is not None:
            body["secondary_color"] = secondary_color
        if theme_mode is not None:
            body["theme_mode"] = theme_mode
        if custom_code_header is not None:
            body["custom_code_header"] = custom_code_header
        if custom_code_footer is not None:
            body["custom_code_footer"] = custom_code_footer
        return self._http.put("/v1/workspace/appearance", body)


class AsyncWorkspaceResource:
    """
    Asynchronous resource class for workspace operations.
    """

    def __init__(self, http: AsyncHttpClient) -> None:
        """
        Initialize the async workspace resource.

        Args:
            http: The async HTTP client to use for requests
        """
        self._http = http

    async def get(self) -> Dict[str, Any]:
        """
        Get detailed information about the current workspace.

        Returns:
            The workspace details response
        """
        return await self._http.get("/v1/workspace")

    async def get_credits(self) -> WorkspaceCredits:
        """
        Get the credit balance for the current workspace.

        Returns:
            The workspace credits information
        """
        data = await self._http.get("/v1/ai/credits")
        return WorkspaceCredits.from_dict(data)

    async def get_client_credits(self, client_id: str) -> Dict[str, Any]:
        """
        Get the credit balance for a specific client.

        Args:
            client_id: The client ID to get credits for

        Returns:
            The client credits information
        """
        return await self._http.get("/v1/ai/credits/client", params={"client_id": client_id})

    async def update(
        self,
        workspace_name: Optional[str] = None,
        workspace_language: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update workspace settings.

        Args:
            workspace_name: New workspace name
            workspace_language: New workspace language
            webhook_url: New webhook URL

        Returns:
            The workspace update response
        """
        body = {}
        if workspace_name is not None:
            body["workspace_name"] = workspace_name
        if workspace_language is not None:
            body["workspace_language"] = workspace_language
        if webhook_url is not None:
            body["webhook_url"] = webhook_url
        return await self._http.put("/v1/workspace", body)

    async def add_team_member(self, email: str, role: str = "Team") -> Dict[str, Any]:
        """
        Add a team member to the workspace.

        Args:
            email: The email address of the team member
            role: The role to assign (default: 'Team')

        Returns:
            The team member add response
        """
        return await self._http.post("/v1/workspace/team", {"email": email, "role": role})

    async def remove_team_member(self, member_id: str) -> Dict[str, Any]:
        """
        Remove a team member from the workspace.

        Args:
            member_id: The member ID to remove

        Returns:
            The team member remove response
        """
        return await self._http.delete(f"/v1/workspace/team/{member_id}")

    async def get_team(self) -> Dict[str, Any]:
        """
        Get the list of team members in the workspace.

        Returns:
            The team list response
        """
        return await self._http.get("/v1/workspace/team")

    async def get_analytics(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get analytics data for the workspace.

        Args:
            from_date: Start date for analytics (ISO format)
            to_date: End date for analytics (ISO format)

        Returns:
            The workspace analytics response
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        return await self._http.get("/v1/workspace/analytics", params=params if params else None)

    async def add_integration(self, integration_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add an integration to the workspace.

        Args:
            integration_type: The type of integration (e.g., 'matomo')
            config: The integration configuration

        Returns:
            The integration add response
        """
        return await self._http.post("/v1/workspace/integration", {
            "integration_type": integration_type,
            "config": config
        })

    async def remove_integration(self, integration_type: str) -> Dict[str, Any]:
        """
        Remove an integration from the workspace.

        Args:
            integration_type: The type of integration to remove

        Returns:
            The integration remove response
        """
        return await self._http.delete(f"/v1/workspace/integration/{integration_type}")

    async def setup_whitelabel(
        self,
        domain: Optional[str] = None,
        subdomain_domain: Optional[str] = None,
        email_sender: Optional[str] = None,
        wl_client_register: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Setup or update workspace whitelabel settings.

        Args:
            domain: Custom domain
            subdomain_domain: Subdomain domain
            email_sender: Email sender address
            wl_client_register: Enable client registration

        Returns:
            The whitelabel update response
        """
        body = {}
        if domain is not None:
            body["domain"] = domain
        if subdomain_domain is not None:
            body["subdomain_domain"] = subdomain_domain
        if email_sender is not None:
            body["email_sender"] = email_sender
        if wl_client_register is not None:
            body["wl_client_register"] = wl_client_register
        return await self._http.put("/v1/workspace/whitelabel", body)

    async def update_appearance(
        self,
        primary_color: Optional[str] = None,
        secondary_color: Optional[str] = None,
        theme_mode: Optional[str] = None,
        custom_code_header: Optional[str] = None,
        custom_code_footer: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update workspace appearance settings.

        Args:
            primary_color: Primary color (hex)
            secondary_color: Secondary color (hex)
            theme_mode: Theme mode ('light' or 'dark')
            custom_code_header: Custom header code
            custom_code_footer: Custom footer code

        Returns:
            The appearance update response
        """
        body = {}
        if primary_color is not None:
            body["primary_color"] = primary_color
        if secondary_color is not None:
            body["secondary_color"] = secondary_color
        if theme_mode is not None:
            body["theme_mode"] = theme_mode
        if custom_code_header is not None:
            body["custom_code_header"] = custom_code_header
        if custom_code_footer is not None:
            body["custom_code_footer"] = custom_code_footer
        return await self._http.put("/v1/workspace/appearance", body)
