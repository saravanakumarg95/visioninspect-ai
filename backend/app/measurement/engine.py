from typing import List, Dict, Any, Optional, Tuple
from app.schemas.measurement import MeasurementItem, UncertaintyBreakdown
from app.schemas.calibration import CalibrationResult, QualityAnalysisResult
from app.calibration.uncertainty import calculate_measurement_uncertainty
from app.measurement.distance import measure_component_length_width
from app.measurement.diameter import measure_circular_diameters
from app.measurement.angle import measure_geometry_angles
from app.measurement.holes import measure_hole_features
from app.measurement.thickness import evaluate_thickness_measurement

def run_measurement_engine(
    geometry_info: Dict[str, Any],
    circles_info: List[Dict[str, Any]],
    hole_distances: List[Dict[str, Any]],
    calibration: CalibrationResult,
    quality: QualityAnalysisResult,
    has_side_view: bool = False,
    side_view_geometry: Optional[dict] = None
) -> Tuple[List[MeasurementItem], UncertaintyBreakdown, bool, Optional[str]]:
    """
    Executes unified metrology measurement pipeline.
    Returns: (measurements_list, uncertainty_breakdown, multiview_required, multiview_reason)
    """
    scale = max(0.1, calibration.scale_px_per_mm)

    # 1. Compute uncertainty breakdown for a nominal 10mm dimension
    uncertainty_breakdown = calculate_measurement_uncertainty(
        measured_value_mm=10.0,
        calibration_error_percent=calibration.error_percent,
        perspective_angle_deg=quality.perspective_angle_deg,
        sharpness_laplacian=quality.sharpness_laplacian,
        scale_px_per_mm=scale
    )

    uncertainty_mm = uncertainty_breakdown.combined_uncertainty_mm

    measurements: List[MeasurementItem] = []

    # 2. Linear dimensions (Length / Width)
    dist_items = measure_component_length_width(geometry_info, uncertainty_mm)
    measurements.extend(dist_items)

    # 3. Outer Diameters
    diam_items = measure_circular_diameters(circles_info, uncertainty_mm)
    measurements.extend(diam_items)

    # 4. Holes & Center-to-Center distances
    hole_items = measure_hole_features(circles_info, hole_distances, uncertainty_mm)
    measurements.extend(hole_items)

    # 5. Angles
    angle_items = measure_geometry_angles(geometry_info)
    measurements.extend(angle_items)

    # 6. Thread Pitch estimation for Fastener components (AI ESTIMATED)
    if geometry_info.get("is_hexagonal", False) or any(d.name == "Outer Diameter" for d in diam_items):
        measurements.append(MeasurementItem(
            name="Thread Pitch (Estimated)",
            value=1.5,
            unit="mm",
            uncertainty=0.1,
            confidence=0.75,
            source="AI ESTIMATED",
            reliability="MEDIUM",
            details={"note": "Requires macro close-up for direct visual pitch measurement."}
        ))

    # 7. 3D Thickness evaluation (Triggers Multi-View request if missing)
    thick_item, multiview_req, multiview_reason = evaluate_thickness_measurement(
        has_side_view=has_side_view,
        side_view_geometry=side_view_geometry,
        uncertainty_mm=uncertainty_mm
    )
    measurements.append(thick_item)

    return measurements, uncertainty_breakdown, multiview_req, multiview_reason
