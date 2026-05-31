from __future__ import annotations

import json
from pathlib import Path

from asbp.profile_source_model import (
    PresetFamilyId,
    ProfileContextFieldModel,
    ProfileLibraryModel,
    ProfileSourceModel,
)


PROFILE_SOURCE_DIR = Path(__file__).resolve().parents[1] / "data" / "source" / "profiles"
DEFAULT_PROFILE_SOURCE_PATH = PROFILE_SOURCE_DIR / "starter_profiles.json"
MVP_PROFILE_SOURCE_PATHS = [
    PROFILE_SOURCE_DIR / "mvp_cleanroom_hvac_profiles.json",
    PROFILE_SOURCE_DIR / "mvp_process_equipment_profiles.json",
    PROFILE_SOURCE_DIR / "mvp_utilities_profiles.json",
    PROFILE_SOURCE_DIR / "mvp_csv_profiles.json",
    PROFILE_SOURCE_DIR / "mvp_qc_lab_equipment_profiles.json",
    PROFILE_SOURCE_DIR / "mvp_decommissioning_profiles.json",
    PROFILE_SOURCE_DIR / "mvp_manual_fallback_profiles.json",
]


def load_profile_library_from_payload(payload: dict) -> ProfileLibraryModel:
    if "profiles" not in payload:
        raise ValueError("profile library payload must include profiles")
    return ProfileLibraryModel(**payload)


def load_profile_library_from_path(path: Path) -> ProfileLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return load_profile_library_from_payload(payload)


def load_default_profile_library() -> ProfileLibraryModel:
    return load_profile_library_from_path(DEFAULT_PROFILE_SOURCE_PATH)


def load_mvp_profile_libraries() -> list[ProfileLibraryModel]:
    return [load_profile_library_from_path(path) for path in MVP_PROFILE_SOURCE_PATHS]


def list_profile_ids(library: ProfileLibraryModel) -> list[str]:
    return [profile.profile_id for profile in library.profiles]


def get_profile_by_id(library: ProfileLibraryModel, profile_id: str) -> ProfileSourceModel:
    for profile in library.profiles:
        if profile.profile_id == profile_id:
            return profile
    raise ValueError(f"Profile source definition not found: {profile_id}")


def list_profiles_by_preset_family(library: ProfileLibraryModel, preset_family: PresetFamilyId) -> list[ProfileSourceModel]:
    return [profile for profile in library.profiles if preset_family in profile.related_preset_families]


def get_profile_context_field_by_id(profile: ProfileSourceModel, field_id: str) -> ProfileContextFieldModel:
    for context_field in profile.context_fields:
        if context_field.field_id == field_id:
            return context_field
    raise ValueError("Profile context field definition not found: " f"{profile.profile_id}::{field_id}")


def build_profile_context_definition_id(profile_id: str, field_id: str) -> str:
    return f"{profile_id}::{field_id}"
