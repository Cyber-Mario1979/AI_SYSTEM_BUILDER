from collections.abc import Iterable, Mapping


def validate_non_empty_string_field(
    candidate_output: Mapping[str, object],
    field_name: str,
) -> str | None:
    value = candidate_output.get(field_name)
    if not isinstance(value, str) or not value.strip():
        return f"{field_name} must be a non-empty string."
    return None


def validate_list_of_strings_field(
    candidate_output: Mapping[str, object],
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


def build_disallowed_grounded_fields_errors(
    grounded_input_fields_used: Iterable[str],
    *,
    allowed_grounded_fields: set[str],
) -> list[str]:
    invalid_grounded_fields = sorted(
        field_name
        for field_name in grounded_input_fields_used
        if field_name not in allowed_grounded_fields
    )
    if not invalid_grounded_fields:
        return []

    return [
        "grounded_input_fields_used contains disallowed fields: "
        + ", ".join(invalid_grounded_fields)
    ]