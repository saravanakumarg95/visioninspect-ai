from typing import List, Optional
from app.schemas.inspection import DefectItem, ComponentInfo
from app.schemas.calibration import CalibrationResult, QualityAnalysisResult
from app.schemas.measurement import MeasurementItem

def determine_inspection_verdict(
    quality: QualityAnalysisResult,
    calibration: CalibrationResult,
    component: ComponentInfo,
    measurements: List[MeasurementItem],
    defects: List[DefectItem]
) -> str:
    """
    Evaluates 3-State Inspection Verdict: PASS, FAIL, REVIEW
    """
    # 1. Uncalibrated or low quality image requires REVIEW
    if not calibration.calibrated or quality.readiness_score < 60.0:
        return "REVIEW"

    # 2. Unknown component or low AI confidence requires REVIEW
    if component.detected_class == "unknown" or component.confidence < 0.65:
        return "REVIEW"

    # 3. High severity defect or out-of-tolerance measurement triggers FAIL
    has_critical_defect = any(d.severity in ["HIGH", "CRITICAL"] for d in defects)
    has_failed_tolerance = any(m.pass_fail == "FAIL" for m in measurements)

    if has_critical_defect or has_failed_tolerance:
        return "FAIL"

    # 4. Low confidence defects or medium quality score trigger REVIEW
    has_medium_defect = any(d.severity == "MEDIUM" for d in defects)
    if has_medium_defect or quality.readiness_score < 75.0:
        return "REVIEW"

    # 5. Otherwise PASS
    return "PASS"
