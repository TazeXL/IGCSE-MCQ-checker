import openpyxl

def read_student_answers(excel_file_path):
    workbook = openpyxl.load_workbook(excel_file_path)
    worksheet = workbook.active
    student_answers = []
    for row in worksheet.iter_rows(min_row=1, max_row=40, min_col=1, max_col=1):
        for cell in row:
            student_answers.append(cell.value)
    return student_answers

def process_mcq_answers(excel_file_path, markscheme):
    student_answers = read_student_answers(excel_file_path)
    
    total_marks = 40 - student_answers.count(None)
    obtained_marks = 0

    for i, (student_answer, correct_answer) in enumerate(zip(student_answers, markscheme), start=1):
        if student_answer:
            if student_answer == correct_answer:
                obtained_marks += 1 
            else:
                print(f"Question {i}: Your Answer - {student_answer}, Correct Answer - {correct_answer}")

    return obtained_marks, total_marks


if __name__ == "__main__":
    excel_file_path = 'path_to_your_excel_file.xlsx'
    markscheme = ['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D']  # Example markscheme

    obtained_marks, total_marks = process_mcq_answers(excel_file_path, markscheme)

    print(f"Total Marks Obtained: {obtained_marks} / {total_marks}")
