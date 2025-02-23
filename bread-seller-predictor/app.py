from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)


from ask_ai import ask_ai
import pandas as pd
from flask import jsonify

@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    try:
        df = pd.read_csv(file)
        if 'sales' not in df.columns:
            return jsonify({"error": "CSV must contain a 'sales' column"}), 400
        sales_data = df['sales'].tolist()
        prompt = f"Given the following daily bread sales data: {sales_data}, predict the number of bread to produce for the next day to meet demand."
        prediction = ask_ai(prompt)
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def index():
    return send_from_directory("", "templates/index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
