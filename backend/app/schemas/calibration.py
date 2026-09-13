from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class CalibrationConfig(BaseModel):
    method: str = Field(default="aruco", description="aruco, ruler, or known_object")
    reference_size_mm: float = Field(default=50.0, description="Known physical dimension in mm")
    aruco_dict: str = Field(default="DICT_4X4_50", description="ArUco dictionary name")
    aruco_id: Optional[int] = Field(default=None, description="Expected ArUco marker ID")

class CalibrationResult(BaseModel):
    calibrated: bool
    method: str
    reference_size_mm: float
    detected_size_px: float
    scale_px_per_mm: float
    error_percent: float
    perspective_corrected: bool = False
    homography_matrix: Optional[List[List[float]]] = None
    uncertainty_percent: float = 0.5
    status: str = "valid"  # valid, uncalibrated, failed
    details: Dict[str, Any] = {}

class QualityAnalysisResult(BaseModel):
    sharpness_laplacian: float
    is_sharp: bool
    brightness_mean: float
    is_well_lit: bool
    glare_percent: float
    is_low_glare: bool
    object_coverage_percent: float
    is_adequate_size: bool
    perspective_angle_deg: float
    is_perpendicular: bool
    readiness_score: float  # 0 to 100
    recommendations: List[str] = []
