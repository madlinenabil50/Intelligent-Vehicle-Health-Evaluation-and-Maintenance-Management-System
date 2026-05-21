import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth

DEFAULT_OUTPUT_DIR = "Desktop/Certificates/"


def _sanitize_text(value):
    return re.sub(r'[\\/*?:"<>|]', '', str(value)).strip()


def _health_status(health_score):
    score = max(0.0, min(100.0, float(health_score)))
    if score >= 80:
        return "Excellent Condition", colors.green
    if score >= 60:
        return "Good Condition", colors.darkgoldenrod
    if score >= 40:
        return "Needs Attention", colors.orange
    return "Critical Condition", colors.red


def _draw_border(canvas, doc):
    canvas.saveState()
    width, height = A4
    margin = 0.5 * mm
    canvas.setStrokeColor(colors.darkblue)
    canvas.setLineWidth(2)
    canvas.rect(margin, margin, width - 2 * margin, height - 2 * margin, stroke=1, fill=0)
    canvas.restoreState()


def _build_certificate_pdf(truck_id, health_score, fleet_id="N/A", output_dir=DEFAULT_OUTPUT_DIR, certificate_date=None):
    """
    Build and save a professional A4 PDF health certificate for a fleet truck.

    Args:
        truck_id (str): Truck identifier
        health_score (float): Computed health score between 0 and 100
        output_dir (str): Directory to save the PDF file
        certificate_date (str, optional): Certificate date text
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, output_dir)
    os.makedirs(output_dir, exist_ok=True)

    truck_id_clean = _sanitize_text(truck_id).replace(' ', '_')
    date_text = certificate_date or datetime.now().strftime("%B %d, %Y")
    score = max(0.0, min(100.0, float(health_score)))
    status_text, status_color = _health_status(score)

    if score >= 80:
        description = "This vehicle has passed all health parameters and is fully operational. No immediate maintenance action required."
        status_dot = colors.HexColor("#25A862")
    elif score >= 60:
        description = "The vehicle is operating well but should be monitored for upcoming maintenance."
        status_dot = colors.HexColor("#25A862")
    elif score >= 40:
        description = "The vehicle shows signs of wear and needs scheduled maintenance soon."
        status_dot = colors.HexColor("#D4793B")
    else:
        description = "Critical issues detected; immediate maintenance is required to avoid failure."
        status_dot = colors.HexColor("#B03A2E")

    year_token = date_text.split()[-1] if date_text else datetime.now().strftime("%Y")
    document_id = f"CERT-{year_token}-{truck_id_clean}"

    filename = f"Truck_{truck_id_clean}_Health_Certificate.pdf"
    filepath = os.path.join(output_dir, filename)

    page_width, page_height = A4
    c = canvas.Canvas(filepath, pagesize=A4)

    bg_color = colors.HexColor("#F9F6EF")
    primary = colors.HexColor("#0B1F3A")
    accent = colors.HexColor("#C9A84C")
    success = colors.HexColor("#25A862")
    gray_text = colors.HexColor("#8A9BB0")
    border_color = colors.HexColor("#D4C5A0")
    white = colors.HexColor("#FFFFFF")

    c.setFillColor(bg_color)
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    outer_margin = 32
    frame_x = outer_margin
    frame_y = outer_margin
    frame_w = page_width - outer_margin * 2
    frame_h = page_height - outer_margin * 2

    c.setStrokeColor(accent)
    c.setLineWidth(4)
    c.roundRect(frame_x, frame_y, frame_w, frame_h, 18, stroke=1, fill=0)

    c.setStrokeColor(border_color)
    c.setLineWidth(1.5)
    c.roundRect(frame_x + 10, frame_y + 10, frame_w - 20, frame_h - 20, 14, stroke=1, fill=0)

    accent_len = 22
    accent_thick = 4
    for x_pos, y_pos, horiz_dir, vert_dir in [
        (frame_x + 10, frame_y + 10, 1, 1),
        (frame_x + frame_w - 10, frame_y + 10, -1, 1),
        (frame_x + 10, frame_y + frame_h - 10, 1, -1),
        (frame_x + frame_w - 10, frame_y + frame_h - 10, -1, -1),
    ]:
        c.setStrokeColor(accent)
        c.setLineWidth(accent_thick)
        c.line(x_pos, y_pos, x_pos + horiz_dir * accent_len, y_pos)
        c.line(x_pos, y_pos, x_pos, y_pos + vert_dir * accent_len)

    header_top = frame_y + frame_h - 40
    box_size = 46
    box_x = frame_x + 28
    logo_text = "VHEMMS"
    logo_font = "Helvetica-Bold"
    logo_font_size = 18
    logo_width = max(box_size, stringWidth(logo_text, logo_font, logo_font_size) + 18)

    box_y = header_top - box_size
    c.setFillColor(primary)
    c.roundRect(box_x, box_y, logo_width, box_size, 10, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(logo_font, logo_font_size)
    c.drawCentredString(box_x + logo_width / 2, box_y + box_size / 2 - 6, logo_text)

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(primary)
    title_x = box_x + logo_width + 18
    text_y = box_y + box_size - 2
    c.drawString(title_x, text_y, " Vehicle Health")
    c.drawString(title_x, text_y - 18, "Evaluation and Maintenance")
    c.drawString(title_x, text_y - 36, "Management System")
    c.setFont("Helvetica", 9)
    c.setFillColor(gray_text)
    c.drawString(title_x, text_y - 54, "CERTIFIED VEHICLE ASSESSMENT PROGRAM")

    right_x = frame_x + frame_w - 180
    c.setFillColor(gray_text)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(right_x, text_y + 4, "ISSUED ON")
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(primary)
    c.drawString(right_x, text_y - 16, date_text)

    badge_width = 110
    badge_height = 22
    badge_x = right_x
    badge_y = text_y - 46
    c.setFillColor(accent)
    c.roundRect(badge_x, badge_y, badge_width, badge_height, badge_height / 2, fill=1, stroke=0)
    c.setFillColor(primary)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(badge_x + badge_width / 2, badge_y + 6, "✓ VERIFIED")

    divider_y = box_y - 18
    c.setStrokeColor(border_color)
    c.setLineWidth(1)
    c.line(frame_x + 28, divider_y, frame_x + frame_w - 28, divider_y)

    title_y = divider_y - 40
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(accent)
    c.drawCentredString(page_width / 2, title_y, "OFFICIAL DOCUMENT")
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(primary)
    c.drawCentredString(page_width / 2, title_y - 28, "Vehicle Health Certificate")

    caption_y = title_y - 54
    caption_text = "This certificate verifies the current health status of the selected  vehicle"
    caption_width = stringWidth(caption_text, "Helvetica-Oblique", 9)
    line_margin = 24
    c.setStrokeColor(border_color)
    c.setLineWidth(1)
    c.line((page_width - caption_width) / 2 - line_margin, caption_y + 5, (page_width - caption_width) / 2 - 6, caption_y + 5)
    c.line((page_width + caption_width) / 2 + 6, caption_y + 5, (page_width + caption_width) / 2 + line_margin, caption_y + 5)
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(gray_text)
    c.drawCentredString(page_width / 2, caption_y - 7, caption_text)

    card_y_top = caption_y - 90
    card_height = 70
    card_gap = 14
    card_width = (frame_w - 56 - card_gap) / 2
    card_left = frame_x + 28
    card_values = [
        ("TRUCK ID", _sanitize_text(truck_id)),
        ("CERTIFICATE DATE", date_text),
    ]
    for idx, (label, value) in enumerate(card_values):
        x = card_left + idx * (card_width + card_gap)
        c.setFillColor(white)
        c.roundRect(x, card_y_top - card_height, card_width, card_height, 10, fill=1, stroke=1)
        c.setStrokeColor(border_color)
        c.setLineWidth(1)
        c.roundRect(x, card_y_top - card_height, card_width, card_height, 10, fill=0, stroke=1)
        c.setFillColor(accent)
        c.rect(x, card_y_top - 4, card_width, 4, fill=1, stroke=0)
        c.setFont("Helvetica", 7)
        c.setFillColor(gray_text)
        c.drawString(x + 10, card_y_top - 22, label)
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(primary)
        c.drawString(x + 10, card_y_top - 44, value)

    score_band_top = card_y_top - card_height - 28
    band_height = 124
    band_left = frame_x + 28
    band_width = frame_w - 56
    c.setFillColor(primary)
    c.roundRect(band_left, score_band_top - band_height, band_width, band_height, 14, fill=1, stroke=0)

    circle_center_x = band_left + 86
    circle_center_y = score_band_top - band_height / 2
    circle_radius = 42
    ring_width = 12
    c.setStrokeColor(colors.HexColor("#D9D9D9"))
    c.setLineWidth(ring_width)
    c.circle(circle_center_x, circle_center_y, circle_radius, stroke=1, fill=0)
    c.setStrokeColor(success if score >= 80 else status_dot)
    c.setLineWidth(ring_width)
    span = 360 * (score / 100.0)
    start_angle = 90
    c.arc(circle_center_x - circle_radius, circle_center_y - circle_radius, circle_center_x + circle_radius, circle_center_y + circle_radius, start_angle, start_angle - span)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(circle_center_x, circle_center_y + 4, f"{score:.1f}")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.75))
    c.drawCentredString(circle_center_x, circle_center_y - 18, "/ 100")

    detail_x = circle_center_x + circle_radius + 28
    detail_y = circle_center_y + 22
    c.setFillColor(success if score >= 80 else status_dot)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(detail_x, detail_y, "● OPERATIONAL STATUS")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(detail_x, detail_y - 24, status_text)
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.85))
    description_lines = [line.strip() for line in description.split('. ') if line.strip()]
    for idx, line in enumerate(description_lines):
        c.drawString(detail_x, detail_y - 44 - idx * 16, line + ('.' if not line.endswith('.') else ''))

    score_label_y = score_band_top - band_height - 28
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(gray_text)
    c.drawString(band_left, score_label_y, "HEALTH SCORE RANGE")

    bar_y = score_label_y - 26
    bar_height = 18
    segments = [0.4, 0.2, 0.2, 0.2]
    segment_colors = [colors.HexColor("#B03A2E"), colors.HexColor("#D4793B"), colors.HexColor("#7DB87A"), colors.HexColor("#1E8A4A")]
    current_x = band_left
    for seg, seg_color in zip(segments, segment_colors):
        seg_w = band_width * seg
        c.setFillColor(seg_color)
        c.rect(current_x, bar_y, seg_w, bar_height, fill=1, stroke=0)
        current_x += seg_w

    pointer_x = band_left + band_width * (score / 100.0)
    c.setFillColor(white)
    c.setStrokeColor(primary)
    c.setLineWidth(1.5)
    c.rect(pointer_x - 3, bar_y + bar_height, 6, 24, fill=1, stroke=1)
    c.circle(pointer_x, bar_y + bar_height + 24, 4, fill=1, stroke=1)

    numbers = [0, 40, 60, 80, 100]
    for value in numbers:
        x = band_left + band_width * (value / 100.0)
        c.setFillColor(gray_text)
        c.setFont("Helvetica", 8)
        c.drawCentredString(x, bar_y - 14, str(value))

    footer_y = bar_y - 58
    c.setStrokeColor(border_color)
    c.setLineWidth(1)
    c.line(frame_x + 28, footer_y + 22, frame_x + frame_w - 28, footer_y + 22)

    sig_left_x = frame_x + 40
    sig_center_x = page_width / 2 - 80
    sig_right_x = frame_x + frame_w - 180
    sig_line_y = footer_y
    line_length = 150

    c.setStrokeColor(primary)
    c.setLineWidth(1)
    c.line(sig_left_x, sig_line_y, sig_left_x + line_length, sig_line_y)
    c.line(sig_center_x, sig_line_y, sig_center_x + line_length, sig_line_y)

    c.setFont("Helvetica", 8)
    c.setFillColor(gray_text)
    c.drawString(sig_left_x, sig_line_y - 16, "AUTHORIZED SIGNATURE")
    c.drawString(sig_center_x, sig_line_y - 16, "Vehicle Monitoring Center")

    c.setFillColor(primary)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(sig_right_x, sig_line_y + 6, document_id)
    c.setFillColor(gray_text)
    c.setFont("Helvetica", 8)
    c.drawString(sig_right_x, sig_line_y - 10, "Document ID · Confidential")

    c.showPage()
    c.save()
    print(f"Certificate generated: {filepath}")
    return filepath


def generate_certificate(truck_id, health_score, fleet_id="N/A", certificate_date=None):
    """Generate a certificate with the required user-facing signature."""
    return _build_certificate_pdf(truck_id, health_score, fleet_id=fleet_id, certificate_date=certificate_date)


def generate_certificates_batch(predictions, output_dir=DEFAULT_OUTPUT_DIR):
    """
    Generate one certificate PDF per truck in the input list.

    Args:
        predictions (list of tuples): List of (truck_id, health_score)
        output_dir (str): Directory to save PDFs
    """
    for item in predictions:
        if len(item) == 3:
            truck_id, health_score, fleet_id = item
            _build_certificate_pdf(truck_id, health_score, fleet_id=fleet_id, output_dir=output_dir)
        else:
            truck_id, health_score = item
            _build_certificate_pdf(truck_id, health_score, output_dir=output_dir)


if __name__ == "__main__":
    sample_predictions = [
        ("Truck_001", 85.5),
        ("Truck_002", 65.2),
        ("Truck_003", 35.8),
    ]
    generate_certificates_batch(sample_predictions)
