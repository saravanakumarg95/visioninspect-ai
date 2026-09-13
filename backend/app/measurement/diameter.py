from typing import List, Dict, Any, Optional
from app.schemas.measurement import MeasurementItem

def measure_circular_diameters(
    circles_info: List[Dict[str, Any]],
    uncertainty_mm: float
) -> List[MeasurementItem]:
    """
    Extracts circular feature measurements (Outer Diameter, Inner Diameter).
    """
    items = []
    for c in circles_info:
        if c.get("type") == "outer_diameter":
            val = c.get("diameter_mm", 0.0)
            if val > 0:
                items.append(MeasurementItem(
                    name="Outer Diameter",
                    value=round(val, 2),
                    unit="mm",
                    uncertainty=uncertainty_mm,
                    confidence=c.get("confidence", 0.90),
                    source="DIRECT",
                    reliability="HIGH"
                ))
    return items
