import cv2
import numpy as np
from typing import List, Dict, Any, Tuple

def detect_circles_and_holes(
    image: np.ndarray,
    component_contour: np.ndarray,
    scale_px_per_mm: float
) -> List[Dict[str, Any]]:
    """
    Detects circular features, outer rims, washer diameters, and inner holes.
    Combines HoughCircles and Ellipse fitting on child contours.
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    results = []

    # 1. Circle fit on main component contour if circular
    if component_contour is not None and len(component_contour) >= 5:
        (cx, cy), radius = cv2.minEnclosingCircle(component_contour)
        ellipse = cv2.fitEllipse(component_contour)
        (ecx, ecy), (d1, d2), eangle = ellipse

        # Check circularity: ratio of area to perimeter squared
        area = cv2.contourArea(component_contour)
        perimeter = cv2.arcLength(component_contour, True)
        circularity = (4 * np.pi * area) / (perimeter**2) if perimeter > 0 else 0.0

        if circularity >= 0.70 or abs(d1 - d2) / max(d1, d2) <= 0.25:
            mean_d_px = (d1 + d2) / 2.0
            diameter_mm = mean_d_px / max(0.1, scale_px_per_mm)
            results.append({
                "type": "outer_diameter",
                "center": [ecx, ecy],
                "diameter_px": mean_d_px,
                "diameter_mm": diameter_mm,
                "circularity": circularity,
                "confidence": round(min(0.98, circularity + 0.1), 2)
            })

    # 2. Detect internal holes via contour hierarchy or HoughCircles inside bounding box
    mask = np.zeros_like(gray)
    if component_contour is not None:
        cv2.drawContours(mask, [component_contour], -1, 255, -1)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=20,
        param1=80,
        param2=25,
        minRadius=5,
        maxRadius=int(min(gray.shape) / 3)
    )

    if circles is not None:
        for circle in circles[0, :]:
            cx, cy, r_px = float(circle[0]), float(circle[1]), float(circle[2])
            # Ensure circle center is inside component mask
            if mask[int(clamp(cy, 0, gray.shape[0]-1)), int(clamp(cx, 0, gray.shape[1]-1))] > 0:
                d_px = 2.0 * r_px
                d_mm = d_px / max(0.1, scale_px_per_mm)
                # Check if this circle isn't duplicate of outer diameter
                if not any(abs(r["diameter_px"] - d_px) < 10 for r in results):
                    results.append({
                        "type": "hole",
                        "center": [cx, cy],
                        "radius_px": r_px,
                        "diameter_px": d_px,
                        "diameter_mm": d_mm,
                        "confidence": 0.88
                    })

    return results

def clamp(n, minn, maxn):
    return max(minn, min(n, maxn))
