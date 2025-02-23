import os

from flask import Flask, render_template
from flask_cors import *
import pandas as pd
from ask_ai import ask_ai

app = Flask(__name__)
CORS(app)


def predict_next_sales(csv_file) -> str:
    try:
        # Read the CSV from the file-like object (e.g., from Flask's request.files)
        df = pd.read_csv(csv_file)
    except Exception as e:
        return f"Error reading CSV file: {e}"

    # Try to identify a column with 'sales' in the name
    sales_col = None
    for col in df.columns:
        if 'sales' in col.lower():
            sales_col = col
            break

    # If no column is found, pick the first numeric column
    if not sales_col:
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                sales_col = col
                break

    if not sales_col:
        return "No valid numeric sales column found in the CSV."

    try:
        # Convert the column values to numeric, dropping non-numeric entries
        sales_data = pd.to_numeric(df[sales_col], errors='coerce').dropna().tolist()
        print(sales_data)
    except Exception as e:
        return f"Error processing sales column: {e}"

    if not sales_data:
        return "Sales data is empty or could not be converted to numbers."

    # Build a prompt that sends the historical sales data to the LLM
    prompt = (
        f"The following is a CSV export of historical daily sales data for a small bread business:\n\n"
        f"{sales_data}\n\n"
        f"Based on this data, please predict the next day's sales number. "
        f"Provide just the number in your response."
    )

    # Call the LLM via the ask_ai method
    prediction = ask_ai(prompt)
    return prediction


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
