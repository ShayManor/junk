from flask import Flask, render_template, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


import random
from ask_ai import ask_ai

# Sample questions database
questions_db = {
    "4th_grade": {
        "easy": [
            {"id": 1, "question": "What is 2 + 2?", "answer": "4"},
            {"id": 2, "question": "What is 5 - 3?", "answer": "2"},
            {"id": 3, "question": "What is 3 x 1?", "answer": "3"},
        ],
        "medium": [
            {"id": 4, "question": "What is 12 ÷ 4?", "answer": "3"},
            {"id": 5, "question": "What is 7 + 6?", "answer": "13"},
            {"id": 6, "question": "What is 9 - 5?", "answer": "4"},
        ],
        "hard": [
            {"id": 7, "question": "What is 15 ÷ 3 + 2?", "answer": "7"},
            {"id": 8, "question": "What is 8 x 7?", "answer": "56"},
            {"id": 9, "question": "What is 14 - 9 + 5?", "answer": "10"},
        ],
    },
    "middle_school": {
        "easy": [
            {"id": 10, "question": "Solve for x: x + 5 = 10", "answer": "5"},
            {"id": 11, "question": "What is 6 x 4?", "answer": "24"},
            {"id": 12, "question": "What is 18 ÷ 2?", "answer": "9"},
        ],
        "medium": [
            {"id": 13, "question": "Solve for y: 2y - 4 = 10", "answer": "7"},
            {"id": 14, "question": "What is the area of a rectangle with length 5 and width 3?", "answer": "15"},
            {"id": 15, "question": "What is 7²?", "answer": "49"},
        ],
        "hard": [
            {"id": 16, "question": "Solve for z: z² - 5z + 6 = 0", "answer": "2 or 3"},
            {"id": 17, "question": "What is the volume of a cube with side length 4?", "answer": "64"},
            {"id": 18, "question": "Simplify: 3(2x + 4) - 5x", "answer": "x + 12"},
        ],
    },
    "high_school": {
        "easy": [
            {"id": 19, "question": "What is the slope of the line y = 2x + 3?", "answer": "2"},
            {"id": 20, "question": "What is 5!", "answer": "120"},
            {"id": 21, "question": "Solve for a: 3a = 12", "answer": "4"},
        ],
        "medium": [
            {"id": 22, "question": "Factor: x² - 9", "answer": "(x - 3)(x + 3)"},
            {"id": 23, "question": "What is the derivative of x³?", "answer": "3x²"},
            {"id": 24, "question": "Solve the inequality: 2x - 5 > 3", "answer": "x > 4"},
        ],
        "hard": [
            {"id": 25, "question": "Integrate: ∫2x dx", "answer": "x² + C"},
            {"id": 26, "question": "Solve for x: eˣ = 5", "answer": "ln(5)"},
            {"id": 27, "question": "Find the limit: limₓ→0 (sin x)/x", "answer": "1"},
        ],
    },
    "college": {
        "easy": [
            {"id": 28, "question": "What is the integral of 1 dx?", "answer": "x + C"},
            {"id": 29, "question": "Solve for x: 2x + 3 = 7", "answer": "2"},
            {"id": 30, "question": "What is the derivative of sin(x)?", "answer": "cos(x)"},
        ],
        "medium": [
            {"id": 31, "question": "Find the eigenvalues of the identity matrix.", "answer": "1"},
            {"id": 32, "question": "What is the dot product of vectors (1,2) and (3,4)?", "answer": "11"},
            {"id": 33, "question": "Solve the differential equation dy/dx = y.", "answer": "y = Ce^x"},
        ],
        "hard": [
            {"id": 34, "question": "Prove that the set of real numbers is uncountable.", "answer": "Use Cantor's diagonal argument."},
            {"id": 35, "question": "Evaluate the integral ∫₀^∞ e^(-x) dx", "answer": "1"},
            {"id": 36, "question": "Find the Fourier transform of a delta function.", "answer": "1"},
        ],
    },
}

# Helper function to retrieve a question based on level and difficulty
def get_random_question(level, difficulty):
    level = level.lower()
    difficulty = difficulty.lower()
    if level not in questions_db:
        return None
    if difficulty not in questions_db[level]:
        return None
    return random.choice(questions_db[level][difficulty])

# Endpoint to fetch a question
@app.route("/get_question", methods=["GET"])
def get_question_route():
    level = request.args.get("level")
    difficulty = request.args.get("difficulty")
    question = get_random_question(level, difficulty)
    if question:
        return {"id": question["id"], "question": question["question"]}
    else:
        return {"error": "Invalid level or difficulty"}, 400

# Endpoint to check the answer
@app.route("/check_answer", methods=["POST"])
def check_answer_route():
    data = request.json
    question_id = data.get("id")
    user_answer = data.get("answer").strip().lower()

    # Find the question by ID
    found_question = None
    for level in questions_db:
        for difficulty in questions_db[level]:
            for question in questions_db[level][difficulty]:
                if question["id"] == question_id:
                    found_question = question
                    break
            if found_question:
                break
        if found_question:
            break

    if not found_question:
        return {"error": "Question not found"}, 404

    correct_answer = found_question["answer"].strip().lower()
    if user_answer == correct_answer:
        return {"correct": True, "message": "Correct!"}
    else:
        # Generate feedback using AI
        prompt = f"Explain why the answer '{user_answer}' is incorrect for the math question: '{found_question['question']}' and provide the correct answer."
        feedback = ask_ai(prompt)
        return {"correct": False, "message": "Incorrect.", "feedback": feedback}


@app.route("/", methods=["GET"])
def index():
    return send_from_directory("", "templates/index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
