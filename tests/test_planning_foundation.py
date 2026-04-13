import json

import pytest
from pydantic import ValidationError

from asbp.planning_logic import generate_next_plan_id
from asbp.state_model import PlanningModel, StateModel, WorkPackageModel
from asbp.state_store import build_persisted_state_payload, load_validated_state


def write_state_file(state_file, payload: dict) -> None:
    state_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_load_validated_state_defaults_missing_plans_to_empty_list(tmp_path):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [],
            "work_packages": [],
            "task_collections": [],
        },
    )

    state = load_validated_state(state_file)

    assert state.plans == []


def test_build_persisted_state_payload_omits_empty_plans_for_backward_compatibility():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.8.0",
        status="in_flight",
    )

    payload = build_persisted_state_payload(state)

    assert "plans" not in payload


def test_generate_next_plan_id_uses_plan_namespace_and_existing_max():
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
        ),
        PlanningModel(
            plan_id="PLAN-007",
            work_package_id="WP-002",
            plan_state="committed",
        ),
    ]

    assert generate_next_plan_id(plans) == "PLAN-008"


def test_load_validated_state_accepts_plan_linked_to_existing_work_package(tmp_path):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [],
            "work_packages": [
                {
                    "wp_id": "WP-001",
                    "title": "Tablet press qualification",
                    "status": "open",
                }
            ],
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                }
            ],
        },
    )

    state = load_validated_state(state_file)

    assert state.plans == [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
        )
    ]


def test_load_validated_state_rejects_duplicate_plan_ids(tmp_path):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [],
            "work_packages": [
                {
                    "wp_id": "WP-001",
                    "title": "Tablet press qualification",
                    "status": "open",
                }
            ],
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                },
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "committed",
                },
            ],
        },
    )

    with pytest.raises(ValidationError) as exc_info:
        load_validated_state(state_file)

    assert "Duplicate plan_id is not allowed: PLAN-001" in str(exc_info.value)


def test_load_validated_state_rejects_dangling_plan_work_package_link(tmp_path):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [],
            "work_packages": [
                {
                    "wp_id": "WP-001",
                    "title": "Tablet press qualification",
                    "status": "open",
                }
            ],
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-999",
                    "plan_state": "draft",
                }
            ],
        },
    )

    with pytest.raises(ValueError) as exc_info:
        load_validated_state(state_file)

    assert (
        "Persisted plan work_package_id does not exist: PLAN-001 -> WP-999"
        in str(exc_info.value)
    )