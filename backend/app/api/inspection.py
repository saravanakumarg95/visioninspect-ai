import os
import cv2
import uuid
import json
import numpy as np
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import InspectionRecord
from app.schemas.inspection import InspectionResponse
from app.cv.preprocessing import analyze_image_quality
from app.calibration.aruco import detect_aruco_marker
from app.calibration.scale import calibrate_by_known_object
from app.cv.contours import extract_component_contours
from app.cv.circles import detect_circles_and_holes
from app.cv.geometry import analyze_component_geometry, calculate_hole_center_distances
from app.cv.perspective import rectify_perspective
from app.ai.detector import classify_mechanical_component
from app.ai.anomaly import inspect_visual_defects
from app.measurement.engine import run_measurement_engine
from app.standards.matcher import match_fastener_to_standards
from app.inspection.tolerance import evaluate_measurement_tolerances
from app.inspection.result import determine_inspection_verdict
from app.reports.generator import generate_pdf_report

router = APIRouter(prefix="/api", tags=["Inspection"])

UPLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../uploads"))
REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../reports"))
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

@router.post("/analyze/image", response_model=InspectionResponse)
async def analyze_image(
    file: UploadFile = File(...),
    side_file: Optional[UploadFile] = File(None),
    reference_size_mm: float = Form(50.0),
    calibration_method: str = Form("aruco"),
    component_name: Optional[str] = Form(None),
    part_number: Optional[str] = Form(None),
    operator_name: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Main image inspection endpoint. Executes complete CV metrology pipeline:
    Quality -> ArUco Calibration -> Segmentation -> Classification -> Geometry -> Measurements -> Defects -> Fastener Match -> 3-State Verdict -> Report.
    """
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Could not decode uploaded image.")

    inspection_id = f"INS-{datetime.utcnow().strftime('%Y')}-{uuid.uuid4().hex[:6].upper()}"

    # 1. Quality Analysis
    quality = analyze_image_quality(image)

    # 2. Calibration
    exclude_corners = None
    if calibration_method == "aruco":
        calibration, homography, exclude_corners = detect_aruco_marker(
            image, reference_size_mm=reference_size_mm
        )
    else:
        calibration = calibrate_by_known_object(image, custom_diameter_mm=reference_size_mm)
        homography = None

    # 3. Perspective Rectification (if homography matrix is present)
    rectified_img = rectify_perspective(image, homography) if homography is not None else image

    # 4. Extract Component Contour
    main_contour, all_contours, contour_meta = extract_component_contours(
        rectified_img, exclude_corners=exclude_corners
    )

    # 5. Detect Geometry & Circles
    circles_info = detect_circles_and_holes(rectified_img, main_contour, calibration.scale_px_per_mm)
    geometry_info = analyze_component_geometry(main_contour, calibration.scale_px_per_mm)
    hole_distances = calculate_hole_center_distances(
        [c for c in circles_info if c.get("type") == "hole"], calibration.scale_px_per_mm
    )

    # 6. Component Classification
    component_info = classify_mechanical_component(geometry_info, circles_info)

    # 7. Side View Processing (for 3D Thickness if provided)
    has_side_view = False
    side_geometry = None
    if side_file is not None:
        side_bytes = await side_file.read()
        side_nparr = np.frombuffer(side_bytes, np.uint8)
        side_img = cv2.imdecode(side_nparr, cv2.IMREAD_COLOR)
        if side_img is not None:
            side_cnt, _, _ = extract_component_contours(side_img)
            side_geometry = analyze_component_geometry(side_cnt, calibration.scale_px_per_mm)
            has_side_view = True

    # 8. Measurement Engine
    raw_measurements, uncertainty_breakdown, multiview_req, multiview_reason = run_measurement_engine(
        geometry_info=geometry_info,
        circles_info=circles_info,
        hole_distances=hole_distances,
        calibration=calibration,
        quality=quality,
        has_side_view=has_side_view,
        side_view_geometry=side_geometry
    )

    # 9. Evaluate Tolerances
    measurements = evaluate_measurement_tolerances(raw_measurements)

    # 10. Defect Inspection
    defects = inspect_visual_defects(
        image=rectified_img,
        contour=main_contour,
        detected_class=component_info.detected_class,
        circles_info=circles_info,
        geometry_info=geometry_info
    )

    # 11. Standards Matching (Fasteners)
    outer_diam = next((m.value for m in measurements if m.name == "Outer Diameter"), None)
    inner_diam = next((m.value for m in measurements if m.name == "Hole #1 Diameter"), None)

    fastener_match = match_fastener_to_standards(
        component_type=component_info.detected_class,
        measured_diameter_mm=outer_diam if outer_diam else (inner_diam if inner_diam else 10.0),
        measured_inner_diameter_mm=inner_diam
    )

    # 12. 3-State Verdict
    status = determine_inspection_verdict(
        quality=quality,
        calibration=calibration,
        component=component_info,
        measurements=measurements,
        defects=defects
    )

    # Save Uploaded Image File
    img_filename = f"{inspection_id}.jpg"
    img_filepath = os.path.join(UPLOADS_DIR, img_filename)
    cv2.imwrite(img_filepath, image)

    response = InspectionResponse(
        inspection_id=inspection_id,
        created_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        mode="photo",
        component=component_info,
        quality=quality,
        calibration=calibration,
        measurements=measurements,
        defects=defects,
        fastener=fastener_match,
        uncertainty=uncertainty_breakdown,
        status=status,
        multiview_required=multiview_req,
        multiview_reason=multiview_reason,
        views_captured=2 if has_side_view else 1,
        annotated_image_url=f"/api/uploads/{img_filename}",
        pdf_report_url=f"/api/reports/{inspection_id}.pdf"
    )

    # Generate PDF Report file safely
    try:
        pdf_path = os.path.join(REPORTS_DIR, f"{inspection_id}.pdf")
        generate_pdf_report(response, pdf_path)
    except Exception as e:
        print(f"Warning: PDF report generation failed: {e}")
        pdf_path = ""

    # Save Inspection Record in SQLite DB safely
    try:
        record = InspectionRecord(
            id=inspection_id,
            mode="photo",
            component_name=component_name,
            part_number=part_number,
            operator_name=operator_name,
            component_type=component_info.detected_class,
            status=status,
            readiness_score=quality.readiness_score,
            scale_px_per_mm=calibration.scale_px_per_mm,
            data_json=json.dumps(response.model_dump()),
            pdf_report_path=pdf_path
        )
        db.add(record)
        db.commit()
    except Exception as e:
        print(f"Warning: DB record insert failed: {e}")

    return response

@router.get("/inspections")
async def get_inspection_history(db: Session = Depends(get_db)):
    """
    Returns list of saved inspection records.
    """
    records = db.query(InspectionRecord).order_by(InspectionRecord.created_at.desc()).all()
    return [r.to_dict() for r in records]

@router.get("/inspections/{inspection_id}")
async def get_inspection_by_id(inspection_id: str, db: Session = Depends(get_db)):
    """
    Returns details for specific inspection.
    """
    record = db.query(InspectionRecord).filter(InspectionRecord.id == inspection_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Inspection record not found.")
    return record.to_dict()
