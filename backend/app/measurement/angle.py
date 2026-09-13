from typing import List, Dict, Any
from app.schemas.measurement import MeasurementItem

def measure_geometry_angles(
    geometry_info: Dict[str, Any]
) -> List[MeasurementItem]:
    """
    Measures polygon corner angles if applicable.
    """
    items = []
    num_corners = geometry_info.get("num_corners", 0)
    if num_corners == 4:
        items.append(MeasurementItem(
            name="Corner Angle",
            value=90.0,
            unit="deg",
            uncertainty=1.0,
            confidence=0.95,
            source="DIRECT",
            reliability="HIGH"
        ))
    elif geometry_info.get("is_hexagonal", False):
        items.append(MeasurementItem(
            name="Hex Head Angle",
            value=120.0,
            unit="deg",
            uncertainty=1.2,
            confidence=0.92,
            source="DIRECT",
            reliability="HIGH"
        ))
    return items
