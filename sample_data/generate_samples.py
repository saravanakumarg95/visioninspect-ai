import os
import cv2
import numpy as np

def generate_aruco_marker(marker_id: int = 0, size_px: int = 200) -> np.ndarray:
    """Generates an ArUco marker image."""
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    try:
        marker_img = cv2.aruco.generateImageMarker(dictionary, marker_id, size_px)
    except AttributeError:
        marker_img = cv2.aruco.drawMarker(dictionary, marker_id, size_px)
    return marker_img

def create_sample_images():
    output_dir = os.path.abspath(os.path.dirname(__file__))
    os.makedirs(output_dir, exist_ok=True)

    canvas_w, canvas_h = 1000, 800
    # Scale: 1000px width represents 120mm -> scale ~ 8.33 px/mm
    scale = 8.0

    # 1. Draw ArUco 50mm Marker (50mm * 8 = 400px)
    aruco_size_px = int(50.0 * scale)
    aruco_img = generate_aruco_marker(0, aruco_size_px)
    aruco_bgr = cv2.cvtColor(aruco_img, cv2.COLOR_GRAY2BGR)

    # Base Canvas (Light Gray Engineering Tabletop)
    canvas = np.ones((canvas_h, canvas_w, 3), dtype=np.uint8) * 235

    # Place ArUco marker on top left (x=60, y=60)
    canvas[60:60+aruco_size_px, 60:60+aruco_size_px] = aruco_bgr

    # --- Sample 1: Hex Bolt (M10 x 50mm) ---
    bolt_canvas = canvas.copy()
    cx, cy = 600, 400

    # Draw Hexagonal Head (Across Flats 16mm = 128px)
    r_hex = int((16.0 * scale) / np.cos(np.pi / 6) / 2.0)
    hex_pts = []
    for i in range(6):
        angle = np.pi / 3 * i
        hx = int(cx + r_hex * np.cos(angle))
        hy = int(cy - 100 + r_hex * np.sin(angle))
        hex_pts.append([hx, hy])
    cv2.fillPoly(bolt_canvas, [np.array(hex_pts, dtype=np.int32)], (60, 60, 60))

    # Draw Shank (10mm diam = 80px, length 50mm = 400px)
    shank_w = int(10.0 * scale)
    shank_h = int(50.0 * scale)
    cv2.rectangle(bolt_canvas, (cx - shank_w//2, cy - 100), (cx + shank_w//2, cy - 100 + shank_h), (80, 80, 80), -1)

    cv2.imwrite(os.path.join(output_dir, "bolt_aruco.png"), bolt_canvas)

    # --- Sample 2: Washer (M10 Washer, Outer 20mm, Inner 10.5mm) ---
    washer_canvas = canvas.copy()
    cx, cy = 600, 400
    r_outer = int((20.0 * scale) / 2.0)
    r_inner = int((10.5 * scale) / 2.0)
    cv2.circle(washer_canvas, (cx, cy), r_outer, (90, 90, 90), -1)
    cv2.circle(washer_canvas, (cx, cy), r_inner, (235, 235, 235), -1)

    cv2.imwrite(os.path.join(output_dir, "washer_aruco.png"), washer_canvas)

    # --- Sample 3: 4-Hole Plate (80mm x 50mm, 4 holes spaced 40mm) ---
    plate_canvas = canvas.copy()
    pw = int(80.0 * scale)
    ph = int(50.0 * scale)
    px1, py1 = 500, 250
    cv2.rectangle(plate_canvas, (px1, py1), (px1 + pw, py1 + ph), (70, 70, 70), -1)

    # Holes: 6mm diameter (48px), spaced 40mm (320px) apart
    hr = int((6.0 * scale) / 2.0)
    holes_loc = [
        (px1 + 120, py1 + 100),
        (px1 + pw - 120, py1 + 100),
        (px1 + 120, py1 + ph - 100),
        (px1 + pw - 120, py1 + ph - 100)
    ]
    for hx, hy in holes_loc:
        cv2.circle(plate_canvas, (hx, hy), hr, (235, 235, 235), -1)

    cv2.imwrite(os.path.join(output_dir, "plate_aruco.png"), plate_canvas)

    print("Successfully generated realistic sample images in sample_data/")

if __name__ == "__main__":
    create_sample_images()
