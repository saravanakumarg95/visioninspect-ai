import numpy as np
from typing import Dict, Any, Tuple
from app.schemas.inspection import ComponentInfo

SUPPORTED_CLASSES = [
    "hex_bolt", "nut", "screw", "washer", "shaft",
    "plate", "bracket", "gear", "flange", "machined_component", "unknown"
]

def classify_mechanical_component(
    geometry_info: Dict[str, Any],
    circles_info: list,
    confidence_threshold: float = 0.65
) -> ComponentInfo:
    """
    Identifies mechanical component type using geometry features, aspect ratio, polygon corners, and circle count.
    If confidence < threshold, returns 'unknown' component.
    """
    if not geometry_info:
        return ComponentInfo(
            detected_class="unknown",
            confidence=0.0,
            detection_method="Classical CV fallback",
            bounding_box=None
        )

    aspect_ratio = geometry_info.get("aspect_ratio", 1.0)
    is_hex = geometry_info.get("is_hexagonal", False)
    num_corners = geometry_info.get("num_corners", 0)
    length_mm = geometry_info.get("length_mm", 0.0)
    width_mm = geometry_info.get("width_mm", 0.0)

    has_outer_circle = any(c.get("type") == "outer_diameter" for c in circles_info)
    has_inner_hole = any(c.get("type") == "hole" for c in circles_info)
    hole_count = sum(1 for c in circles_info if c.get("type") == "hole")

    # Rule-based classification engine with confidence scoring
    detected_class = "unknown"
    confidence = 0.50

    # 1. Hex Bolt (Hexagonal head + elongated shank)
    if is_hex or (aspect_ratio >= 2.2 and num_corners >= 5):
        detected_class = "hex_bolt"
        confidence = 0.92 if is_hex else 0.81

    # 2. Washer (Circular outer + central hole + low thickness ratio)
    elif has_outer_circle and has_inner_hole and hole_count == 1 and aspect_ratio <= 1.3:
        detected_class = "washer"
        confidence = 0.94

    # 3. Nut (Hexagonal outer + central threaded hole)
    elif is_hex and has_inner_hole and aspect_ratio <= 1.4:
        detected_class = "nut"
        confidence = 0.91

    # 4. Plate / Bracket (Flat rectangular body with 1 or more holes)
    elif geometry_info.get("is_rectangular", False) or hole_count >= 2:
        detected_class = "plate" if hole_count > 0 else "bracket"
        confidence = 0.88

    # 5. Shaft / Rod (Elongated cylinder with circular cross section)
    elif has_outer_circle and aspect_ratio >= 2.5:
        detected_class = "shaft"
        confidence = 0.85

    # 6. Machined Component
    elif num_corners >= 4:
        detected_class = "machined_component"
        confidence = 0.72

    # Enforce threshold
    if confidence < confidence_threshold:
        return ComponentInfo(
            detected_class="unknown",
            confidence=round(confidence, 2),
            detection_method="Classical CV fallback",
            bounding_box=None
        )

    return ComponentInfo(
        detected_class=detected_class,
        confidence=round(confidence, 2),
        detection_method="Classical CV fallback",
        bounding_box=[
            geometry_info.get("centroid", [0, 0])[0] - width_mm/2,
            geometry_info.get("centroid", [0, 0])[1] - length_mm/2,
            width_mm,
            length_mm
        ]
    )
