import pytest
from app.standards.matcher import match_fastener_to_standards
from app.standards.fasteners import search_fasteners_database

def test_fastener_standards_matching():
    match = match_fastener_to_standards(
        component_type="hex_bolt",
        measured_diameter_mm=10.1,
        measured_length_mm=50.0
    )
    assert match is not None
    assert match.matched is True
    assert match.nominal_diameter_mm == 10.0
    assert match.designation == "M10 x 1.5"
    assert match.confidence >= 0.85

def test_fastener_database_search():
    results = search_fasteners_database("M10")
    assert len(results) >= 1
    assert any("M10" in item["nominal_size"] for item in results)
