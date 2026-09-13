import math
from typing import Optional, List, Dict, Any
from app.schemas.inspection import FastenerMatch
from .database import ISO_METRIC_FASTENERS

def match_fastener_to_standards(
    component_type: str,
    measured_diameter_mm: Optional[float],
    measured_length_mm: Optional[float] = None,
    measured_inner_diameter_mm: Optional[float] = None
) -> Optional[FastenerMatch]:
    """
    Matches measured component dimensions against ISO Metric standards table.
    """
    if component_type not in ["hex_bolt", "nut", "screw", "washer"]:
        return None

    if measured_diameter_mm is None or measured_diameter_mm <= 0:
        return None

    candidates = [f for f in ISO_METRIC_FASTENERS if f["type"] == component_type]
    if not candidates:
        return None

    best_match = None
    best_score = float("inf")

    for cand in candidates:
        if component_type == "washer":
            target_d = cand.get("outer_diameter_mm", 0.0)
            diff = abs(target_d - measured_diameter_mm)
            if measured_inner_diameter_mm and "inner_diameter_mm" in cand:
                diff += abs(cand["inner_diameter_mm"] - measured_inner_diameter_mm)
        else:
            target_d = cand.get("nominal_diameter_mm", 0.0)
            diff = abs(target_d - measured_diameter_mm)

        if diff < best_score:
            best_score = diff
            best_match = cand

    if best_match is None or best_score > 3.5:  # Tolerance cutoff
        return None

    confidence = round(max(0.60, 1.0 - (best_score / 10.0)), 2)

    return FastenerMatch(
        matched=True,
        standard=best_match["standard"],
        designation=best_match["designation"],
        type=best_match["type"],
        nominal_diameter_mm=best_match.get("nominal_diameter_mm", measured_diameter_mm),
        pitch_mm=best_match.get("pitch_mm", 1.5),
        confidence=confidence,
        match_source="DATABASE MATCH"
    )
