import cv2
import numpy as np
from typing import Tuple, Dict, Any
from app.schemas.calibration import QualityAnalysisResult

def analyze_image_quality(image: np.ndarray) -> QualityAnalysisResult:
    """
    Calculates image quality metrics:
    - Sharpness via Laplacian variance
    - Brightness mean & exposure check
    - Glare percentage (saturated highlights > 250)
    - Object coverage area ratio
    - Perspective angle estimate
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    height, width = gray.shape[:2]

    # 1. Blur / Sharpness
    laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    is_sharp = laplacian_var >= 80.0

    # 2. Brightness
    brightness_mean = float(np.mean(gray))
    is_well_lit = 50.0 <= brightness_mean <= 220.0

    # 3. Glare
    saturated_pixels = np.sum(gray >= 250)
    glare_percent = float((saturated_pixels / (height * width)) * 100.0)
    is_low_glare = glare_percent <= 5.0

    # 4. Object coverage via simple foreground thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    fg_pixels = np.sum(thresh > 0)
    coverage_percent = float((fg_pixels / (height * width)) * 100.0)
    is_adequate_size = 5.0 <= coverage_percent <= 85.0

    # 5. Perspective angle estimate (ratio of aspect ratios of convex hull)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    perspective_angle_deg = 0.0
    is_perpendicular = True

    if contours:
        largest = max(contours, key=cv2.contourArea)
        if len(largest) >= 5:
            rect = cv2.minAreaRect(largest)
            box = cv2.boxPoints(rect)
            # check ratio of edge lengths vs bounding box
            hull = cv2.convexHull(largest)
            hull_area = cv2.contourArea(hull)
            rect_area = rect[1][0] * rect[1][1]
            if rect_area > 0:
                solidity = hull_area / rect_area
                # estimate tilt angle
                perspective_angle_deg = float(abs(1.0 - solidity) * 45.0)
                is_perpendicular = perspective_angle_deg <= 15.0

    # Calculate overall readiness score (0-100)
    score = 0.0
    recommendations = []

    if is_sharp:
        score += 30.0
    else:
        recommendations.append("Image is blurry. Hold camera steady or move closer.")

    if is_well_lit:
        score += 25.0
    else:
        recommendations.append("Lighting is suboptimal. Adjust environment lighting.")

    if is_low_glare:
        score += 20.0
    else:
        recommendations.append("Glare detected. Reduce direct light reflection.")

    if is_adequate_size:
        score += 15.0
    else:
        recommendations.append("Component size is too small or too large in frame.")

    if is_perpendicular:
        score += 10.0
    else:
        recommendations.append("Hold camera directly perpendicular above component.")

    return QualityAnalysisResult(
        sharpness_laplacian=round(laplacian_var, 2),
        is_sharp=is_sharp,
        brightness_mean=round(brightness_mean, 2),
        is_well_lit=is_well_lit,
        glare_percent=round(glare_percent, 2),
        is_low_glare=is_low_glare,
        object_coverage_percent=round(coverage_percent, 2),
        is_adequate_size=is_adequate_size,
        perspective_angle_deg=round(perspective_angle_deg, 2),
        is_perpendicular=is_perpendicular,
        readiness_score=round(score, 1),
        recommendations=recommendations
    )
