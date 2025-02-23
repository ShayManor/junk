from flask import Flask, render_template, request
from ask_ai import ask_ai

app = Flask(__name__)

def get_grade(score):
    """
    Map the current score to a school grade.
    0-1: 1st Grade,
    2-3: 2nd Grade,
    4-5: 3rd Grade,
    6-7: 4th Grade,
    8-9: 5th Grade,
    10-11: 6th Grade,
    12-13: 7th Grade,
    14-15: 8th Grade,
    16-17: 9th Grade,
    18-19: 10th Grade,
    20-21: 11th Grade,
    22-23: 12th Grade,
    24+: College.
    """
    if score <= 1:
        return "1st Grade"
    elif score <= 3:
        return "2nd Grade"
    elif score <= 5:
        return "3rd Grade"
    elif score <= 7:
        return "4th Grade"
    elif score <= 9:
        return "5th Grade"
    elif score <= 11:
        return "6th Grade"
    elif score <= 13:
        return "7th Grade"
    elif score <= 15:
        return "8th Grade"
    elif score <= 17:
        return "9th Grade"
    elif score <= 19:
        return "10th Grade"
    elif score <= 21:
        return "11th Grade"
    elif score <= 23:
        return "12th Grade"
    else:
        return "College"

def generate_problem(difficulty):
    """
    Use ask_ai to generate a math problem based on the current difficulty.
    The prompt instructs the AI to return the problem on the first line and the answer on the second.
    """
    response = ask_ai(f"Generate a math problem for someone in {get_grade(difficulty)} with the first part of the problem on line 1 and the answer on line 2. The answer should just be a number or equation with no units. The question should have little text. For example, dont do x = 6, just have the answer be 6.")
    parts = response.split("\n")
    print(parts)
    if len(parts) >= 2:
        problem_text = parts[0].strip()
        try:
            answer = int(parts[1].strip())
        except ValueError:
            answer = None
    else:
        problem_text = "Error generating problem."
        answer = None
    return problem_text, answer

@app.route('/')
def index():
    # Start with default state.
    score = 0
    difficulty = 1
    problem_text, correct_answer = generate_problem(difficulty)
    grade = get_grade(score)
    return render_template('index.html',
                           problem=problem_text,
                           score=score,
                           difficulty=difficulty,
                           grade=grade,
                           message="",
                           correct_answer=correct_answer)

@app.route('/answer', methods=['POST'])
def answer():
    # Retrieve state from hidden form fields.
    try:
        score = int(request.form.get('score', 0))
    except ValueError:
        score = 0
    try:
        difficulty = int(request.form.get('difficulty', 1))
    except ValueError:
        difficulty = 1
    try:
        correct_answer = int(request.form.get('correct_answer'))
    except (ValueError, TypeError):
        correct_answer = None

    user_answer_str = request.form.get('user_answer', '').strip()
    try:
        user_answer = int(user_answer_str)
    except ValueError:
        message = "Please enter a valid integer."
        problem_text, new_correct = generate_problem(difficulty)
        grade = get_grade(score)
        return render_template('index.html',
                               problem=problem_text,
                               score=score,
                               difficulty=difficulty,
                               grade=grade,
                               message=message,
                               correct_answer=new_correct)

    if correct_answer is None:
        message = "There was an error with the problem. Please try again."
    else:
        if user_answer == correct_answer:
            message = "Correct!"
            score += 1
            difficulty += 1
        else:
            message = f"Incorrect. The correct answer was {correct_answer}."
            # Decrease score (not below 0) and difficulty (not below 1)
            score = max(score - 1, 0)
            difficulty = max(difficulty - 1, 1)

    # Generate a new problem with the updated difficulty.
    problem_text, new_correct = generate_problem(difficulty)
    grade = get_grade(score)
    return render_template('index.html',
                           problem=problem_text,
                           score=score,
                           difficulty=difficulty,
                           grade=grade,
                           message=message,
                           correct_answer=new_correct)

if __name__ == '__main__':
    app.run(debug=True)
