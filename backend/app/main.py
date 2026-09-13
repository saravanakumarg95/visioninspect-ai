import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.api import camera, calibration, inspection, fasteners, reports, measurement, defects

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VisionInspect AI Backend API",
    description="AI-Powered Mechanical Vision Inspection & Metrology API",
    version="1.0.0"
)

# Enable CORS for Mobile & Web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(camera.router)
app.include_router(calibration.router)
app.include_router(inspection.router)
app.include_router(fasteners.router)
app.include_router(reports.router)
app.include_router(measurement.router)
app.include_router(defects.router)

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "VisionInspect AI API",
        "metrology_engine": "active",
        "cv2_aruco": "enabled"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
