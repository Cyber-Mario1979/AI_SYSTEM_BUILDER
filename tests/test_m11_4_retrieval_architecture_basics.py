from typing import cast

import pytest

from asbp.retrieval import (
    GOVERNED_DETERMINISTIC_RETRIEVAL_MODE,
    GOVERNED_SOURCE_OF_TRUTH_ROLE,
    PROBABILISTIC_SEARCH_RETRIEVAL_MODE,
    PROBABILISTIC_SOURCE_OF_TRUTH_ROLE,
    build_governed_retrieval_request,
    build_probabilistic_search_retrieval_request,
    build_retrieval_architecture_baseline,
    validate_retrieval_request,
)


def test_m11_4_retrieval_categories_are_explicitly_separated() -> None:
    baseline = build_retrieval_architecture_baseline()
    retrieval_categories = cast(
        dict[str, dict[str, str]],
        baseline["retrieval_categories"],
    )

    assert baseline["checkpoint"] == "M11.4"
    assert (
        baseline["resolver_registry_dependency"]
        == "required_before_live_governed_retrieval"
    )
    assert (
        retrieval_categories[GOVERNED_DETERMINISTIC_RETRIEVAL_MODE][
            "source_of_truth_role"
        ]
        == GOVERNED_SOURCE_OF_TRUTH_ROLE
    )
    assert (
        retrieval_categories[PROBABILISTIC_SEARCH_RETRIEVAL_MODE][
            "source_of_truth_role"
        ]
        == PROBABILISTIC_SOURCE_OF_TRUTH_ROLE
    )


def test_m11_4_governed_request_is_version_pinned_and_compiled_surface_bound() -> None:
    request = build_governed_retrieval_request(
        artifact_kind="task_pool",
        lookup_id="oral-solid-dose-standard",
        compiled_surface_id="task_pool_manifest_v1",
        library_version="2026.04",
    )

    assert request["mode"] == GOVERNED_DETERMINISTIC_RETRIEVAL_MODE
    assert request["artifact_kind"] == "task_pool"
    assert request["lookup_id"] == "oral-solid-dose-standard"
    assert request["compiled_surface_id"] == "task_pool_manifest_v1"
    assert request["library_version"] == "2026.04"
    assert request["source_of_truth_role"] == GOVERNED_SOURCE_OF_TRUTH_ROLE


def test_m11_4_governed_request_rejects_probabilistic_query_shape() -> None:
    request = build_governed_retrieval_request(
        artifact_kind="task_pool",
        lookup_id="oral-solid-dose-standard",
        compiled_surface_id="task_pool_manifest_v1",
        library_version="2026.04",
    )
    request["query_text"] = "tablet press qualification"

    with pytest.raises(ValueError, match="query_text"):
        validate_retrieval_request(request)


def test_m11_4_probabilistic_request_rejects_governed_lookup_identity() -> None:
    request = build_probabilistic_search_retrieval_request(
        query_text="tablet press containment cleaning verification",
        search_scope="authored_content_index",
    )
    request["lookup_id"] = "oral-solid-dose-standard"

    with pytest.raises(ValueError, match="lookup_id"):
        validate_retrieval_request(request)


def test_m11_4_requests_may_not_claim_source_authority_override() -> None:
    request = build_probabilistic_search_retrieval_request(
        query_text="tablet press containment cleaning verification",
        search_scope="authored_content_index",
    )
    request["source_authority_override"] = "true"

    with pytest.raises(ValueError, match="source_authority_override"):
        validate_retrieval_request(request)