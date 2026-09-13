from fastapi import APIRouter, Query, HTTPException
from app.standards.fasteners import search_fasteners_database
from app.standards.matcher import match_fastener_to_standards
from app.schemas.inspection import FastenerMatch

router = APIRouter(prefix="/api/standards", tags=["Standards & Fasteners"])

@router.get("/search")
async def search_standards(query: str = Query("", description="Query string e.g. M10, Washer")):
    """
    Searches ISO Metric fastener database.
    """
    results = search_fasteners_database(query)
    return {"query": query, "count": len(results), "items": results}

@router.post("/match", response_model=FastenerMatch)
async def match_fastener(
    component_type: str = Query("hex_bolt"),
    measured_diameter_mm: float = Query(10.0),
    measured_length_mm: float = Query(None),
    measured_inner_diameter_mm: float = Query(None)
):
    """
    Matches measured component dimensions against ISO Metric standard candidates.
    """
    match = match_fastener_to_standards(
        component_type=component_type,
        measured_diameter_mm=measured_diameter_mm,
        measured_length_mm=measured_length_mm,
        measured_inner_diameter_mm=measured_inner_diameter_mm
    )
    if not match:
        raise HTTPException(status_code=444, detail="No matching standard fastener candidate found.")
    return match
