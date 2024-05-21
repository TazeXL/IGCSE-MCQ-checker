import os
import time
import re
import webbrowser
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib import colors

def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9_\-\. ]', '', filename)

def create_report_pdf(total_marks_obtained, total_marks_possible, incorrect_answers, subject_name, syllabus_code, paper_code, variant, year):
    # Ensure default values if any are None
    subject_name = subject_name or "Subject"
    syllabus_code = syllabus_code or "SyllabusCode"
    paper_code = paper_code or "PaperCode"
    variant = variant or "Variant"
    year = year or "Year"

    # Generate a unique filename using timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_name = f"{subject_name} {year} {variant} {paper_code} checked {timestamp}.pdf"
    sanitized_file_name = sanitize_filename(file_name)
    directory = os.path.dirname(__file__)  # Get the current script directory
    file_path = os.path.join(directory, sanitized_file_name)

    print(f"PDF file path: {file_path}")

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    centered_style = ParagraphStyle(
        name="Centered",
        alignment=TA_CENTER,
        fontSize=14,
        leading=16,
        fontName='Helvetica-Bold',
    )
    right_aligned_style = ParagraphStyle(
        name="RightAligned",
        alignment=TA_RIGHT,
        fontSize=12,
    )
    left_aligned_style = ParagraphStyle(
        name="LeftAligned",
        alignment=TA_LEFT,
        fontSize=12,
    )

    # Add subject name and exam details
    heading = Paragraph(subject_name, centered_style)
    elements.append(heading)
    elements.append(Spacer(0, 0.5 * inch))

    # Create a table for the exam details
    exam_details = [
        [Paragraph(f"Syllabus Code: {syllabus_code}", left_aligned_style), "", Paragraph(f"Paper Code: {paper_code}", right_aligned_style)],
        [Paragraph(f"Year: {year}", left_aligned_style), "", Paragraph(f"Variant: {variant}", right_aligned_style)]
    ]

    table = Table(exam_details, colWidths=[2.5*inch, 1*inch, 2.5*inch])
    table.setStyle(TableStyle([
        ('SPAN', (1, 0), (1, 1)),  # Span the middle column
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),  # Add padding to match spacing
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.5 * inch))  # Add some vertical space

    total_marks_style = ParagraphStyle(
        name="TotalMarks",
        alignment=TA_CENTER,
        fontSize=16,
        leading=18,
        fontName='Helvetica-Bold',
    )

    total_marks_text = Paragraph(f"Total Marks Obtained: {total_marks_obtained}/{total_marks_possible}", total_marks_style)
    elements.append(total_marks_text)
    elements.append(Spacer(1, 0.5 * inch))  # Add some vertical space

    if incorrect_answers:
        incorrect_answers_text = Paragraph("Incorrect Answers:", styles["Heading2"])
        elements.append(incorrect_answers_text)
        elements.append(Spacer(1, 0.25 * inch))

        for question_no, student_answer, correct_answer in incorrect_answers:
            answer_text = f"Question {question_no}: Your Answer - {student_answer}, Correct Answer - {correct_answer}"
            elements.append(Paragraph(answer_text, styles["BodyText"]))

    doc.build(elements)

    # Open the PDF after it is generated
    webbrowser.open(f"file://{file_path}")

    return file_path
