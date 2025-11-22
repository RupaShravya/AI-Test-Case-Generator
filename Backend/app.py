from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from any origin

@app.route('/generate-testcases', methods=['POST'])
def generate_testcases():
    data = request.get_json()
    requirement = data.get("requirement", "")

    # Dummy structured test cases (positive and negative)
    test_cases = [
        {
            "test_case": 1,
            "description": f"Verify the requirement: {requirement}",
            "steps": [
                "Navigate to the login page",
                "Enter valid username",
                "Enter valid password",
                "Click the login button",
                "Verify that the user is logged in successfully"
            ],
            "expected_result": "User is able to log in with valid credentials"
        },
        {
            "test_case": 2,
            "description": f"Verify invalid login for requirement: {requirement}",
            "steps": [
                "Navigate to the login page",
                "Enter invalid username or password",
                "Click the login button",
                "Verify that an error message is displayed"
            ],
            "expected_result": "User is not able to log in and sees an error message"
        }
    ]

    return jsonify({"result": test_cases})

if __name__ == "__main__":
    app.run(debug=True)
