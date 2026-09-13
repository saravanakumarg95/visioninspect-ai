# VisionInspect AI — AI-Powered Mechanical Vision Inspection & Measurement

**VisionInspect AI** is an industrial-grade, mobile-first full-stack web application designed to turn any smartphone or browser into a mechanical component inspection device.

---

## 🌟 Key Features

- 📱 **Mobile-First Smartphone Camera Interface**: HTML5 `getUserMedia` camera feed with rear environment camera preference, Photo capture, Video recording, and Live stream preview.
- 📐 **Automatic ArUco Reference Calibration**: Detects OpenCV ArUco markers (`DICT_4X4_50`, 50mm reference) with sub-pixel refinement, computing exact scale ($px/mm$), perspective homography matrix, and calibration error.
- 🔍 **Capture Quality Meter**: Evaluates Laplacian blur, mean exposure, glare percentage, object coverage, and perspective tilt prior to inspection.
- ⚙️ **Real Computer Vision Metrology**: Computes real outer/inner diameters, shank lengths, hole center-to-center distances, angles, and edge widths using sub-pixel contour fitting and Hough transforms.
- 🏷️ **Strict Source Labeling**: Every measurement displays transparent source badges: `DIRECT` (CV geometry), `AI ESTIMATED` (AI parameter), `DATABASE MATCH` (Standard table lookup), or `INSUFFICIENT DATA`.
- 📊 **Metrology Uncertainty Engine**: Calculates Root-Sum-Square (RSS) measurement uncertainty bounds ($\pm\text{mm}$) combining calibration, perspective tilt, edge quantization, and temporal variation.
- 🔩 **ISO Metric Standards Matching**: Matches observed component geometry against standard candidate tables (ISO 4014 / DIN 931 Hex Bolts, ISO 7089 Washers, M3–M24 pitch tables).
- 🚩 **Visual Defect Detection & 3-State Verdict**: Identifies edge roughness, surface anomalies, and missing holes, outputting **PASS**, **FAIL**, or **REVIEW**.
- 📑 **ReportLab PDF Generator**: Generates downloadable engineering metrology inspection reports with annotated images, measurement tables, defect breakdowns, and signature footers.

---

## 🛠️ Architecture & Tech Stack

```text
visioninspect-ai/
├── frontend/             # React 18 + Vite + TypeScript + Tailwind CSS
├── backend/              # Python 3.11 + FastAPI + OpenCV + ReportLab + SQLAlchemy
├── database/             # SQLite Local Database (visioninspect.db)
├── sample_data/          # Synthetic test image generator (ArUco 50mm + Bolt/Washer/Plate)
├── reports/              # Generated PDF metrology reports
└── tests/                # Automated pytest suite
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.11+
- Node.js v18+ & npm

### 1. Run Backend Server
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Backend API will be live at `http://localhost:8000` (Swagger UI at `http://localhost:8000/docs`).

### 2. Run Frontend Application
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser or smartphone.

---

## 🧪 Running Automated Tests

Run backend metrology tests:
```bash
cd backend
python -m pytest ../tests/
```

Run frontend build verification:
```bash
cd frontend
npm run build
```

---

## 🐋 Docker Setup

Run backend and frontend using Docker Compose:
```bash
docker-compose up --build
```

---

## 📄 License & Metrology Disclaimer
VisionInspect AI is provided for mechanical component inspection. Measurements are subject to stated uncertainty bounds ($\pm\text{mm}$) and physical camera alignment.
