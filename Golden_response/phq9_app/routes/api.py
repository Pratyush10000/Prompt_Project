"""
Flask route handlers — prediction API and PDF download.
"""

from flask import Blueprint, request, jsonify, send_file
import io

from utils.preprocessing import validate_payload
from services.prediction_service import predict
from services.report_service import generate_pdf

bp = Blueprint("api", __name__)


@bp.route("/predict", methods=["POST"])
def predict_route():
    """
    POST /predict
    Body: JSON with phq1–phq9, age, gender, sleep_quality, study_pressure, financial_pressure
    Returns: JSON result with phq_score, severity, confidence, explanation, suggestions
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body."}), 400

    errors = validate_payload(data)
    if errors:
        return jsonify({"error": "Validation failed.", "details": errors}), 422

    try:
        result = predict(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": "Prediction failed.", "details": str(e)}), 500


@bp.route("/report", methods=["POST"])
def report_route():
    """
    POST /report
    Body: same JSON as /predict — runs prediction and returns a PDF report.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body."}), 400

    errors = validate_payload(data)
    if errors:
        return jsonify({"error": "Validation failed.", "details": errors}), 422

    try:
        result = predict(data)
        pdf_bytes = generate_pdf(result)
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="phq9_wellness_report.pdf",
        )
    except Exception as e:
        return jsonify({"error": "Report generation failed.", "details": str(e)}), 500
