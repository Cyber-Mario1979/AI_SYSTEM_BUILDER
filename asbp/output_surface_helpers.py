# asbp/output_surface_helpers.py

REQUESTED_OUTPUT_FAMILY_UNAVAILABLE_PREFIX = (
    "Requested output family is not available:"
)
INVALID_RETRY_CONTROL_PREFIX = "invalid_retry_control_state:"


def find_output_family_by_id(
    available_output_families: list[dict],
    output_family_id: str,
) -> dict | None:
    return next(
        (
            family
            for family in available_output_families
            if family["output_family_id"] == output_family_id
        ),
        None,
    )


def list_contains_prefixed_value(
    values: list[str],
    prefix: str,
) -> bool:
    return any(value.startswith(prefix) for value in values)


def build_output_runtime_trace_payload(
    *,
    retry_policy: dict,
    decision_rationale: list[str],
    validation_errors: list[str],
    consistency_errors: list[str] | None = None,
) -> dict:
    payload = {
        "retry_policy": dict(retry_policy),
        "decision_rationale": list(decision_rationale),
        "validation_errors": list(validation_errors),
    }
    if consistency_errors is not None:
        payload["consistency_errors"] = list(consistency_errors)
    return payload