import cv2
import numpy as np
from typing import List, Dict, Any
from app.schemas.inspection import DefectItem

def inspect_visual_defects(
    image: np.ndarray,
    contour: np.ndarray,
    detected_class: str,
    circles_info: List[Dict[str, Any]],
    geometry_info: Dict[str, Any]
) -> List[DefectItem]:
    """
    Detects visual mechanical defects:
    - Damaged/jagged edge roughness
    - Surface texture damage/scratch
    - Missing feature/hole anomaly
    """
    defects: List[DefectItem] = []
    if contour is None:
        return defects

    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # 1. Edge roughness / jaggedness (perimeter vs convex hull perimeter)
    perimeter = cv2.arcLength(contour, True)
    hull = cv2.convexHull(contour)
    hull_perimeter = cv2.arcLength(hull, True)

    roughness_ratio = (perimeter / max(1.0, hull_perimeter))
    if roughness_ratio > 1.25:
        defects.append(DefectItem(
            defect_type="damaged_edge",
            confidence=round(min(0.95, (roughness_ratio - 1.2) * 2.0), 2),
            severity="MEDIUM" if roughness_ratio < 1.4 else "HIGH",
            location_bbox=None,
            description=f"Irregular edge roughness detected (ratio: {roughness_ratio:.2f})."
        ))

    # 2. Surface scratch / texture anomaly inside component mask
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [contour], -1, 255, -1)
    mean_val, std_val = cv2.meanStdDev(gray, mask=mask)

    if float(std_val[0][0]) > 55.0:
        defects.append(DefectItem(
            defect_type="surface_scratch",
            confidence=round(min(0.90, (float(std_val[0][0]) - 50) / 40.0), 2),
            severity="LOW",
            location_bbox=None,
            description=f"High surface texture intensity variation (std: {std_val[0][0]:.1f})."
        ))

    # 3. Missing hole anomaly (e.g., Plate expecting >= 4 holes but observing fewer)
    if detected_class == "plate" and geometry_info.get("is_rectangular", False):
        hole_count = sum(1 for c in circles_info if c.get("type") == "hole")
        if hole_count == 3:
            defects.append(DefectItem(
                defect_type="missing_hole",
                confidence=0.88,
                severity="HIGH",
                location_bbox=None,
                description="Plate geometry indicates 4-hole pattern, but only 3 holes were detected (Hole #4 missing)."
            ))

    return defects
