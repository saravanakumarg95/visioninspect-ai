from typing import Optional, List
import os
import io
import cv2
import numpy as np
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from app.schemas.inspection import InspectionResponse

def generate_pdf_report(inspection: InspectionResponse, output_pdf_path: str, annotated_img_bytes: Optional[bytes] = None) -> str:
    """
    Generates a professional multi-page industrial metrology PDF inspection report.
    Returns: Absolute path to generated PDF file.
    """
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom Engineering Palette Colors
    primary_color = colors.HexColor("#0f172a")    # Slate 900
    accent_color = colors.HexColor("#0284c7")     # Sky 600
    pass_color = colors.HexColor("#16a34a")       # Green 600
    fail_color = colors.HexColor("#dc2626")       # Red 600
    review_color = colors.HexColor("#d97706")     # Amber 600
    bg_light = colors.HexColor("#f8fafc")

    status_bg = pass_color if inspection.status == "PASS" else (fail_color if inspection.status == "FAIL" else review_color)

    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=primary_color
    )
    subtitle_style = ParagraphStyle(
        "SubTitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#64748b")
    )
    section_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        "BodyText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#334155")
    )
    bold_style = ParagraphStyle(
        "BoldText",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=primary_color
    )

    story = []

    # 1. Header Banner
    header_data = [
        [
            Paragraph("<b>VISIONINSPECT AI</b><br/><font size=9 color='#64748b'>Industrial Metrology Inspection Report</font>", title_style),
            Paragraph(f"<font size=14 color='white'><b>{inspection.status}</b></font>", ParagraphStyle(
                "StatusBadge",
                alignment=1,
                fontName="Helvetica-Bold",
                textColor=colors.white,
                fontSize=14
            ))
        ]
    ]

    header_table = Table(header_data, colWidths=[380, 160])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (1, 0), (1, 0), status_bg),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('TOPPADDING', (1, 0), (1, 0), 10),
        ('BOTTOMPADDING', (1, 0), (1, 0), 10),
        ('ROUNDEDCORNERS', [4, 4, 4, 4])
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=12))

    # 2. Inspection Metadata Table
    meta_data = [
        [
            Paragraph("<b>Inspection ID:</b>", bold_style), Paragraph(inspection.inspection_id, body_style),
            Paragraph("<b>Date/Time:</b>", bold_style), Paragraph(inspection.created_at, body_style)
        ],
        [
            Paragraph("<b>Component Type:</b>", bold_style), Paragraph(f"{inspection.component.detected_class.upper()} ({int(inspection.component.confidence*100)}% AI Conf)", body_style),
            Paragraph("<b>Calibration:</b>", bold_style), Paragraph(f"{inspection.calibration.method.upper()} ({inspection.calibration.scale_px_per_mm:.2f} px/mm)", body_style)
        ],
        [
            Paragraph("<b>Mode:</b>", bold_style), Paragraph(inspection.mode.upper(), body_style),
            Paragraph("<b>Calibration Error:</b>", bold_style), Paragraph(f"{inspection.calibration.error_percent:.2f}%", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[110, 160, 110, 160])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_light),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # 3. Measurements Section
    story.append(Paragraph("Dimensional Measurements & Metrology", section_style))

    meas_rows = [["Feature", "Measured Value", "Uncertainty", "Confidence", "Source", "Status"]]
    for m in inspection.measurements:
        val_str = f"{m.value:.2f} {m.unit}" if m.value is not None else "INSUFFICIENT DATA"
        unc_str = f"±{m.uncertainty:.2f} {m.unit}" if m.value is not None else "-"
        meas_rows.append([
            m.name,
            val_str,
            unc_str,
            f"{int(m.confidence*100)}%",
            m.source,
            m.pass_fail
        ])

    meas_table = Table(meas_rows, colWidths=[130, 100, 80, 70, 90, 70])
    meas_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('ALIGN', (1, 0), (3, -1), 'CENTER'),
        ('ALIGN', (4, 0), (-1, -1), 'CENTER')
    ]))
    story.append(meas_table)
    story.append(Spacer(1, 12))

    # 4. Fastener Match & Defects Section
    if inspection.fastener and inspection.fastener.matched:
        story.append(Paragraph("Engineering Standards Candidate Match", section_style))
        fastener_text = (
            f"<b>Match:</b> {inspection.fastener.designation} ({inspection.fastener.standard}) | "
            f"<b>Nominal Diameter:</b> {inspection.fastener.nominal_diameter_mm} mm | "
            f"<b>Pitch:</b> {inspection.fastener.pitch_mm} mm | "
            f"<b>Confidence:</b> {int(inspection.fastener.confidence*100)}%"
        )
        story.append(Paragraph(fastener_text, body_style))
        story.append(Spacer(1, 10))

    # 5. Defect Analysis Section
    story.append(Paragraph("Visual Defect Inspection", section_style))
    if not inspection.defects:
        story.append(Paragraph("✓ No visual defects detected. Component surface and edge geometry satisfy inspection criteria.", body_style))
    else:
        defect_rows = [["Defect Type", "Severity", "Confidence", "Description"]]
        for d in inspection.defects:
            defect_rows.append([
                d.defect_type.replace("_", " ").title(),
                d.severity,
                f"{int(d.confidence*100)}%",
                d.description
            ])
        defect_table = Table(defect_rows, colWidths=[120, 70, 70, 280])
        defect_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#475569")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0, 0), (-1, -1), 5)
        ]))
        story.append(defect_table)

    story.append(Spacer(1, 12))

    # 6. Uncertainty Explanation & Metrology Notes
    story.append(Paragraph("Measurement Uncertainty Model & Limitations", section_style))
    unc_text = (
        f"<b>Combined Uncertainty:</b> ±{inspection.uncertainty.combined_uncertainty_mm:.2f} mm<br/>"
        f"<i>{inspection.uncertainty.explanation}</i><br/>"
        f"<b>Note:</b> Dimensional results are computed using ArUco reference scale calibration and planar homography perspective transformation. "
        f"Measurements are valid under controlled lighting and perpendicular camera alignment."
    )
    story.append(Paragraph(unc_text, body_style))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=10))

    # Footer Disclaimer & Signature
    footer_text = (
        "<b>VisionInspect AI Metrology Report</b> | Generated automatically by VisionInspect AI System.<br/>"
        "This report certifies automated computer vision analysis. For safety-critical aerospace/automotive parts, verify with calibrated physical gauges."
    )
    story.append(Paragraph(footer_text, ParagraphStyle("Footer", parent=styles["Normal"], fontSize=7, leading=9, textColor=colors.HexColor("#94a3b8"), alignment=1)))

    doc.build(story)
    return output_pdf_path
