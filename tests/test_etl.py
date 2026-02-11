from etl import transform_claim
from types import SimpleNamespace
from datetime import date


def mock_claim():
    # Mock line items
    line_items = [
        SimpleNamespace(
            procedure_code="PROC1",
            billed_amount=200,
            paid_amount=100,
        ),
        SimpleNamespace(
            procedure_code="PROC2",
            billed_amount=300,
            paid_amount=300,
        ),
    ]

    # Mock member object
    member = SimpleNamespace(
        employer_group_id=100,
    )

    # Mock claim object
    claim = SimpleNamespace(
        claim_id=1,
        member_id=10,
        provider_id=20,
        service_date=date(2026, 1, 15),
        line_items=line_items,
        member=member,
    )

    return claim


def test_transform_claim_totals():
    claim = mock_claim()
    result = transform_claim(claim)

    assert result["total_paid"] == 400
    assert result["status"] == "Processed"


def test_transform_claim_structure():
    claim = mock_claim()
    result = transform_claim(claim)

    assert "claim_id" in result
    assert "line_items" in result
    assert isinstance(result["line_items"], list)
