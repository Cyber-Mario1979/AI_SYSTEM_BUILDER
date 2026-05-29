import pytest
from pydantic import ValidationError

from asbp.standards_registry_model import (
    StandardsRegistryModel,
    StandardsRegistrySourceRecordModel,
)


def _verified_authoritative_source_payload() -> dict:
    return {
        "std_id": "STD-TEST-VERIFIED",
        "source_name": "Verified test standard",
        "source_type": "regulation",
        "authority_status": "authoritative",
        "verification_status": "verified",
        "version_or_effective_date": "2026",
        "jurisdiction_or_owner": "TEST",
        "applicability_scope": ["test_scope"],
        "applicability_conditions": ["Applies to test scope."],
        "citation_depths": ["document", "version", "section", "clause"],
        "source_location": "controlled://test-source",
        "mandatory_flag": "mandatory_when_applicable",
        "source_limitations": [],
    }


def _limited_reference_source_payload() -> dict:
    payload = _verified_authoritative_source_payload()
    payload.update(
        {
            "std_id": "STD-TEST-REFERENCE",
            "authority_status": "reference",
            "verification_status": "pending_verification",
            "version_or_effective_date": "TBD",
            "citation_depths": ["document"],
            "mandatory_flag": "not_mandatory_unless_adopted",
            "source_limitations": [
                "Reference source cannot drive mandatory output unless adopted."
            ],
        }
    )
    return payload


def _registry_payload(source: dict | None = None) -> dict:
    return {
        "registry_id": "STANDARDS_SOURCE_REGISTRY@v0.1",
        "registry_version": "v0.1",
        "status": "runtime_registry_source",
        "approval_status": "approved_source_authority_model",
        "source_authority_reference": "docs/standards/STANDARDS_SOURCE_REGISTRY.md",
        "source_records": [source or _verified_authoritative_source_payload()],
        "registry_controls": ["Registry records are source metadata only."],
        "explicit_non_implementation_claims": [
            "does_not_embed_controlled_standards_text",
            "does_not_implement_standards_retrieval_or_embedding",
            "does_not_generate_product_ready_standards_output",
            "does_not_verify_public_regulatory_meaning",
        ],
    }


def test_verified_authoritative_source_can_support_mandatory_use():
    source = StandardsRegistrySourceRecordModel(
        **_verified_authoritative_source_payload()
    )

    assert source.can_support_mandatory_use() is True
    assert source.requires_visible_limitations() is False


def test_pending_reference_source_requires_visible_limitations():
    source = StandardsRegistrySourceRecordModel(**_limited_reference_source_payload())

    assert source.can_support_mandatory_use() is False
    assert source.requires_visible_limitations() is True


def test_limited_source_rejects_missing_source_limitations():
    payload = _limited_reference_source_payload()
    payload["source_limitations"] = []

    with pytest.raises(ValidationError) as exc_info:
        StandardsRegistrySourceRecordModel(**payload)

    assert "Limited standards registry source requires source_limitations" in str(
        exc_info.value
    )


def test_verified_source_rejects_tbd_version():
    payload = _verified_authoritative_source_payload()
    payload["version_or_effective_date"] = "TBD"

    with pytest.raises(ValidationError) as exc_info:
        StandardsRegistrySourceRecordModel(**payload)

    assert "Verified standards registry source cannot have TBD version" in str(
        exc_info.value
    )


def test_section_or_clause_depth_requires_verified_source():
    payload = _limited_reference_source_payload()
    payload["citation_depths"] = ["document", "clause"]

    with pytest.raises(ValidationError) as exc_info:
        StandardsRegistrySourceRecordModel(**payload)

    assert "Section or clause citation depth requires verified source evidence" in str(
        exc_info.value
    )


def test_version_depth_rejects_tbd_version():
    payload = _limited_reference_source_payload()
    payload["citation_depths"] = ["document", "version"]

    with pytest.raises(ValidationError) as exc_info:
        StandardsRegistrySourceRecordModel(**payload)

    assert "Version-level citation requires known version or effective date" in str(
        exc_info.value
    )


def test_registry_rejects_duplicate_source_ids():
    source = _verified_authoritative_source_payload()
    payload = _registry_payload(source)
    payload["source_records"].append(source.copy())

    with pytest.raises(ValidationError) as exc_info:
        StandardsRegistryModel(**payload)

    assert "Duplicate standards registry source id is not allowed" in str(
        exc_info.value
    )


def test_registry_requires_explicit_non_implementation_claims():
    payload = _registry_payload()
    payload["explicit_non_implementation_claims"] = [
        "does_not_embed_controlled_standards_text"
    ]

    with pytest.raises(ValidationError) as exc_info:
        StandardsRegistryModel(**payload)

    assert "M28.8 runtime standards registry is missing explicit" in str(
        exc_info.value
    )
