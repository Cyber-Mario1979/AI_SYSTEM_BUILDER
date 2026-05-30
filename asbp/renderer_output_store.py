from __future__ import annotations

import json
from pathlib import Path

from asbp.renderer_output_model import (
    RendererOutputContractModel,
    RendererOutputFormat,
    RendererSupportedOutputFormat,
)


DEFAULT_RENDERER_OUTPUT_CONTRACT_SOURCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "renderer_output"
    / "starter_renderer_output_contracts.json"
)


def load_renderer_output_contract_from_payload(
    payload: dict,
) -> RendererOutputContractModel:
    if "supported_formats" not in payload:
        raise ValueError("renderer output contract payload must include supported_formats")

    return RendererOutputContractModel(**payload)


def load_renderer_output_contract_from_path(
    path: Path,
) -> RendererOutputContractModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_renderer_output_contract_from_payload(payload)


def load_default_renderer_output_contract() -> RendererOutputContractModel:
    return load_renderer_output_contract_from_path(
        DEFAULT_RENDERER_OUTPUT_CONTRACT_SOURCE_PATH,
    )


def list_supported_renderer_output_formats(
    contract: RendererOutputContractModel,
) -> list[RendererSupportedOutputFormat]:
    return list(contract.supported_formats)


def assert_renderer_output_format_supported(
    contract: RendererOutputContractModel,
    output_format: RendererOutputFormat,
) -> None:
    if output_format in contract.supported_formats:
        return

    raise ValueError(
        "Unsupported renderer output format for M29.7: "
        f"{output_format}"
    )


def media_type_for_renderer_output_format(
    output_format: RendererSupportedOutputFormat,
) -> str:
    return {
        "markdown": "text/markdown",
        "csv_summary": "text/csv",
    }[output_format]
