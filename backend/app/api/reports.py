import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/api", tags=["Reports & Static Files"])

REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../reports"))
UPLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../uploads"))

@router.get("/reports/{filename}")
async def get_pdf_report(filename: str):
    """
    Serves generated inspection PDF report file.
    """
    filepath = os.path.join(REPORTS_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="PDF report file not found.")
    return FileResponse(filepath, media_type="application/pdf", filename=filename)

@router.get("/uploads/{filename}")
async def get_uploaded_image(filename: str):
    """
    Serves uploaded component image file.
    """
    filepath = os.path.join(UPLOADS_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Image file not found.")
    return FileResponse(filepath, media_type="image/jpeg")
