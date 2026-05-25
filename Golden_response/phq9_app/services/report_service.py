"""
PDF report generation using ReportLab.

Produces a clean, printable, professional single-page wellness report.
"""

import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)


# ─────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────
TEAL     = colors.HexColor("#2A7F7F")
SOFT_BG  = colors.HexColor("#F4F9F9")
DARK     = colors.HexColor("#1C2B2B")
MUTED    = colors.HexColor("#607070")
ACCENT   = colors.HexColor("#5BAD9A")
WARN     = colors.HexColor("#D4704A")
LIGHT_HR = colors.HexColor("#CCDEDE")


SEVERITY_COLORS = {
    "Minimal":            colors.HexColor("#4CAF82"),
    "Mild":               colors.HexColor("#8BC34A"),
    "Moderate":           colors.HexColor("#FFC107"),
    "Moderately Severe":  colors.HexColor("#FF9800"),
    "Severe":             colors.HexColor("#F44336"),
}


def _styles() -> dict:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ReportTitle",
            fontSize=22,
            textColor=TEAL,
            spaceAfter=2,
            fontName="Helvetica-Bold",
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            fontSize=10,
            textColor=MUTED,
            spaceAfter=10,
            fontName="Helvetica",
        ),
        "section": ParagraphStyle(
            "Section",
            fontSize=12,
            textColor=TEAL,
            spaceBefore=14,
            spaceAfter=4,
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "Body",
            fontSize=10,
            textColor=DARK,
            spaceAfter=4,
            fontName="Helvetica",
            leading=15,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            fontSize=10,
            textColor=DARK,
            spaceAfter=3,
            fontName="Helvetica",
            leftIndent=14,
            bulletIndent=4,
            leading=14,
        ),
        "disclaimer": ParagraphStyle(
            "Disclaimer",
            fontSize=8,
            textColor=MUTED,
            fontName="Helvetica-Oblique",
            spaceAfter=6,
            leading=11,
        ),
    }


def generate_pdf(result: dict) -> bytes:
    """
    Generate a PDF report from a prediction result dict.

    Parameters
    ----------
    result : dict
        Keys: phq_score, severity, confidence, explanation, suggestions

    Returns
    -------
    bytes  PDF file content
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    s = _styles()
    story = []

    # ── Header ──────────────────────────────────
    story.append(Paragraph("PHQ-9 Wellness Assessment", s["title"]))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%A, %d %B %Y at %H:%M')}  •  Educational Awareness Tool",
        s["subtitle"],
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=10))

    # ── Score Summary Table ──────────────────────
    severity = result.get("severity", "—")
    phq_score = result.get("phq_score", "—")
    confidence_pct = int(result.get("confidence", 0) * 100)
    sev_color = SEVERITY_COLORS.get(severity, ACCENT)

    summary_data = [
        [
            Paragraph("Estimated PHQ Score", s["body"]),
            Paragraph("Severity Level", s["body"]),
            Paragraph("Model Confidence", s["body"]),
        ],
        [
            Paragraph(f"<b>{phq_score} / 27</b>", ParagraphStyle(
                "Big", fontSize=18, textColor=DARK, fontName="Helvetica-Bold"
            )),
            Paragraph(f"<b>{severity}</b>", ParagraphStyle(
                "BigSev", fontSize=16, textColor=sev_color, fontName="Helvetica-Bold"
            )),
            Paragraph(f"<b>{confidence_pct}%</b>", ParagraphStyle(
                "BigConf", fontSize=18, textColor=TEAL, fontName="Helvetica-Bold"
            )),
        ],
    ]

    summary_table = Table(summary_data, colWidths=["33%", "34%", "33%"])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), SOFT_BG),
        ("BACKGROUND",   (0, 1), (-1, 1), colors.white),
        ("BOX",          (0, 0), (-1, -1), 1, LIGHT_HR),
        ("INNERGRID",    (0, 0), (-1, -1), 0.5, LIGHT_HR),
        ("TOPPADDING",   (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 8),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 8))

    # ── Risk Summary ─────────────────────────────
    story.append(Paragraph("About Your Score", s["section"]))
    risk_text = _risk_summary(phq_score, severity)
    story.append(Paragraph(risk_text, s["body"]))

    # ── Key Factors ──────────────────────────────
    explanation = result.get("explanation", [])
    if explanation:
        story.append(Paragraph("Key Factors in This Estimate", s["section"]))
        story.append(Paragraph(
            "The following areas had the most influence on your estimated score. "
            "These are not judgements — they are observations based on your responses.",
            s["body"],
        ))
        for item in explanation:
            arrow = "↑" if item["direction"] == "increased" else "↓"
            story.append(Paragraph(
                f"• {arrow} <b>{item['label']}</b>: {item['explanation']}",
                s["bullet"],
            ))

    # ── Suggestions ──────────────────────────────
    suggestions = result.get("suggestions", [])
    if suggestions:
        story.append(Paragraph("Supportive Suggestions", s["section"]))
        for sug in suggestions:
            story.append(Paragraph(f"• {sug}", s["bullet"]))

    # ── Separator ────────────────────────────────
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=0.8, color=LIGHT_HR))
    story.append(Spacer(1, 6))

    # ── Disclaimer ───────────────────────────────
    story.append(Paragraph(
        "<b>Important Disclaimer:</b> This report is generated by an AI-based educational awareness tool "
        "and does <b>not</b> constitute a medical diagnosis, clinical assessment, or professional mental health advice. "
        "PHQ-9 scores and severity labels are estimates based on self-reported responses and a machine learning model trained "
        "on population data. Individual results may vary. If you are experiencing emotional distress, please speak with "
        "a qualified mental health professional, counsellor, or your GP.",
        s["disclaimer"],
    ))
    story.append(Paragraph(
        "If you are in crisis or need immediate support, please contact a mental health helpline in your region.",
        s["disclaimer"],
    ))

    doc.build(story)
    return buffer.getvalue()


def _risk_summary(score, severity: str) -> str:
    """Return a supportive narrative based on severity."""
    summaries = {
        "Minimal": (
            "Your responses suggest minimal emotional distress at this time. This is a positive sign. "
            "Continuing self-care routines, maintaining social connections, and staying active can support ongoing wellbeing."
        ),
        "Mild": (
            "Your responses indicate mild levels of emotional distress. Many people experience this during periods of change or stress. "
            "Practising self-care, reaching out to supportive people, and being kind to yourself are all valuable steps."
        ),
        "Moderate": (
            "Your responses suggest a moderate level of distress. It may be helpful to speak with someone you trust, "
            "or to consider consulting a counsellor or mental health professional for personalised support."
        ),
        "Moderately Severe": (
            "Your responses suggest a moderately severe level of distress. We encourage you to speak with a mental health professional "
            "or your GP soon. You deserve support, and asking for help is a sign of strength."
        ),
        "Severe": (
            "Your responses suggest a significant level of distress. Please consider reaching out to a qualified mental health professional, "
            "counsellor, or your GP as soon as possible. You are not alone, and support is available."
        ),
    }
    return summaries.get(severity, "Your wellbeing matters. Please seek support from someone you trust.")
