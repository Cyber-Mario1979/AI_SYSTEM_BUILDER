import importlib


MODULE_NAMES = [
    "asbp.adapters",
    "asbp.adapters.cli",
    "asbp.core",
    "asbp.core.binding_context",
    "asbp.core.collections",
    "asbp.core.models",
    "asbp.core.planning",
    "asbp.core.source_of_work",
    "asbp.core.tasks",
    "asbp.core.work_packages",
    "asbp.runtime",
    "asbp.runtime.boundary",
    "asbp.runtime.contracts",
    "asbp.runtime.generation",
    "asbp.runtime.handoff",
    "asbp.runtime.output_validation",
    "asbp.runtime.prompt_contract",
    "asbp.runtime.retry_fail",
    "asbp.services",
    "asbp.services.orchestration",
    "asbp.state",
    "asbp.state.store",
]


def test_m11_1_production_structure_modules_import() -> None:
    for module_name in MODULE_NAMES:
        importlib.import_module(module_name)


def test_adapter_cli_entrypoint_matches_legacy_cli() -> None:
    from asbp import cli as legacy_cli
    from asbp.adapters.cli import VERSION, build_parser, main

    assert VERSION == legacy_cli.VERSION
    assert build_parser is legacy_cli.build_parser
    assert main is legacy_cli.main


def test_runtime_boundary_wrapper_matches_legacy_runtime_boundary() -> None:
    from asbp.runtime.boundary import build_work_package_runtime_boundary_payload
    from asbp.runtime_boundary_logic import (
        build_work_package_runtime_boundary_payload as legacy_runtime_boundary,
    )

    assert build_work_package_runtime_boundary_payload is legacy_runtime_boundary


def test_state_store_wrapper_matches_legacy_state_store() -> None:
    from asbp.state.store import get_state_file_path
    from asbp.state_store import get_state_file_path as legacy_get_state_file_path

    assert get_state_file_path is legacy_get_state_file_path


def test_package_main_uses_adapter_entrypoint() -> None:
    import asbp.__main__ as package_main
    from asbp.adapters.cli import main as adapter_main

    assert package_main.main is adapter_main
