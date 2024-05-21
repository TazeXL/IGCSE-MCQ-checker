def match_answers(student_answers, correct_answers):
    total_marks_obtained = 0
    total_marks_possible = 0
    incorrect_answers = []
    
    for i, student_answer in enumerate(student_answers):
        if student_answer:  
            total_marks_possible += 1 
            if student_answer.lower() == correct_answers[i].lower():
                total_marks_obtained += 1  
            else:
                incorrect_answers.append((i + 1, student_answer, correct_answers[i])) 
    
    return total_marks_obtained, total_marks_possible, incorrect_answers
