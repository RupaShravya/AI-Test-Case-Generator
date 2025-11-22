# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# Replace these with your Gemini API details
GEMINI_API_KEY = "AIzaSyBdUgebHr2xhbOwMHgQWtIN9edVL9DVKgo"
GEMINI_MODEL_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

HEADERS = {
    "Authorization": f"Bearer {GEMINI_API_KEY}",
    "Content-Type": "application/json"
}

def generate_test_cases(requirement):
    """
    Sends requirement to Gemini API and returns structured test case output
    """
    prompt = f"""
    Generate structured test cases for the following requirement.
    Include Positive, Negative, and Boundary test cases in JSON format.
    Requirement: {requirement}
    """
    payload = {
        "prompt": prompt,
        "maxOutputTokens": 500,
        "temperature": 0.7
    }

    try:
        response = requests.post(GEMINI_MODEL_ENDPOINT, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()

        # Gemini's response parsing (adjust according to actual API output)
        if "candidates" in data and len(data["candidates"]) > 0:
            result_text = data["candidates"][0]["content"]
            try:
                # Attempt to parse JSON returned by Gemini
                result_json = json.loads(result_text)
                return result_json
            except json.JSONDecodeError:
                # If parsing fails, return raw text
                return [{"description": result_text, "type": "Raw Text"}]
        else:
            return [{"description": "No response from Gemini", "type": "Info"}]

    except requests.exceptions.RequestException as e:
        return [{"description": f"Error: {str(e)}", "type": "Error"}]

@app.route("/generate-testcases", methods=["POST"])
def generate_endpoint():
    data = request.get_json()
    requirement = data.get("requirement", "")
    if not requirement:
        return jsonify({"result": [{"description": "No requirement provided", "type": "Error"}]})

    test_cases = generate_test_cases(requirement)
    return jsonify({"result": test_cases})

if __name__ == "__main__":
    app.run(debug=True)
