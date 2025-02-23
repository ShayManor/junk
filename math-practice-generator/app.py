from flask import Flask, render_template, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


import random
from flask import jsonify
from ask_ai import ask_ai

# Define math problems
problems = {
    "easy": [
        {"id": 1, "question": "What is 2 + 2?", "answer": "4"},
        {"id": 2, "question": "What is 5 - 3?", "answer": "2"},
        {"id": 3, "question": "What is 3 * 3?", "answer": "9"}
    ],
    "medium": [
        {"id": 4, "question": "What is 12 / 4?", "answer": "3"},
        {"id": 5, "question": "What is 15 + 6?", "answer": "21"},
        {"id": 6, "question": "What is 7 * 8?", "answer": "56"}
    ],
    "hard": [
        {"id": 7, "question": "What is the square root of 144?", "answer": "12"},
        {"id": 8, "question": "Solve for x: 2x + 5 = 17", "answer": "6"},
        {"id": 9, "question": "What is 13 * 12?", "answer": "156"}
    ]
}

@app.route("/get_problem", methods=["GET"])
def get_problem():
    difficulty = request.args.get("difficulty", "medium").lower()
    if difficulty not in problems:
        difficulty = "medium"
    problem = random.choice(problems[difficulty])
    return jsonify({"id": problem["id"], "question": problem["question"]})

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.get_json()
    problem_id = data.get("id")
    user_answer = data.get("answer")

    # Find the problem by ID
    problem = None
    for level in problems.values():
        for p in level:
            if p["id"] == problem_id:
                problem = p
                break
        if problem:
            break

    if not problem:
        return jsonify({"success": False, "message": "Problem not found"}), 404

    correct_answer = problem["answer"]
    if str(user_answer).strip() == str(correct_answer):
        return jsonify({"success": True, "correct": True})
    else:
        prompt = (
            f"The user answered '{user_answer}' to the question: '{problem['question']}'. "
            f"The correct answer is '{correct_answer}'. Explain why the user's answer is incorrect."
        )
        explanation = ask_ai(prompt)
        return jsonify({"success": True, "correct": False, "explanation": explanation})


@app.route("/", methods=["GET"])
def index():
    return send_from_directory("", "templates/index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
