import json
from sqlalchemy import Column, String, Float, Integer, DateTime, Text
from datetime import datetime
from .database import Base

class InspectionRecord(Base):
    __tablename__ = "inspections"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    mode = Column(String, default="photo")
    component_name = Column(String, nullable=True)
    part_number = Column(String, nullable=True)
    operator_name = Column(String, nullable=True)
    component_type = Column(String, default="unknown")
    status = Column(String, default="REVIEW")
    readiness_score = Column(Float, default=0.0)
    scale_px_per_mm = Column(Float, default=1.0)
    data_json = Column(Text, default="{}")
    pdf_report_path = Column(String, nullable=True)

    def to_dict(self):
        return {
            "inspection_id": self.id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "mode": self.mode,
            "component_name": self.component_name,
            "part_number": self.part_number,
            "operator_name": self.operator_name,
            "component_type": self.component_type,
            "status": self.status,
            "readiness_score": self.readiness_score,
            "scale_px_per_mm": self.scale_px_per_mm,
            "data": json.loads(self.data_json) if self.data_json else {},
            "pdf_report_path": self.pdf_report_path
        }
