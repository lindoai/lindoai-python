"""
Property-based tests for Python SDK serialization round-trip.

**Property 17: Python SDK Serialization Round-Trip**
*For any* valid Python SDK request dataclass, calling to_dict() and then from_dict()
on the result SHALL produce an equivalent dataclass instance.

**Validates: Requirements 6.7, 6.8**

Uses hypothesis for property-based testing with minimum 100 iterations.
"""

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st
from typing import Any, Dict, List, Optional

from lindoai.types import (
    AgentRunRequest,
    AgentRunResponse,
    WorkflowStartRequest,
    WorkflowStartResponse,
    WorkflowBatchStartRequest,
    WorkflowBatchStartResponse,
    WorkflowStatus,
    WorkflowActionResponse,
    WorkspaceCreditsResponse,
    WorkspaceCreditsResult,
    CreditBalanceDetails,
    CreditBucket,
    AnalyticsQuery,
    AnalyticsPeriod,
    WorkspaceAnalytics,
    WebsiteAnalytics,
    TopPage,
)


# ============================================================================
# Custom Strategies
# ============================================================================

# Strategy for generating safe JSON-serializable values
json_primitives = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(min_value=-2**31, max_value=2**31),
    st.floats(allow_nan=False, allow_infinity=False),
    st.text(max_size=100),
)

# Strategy for generating JSON-serializable dictionaries
json_dict = st.dictionaries(
    keys=st.text(min_size=1, max_size=50).filter(lambda x: x.isidentifier() or x.replace("_", "").isalnum()),
    values=json_primitives,
    max_size=10,
)

# Strategy for workflow status types
workflow_status_type = st.sampled_from([
    "queued", "running", "paused", "completed", "failed", "terminated"
])

# Strategy for ISO date strings
iso_date = st.from_regex(r"20[0-9]{2}-[01][0-9]-[0-3][0-9]", fullmatch=True)


# ============================================================================
# Agent Types Tests
# ============================================================================

class TestAgentRunRequestRoundTrip:
    """
    Property tests for AgentRunRequest serialization round-trip.
    
    **Validates: Requirements 6.7, 6.8**
    """

    @settings(max_examples=100)
    @given(
        agent_id=st.text(min_size=1, max_size=100),
        input_data=json_dict,
        stream=st.one_of(st.none(), st.booleans()),
    )
    def test_round_trip(
        self,
        agent_id: str,
        input_data: Dict[str, Any],
        stream: Optional[bool],
    ) -> None:
        """
        **Property 17: Python SDK Serialization Round-Trip**
        
        For any valid AgentRunRequest, to_dict() followed by from_dict()
        produces an equivalent instance.
        """
        # Create original request
        original = AgentRunRequest(
            agent_id=agent_id,
            input=input_data,
            stream=stream,
        )
        
        # Serialize and deserialize
        serialized = original.to_dict()
        deserialized = AgentRunRequest.from_dict(serialized)
        
        # Verify equivalence
        assert deserialized.agent_id == original.agent_id
        assert deserialized.input == original.input
        assert deserialized.stream == original.stream


class TestAgentRunResponseRoundTrip:
    """
    Property tests for AgentRunResponse serialization round-trip.
    
    **Validates: Requirements 6.7, 6.8**
    """

    @settings(max_examples=100)
    @given(
        success=st.booleans(),
        output=st.one_of(st.none(), json_dict),
        credits_used=st.one_of(st.none(), st.floats(min_value=0, max_value=1000000, allow_nan=False)),
        error=st.one_of(st.none(), st.text(max_size=200)),
    )
    def test_round_trip(
        self,
        success: bool,
        output: Optional[Dict[str, Any]],
        credits_used: Optional[float],
        error: Optional[str],
    ) -> None:
        """
        **Property 17: Python SDK Serialization Round-Trip**
        
        For any valid AgentRunResponse, to_dict() followed by from_dict()
        produces an equivalent instance.
        """
        original = AgentRunResponse(
            success=success,
            output=output,
            credits_used=credits_used,
            error=error,
        )
        
        serialized = original.to_dict()
        deserialized = AgentRunResponse.from_dict(serialized)
        
        assert deserialized.success == original.success
        assert deserialized.output == original.output
        assert deserialized.credits_used == original.credits_used
        assert deserialized.error == original.error


# ============================================================================
# Workflow Types Tests
# ============================================================================

class TestWorkflowStartRequestRoundTrip:
    """
    Property tests for WorkflowStartRequest serialization round-trip.
    
    **Validates: Requirements 6.7, 6.8**
    """

    @settings(max_examples=100)
    @given(
        workflow_name=st.text(min_size=1, max_size=100),
        params=st.one_of(st.none(), json_dict),
    )
    def test_round_trip(
        self,
        workflow_name: str,
        params: Optional[Dict[str, Any]],
    ) -> None:
        """
        **Property 17: Python SDK Serialization Round-Trip**
        
        For any valid WorkflowStartRequest, to_dict() followed by from_dict()
        produces an equivalent instance.
        """
        original = WorkflowStartRequest(
            workflow_name=workflow_name,
            params=params,
        )
        
        serialized = original.to_dict()
        deserialized = WorkflowStartRequest.from_dict(serialized)
        
        assert deserialized.workflow_name == original.workflow_name
        assert deserialized.params == original.params


class TestWorkflowStartResponseRoundTrip:
    """
    Property tests for WorkflowStartResponse serialization round-trip.
    
    **Validates: Requirements 6.7, 6.8**
    """

    @settings(max_examples=100)
    @given(
        success=st.booleans(),
        instance_id=st.text(min_size=1, max_size=100),
        status=workflow_status_type,
    )
    def test_round_trip(
        self,
        success: bool,
        instance_id: str,
        status: str,
    ) -> None:
        """
        **Property 17: Python SDK Serialization Round-Trip**
        
        For any valid WorkflowStartResponse, to_dict() followed by from_dict()
        produces an equivalent instance.
        """
        original = WorkflowStartResponse(
            success=success,
            instance_id=instance_id,
            status=status,  # type: ignore
        )
        
        serialized = original.to_dict()
        deserialized = WorkflowStartResponse.from_dict(serialized)
        
        assert deserialized.success == original.success
        assert deserialized.instance_id == original.instance_id
        assert deserialized.status == original.status


class TestWorkflowStatusRoundTrip:
    """
    Property tests for WorkflowStatus serialization round-trip.
    
    **Validates: Requirements 6.7, 6.8**
    """

    @settings(max_examples=100)
    @given(
        instance_id=st.text(min_size=1, max_size=100),
        workflow_name=st.text(min_size=1, max_size=100),
        status=workflow_status_type,
        created_at=iso_date,
        updated_at=iso_date,
        output=st.one_of(st.none(), json_dict),
        error=st.one_of(st.none(), st.text(max_size=200)),
    )
    def test_round_trip(
        self,
        instance_id: str,
        workflow_name: str,
        status: str,
        created_at: str,
        updated_at: str,
        output: Optional[Dict[str, Any]],
        error: Optional[str],
    ) -> None:
        """
        **Property 17: Python SDK Serialization Round-Trip**
        
        For any valid WorkflowStatus, to_dict() followed by from_dict()
        produces an equivalent instance.
        """
        original = WorkflowStatus(
            instance_id=instance_id,
            workflow_name=workflow_name,
            status=status,  # type: ignore
            created_at=created_at,
            updated_at=updated_at,
            output=output,
            error=error,
        )
        
        serialized = original.to_dict()
        deserialized = WorkflowStatus.from_dict(serialized)
        
        assert deserialized.instance_id == original.instance_id
        assert deserialized.workflow_name == original.workflow_name
        assert deserialized.status == original.status
        assert deserialized.created_at == original.created_at
        assert deserialized.updated_at == original.updated_at
        assert deserialized.output == original.output
        assert deserialized.error == original.error


class TestWorkflowActionResponseRoundTrip:
    """
    Property tests for WorkflowActionResponse serialization round-trip.
    
    **Validates: Requirements 6.7, 6.8**
    """

    @settings(max_examples=100)
    @given(
        success=st.booleans(),
        message=st.text(max_size=200),
    )
    def test_round_trip(
        self,
        success: bool,
        message: str,
    ) -> None:
        """
        **Property 17: Python SDK Serialization Round-Trip**
        
        For any valid WorkflowActionResponse, to_dict() followed by from_dict()
        produces an equivalent instance.
        """
        original = WorkflowActionResponse(
            success=success,
            message=message,
        )
        
        serialized = original.to_dict()
        deserialized = WorkflowActionResponse.from_dict(serialized)
        
        assert deserialized.success == original.success
        assert deserialized.message == original.message


class TestWorkflowBatchStartRequestRoundTrip:
    """
    Property tests for WorkflowBatchStartRequest serialization round-trip.
    
    **Validates: Requirements 6.7, 6.8**
    """

    @settings(max_examples=100)
    @given(
        workflows=st.lists(
            st.fixed_dictionaries({
                "workflow_name": st.text(min_size=1, max_size=50),
            }),
            min_size=0,
            max_size=5,
        ),
    )
    def test_round_trip(
        self,
        workflows: List[Dict[str, Any]],
    ) -> None:
        """
        **Property 17: Python SDK Serialization Round-Trip**
        
        For any valid WorkflowBatchStartRequest, to_dict() followed by from_dict()
        produces an equivalent instance.
        """
        original = WorkflowBatchStartRequest(workflows=workflows)
        
        serialized = original.to_dict()
        deserialized = WorkflowBatchStartRequest.from_dict(serialized)
        
        assert deserialized.workflows == original.workflows


# ============================================================================
# Workspace Types Tests
# ============================================================================

class TestWorkspaceCreditsRoundTrip:
    """
    Property tests for WorkspaceCreditsResponse serialization round-trip.

    **Validates: Requirements 6.7, 6.8**
    """

    @settings(max_examples=100)
    @given(
        workspace_id=st.text(min_size=1, max_size=100),
        monthly_available=st.integers(min_value=0, max_value=1_000_000),
        monthly_used=st.integers(min_value=0, max_value=1_000_000),
        monthly_limit=st.integers(min_value=0, max_value=1_000_000),
        monthly_util=st.floats(min_value=0, max_value=100, allow_nan=False),
        purchased_available=st.integers(min_value=0, max_value=1_000_000),
        purchased_used=st.integers(min_value=0, max_value=1_000_000),
        purchased_total=st.integers(min_value=0, max_value=1_000_000),
        daily_available=st.integers(min_value=0, max_value=1_000_000),
        daily_used=st.integers(min_value=0, max_value=1_000_000),
        daily_limit=st.integers(min_value=0, max_value=1_000_000),
        daily_resets_at=iso_date,
        total_available=st.integers(min_value=0, max_value=3_000_000),
        current_plan=st.one_of(st.none(), st.text(min_size=1, max_size=20)),
        plan_monthly_limit=st.integers(min_value=0, max_value=1_000_000),
        plan_daily_limit=st.integers(min_value=0, max_value=1_000_000),
        next_monthly_reset=iso_date,
        next_daily_reset=iso_date,
        last_updated=iso_date,
        success=st.booleans(),
    )
    def test_round_trip(
        self,
        workspace_id: str,
        monthly_available: int,
        monthly_used: int,
        monthly_limit: int,
        monthly_util: float,
        purchased_available: int,
        purchased_used: int,
        purchased_total: int,
        daily_available: int,
        daily_used: int,
        daily_limit: int,
        daily_resets_at: str,
        total_available: int,
        current_plan: Optional[str],
        plan_monthly_limit: int,
        plan_daily_limit: int,
        next_monthly_reset: str,
        next_daily_reset: str,
        last_updated: str,
        success: bool,
    ) -> None:
        """
        **Property 17: Python SDK Serialization Round-Trip**

        For any valid WorkspaceCreditsResponse, to_dict() followed by from_dict()
        produces an equivalent instance.
        """
        balance = CreditBalanceDetails(
            workspace_id=workspace_id,
            monthly=CreditBucket(
                available=monthly_available,
                used=monthly_used,
                limit=monthly_limit,
                utilization_percentage=monthly_util,
            ),
            purchased=CreditBucket(
                available=purchased_available,
                used=purchased_used,
                total_allocated=purchased_total,
            ),
            daily=CreditBucket(
                available=daily_available,
                used=daily_used,
                limit=daily_limit,
                resets_at=daily_resets_at,
            ),
            total_available=total_available,
            current_plan=current_plan,
            monthly_limit=plan_monthly_limit,
            daily_limit=plan_daily_limit,
            next_monthly_reset=next_monthly_reset,
            next_daily_reset=next_daily_reset,
            last_updated=last_updated,
        )

        original = WorkspaceCreditsResponse(
            success=success,
            result=WorkspaceCreditsResult(
                type="workspace",
                workspace_id=workspace_id,
                balance=balance,
            ),
        )

        serialized = original.to_dict()
        deserialized = WorkspaceCreditsResponse.from_dict(serialized)

        assert deserialized.success == original.success
        assert deserialized.result is not None
        assert deserialized.result.type == "workspace"
        assert deserialized.result.workspace_id == workspace_id
        assert deserialized.result.balance.monthly.available == monthly_available
        assert deserialized.result.balance.monthly.used == monthly_used
        assert deserialized.result.balance.monthly.limit == monthly_limit
        assert deserialized.result.balance.purchased.total_allocated == purchased_total
        assert deserialized.result.balance.daily.resets_at == daily_resets_at
        assert deserialized.result.balance.total_available == total_available
        assert deserialized.result.balance.current_plan == current_plan
        assert deserialized.result.balance.last_updated == last_updated


# ============================================================================
# Analytics Types Tests
# ============================================================================

class TestAnalyticsQueryRoundTrip:
    """
    Property tests for AnalyticsQuery serialization round-trip.
    
    **Validates: Requirements 6.7, 6.8**
    """

    @settings(max_examples=100)
    @given(
        from_date=st.one_of(st.none(), iso_date),
        to_date=st.one_of(st.none(), iso_date),
    )
    def test_round_trip(
        self,
        from_date: Optional[str],
        to_date: Optional[str],
    ) -> None:
        """
        **Property 17: Python SDK Serialization Round-Trip**
        
        For any valid AnalyticsQuery, to_dict() followed by from_dict()
        produces an equivalent instance.
        """
        original = AnalyticsQuery(
            from_date=from_date,
            to_date=to_date,
        )
        
        serialized = original.to_dict()
        deserialized = AnalyticsQuery.from_dict(serialized)
        
        assert deserialized.from_date == original.from_date
        assert deserialized.to_date == original.to_date


class TestAnalyticsPeriodRoundTrip:
    """
    Property tests for AnalyticsPeriod serialization round-trip.
    
    **Validates: Requirements 6.7, 6.8**
    """

    @settings(max_examples=100)
    @given(
        from_date=iso_date,
        to_date=iso_date,
    )
    def test_round_trip(
        self,
        from_date: str,
        to_date: str,
    ) -> None:
        """
        **Property 17: Python SDK Serialization Round-Trip**
        
        For any valid AnalyticsPeriod, to_dict() followed by from_dict()
        produces an equivalent instance.
        """
        original = AnalyticsPeriod(
            from_date=from_date,
            to_date=to_date,
        )
        
        serialized = original.to_dict()
        deserialized = AnalyticsPeriod.from_dict(serialized)
        
        assert deserialized.from_date == original.from_date
        assert deserialized.to_date == original.to_date


class TestWorkspaceAnalyticsRoundTrip:
    """
    Property tests for WorkspaceAnalytics serialization round-trip.
    
    **Validates: Requirements 6.7, 6.8**
    """

    @settings(max_examples=100)
    @given(
        workspace_id=st.text(min_size=1, max_size=100),
        total_views=st.integers(min_value=0, max_value=1000000),
        unique_visitors=st.integers(min_value=0, max_value=1000000),
        page_views=st.dictionaries(
            keys=st.text(min_size=1, max_size=50),
            values=st.integers(min_value=0, max_value=100000),
            max_size=10,
        ),
        from_date=iso_date,
        to_date=iso_date,
    )
    def test_round_trip(
        self,
        workspace_id: str,
        total_views: int,
        unique_visitors: int,
        page_views: Dict[str, int],
        from_date: str,
        to_date: str,
    ) -> None:
        """
        **Property 17: Python SDK Serialization Round-Trip**
        
        For any valid WorkspaceAnalytics, to_dict() followed by from_dict()
        produces an equivalent instance.
        """
        period = AnalyticsPeriod(from_date=from_date, to_date=to_date)
        original = WorkspaceAnalytics(
            workspace_id=workspace_id,
            total_views=total_views,
            unique_visitors=unique_visitors,
            page_views=page_views,
            period=period,
        )
        
        serialized = original.to_dict()
        deserialized = WorkspaceAnalytics.from_dict(serialized)
        
        assert deserialized.workspace_id == original.workspace_id
        assert deserialized.total_views == original.total_views
        assert deserialized.unique_visitors == original.unique_visitors
        assert deserialized.page_views == original.page_views
        assert deserialized.period.from_date == original.period.from_date
        assert deserialized.period.to_date == original.period.to_date


class TestTopPageRoundTrip:
    """
    Property tests for TopPage serialization round-trip.
    
    **Validates: Requirements 6.7, 6.8**
    """

    @settings(max_examples=100)
    @given(
        path=st.text(min_size=1, max_size=200),
        views=st.integers(min_value=0, max_value=1000000),
    )
    def test_round_trip(
        self,
        path: str,
        views: int,
    ) -> None:
        """
        **Property 17: Python SDK Serialization Round-Trip**
        
        For any valid TopPage, to_dict() followed by from_dict()
        produces an equivalent instance.
        """
        original = TopPage(path=path, views=views)
        
        serialized = original.to_dict()
        deserialized = TopPage.from_dict(serialized)
        
        assert deserialized.path == original.path
        assert deserialized.views == original.views


class TestWebsiteAnalyticsRoundTrip:
    """
    Property tests for WebsiteAnalytics serialization round-trip.
    
    **Validates: Requirements 6.7, 6.8**
    """

    @settings(max_examples=100)
    @given(
        website_id=st.text(min_size=1, max_size=100),
        workspace_id=st.text(min_size=1, max_size=100),
        total_views=st.integers(min_value=0, max_value=1000000),
        unique_visitors=st.integers(min_value=0, max_value=1000000),
        top_pages=st.lists(
            st.builds(
                TopPage,
                path=st.text(min_size=1, max_size=100),
                views=st.integers(min_value=0, max_value=100000),
            ),
            max_size=10,
        ),
        from_date=iso_date,
        to_date=iso_date,
    )
    def test_round_trip(
        self,
        website_id: str,
        workspace_id: str,
        total_views: int,
        unique_visitors: int,
        top_pages: List[TopPage],
        from_date: str,
        to_date: str,
    ) -> None:
        """
        **Property 17: Python SDK Serialization Round-Trip**
        
        For any valid WebsiteAnalytics, to_dict() followed by from_dict()
        produces an equivalent instance.
        """
        period = AnalyticsPeriod(from_date=from_date, to_date=to_date)
        original = WebsiteAnalytics(
            website_id=website_id,
            workspace_id=workspace_id,
            total_views=total_views,
            unique_visitors=unique_visitors,
            top_pages=top_pages,
            period=period,
        )
        
        serialized = original.to_dict()
        deserialized = WebsiteAnalytics.from_dict(serialized)
        
        assert deserialized.website_id == original.website_id
        assert deserialized.workspace_id == original.workspace_id
        assert deserialized.total_views == original.total_views
        assert deserialized.unique_visitors == original.unique_visitors
        assert len(deserialized.top_pages) == len(original.top_pages)
        for i, page in enumerate(deserialized.top_pages):
            assert page.path == original.top_pages[i].path
            assert page.views == original.top_pages[i].views
        assert deserialized.period.from_date == original.period.from_date
        assert deserialized.period.to_date == original.period.to_date
