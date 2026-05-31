from __future__ import annotations

import json
from pathlib import Path

from asbp.trial_document_generation_model import (
    TrialDocumentScenarioLibraryModel,
    TrialDocumentScenarioModel,
)


DEFAULT_TRIAL_DOCUMENT_SCENARIO_SOURCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "trial_documents"
    / "starter_trial_document_scenarios.json"
)


def load_trial_document_scenario_library_from_payload(
    payload: dict,
) -> TrialDocumentScenarioLibraryModel:
    if "scenarios" not in payload:
        raise ValueError("trial document scenario library payload must include scenarios")

    return TrialDocumentScenarioLibraryModel(**payload)


def load_trial_document_scenario_library_from_path(
    path: Path,
) -> TrialDocumentScenarioLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_trial_document_scenario_library_from_payload(payload)


def load_default_trial_document_scenario_library() -> TrialDocumentScenarioLibraryModel:
    return load_trial_document_scenario_library_from_path(
        DEFAULT_TRIAL_DOCUMENT_SCENARIO_SOURCE_PATH,
    )


def list_trial_document_scenario_ids(
    library: TrialDocumentScenarioLibraryModel,
) -> list[str]:
    return [scenario.scenario_id for scenario in library.scenarios]


def get_trial_document_scenario_by_id(
    library: TrialDocumentScenarioLibraryModel,
    scenario_id: str,
) -> TrialDocumentScenarioModel:
    for scenario in library.scenarios:
        if scenario.scenario_id == scenario_id:
            return scenario

    raise ValueError(f"Trial document scenario source record not found: {scenario_id}")


def assert_trial_document_scenarios_exist(
    library: TrialDocumentScenarioLibraryModel,
    required_scenario_ids: set[str],
) -> None:
    registered_scenario_ids = set(list_trial_document_scenario_ids(library))
    missing_scenario_ids = sorted(required_scenario_ids - registered_scenario_ids)
    if missing_scenario_ids:
        joined_missing_ids = ", ".join(missing_scenario_ids)
        raise ValueError(
            "Trial document scenario source records not found: "
            f"{joined_missing_ids}"
        )
