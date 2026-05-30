from __future__ import annotations

import json
from pathlib import Path

from asbp.standards_backed_output_model import (
    StandardsBackedOutputControlLibraryModel,
    StandardsBackedOutputControlPacketModel,
)

DEFAULT_STANDARDS_BACKED_OUTPUT_SOURCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "standards_backed_output"
    / "starter_standards_backed_output_controls.json"
)


def load_standards_backed_output_library_from_payload(
    payload: dict,
) -> StandardsBackedOutputControlLibraryModel:
    if "control_packets" not in payload:
        raise ValueError(
            "standards-backed output library payload must include control_packets"
        )
    return StandardsBackedOutputControlLibraryModel(**payload)


def load_standards_backed_output_library_from_path(
    path: Path,
) -> StandardsBackedOutputControlLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return load_standards_backed_output_library_from_payload(payload)


def load_default_standards_backed_output_library() -> StandardsBackedOutputControlLibraryModel:
    return load_standards_backed_output_library_from_path(
        DEFAULT_STANDARDS_BACKED_OUTPUT_SOURCE_PATH,
    )


def list_standards_backed_output_packet_ids(
    library: StandardsBackedOutputControlLibraryModel,
) -> list[str]:
    return [packet.control_packet_id for packet in library.control_packets]


def get_standards_backed_output_packet_by_id(
    library: StandardsBackedOutputControlLibraryModel,
    control_packet_id: str,
) -> StandardsBackedOutputControlPacketModel:
    for packet in library.control_packets:
        if packet.control_packet_id == control_packet_id:
            return packet
    raise ValueError(
        f"Standards-backed output control packet not found: {control_packet_id}"
    )


def list_standards_backed_output_packet_ids_by_template(
    library: StandardsBackedOutputControlLibraryModel,
    template_id: str,
) -> list[str]:
    return [
        packet.control_packet_id
        for packet in library.control_packets
        if packet.template_id == template_id
    ]


def assert_standards_backed_output_packets_exist(
    library: StandardsBackedOutputControlLibraryModel,
    required_packet_ids: set[str],
) -> None:
    registered_packet_ids = set(list_standards_backed_output_packet_ids(library))
    missing_packet_ids = sorted(required_packet_ids - registered_packet_ids)
    if missing_packet_ids:
        joined_missing_ids = ", ".join(missing_packet_ids)
        raise ValueError(
            "Standards-backed output control packets not found: "
            f"{joined_missing_ids}"
        )
