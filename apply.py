from pathlib import Path
from textwrap import dedent


FILES: dict[str, str] = {
    "asbp/adapters/__init__.py": dedent("""
        \"\"\"Delivery adapters for the M11.1 production-structure baseline.\"\"\"

        from .cli import VERSION, build_parser, main

        __all__ = ["VERSION", "build_parser", "main"]
    """).lstrip(),
    "asbp/adapters/cli.py": dedent("""
        \"\"\"CLI adapter surface for the M11.1 production-structure baseline.\"\"\"

        from asbp.cli import VERSION, build_parser, main

        __all__ = ["VERSION", "build_parser", "main"]
    """).lstrip(),
    "asbp/core/__init__.py": dedent("""
        \"\"\"Deterministic core package for the M11.1 production-structure baseline.\"\"\"

        from . import (
            binding_context,
            collections,
            models,
            planning,
            source_of_work,
            tasks,
            work_packages,
        )

        __all__ = [
            "binding_context",
            "collections",
            "models",
            "planning",
            "source_of_work",
            "tasks",
            "work_packages",
        ]
    """).lstrip(),
    "asbp/core/models.py": dedent("""
        \"\"\"State and entity models exposed through the core boundary.\"\"\"

        from asbp.state_model import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/core/tasks.py": dedent("""
        \"\"\"Task-domain logic exposed through the core boundary.\"\"\"

        from asbp.task_logic import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/core/collections.py": dedent("""
        \"\"\"Collection-domain logic exposed through the core boundary.\"\"\"

        from asbp.collection_logic import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/core/work_packages.py": dedent("""
        \"\"\"Work Package-domain logic exposed through the core boundary.\"\"\"

        from asbp.work_package_logic import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/core/binding_context.py": dedent("""
        \"\"\"Binding-context logic exposed through the core boundary.\"\"\"

        from asbp.binding_context_logic import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/core/planning.py": dedent("""
        \"\"\"Planning logic exposed through the core boundary.\"\"\"

        from asbp.planning_logic import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/core/source_of_work.py": dedent("""
        \"\"\"Source-of-work logic exposed through the core boundary.\"\"\"

        from asbp.source_of_work_logic import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/state/__init__.py": dedent("""
        \"\"\"State-boundary package for the M11.1 production-structure baseline.\"\"\"

        from .store import (
            build_persisted_state_payload,
            get_state_file_path,
            load_raw_state,
            load_state_or_none,
            load_validated_state,
            save_validated_state,
            save_validated_state_to_path,
        )

        __all__ = [
            "build_persisted_state_payload",
            "get_state_file_path",
            "load_raw_state",
            "load_state_or_none",
            "load_validated_state",
            "save_validated_state",
            "save_validated_state_to_path",
        ]
    """).lstrip(),
    "asbp/state/store.py": dedent("""
        \"\"\"State persistence boundary for the M11.1 production-structure baseline.\"\"\"

        from asbp.state_store import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/services/__init__.py": dedent("""
        \"\"\"Service/orchestration package for the M11.1 production-structure baseline.\"\"\"

        from .orchestration import build_work_package_orchestration_payload

        __all__ = ["build_work_package_orchestration_payload"]
    """).lstrip(),
    "asbp/services/orchestration.py": dedent("""
        \"\"\"Orchestration service surface for the M11.1 production-structure baseline.\"\"\"

        from asbp.orchestration_logic import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/runtime/__init__.py": dedent("""
        \"\"\"Runtime package for the M11.1 production-structure baseline.\"\"\"

        from .boundary import build_work_package_runtime_boundary_payload
        from .contracts import (
            EXPECTED_OUTPUT_FIELDS,
            GENERATION_SURFACE_ID,
            HANDOFF_CONTRACT_ID,
            MODEL_MAY,
            MODEL_MAY_NOT,
            OUTPUT_FIELD_TYPES,
            PROMPT_CONTRACT_ID,
            PROHIBITED_FREEFORM_DRIFT,
            REQUIRED_INPUT_FIELDS,
            build_candidate_response_template,
            build_generation_state,
            build_handoff_state,
            build_output_contract,
            build_prompt_contract_state_and_mode,
            build_prose_generation_instructions,
            build_runtime_boundary_state,
        )
        from .generation import build_work_package_generation_request_payload
        from .handoff import build_work_package_llm_handoff_payload
        from .output_validation import (
            load_candidate_response_json,
            validate_work_package_candidate_response,
        )
        from .prompt_contract import build_work_package_prompt_contract_payload
        from .retry_fail import evaluate_work_package_candidate_response_attempt

        __all__ = [
            "EXPECTED_OUTPUT_FIELDS",
            "GENERATION_SURFACE_ID",
            "HANDOFF_CONTRACT_ID",
            "MODEL_MAY",
            "MODEL_MAY_NOT",
            "OUTPUT_FIELD_TYPES",
            "PROMPT_CONTRACT_ID",
            "PROHIBITED_FREEFORM_DRIFT",
            "REQUIRED_INPUT_FIELDS",
            "build_candidate_response_template",
            "build_generation_state",
            "build_handoff_state",
            "build_output_contract",
            "build_prompt_contract_state_and_mode",
            "build_prose_generation_instructions",
            "build_runtime_boundary_state",
            "build_work_package_generation_request_payload",
            "build_work_package_llm_handoff_payload",
            "build_work_package_prompt_contract_payload",
            "build_work_package_runtime_boundary_payload",
            "evaluate_work_package_candidate_response_attempt",
            "load_candidate_response_json",
            "validate_work_package_candidate_response",
        ]
    """).lstrip(),
    "asbp/runtime/boundary.py": dedent("""
        \"\"\"Runtime boundary surface for the M11.1 production-structure baseline.\"\"\"

        from asbp.runtime_boundary_logic import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/runtime/contracts.py": dedent("""
        \"\"\"Runtime contract helpers for the M11.1 production-structure baseline.\"\"\"

        from asbp.runtime_surface_helpers import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/runtime/prompt_contract.py": dedent("""
        \"\"\"Prompt-contract surface for the M11.1 production-structure baseline.\"\"\"

        from asbp.prompt_contract_logic import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/runtime/handoff.py": dedent("""
        \"\"\"LLM handoff surface for the M11.1 production-structure baseline.\"\"\"

        from asbp.runtime_handoff_logic import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/runtime/generation.py": dedent("""
        \"\"\"Controlled-generation surface for the M11.1 production-structure baseline.\"\"\"

        from asbp.generation_surface_logic import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/runtime/output_validation.py": dedent("""
        \"\"\"Output-validation surface for the M11.1 production-structure baseline.\"\"\"

        from asbp.output_validation_logic import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/runtime/retry_fail.py": dedent("""
        \"\"\"Retry/fail decision surface for the M11.1 production-structure baseline.\"\"\"

        from asbp.retry_fail_logic import *  # noqa: F401,F403
    """).lstrip(),
    "asbp/__main__.py": dedent("""
        from asbp.adapters.cli import main

        if __name__ == "__main__":
            main()
    """).lstrip(),
    "tests/test_m11_1_production_structure_baseline.py": dedent("""
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
    """).lstrip(),
}


def write_file(repo_root: Path, relative_path: str, content: str) -> None:
    target = repo_root / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")
    print(f"Wrote: {relative_path}")


def main() -> None:
    repo_root = Path(__file__).resolve().parent

    for relative_path, content in FILES.items():
        write_file(repo_root, relative_path, content)

    print()
    print("M11.1 production-structure baseline files applied.")
    print("Next run: python -m pytest -q")


if __name__ == "__main__":
    main()