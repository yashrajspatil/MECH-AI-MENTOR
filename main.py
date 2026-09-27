import os

from flask import Flask, request, jsonify

from sarvamai import SarvamAI


# ============================================================
# LOAD API KEY FROM .env
# ============================================================

def load_env_file():

    if not os.path.exists(".env"):
        print("ERROR: .env file not found.")
        return

    with open(".env", "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)

            key = key.strip()
            value = value.strip()

            os.environ[key] = value


load_env_file()


# ============================================================
# CHECK API KEY
# ============================================================

api_key = os.getenv("SARVAM_API_KEY")


if not api_key:

    print("")
    print("❌ ERROR: SARVAM_API_KEY was not found.")
    print("Make sure your .env file contains:")
    print("")
    print("SARVAM_API_KEY=your_api_key")
    print("")

else:

    print("✅ Sarvam API key loaded.")


# ============================================================
# SARVAM CLIENT
# ============================================================

client = None

if api_key:

    client = SarvamAI(
        api_subscription_key=api_key
    )


# ============================================================
# FLASK
# ============================================================

app = Flask(__name__)


# ============================================================
# WEBPAGE
# ============================================================

HTML = """
<!DOCTYPE html>

<html>

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Mech AI Mentor</title>


    <style>

        * {
            box-sizing: border-box;
        }


        body {

            margin: 0;

            font-family: Arial, sans-serif;

            background: #f4f6f8;

            color: #222;
        }


        .container {

            max-width: 900px;

            margin: 50px auto;

            padding: 20px;
        }


        h1 {

            text-align: center;

            font-size: 40px;

            margin-bottom: 10px;
        }


        .subtitle {

            text-align: center;

            color: #666;

            margin-bottom: 30px;
        }


        .chat-box {

            background: white;

            border-radius: 16px;

            padding: 25px;

            box-shadow: 0 5px 25px rgba(0,0,0,0.08);
        }


        #chat {

            min-height: 300px;

            margin-bottom: 20px;
        }


        .message {

            padding: 16px;

            border-radius: 12px;

            margin-bottom: 15px;

            line-height: 1.6;

            white-space: pre-wrap;
        }


        .user {

            background: #e8f0fe;
        }


        .bot {

            background: #eeeeee;
        }


        .input-area {

            display: flex;

            gap: 10px;
        }


        input {

            flex: 1;

            padding: 15px;

            font-size: 16px;

            border: 1px solid #ccc;

            border-radius: 8px;

            outline: none;
        }


        button {

            padding: 15px 22px;

            border: none;

            border-radius: 8px;

            background: #222;

            color: white;

            font-size: 16px;

            cursor: pointer;
        }


        button:disabled {

            opacity: 0.5;

            cursor: not-allowed;
        }


        .error {

            background: #ffe5e5;

            color: #b00000;
        }


        @media (max-width: 600px) {

            .input-area {

                flex-direction: column;
            }

            button {

                width: 100%;
            }

        }

    </style>

</head>


<body>


<div class="container">


    <h1>🔧 Mech AI Mentor</h1>


    <p class="subtitle">

        AI-powered Mechanical Engineering Mentor

    </p>


    <div class="chat-box">


        <div id="chat">

            <div class="message bot">

                🤖 <strong>Sarvam:</strong>

                <br>

                Ask me any Mechanical Engineering question.

            </div>

        </div>


        <div class="input-area">

            <input
                id="question"
                type="text"
                placeholder="Ask a Mechanical Engineering question..."
            >


            <button id="askButton">

                Ask Sarvam

            </button>

        </div>


    </div>


</div>



<script>


const input = document.getElementById("question");

const button = document.getElementById("askButton");

const chat = document.getElementById("chat");



button.addEventListener("click", askQuestion);



input.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {

        askQuestion();

    }

});



async function askQuestion() {


    const question = input.value.trim();


    if (!question) {

        return;

    }


    // Show user message

    const userMessage = document.createElement("div");

    userMessage.className = "message user";

    userMessage.innerHTML = "👤 <strong>You:</strong><br>";

    userMessage.appendChild(
        document.createTextNode(question)
    );

    chat.appendChild(userMessage);


    input.value = "";

    button.disabled = true;

    button.innerText = "Thinking...";


    // Temporary bot message

    const botMessage = document.createElement("div");

    botMessage.className = "message bot";

    botMessage.innerHTML =
        "🤖 <strong>Sarvam:</strong><br>Thinking...";

    chat.appendChild(botMessage);


    try {


        console.log("Sending request...");


        const response = await fetch("/ask", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                question: question

            })

        });


        console.log(
            "Server response:",
            response.status
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.error || "Server error"
            );

        }


        botMessage.innerHTML =
            "🤖 <strong>Sarvam:</strong><br>";


        botMessage.appendChild(
            document.createTextNode(data.answer)
        );


    }


    catch (error) {


        console.error(error);


        botMessage.className =
            "message error";


        botMessage.innerHTML =
            "❌ <strong>Error:</strong><br>";


        botMessage.appendChild(
            document.createTextNode(error.message)
        );


    }


    button.disabled = false;

    button.innerText = "Ask Sarvam";


}


</script>


</body>

</html>
"""


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return HTML


# ============================================================
# SARVAM API
# ============================================================

@app.route("/ask", methods=["POST"])
def ask():

    print("")
    print("========== NEW QUESTION ==========")


    # Check client

    if client is None:

        return jsonify({

            "error":
            "Sarvam API key is not loaded."

        }), 500


    # Get request data

    data = request.get_json()


    if not data:

        return jsonify({

            "error":
            "No JSON data received."

        }), 400


    question = data.get("question", "").strip()


    print("Question:", question)


    if not question:

        return jsonify({

            "error":
            "Question is empty."

        }), 400


    try:


        print("Sending request to Sarvam...")


        response = client.chat.completions(

            model="sarvam-105b-conversations",

            messages=[

                {

                    "role": "system",

                    "content":
                    """You are a Mechanical Engineering mentor.

Explain concepts clearly to an undergraduate student.

Use simple language, equations, and real-world examples when useful.

Keep answers concise and technically correct."""

                },

                {

                    "role": "user",

                    "content": question

                }

            ]

        )


        answer = response.choices[0].message.content


        print("✅ Sarvam response received.")


        return jsonify({

            "answer": answer

        })


    except Exception as e:


        print("")
        print("❌ SARVAM ERROR:")
        print(repr(e))
        print("")


        return jsonify({

            "error":
            "Sarvam API error: " + str(e)

        }), 500



# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("")
    print("===================================")
    print("🔧 MECH AI MENTOR")
    print("===================================")
    print("")
    print("Open:")
    print("http://127.0.0.1:5000")
    print("")


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )
