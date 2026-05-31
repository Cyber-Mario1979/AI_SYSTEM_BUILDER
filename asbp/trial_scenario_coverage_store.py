from __future__ import annotations

import json
from pathlib import Path

from asbp.trial_scenario_coverage_model import (
    TrialScenarioCoverageLibraryModel,
    TrialScenarioCoverageRecordModel,
)


DEFAULT_TRIAL_SCENARIO_COVERAGE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "trial_documents"
    / "mvp_trial_scenario_coverage.json"
)


def load_trial_scenario_coverage_library_from_payload(
    payload: dict,
) -> TrialScenarioCoverageLibraryModel:
    if "scenarios" not in payload:
        raise ValueError("trial scenario coverage payload must include scenarios")
    return TrialScenarioCoverageLibraryModel(**payload)


def load_trial_scenario_coverage_library_from_path(
    path: Path,
) -> TrialScenarioCoverageLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return load_trial_scenario_coverage_library_from_payload(payload)


def load_default_trial_scenario_coverage_library() -> TrialScenarioCoverageLibraryModel:
    return load_trial_scenario_coverage_library_from_path(
        DEFAULT_TRIAL_SCENARIO_COVERAGE_PATH
    )


def list_trial_scenario_coverage_ids(
    library: TrialScenarioCoverageLibraryModel,
) -> list[str]:
    return [scenario.scenario_id for scenario in library.scenarios]


def get_trial_scenario_coverage_by_id(
    library: TrialScenarioCoverageLibraryModel,
    scenario_id: str,
) -> TrialScenarioCoverageRecordModel:
    for scenario in library.scenarios:
        if scenario.scenario_id == scenario_id:
            return scenario
    raise ValueError(f"Trial scenario coverage record not found: {scenario_id}")


def collect_trial_scenario_domains(
    library: TrialScenarioCoverageLibraryModel,
) -> set[str]:
    return {scenario.domain for scenario in library.scenarios}


def collect_trial_scenario_document_refs(
    library: TrialScenarioCoverageLibraryModel,
) -> set[str]:
    return {
        document_ref
        for scenario in library.scenarios
        for document_ref in scenario.document_refs
    }


def collect_trial_scenario_utility_systems(
    library: TrialScenarioCoverageLibraryModel,
) -> set[str]:
    return {
        scenario.utility_system
        for scenario in library.scenarios
        if scenario.utility_system is not None
    }


def collect_trial_scenario_asset_archetypes(
    library: TrialScenarioCoverageLibraryModel,
) -> set[str]:
    return {
        scenario.asset_archetype
        for scenario in library.scenarios
        if scenario.asset_archetype is not None
    }


def assert_trial_scenario_domains_exist(
    library: TrialScenarioCoverageLibraryModel,
    required_domains: set[str],
) -> None:
    missing_domains = sorted(required_domains - collect_trial_scenario_domains(library))
    if missing_domains:
        raise ValueError(
            "Trial scenario coverage is missing required domain(s): "
            f"{', '.join(missing_domains)}"
        )
