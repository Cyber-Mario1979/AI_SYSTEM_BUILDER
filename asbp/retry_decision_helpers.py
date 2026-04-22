from typing import Literal, TypedDict


DecisionState = Literal["accepted", "retry_allowed", "fail_closed"]


class RetryDecision(TypedDict):
    decision_state: DecisionState
    action: str
    retries_remaining: int
    decision_rationale: list[str]


def build_retry_decision(
    *,
    validation_state: str,
    attempt_number: int,
    max_attempts: int,
    accepted_action: str,
    retry_action: str,
    fail_closed_action: str,
) -> RetryDecision:
    decision_rationale: list[str] = []

    if max_attempts < 1:
        return {
            "decision_state": "fail_closed",
            "action": fail_closed_action,
            "retries_remaining": 0,
            "decision_rationale": [
                "invalid_retry_control_state:max_attempts_must_be_positive"
            ],
        }

    if attempt_number < 1:
        return {
            "decision_state": "fail_closed",
            "action": fail_closed_action,
            "retries_remaining": 0,
            "decision_rationale": [
                "invalid_retry_control_state:attempt_number_must_be_positive"
            ],
        }

    if attempt_number > max_attempts:
        return {
            "decision_state": "fail_closed",
            "action": fail_closed_action,
            "retries_remaining": 0,
            "decision_rationale": [
                "invalid_retry_control_state:attempt_number_exceeds_max_attempts"
            ],
        }

    if validation_state == "accepted":
        return {
            "decision_state": "accepted",
            "action": accepted_action,
            "retries_remaining": max_attempts - attempt_number,
            "decision_rationale": ["validated_output_accepted"],
        }

    if attempt_number < max_attempts:
        return {
            "decision_state": "retry_allowed",
            "action": retry_action,
            "retries_remaining": max_attempts - attempt_number,
            "decision_rationale": [
                "validation_rejected_but_retry_budget_remaining"
            ],
        }

    return {
        "decision_state": "fail_closed",
        "action": fail_closed_action,
        "retries_remaining": 0,
        "decision_rationale": [
            "validation_rejected_and_retry_budget_exhausted"
        ],
    }