from typing import Optional, Tuple
from app.schemas.measurement import MeasurementItem

def evaluate_thickness_measurement(
    has_side_view: bool = False,
    side_view_geometry: Optional[dict] = None,
    uncertainty_mm: float = 0.1
) -> Tuple[MeasurementItem, bool, str]:
    """
    Evaluates 3D thickness / height dimension.
    If only top-down view is available, returns 'INSUFFICIENT DATA' item and flags multiview_required=True.
    """
    if not has_side_view or not side_view_geometry:
        item = MeasurementItem(
            name="Thickness / Height",
            value=None,  # Null value indicates insufficient data
            unit="mm",
            uncertainty=0.0,
            confidence=0.0,
            source="INSUFFICIENT DATA",
            reliability="INSUFFICIENT",
            details={"reason": "Thickness cannot be measured from a single top-down image. A side view is required."}
        )
        return item, True, "Thickness measurement requires a side view capture."

    # If side view geometry is provided
    thickness_val = side_view_geometry.get("width_mm", 0.0)
    item = MeasurementItem(
        name="Thickness / Height",
        value=round(thickness_val, 2),
        unit="mm",
        uncertainty=uncertainty_mm,
        confidence=0.88,
        source="DIRECT",
        reliability="HIGH"
    )
    return item, False, ""
