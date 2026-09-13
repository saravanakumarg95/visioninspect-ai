from fastapi import APIRouter

router = APIRouter(prefix="/api/defects", tags=["Defects"])

@router.get("/types")
async def get_defect_types():
    return {
        "supported_defects": [
            "damaged_edge",
            "surface_scratch",
            "missing_hole",
            "deformation",
            "abnormal_geometry"
        ]
    }
