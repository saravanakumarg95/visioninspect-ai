from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from .calibration import CalibrationResult, QualityAnalysisResult
from .measurement import MeasurementItem, GeometricFeature, UncertaintyBreakdown

class DefectItem(BaseModel):
    defect_type: str = Field(..., description="damaged_edge, surface_scratch, missing_hole, deformation, abnormal_geometry")
    confidence: float = Field(..., description="0.0 to 1.0")
    severity: str = Field(default="MEDIUM", description="LOW, MEDIUM, HIGH, CRITICAL")
    location_bbox: Optional[List[float]] = None  # [x, y, w, h]
    description: str = ""

class FastenerMatch(BaseModel):
    matched: bool
    standard: str = "ISO Metric"
    designation: str = "M10 x 1.5"
    type: str = "hex_bolt"
    nominal_diameter_mm: float = 10.0
    pitch_mm: Optional[float] = 1.5
    confidence: float = 0.90
    match_source: str = "DATABASE MATCH"

class ComponentInfo(BaseModel):
    detected_class: str = Field(default="unknown", description="hex_bolt, nut, screw, washer, shaft, plate, bracket, gear, flange, machined_component")
    confidence: float = Field(default=0.0)
    detection_method: str = Field(default="Classical CV fallback", description="YOLO AI model or Classical CV fallback")
    bounding_box: Optional[List[float]] = None

class InspectionCreateRequest(BaseModel):
    component_name: Optional[str] = None
    part_number: Optional[str] = None
    operator_name: Optional[str] = None
    reference_size_mm: float = 50.0
    calibration_method: str = "aruco"

class InspectionResponse(BaseModel):
    inspection_id: str
    created_at: str
    mode: str = Field(default="photo", description="photo, video, live")
    component: ComponentInfo
    quality: QualityAnalysisResult
    calibration: CalibrationResult
    measurements: List[MeasurementItem]
    defects: List[DefectItem]
    fastener: Optional[FastenerMatch] = None
    uncertainty: UncertaintyBreakdown
    status: str = Field(default="REVIEW", description="PASS, FAIL, or REVIEW")
    multiview_required: bool = False
    multiview_reason: Optional[str] = None
    views_captured: int = 1
    annotated_image_url: Optional[str] = None
    pdf_report_url: Optional[str] = None
    notes: List[str] = []
