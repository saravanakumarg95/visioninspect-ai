from typing import Dict, Any, Optional
from app.schemas.measurement import MeasurementItem

def measure_component_length_width(
    geometry_info: Dict[str, Any],
    uncertainty_mm: float
) -> list[MeasurementItem]:
    """
    Measures linear length and width from bounding min area rectangle.
    """
    items = []
    length_mm = geometry_info.get("length_mm")
    width_mm = geometry_info.get("width_mm")

    if length_mm and length_mm > 0:
        items.append(MeasurementItem(
            name="Length",
            value=round(length_mm, 2),
            unit="mm",
            uncertainty=uncertainty_mm,
            confidence=0.92,
            source="DIRECT",
            reliability="HIGH" if uncertainty_mm <= 0.3 else "MEDIUM"
        ))

    if width_mm and width_mm > 0:
        items.append(MeasurementItem(
            name="Width",
            value=round(width_mm, 2),
            unit="mm",
            uncertainty=uncertainty_mm,
            confidence=0.91,
            source="DIRECT",
            reliability="HIGH" if uncertainty_mm <= 0.3 else "MEDIUM"
        ))

    return items
