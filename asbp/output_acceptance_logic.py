from asbp.output_mapping_logic import (
    build_work_package_output_mapping_payload,
)
from asbp.output_validation_helpers import (
    build_disallowed_grounded_fields_errors,
    validate_list_of_strings_field,
    validate_non_empty_string_field,
)
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

OUTPUT_ACCEPTANCE_ID = "work_package_output_acceptance_v1"


def validate_work_package_output_before_acceptance(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
    candidate_output: object,
) -> dict | None:
    output_mapping_payload = build_work_package_output_mapping_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
    )
    if output_mapping_payload is None:
        return None

    output_mapping_metadata = output_mapping_payload["output_mapping_metadata"]
    mapped_output_contract = output_mapping_payload["mapped_output_contract"]
    generation_instructions = output_mapping_payload["generation_instructions"]

    errors: list[str] = []

    if not isinstance(candidate_output, dict):
        errors.append("Candidate output must be an object.")
        return {
            "wp_id": output_mapping_payload["wp_id"],
            "output_acceptance_metadata": {
                "output_acceptance_id": OUTPUT_ACCEPTANCE_ID,
                "output_mapping_id": output_mapping_metadata["output_mapping_id"],
                "output_contract_id": output_mapping_metadata["output_contract_id"],
                "validation_state": "rejected",
                "acceptance_ready": False,
                "current_response_mode": output_mapping_metadata[
                    "current_response_mode"
                ],
                "selected_plan_id": output_mapping_metadata["selected_plan_id"],
            },
            "errors": errors,
            "validated_output": None,
        }

    required_output_fields = list(
        mapped_output_contract["required_output_fields"]
    )
    required_output_field_set = set(required_output_fields)
    allowed_response_modes = set(
        mapped_output_contract["allowed_response_modes"]
    )
    expected_response_mode = output_mapping_metadata["current_response_mode"]
    allowed_grounded_fields = set(
        generation_instructions["grounded_input_fields"]
    )

    missing_fields = [
        field_name
        for field_name in required_output_fields
        if field_name not in candidate_output
    ]
    if missing_fields:
        errors.append(
            "Missing required output fields: " + ", ".join(missing_fields)
        )

    acceptance_shape = mapped_output_contract["acceptance_shape"]
    extra_fields_allowed = acceptance_shape["extra_fields_allowed"]
    if not extra_fields_allowed:
        unexpected_fields = sorted(
            field_name
            for field_name in candidate_output.keys()
            if field_name not in required_output_field_set
        )
        if unexpected_fields:
            errors.append(
                "Unexpected output fields: " + ", ".join(unexpected_fields)
            )

    response_mode = candidate_output.get("response_mode")
    if response_mode not in allowed_response_modes:
        errors.append(
            "response_mode must be one of: "
            + ", ".join(sorted(allowed_response_modes))
        )
    if response_mode != expected_response_mode:
        errors.append(
            "response_mode mismatch: "
            f"expected {expected_response_mode}, got {response_mode!r}"
        )

    operator_message_error = validate_non_empty_string_field(
        candidate_output,
        "operator_message",
    )
    if operator_message_error is not None:
        errors.append(operator_message_error)

    recommended_next_actions, recommended_next_actions_errors = (
        validate_list_of_strings_field(
            candidate_output,
            "recommended_next_actions",
        )
    )
    errors.extend(recommended_next_actions_errors)

    grounded_input_fields_used, grounded_input_fields_used_errors = (
        validate_list_of_strings_field(
            candidate_output,
            "grounded_input_fields_used",
        )
    )
    errors.extend(grounded_input_fields_used_errors)

    if not grounded_input_fields_used:
        errors.append("grounded_input_fields_used must not be empty.")
    else:
        errors.extend(
            build_disallowed_grounded_fields_errors(
                grounded_input_fields_used,
                allowed_grounded_fields=allowed_grounded_fields,
            )
        )

    return {
        "wp_id": output_mapping_payload["wp_id"],
        "output_acceptance_metadata": {
            "output_acceptance_id": OUTPUT_ACCEPTANCE_ID,
            "output_mapping_id": output_mapping_metadata["output_mapping_id"],
            "output_contract_id": output_mapping_metadata["output_contract_id"],
            "validation_state": "accepted" if not errors else "rejected",
            "acceptance_ready": not errors,
            "current_response_mode": output_mapping_metadata[
                "current_response_mode"
            ],
            "selected_plan_id": output_mapping_metadata["selected_plan_id"],
        },
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