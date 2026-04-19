from datetime import datetime, timezone

from asbp.runtime_handoff_logic import build_work_package_llm_handoff_payload
from asbp.state_model import (
    PlanningBasisModel,
    PlanningCalendarModel,
    PlanningModel,
    SelectorContextModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)


def make_bound_context_work_package(
    wp_id: str = "WP-001",
    title: str = "Tablet press qualification",
) -> WorkPackageModel:
    return WorkPackageModel(
        wp_id=wp_id,
        title=title,
        status="open",
        selector_context=SelectorContextModel(
            preset_id="oral-solid-dose-standard",
            scope_intent="qualification-only",
            standards_bundles=["cqv-core", "automation"],
        ),
    )


def test_runtime_handoff_returns_none_for_missing_work_package():
    payload = build_work_package_llm_handoff_payload(
        [],
        [],
        [],
        [],
        wp_id="WP-404",
    )

    assert payload is None


def test_runtime_handoff_reports_blocked_handoff_with_separated_sections():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = build_work_package_llm_handoff_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    )

    assert payload == {
        "wp_id": "WP-001",
        "handoff_metadata": {
            "handoff_contract_id": "work_package_llm_handoff_v1",
            "source_prompt_contract_id": "work_package_runtime_prompt_contract_v1",
            "handoff_state": "blocked",
            "generation_allowed": False,
            "selected_plan_id": None,
            "prompt_contract_state": "blocked",
            "prompt_contract_mode": "blocked_explainer",
        },
        "structured_facts": {
            "work_package_status": "open",
            "orchestration_stage": "binding_context_required",
            "blocking_conditions": ["selector_context_missing"],
            "next_actions": [
                "Complete deterministic selector context before orchestration can proceed."
            ],
            "selector_context_ready": False,
            "work_package_task_ids": [],
            "bound_committed_collection_ids": [],
            "bound_committed_task_ids": [],
            "plan_ids": [],
        },
        "prose_generation_instructions": {
            "response_mode": "blocked_explainer",
            "writing_goal": (
                "Explain why generation cannot proceed yet using only the "
                "structured facts, blockers, and next actions in this handoff payload."
            ),
            "required_output_fields": [
                "response_mode",
                "operator_message",
                "recommended_next_actions",
                "grounded_input_fields_used",
            ],
            "grounded_input_fields": [
                "wp_id",
                "runtime_boundary_state",
                "eligible_for_prompt_contract",
                "selected_plan_id",
                "deterministic_facts.work_package_status",
                "deterministic_facts.orchestration_stage",
                "deterministic_facts.blocking_conditions",
                "deterministic_facts.next_actions",
                "deterministic_facts.selector_context_ready",
                "deterministic_facts.work_package_task_ids",
                "deterministic_facts.bound_committed_collection_ids",
                "deterministic_facts.bound_committed_task_ids",
                "deterministic_facts.plan_ids",
            ],
            "prohibited_freeform_drift": [
                "omit required output fields",
                "add output fields outside the declared contract",
                "invent facts outside the validated deterministic inputs",
                "change or reinterpret blocking conditions",
                "change selected plan, task scope, or collection scope",
                "propose state mutation as if it already occurred",
            ],
        },
    }


def test_runtime_handoff_reports_ready_for_generation_when_prompt_contract_is_ready():
    work_packages = [make_bound_context_work_package()]
    task_collections = [
        TaskCollectionModel(
            collection_id="TC-001",
            title="Committed Selection",
            collection_state="committed",
            work_package_id="WP-001",
            task_ids=["TASK-001"],
        )
    ]
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT",
            duration=1,
            work_package_id="WP-001",
            status="planned",
        )
    ]
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="committed",
            planning_basis=PlanningBasisModel(
                duration_source="task_duration",
            ),
            planned_start_at=datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc),
            planning_calendar=PlanningCalendarModel(
                working_days=["monday", "wednesday", "friday"],
                workday_hours=8,
                workmonth_mode="calendar_month",
            ),
        )
    ]

    payload = build_work_package_llm_handoff_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    )

    assert payload["wp_id"] == "WP-001"
    assert payload["handoff_metadata"] == {
        "handoff_contract_id": "work_package_llm_handoff_v1",
        "source_prompt_contract_id": "work_package_runtime_prompt_contract_v1",
        "handoff_state": "ready_for_generation",
        "generation_allowed": True,
        "selected_plan_id": "PLAN-001",
        "prompt_contract_state": "ready",
        "prompt_contract_mode": "execution_ready_summary",
    }
    assert payload["structured_facts"] == {
        "work_package_status": "open",
        "orchestration_stage": "execution_ready",
        "blocking_conditions": [],
        "next_actions": [
            "Execution-ready deterministic state reached."
        ],
        "selector_context_ready": True,
        "work_package_task_ids": ["TASK-001"],
        "bound_committed_collection_ids": ["TC-001"],
        "bound_committed_task_ids": ["TASK-001"],
        "plan_ids": ["PLAN-001"],
    }
    assert payload["prose_generation_instructions"]["response_mode"] == (
        "execution_ready_summary"
    )
