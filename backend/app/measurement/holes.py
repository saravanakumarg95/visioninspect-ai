from typing import List, Dict, Any
from app.schemas.measurement import MeasurementItem

def measure_hole_features(
    circles_info: List[Dict[str, Any]],
    hole_distances: List[Dict[str, Any]],
    uncertainty_mm: float
) -> List[MeasurementItem]:
    """
    Measures hole diameters and center-to-center distances between holes.
    """
    items = []
    holes = [c for c in circles_info if c.get("type") == "hole"]

    for idx, h in enumerate(holes):
        val = h.get("diameter_mm", 0.0)
        items.append(MeasurementItem(
            name=f"Hole #{idx + 1} Diameter",
            value=round(val, 2),
            unit="mm",
            uncertainty=uncertainty_mm,
            confidence=h.get("confidence", 0.88),
            source="DIRECT",
            reliability="HIGH"
        ))

    for d in hole_distances:
        h1 = d["hole_index_1"]
        h2 = d["hole_index_2"]
        val = d["distance_mm"]
        items.append(MeasurementItem(
            name=f"Hole #{h1} to #{h2} Distance",
            value=round(val, 2),
            unit="mm",
            uncertainty=uncertainty_mm,
            confidence=0.89,
            source="DIRECT",
            reliability="HIGH"
        ))

    return items
