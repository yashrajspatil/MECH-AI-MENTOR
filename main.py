import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from sarvamai import SarvamAI

load_dotenv()

app = Flask(__name__)

client = SarvamAI(
    api_subscription_key=os.getenv("SARVAM_API_KEY")
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():

    question = request.json["question"]

    print("Question:", question)

    response = client.chat.completions(
        model="sarvam-105b-conversations",
        messages=[
            {
                "role": "system",
                "content": """You are a Mechanical Engineering mentor.
Explain concepts simply to an undergraduate student.
Use equations and real-world examples when useful.
Keep answers concise and technically correct."""
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    answer = response.choices[0].message.content

    print("Answer received.")

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)