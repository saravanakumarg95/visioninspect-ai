export interface CalibrationResult {
  calibrated: boolean;
  method: string;
  reference_size_mm: number;
  detected_size_px: number;
  scale_px_per_mm: number;
  error_percent: number;
  perspective_corrected: boolean;
  homography_matrix?: number[][];
  uncertainty_percent: number;
  status: string;
  details?: Record<string, any>;
}

export interface QualityAnalysisResult {
  sharpness_laplacian: number;
  is_sharp: boolean;
  brightness_mean: number;
  is_well_lit: boolean;
  glare_percent: number;
  is_low_glare: boolean;
  object_coverage_percent: number;
  is_adequate_size: boolean;
  perspective_angle_deg: number;
  is_perpendicular: boolean;
  readiness_score: number;
  recommendations: string[];
}

export interface MeasurementItem {
  name: string;
  value: number | null;
  unit: string;
  uncertainty: number;
  confidence: number;
  source: 'DIRECT' | 'AI ESTIMATED' | 'DATABASE MATCH' | 'INSUFFICIENT DATA';
  reliability: 'HIGH' | 'MEDIUM' | 'LOW' | 'INSUFFICIENT';
  tolerance_nominal?: number;
  tolerance_min?: number;
  tolerance_max?: number;
  pass_fail: 'PASS' | 'FAIL' | 'UNVERIFIED';
  details?: Record<string, any>;
}

export interface DefectItem {
  defect_type: string;
  confidence: number;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  location_bbox?: number[];
  description: string;
}

export interface FastenerMatch {
  matched: boolean;
  standard: string;
  designation: string;
  type: string;
  nominal_diameter_mm: number;
  pitch_mm?: number;
  confidence: number;
  match_source: string;
}

export interface UncertaintyBreakdown {
  calibration_uncertainty_percent: number;
  perspective_uncertainty_percent: number;
  edge_detection_uncertainty_percent: number;
  video_temporal_variance_percent: number;
  combined_uncertainty_mm: number;
  explanation: string;
}

export interface ComponentInfo {
  detected_class: string;
  confidence: number;
  detection_method: string;
  bounding_box?: number[];
}

export interface InspectionResponse {
  inspection_id: string;
  created_at: string;
  mode: 'photo' | 'video' | 'live';
  component: ComponentInfo;
  quality: QualityAnalysisResult;
  calibration: CalibrationResult;
  measurements: MeasurementItem[];
  defects: DefectItem[];
  fastener?: FastenerMatch;
  uncertainty: UncertaintyBreakdown;
  status: 'PASS' | 'FAIL' | 'REVIEW';
  multiview_required: boolean;
  multiview_reason?: string;
  views_captured: number;
  annotated_image_url?: string;
  pdf_report_url?: string;
  notes: string[];
}
