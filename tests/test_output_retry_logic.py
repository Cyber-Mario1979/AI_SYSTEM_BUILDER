# tests/test_output_retry_logic.py

from asbp.output_retry_logic import evaluate_work_package_output_attempt
from asbp.state_model import WorkPackageModel


def test_output_retry_returns_none_for_missing_work_package():
    payload = evaluate_work_package_output_attempt(
        [],
        [],
        [],
        [],
        wp_id="WP-404",
        candidate_output={},
        attempt_number=1,
        max_attempts=2,
    )

    assert payload is None


def test_output_retry_accepts_valid_blocked_explainer_output():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = evaluate_work_package_output_attempt(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
        candidate_output={
            "response_mode": "blocked_explainer",
            "operator_message": (
                "Generation cannot proceed until selector context is completed."
            ),
            "recommended_next_actions": [
                "Complete deterministic selector context before orchestration can proceed."
            ],
            "grounded_input_fields_used": [
                "wp_id",
                "deterministic_facts.orchestration_stage",
                "deterministic_facts.blocking_conditions",
                "deterministic_facts.next_actions",
            ],
        },
        attempt_number=1,
        max_attempts=2,
    )

    assert payload is not None
    assert payload["output_retry_metadata"] == {
        "output_retry_id": "work_package_output_retry_v1",
        "output_acceptance_id": "work_package_output_acceptance_v1",
        "output_mapping_id": "work_package_output_mapping_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "validation_state": "accepted",
        "decision_state": "accepted",
        "regeneration_action": "use_validated_output",
        "current_response_mode": "blocked_explainer",
        "selected_plan_id": None,
    }
    assert payload["retry_policy"] == {
        "attempt_number": 1,
        "max_attempts": 2,
        "retries_remaining": 1,
    }
    assert payload["decision_rationale"] == ["validated_output_accepted"]
    assert payload["validation_errors"] == []
    assert payload["validated_output"] == {
        "response_mode": "blocked_explainer",
        "operator_message": (
            "Generation cannot proceed until selector context is completed."
        ),
        "recommended_next_actions": [
            "Complete deterministic selector context before orchestration can proceed."
        ],
        "grounded_input_fields_used": [
            "wp_id",
            "deterministic_facts.orchestration_stage",
            "deterministic_facts.blocking_conditions",
            "deterministic_facts.next_actions",
        ],
    }


def test_output_retry_allows_retry_when_validation_rejected_and_budget_remains():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = evaluate_work_package_output_attempt(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
        candidate_output={
            "response_mode": "execution_ready_summary",
            "operator_message": "",
            "recommended_next_actions": "not-a-list",
            "grounded_input_fields_used": [
                "wp_id",
                "disallowed.field",
            ],
            "extra_field": "unexpected",
        },
        attempt_number=1,
        max_attempts=2,
    )

    assert payload is not None
    assert payload["output_retry_metadata"] == {
        "output_retry_id": "work_package_output_retry_v1",
        "output_acceptance_id": "work_package_output_acceptance_v1",
        "output_mapping_id": "work_package_output_mapping_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "validation_state": "rejected",
        "decision_state": "retry_allowed",
        "regeneration_action": "request_regenerated_output_from_same_mapping_contract",
        "current_response_mode": "blocked_explainer",
        "selected_plan_id": None,
    }
    assert payload["retry_policy"] == {
        "attempt_number": 1,
        "max_attempts": 2,
        "retries_remaining": 1,
    }
    assert payload["decision_rationale"] == [
        "validation_rejected_but_retry_budget_remaining"
    ]
    assert payload["validation_errors"] == [
        "Unexpected output fields: extra_field",
        "response_mode must be one of: blocked_explainer",
        "response_mode mismatch: expected blocked_explainer, got 'execution_ready_summary'",
        "operator_message must be a non-empty string.",
        "recommended_next_actions must be a list of strings.",
        "grounded_input_fields_used contains disallowed fields: disallowed.field",
    ]


def test_output_retry_fails_closed_for_invalid_retry_control_state():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = evaluate_work_package_output_attempt(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
        candidate_output={
            "response_mode": "blocked_explainer",
            "operator_message": (
                "Generation cannot proceed until selector context is completed."
            ),
            "recommended_next_actions": [
                "Complete deterministic selector context before orchestration can proceed."
            ],
            "grounded_input_fields_used": [
                "wp_id",
                "deterministic_facts.orchestration_stage",
                "deterministic_facts.blocking_conditions",
                "deterministic_facts.next_actions",
            ],
        },
        attempt_number=3,
        max_attempts=2,
    )

    assert payload is not None
    assert payload["output_retry_metadata"] == {
        "output_retry_id": "work_package_output_retry_v1",
        "output_acceptance_id": "work_package_output_acceptance_v1",
        "output_mapping_id": "work_package_output_mapping_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "validation_state": "accepted",
        "decision_state": "fail_closed",
        "regeneration_action": "return_rejected_output_without_acceptance",
        "current_response_mode": "blocked_explainer",
        "selected_plan_id": None,
    }
    assert payload["retry_policy"] == {
        "attempt_number": 3,
        "max_attempts": 2,
        "retries_remaining": 0,
    }
    assert payload["decision_rationale"] == [
        "invalid_retry_control_state:attempt_number_exceeds_max_attempts"
    ]


def test_output_retry_fails_closed_when_retry_budget_is_exhausted():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = evaluate_work_package_output_attempt(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
        candidate_output={
            "response_mode": "execution_ready_summary",
            "operator_message": "",
            "recommended_next_actions": "not-a-list",
            "grounded_input_fields_used": [
                "wp_id",
                "disallowed.field",
            ],
            "extra_field": "unexpected",
        },
        attempt_number=2,
        max_attempts=2,
    )

    assert payload is not None
    assert payload["output_retry_metadata"] == {
        "output_retry_id": "work_package_output_retry_v1",
        "output_acceptance_id": "work_package_output_acceptance_v1",
        "output_mapping_id": "work_package_output_mapping_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "validation_state": "rejected",
        "decision_state": "fail_closed",
        "regeneration_action": "return_rejected_output_without_acceptance",
        "current_response_mode": "blocked_explainer",
        "selected_plan_id": None,
    }
    assert payload["retry_policy"] == {
        "attempt_number": 2,
        "max_attempts": 2,
        "retries_remaining": 0,
    }
    assert payload["decision_rationale"] == [
        "validation_rejected_and_retry_budget_exhausted"
    ]
    assert payload["validated_output"] is None