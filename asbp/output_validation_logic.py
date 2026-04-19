import json
from pathlib import Path

from asbp.runtime_handoff_logic import build_work_package_llm_handoff_payload
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)


def load_candidate_response_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise ValueError("Candidate response JSON must be a JSON object.")

    return payload


def _validate_string_field(candidate_output: dict, field_name: str) -> str | None:
    value = candidate_output.get(field_name)
    if not isinstance(value, str) or not value.strip():
        return f"{field_name} must be a non-empty string."
    return None


def _validate_list_of_strings_field(
    candidate_output: dict,
    field_name: str,
) -> tuple[list[str], list[str]]:
    value = candidate_output.get(field_name)
    if not isinstance(value, list):
        return [], [f"{field_name} must be a list of strings."]

    errors: list[str] = []
    normalized_values: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{field_name} must contain only non-empty strings.")
            continue
        normalized_values.append(item)

    return normalized_values, errors


def validate_work_package_candidate_response(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
    candidate_output: dict,
) -> dict | None:
    handoff_payload = build_work_package_llm_handoff_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
    )
    if handoff_payload is None:
        return None

    instructions = handoff_payload["prose_generation_instructions"]
    expected_output_fields = list(instructions["required_output_fields"])
    expected_output_field_set = set(expected_output_fields)
    allowed_grounded_fields = set(instructions["grounded_input_fields"])
    expected_response_mode = instructions["response_mode"]

    errors: list[str] = []

    missing_fields = [
        field_name
        for field_name in expected_output_fields
        if field_name not in candidate_output
    ]
    if missing_fields:
        errors.append(
            "Missing required output fields: "
            + ", ".join(missing_fields)
        )

    unexpected_fields = sorted(
        field_name
        for field_name in candidate_output.keys()
        if field_name not in expected_output_field_set
    )
    if unexpected_fields:
        errors.append(
            "Unexpected output fields: "
            + ", ".join(unexpected_fields)
        )

    response_mode = candidate_output.get("response_mode")
    if response_mode != expected_response_mode:
        errors.append(
            "response_mode mismatch: "
            f"expected {expected_response_mode}, got {response_mode!r}"
        )

    operator_message_error = _validate_string_field(
        candidate_output,
        "operator_message",
    )
    if operator_message_error is not None:
        errors.append(operator_message_error)

    recommended_next_actions, recommended_next_actions_errors = (
        _validate_list_of_strings_field(
            candidate_output,
            "recommended_next_actions",
        )
    )
    errors.extend(recommended_next_actions_errors)

    grounded_input_fields_used, grounded_input_fields_used_errors = (
        _validate_list_of_strings_field(
            candidate_output,
            "grounded_input_fields_used",
        )
    )
    errors.extend(grounded_input_fields_used_errors)

    if not grounded_input_fields_used:
        errors.append("grounded_input_fields_used must not be empty.")
    else:
        invalid_grounded_fields = sorted(
            field_name
            for field_name in grounded_input_fields_used
            if field_name not in allowed_grounded_fields
        )
        if invalid_grounded_fields:
            errors.append(
                "grounded_input_fields_used contains disallowed fields: "
                + ", ".join(invalid_grounded_fields)
            )

    return {
        "wp_id": handoff_payload["wp_id"],
        "handoff_contract_id": handoff_payload["handoff_metadata"][
            "handoff_contract_id"
        ],
        "validation_state": (
            "accepted"
            if not errors
            else "rejected"
        ),
        "expected_response_mode": expected_response_mode,
        "candidate_response_mode": response_mode,
        "errors": errors,
        "validated_output": (
            {
                "response_mode": response_mode,
                "operator_message": candidate_output.get("operator_message"),
                "recommended_next_actions": recommended_next_actions,
                "grounded_input_fields_used": grounded_input_fields_used,
            }
            if not errors
            else None
        ),
    }
