# VisionInspect AI — Engineering Metrology Documentation

## 1. Introduction & Physical Metrology Limitations
Smartphone camera metrology provides rapid non-contact automated component inspection. However, unlike coordinate measuring machines (CMM) or calibrated telecentric optical comparators, smartphone camera vision operates with standard perspective lenses, CMOS Bayer sensors, variable distance, and handheld perspective tilt. 

VisionInspect AI overcomes these physical challenges through automated ArUco reference calibration, sub-pixel edge detection, homography perspective transformation, candidate fastener matching, and Root-Sum-Square (RSS) measurement uncertainty modeling.

---

## 2. ArUco Calibration & Scale Estimation
Primary calibration uses OpenCV ArUco markers (default dictionary `DICT_4X4_50`, 50.0 mm reference size).

1. Corner sub-pixel refinement (`cv2.cornerSubPix`) locates all four marker corners with sub-pixel resolution.
2. Side lengths $s_0, s_1, s_2, s_3$ in pixels are computed.
3. Mean pixel scale factor $s_{\text{px/mm}}$:
   $$s_{\text{px/mm}} = \frac{s_{\text{mean}}}{D_{\text{known}}}$$
4. Calibration error percentage is derived from standard deviation across edges:
   $$E_{\text{cal}} = \frac{\sigma_{\text{side}}}{s_{\text{mean}}} \times 100\%$$

---

## 3. Perspective Rectification & Homography
When a planar component and reference marker are captured under camera tilt angle $\theta$, perspective distortion distorts square geometry into quadrilaterals.

VisionInspect AI computes a $3 \times 3$ Homography matrix $H$:
$$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = H \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$
Perspective rectification is applied via `cv2.warpPerspective` to obtain a perpendicular planar view before feature extraction.

---

## 4. Measurement Uncertainty Model
Measurement values are stated with estimated standard uncertainty:
$$y \pm u_{\text{combined}}$$

The combined measurement uncertainty is computed using Root-Sum-Square (RSS):
$$u_{\text{combined}} = \sqrt{u_{\text{cal}}^2 + u_{\text{persp}}^2 + u_{\text{edge}}^2 + u_{\text{temp}}^2}$$

Where:
- $u_{\text{cal}}$: Calibration reference error.
- $u_{\text{persp}}$: Tilt angle error derived from $(1 - \cos\theta)$.
- $u_{\text{edge}}$: Sub-pixel quantization error ($\pm 0.5 \text{ px} / s_{\text{px/mm}}$).
- $u_{\text{temp}}$: Multi-frame temporal variance over video streams.

---

## 5. Classical CV vs. AI Detector
- **AI Classification**: Fast rule-assisted & model component classification (`hex_bolt`, `nut`, `washer`, `plate`, `shaft`, `bracket`).
- **Classical OpenCV Metrology**: Sub-pixel contours, Hough circle transforms, fitEllipse, and minimum area rectangle fits ensure deterministic mathematical precision without AI hallucination.

---

## 6. Multi-View Reasoning Engine
Single top-down images cannot measure 3D height or thickness. If a single view is uploaded, thickness is flagged as `INSUFFICIENT DATA` and a side profile capture (`View 2`) is requested.

---

## 7. Reliable vs. Unreliable Conditions

### Reliable Conditions
- ArUco reference marker placed on the same focal plane as the component.
- Camera positioned near-perpendicular ($\le 15^\circ$ tilt).
- Sharp lighting with low specular reflection/glare.
- High-contrast background.

### Unreliable Conditions
- Severe camera tilt angle ($> 30^\circ$).
- Blurry focus (Laplacian variance $< 80$).
- Heavy direct glare masking component edges.
- Attempting 3D thickness measurement from a single 2D top-down view.
