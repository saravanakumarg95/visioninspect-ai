import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_image_inspection_endpoint():
    sample_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../sample_data/bolt_aruco.png"))
    assert os.path.exists(sample_path), f"Sample image does not exist at {sample_path}"

    with open(sample_path, "rb") as f:
        response = client.post(
            "/api/analyze/image",
            files={"file": ("bolt_aruco.png", f, "image/png")},
            data={
                "reference_size_mm": "50.0",
                "calibration_method": "aruco",
                "component_name": "M10 Hex Bolt Test"
            }
        )

    assert response.status_code == 200
    data = response.json()
    assert "inspection_id" in data
    assert data["calibration"]["calibrated"] is True
    assert data["status"] in ["PASS", "FAIL", "REVIEW"]
    assert len(data["measurements"]) > 0
