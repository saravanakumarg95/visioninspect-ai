from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class MeasurementItem(BaseModel):
    name: str = Field(..., description="diameter, length, width, angle, hole_distance, thickness")
    value: Optional[float] = Field(None, description="Measured numeric value or None if insufficient data")
    unit: str = Field(default="mm")
    uncertainty: float = Field(default=0.0, description="Estimated measurement uncertainty ±mm or ±deg")
    confidence: float = Field(default=0.0, description="Confidence score 0.0 to 1.0")
    source: str = Field(default="DIRECT", description="DIRECT, AI ESTIMATED, or DATABASE MATCH")
    reliability: str = Field(default="HIGH", description="HIGH, MEDIUM, LOW, or INSUFFICIENT")
    tolerance_nominal: Optional[float] = None
    tolerance_min: Optional[float] = None
    tolerance_max: Optional[float] = None
    pass_fail: str = Field(default="UNVERIFIED", description="PASS, FAIL, or UNVERIFIED")
    details: Dict[str, Any] = {}

class GeometricFeature(BaseModel):
    feature_type: str = Field(..., description="circle, line, polygon, hole, contour")
    center: Optional[List[float]] = None
    bounding_box: Optional[List[float]] = None  # [x, y, w, h]
    area_px: Optional[float] = None
    perimeter_px: Optional[float] = None
    radius_px: Optional[float] = None
    points: Optional[List[List[float]]] = None

class UncertaintyBreakdown(BaseModel):
    calibration_uncertainty_percent: float = 0.5
    perspective_uncertainty_percent: float = 0.5
    edge_detection_uncertainty_percent: float = 0.5
    video_temporal_variance_percent: float = 0.0
    combined_uncertainty_mm: float = 0.1
    explanation: str = ""
