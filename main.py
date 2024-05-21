import sys
from PyQt5.QtWidgets import QApplication
from gui import MCQChecker
from excel_processing import read_student_answers
from pdf_processing import extract_correct_answers
from answer_matching import match_answers
from report_generation import create_report_pdf
from logger import setup_logger
import requests

logger = setup_logger()

CURRENT_VERSION = "1.0.0"

def check_for_updates():
    try:
        response = requests.get("https://raw.githubusercontent.com/TazeXL/IGCSE-MCQ-checker/main/version.py")
        response.raise_for_status()
        latest_version = response.text.split("CURRENT_VERSION = ")[1].strip('"')

        if latest_version > CURRENT_VERSION:
            logger.warning(f"A newer version ({latest_version}) is available. Please update your software.")
            return False
        else:
            logger.info(f"You are running the latest version ({CURRENT_VERSION}).")
            return True
    except (requests.exceptions.RequestException, IndexError):
        logger.warning("Failed to check for updates. Please try again later.")
        return True

def process_files(window):
    logger.info("Processing files...")

    excel_file_path = window.excel_file_path
    markscheme_pdf_path = window.markscheme_pdf_path

    if excel_file_path and markscheme_pdf_path:
        logger.info(f"Excel file path: {excel_file_path}")
        logger.info(f"Markscheme PDF path: {markscheme_pdf_path}")

        logger.info("Reading student answers from Excel file...")
        student_answers = read_student_answers(excel_file_path)

        logger.info("Extracting correct answers from markscheme PDF...")
        correct_answers, subject_name, syllabus_code, paper_code, variant, year = extract_correct_answers(markscheme_pdf_path)

        logger.info("Matching answers...")
        total_marks_obtained, total_marks_possible, incorrect_answers = match_answers(student_answers, correct_answers)

        logger.info("Generating report PDF...")
        report_pdf = create_report_pdf(total_marks_obtained, total_marks_possible, incorrect_answers, subject_name, syllabus_code, paper_code, variant, year)
        logger.info("Report PDF generated successfully.")
    else:
        logger.error("Please select both Excel file and Markscheme PDF.")

def main():
    if not check_for_updates():
        sys.exit(0)

    app = QApplication(sys.argv)
    window = MCQChecker()
    logger.info("Assigning process_files_callback...")
    window.process_files_callback = process_files
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()