import numpy as np
from app.schemas.measurement import UncertaintyBreakdown

def calculate_measurement_uncertainty(
    measured_value_mm: float,
    calibration_error_percent: float = 0.5,
    perspective_angle_deg: float = 0.0,
    sharpness_laplacian: float = 100.0,
    video_temporal_std_mm: float = 0.0,
    scale_px_per_mm: float = 10.0
) -> UncertaintyBreakdown:
    """
    Computes root-sum-square combined uncertainty:
    1. Calibration uncertainty u_cal (from ArUco / reference error)
    2. Perspective tilt uncertainty u_persp = (1 - cos(angle)) * 100%
    3. Edge quantization uncertainty u_edge = (0.5 / scale_px_per_mm) / value * 100%
    4. Video temporal variation u_temporal = std / value * 100%
    """
    if measured_value_mm <= 0:
        return UncertaintyBreakdown(
            calibration_uncertainty_percent=0.5,
            perspective_uncertainty_percent=0.5,
            edge_detection_uncertainty_percent=0.5,
            video_temporal_variance_percent=0.0,
            combined_uncertainty_mm=0.1,
            explanation="Default baseline uncertainty"
        )

    # 1. Calibration
    u_cal_pct = max(0.2, float(calibration_error_percent))

    # 2. Perspective angle error: d_measured = d_actual * cos(tilt) -> error = 1 - cos(tilt)
    tilt_rad = np.radians(min(80.0, float(perspective_angle_deg)))
    u_persp_pct = float(abs(1.0 - np.cos(tilt_rad)) * 100.0)
    u_persp_pct = max(0.1, u_persp_pct)

    # 3. Edge detection sub-pixel quantization (0.5 px)
    edge_px_err = 0.5
    if sharpness_laplacian < 80.0:
        edge_px_err = 1.5  # Higher quantization error if blurry
    u_edge_mm = edge_px_err / max(0.1, scale_px_per_mm)
    u_edge_pct = (u_edge_mm / measured_value_mm) * 100.0

    # 4. Temporal variation
    u_temp_pct = (video_temporal_std_mm / measured_value_mm * 100.0) if video_temporal_std_mm > 0 else 0.0

    # Combined percentage via RSS (Root-Sum-Square)
    rss_pct = float(np.sqrt(u_cal_pct**2 + u_persp_pct**2 + u_edge_pct**2 + u_temp_pct**2))
    combined_mm = float((rss_pct / 100.0) * measured_value_mm)

    # Round to reasonable precision (e.g. 0.05mm minimum limit)
    combined_mm = max(0.05, round(combined_mm, 2))

    explanation = (
        f"Combined RSS uncertainty of ±{combined_mm} mm ({rss_pct:.2f}%) derived from "
        f"Calibration ({u_cal_pct:.2f}%), Perspective Tilt ({u_persp_pct:.2f}%), "
        f"Edge Quantization ({u_edge_pct:.2f}%), and Temporal Variation ({u_temp_pct:.2f}%)."
    )

    return UncertaintyBreakdown(
        calibration_uncertainty_percent=round(u_cal_pct, 2),
        perspective_uncertainty_percent=round(u_persp_pct, 2),
        edge_detection_uncertainty_percent=round(u_edge_pct, 2),
        video_temporal_variance_percent=round(u_temp_pct, 2),
        combined_uncertainty_mm=combined_mm,
        explanation=explanation
    )
