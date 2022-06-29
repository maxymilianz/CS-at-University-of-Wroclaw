with open('pytania.txt', encoding='utf8') as questions_file:
    questions = questions_file.readlines()

with open('sorted_questions.txt', 'w', encoding='utf8') as target_file:
    for question in sorted(questions):
        target_file.write(question)
