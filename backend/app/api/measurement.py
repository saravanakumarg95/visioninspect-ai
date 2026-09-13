from fastapi import APIRouter

router = APIRouter(prefix="/api/measurement", tags=["Measurement Engine"])

@router.get("/info")
async def measurement_info():
    return {
        "engine": "VisionInspect Metrology Engine v1.0",
        "supported_units": ["mm", "deg"],
        "supported_features": ["outer_diameter", "inner_diameter", "hole_distance", "length", "width", "angle", "thickness"]
    }
