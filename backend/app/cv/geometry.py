import cv2
import numpy as np
from typing import List, Dict, Any, Tuple

def analyze_component_geometry(
    contour: np.ndarray,
    scale_px_per_mm: float
) -> Dict[str, Any]:
    """
    Analyzes geometric shape of component contour:
    - Hexagon check (6 corners -> Hex Bolt head)
    - Rectangle check (4 corners -> Plate/Bracket)
    - Min area rectangle length and width
    - Convexity defects
    """
    if contour is None or len(contour) < 3:
        return {}

    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    num_corners = len(approx)

    rect = cv2.minAreaRect(contour)
    (cx, cy), (w, h), angle = rect
    length_px = float(max(w, h))
    width_px = float(min(w, h))

    length_mm = length_px / max(0.1, scale_px_per_mm)
    width_mm = width_px / max(0.1, scale_px_per_mm)

    is_hexagonal = num_corners in [5, 6, 7]
    is_rectangular = num_corners == 4

    return {
        "num_corners": num_corners,
        "is_hexagonal": is_hexagonal,
        "is_rectangular": is_rectangular,
        "length_px": length_px,
        "width_px": width_px,
        "length_mm": length_mm,
        "width_mm": width_mm,
        "centroid": [cx, cy],
        "approx_polygon": approx.reshape(-1, 2).tolist()
    }

def calculate_hole_center_distances(
    holes: List[Dict[str, Any]],
    scale_px_per_mm: float
) -> List[Dict[str, Any]]:
    """
    Calculates distances between detected hole centers.
    """
    distances = []
    n = len(holes)
    for i in range(n):
        for j in range(i + 1, n):
            c1 = holes[i]["center"]
            c2 = holes[j]["center"]
            dist_px = float(np.sqrt((c2[0] - c1[0])**2 + (c2[1] - c1[1])**2))
            dist_mm = dist_px / max(0.1, scale_px_per_mm)
            distances.append({
                "hole_index_1": i + 1,
                "hole_index_2": j + 1,
                "distance_px": dist_px,
                "distance_mm": dist_mm
            })
    return distances
