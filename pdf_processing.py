import pdfplumber
import re

def extract_correct_answers(markscheme_pdf_path):
    correct_answers = {}
    subject_name = None
    syllabus_code = None
    paper_code = None
    variant = None
    year = None

    with pdfplumber.open(markscheme_pdf_path) as pdf:
        # Extract text from the first page
        first_page_text = pdf.pages[0].extract_text()

        # Find the subject name
        subject_match = re.search(r'Cambridge IGCSE\u2122\r?\n?([A-Z ]+)', first_page_text)
        if subject_match:
            subject_name = subject_match.group(1)

        # Find the syllabus code and paper code
        code_match = re.search(r'(\d{4})/(\d{2})', first_page_text)
        if code_match:
            syllabus_code = code_match.group(1)
            paper_code = code_match.group(2)

        # Find the variant (May/June or October/November)
        variant_match = re.search(r'(October/November)', first_page_text)
        if variant_match:
            variant = variant_match.group(1)

        # Find the year
        year_match = re.search(r'October/November\s+(\d{4})', first_page_text)
        if year_match:
            year = year_match.group(1)

        # Extract text from all pages
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

        # Split the text by newline characters
        lines = text.splitlines()

        # Iterate over each line
        for line in lines:
            # Check if the line starts with a number (question number)
            line_parts = line.strip().split()
            if line_parts and line_parts[0].isdigit():
                question_no = int(line_parts[0])
                answer = line_parts[1]  # Assuming the answer is the second part

                # Store the answer in the dictionary
                correct_answers[question_no] = answer

    # Construct the list of correct answers
    correct_answers_list = [correct_answers.get(i, "") for i in range(1, 41)]

    return correct_answers_list, subject_name, syllabus_code, paper_code, variant, year