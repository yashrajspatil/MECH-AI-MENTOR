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

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Mech AI Mentor</title>


<style>

* {
    box-sizing: border-box;
}


body {

    margin: 0;

    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    background:
        radial-gradient(
            circle at top right,
            #1e3a5f,
            #0b1120 45%,
            #070b14
        );

    color: #f5f7fa;

    min-height: 100vh;

}


/* MAIN CONTAINER */

.container {

    width: 100%;

    max-width: 1100px;

    margin: auto;

    padding: 35px 20px;

}


/* HEADER */

.header {

    text-align: center;

    margin-bottom: 30px;

}


.logo {

    font-size: 42px;

    margin-bottom: 8px;

}


.title {

    font-size: 38px;

    font-weight: 700;

    margin: 0;

    letter-spacing: -1px;

}


.subtitle {

    color: #9ca9bb;

    margin-top: 10px;

    font-size: 16px;

}


/* MAIN CARD */

.chat-card {

    background: rgba(15, 23, 42, 0.88);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 20px;

    overflow: hidden;

    box-shadow:
        0 25px 70px rgba(0,0,0,0.35);

    backdrop-filter: blur(15px);

}


/* TOP BAR */

.top-bar {

    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 18px 24px;

    border-bottom: 1px solid rgba(255,255,255,0.08);

}


.status {

    display: flex;

    align-items: center;

    gap: 8px;

    color: #cbd5e1;

    font-size: 14px;

}


.status-dot {

    width: 9px;

    height: 9px;

    background: #22c55e;

    border-radius: 50%;

    box-shadow: 0 0 10px #22c55e;

}


.model {

    color: #718096;

    font-size: 13px;

}


/* CHAT */

#chat {

    height: 480px;

    overflow-y: auto;

    padding: 25px;

}


.message {

    max-width: 80%;

    padding: 15px 18px;

    border-radius: 15px;

    margin-bottom: 18px;

    line-height: 1.65;

    white-space: pre-wrap;

    animation: fadeIn 0.25s ease;

}


@keyframes fadeIn {

    from {

        opacity: 0;

        transform: translateY(5px);

    }

    to {

        opacity: 1;

        transform: translateY(0);

    }

}


.user {

    margin-left: auto;

    background: #2563eb;

    border-bottom-right-radius: 4px;

}


.bot {

    margin-right: auto;

    background: #182235;

    border: 1px solid rgba(255,255,255,0.07);

    border-bottom-left-radius: 4px;

}


.message-label {

    font-size: 13px;

    font-weight: 600;

    margin-bottom: 5px;

    opacity: 0.8;

}


/* SUGGESTIONS */

.suggestions {

    padding: 0 25px 20px;

}


.suggestions-title {

    color: #7f8da3;

    font-size: 12px;

    text-transform: uppercase;

    letter-spacing: 1px;

    margin-bottom: 10px;

}


.suggestion-buttons {

    display: flex;

    gap: 10px;

    flex-wrap: wrap;

}


.suggestion {

    background: #111a2b;

    border: 1px solid #26344d;

    color: #cbd5e1;

    padding: 9px 13px;

    border-radius: 9px;

    cursor: pointer;

    font-size: 13px;

    transition: 0.2s;

}


.suggestion:hover {

    border-color: #3b82f6;

    color: white;

    background: #17243a;

}


/* INPUT */

.input-section {

    padding: 20px 25px 25px;

    border-top: 1px solid rgba(255,255,255,0.08);

}


.input-box {

    display: flex;

    gap: 10px;

    background: #0c1424;

    border: 1px solid #26344d;

    border-radius: 13px;

    padding: 7px;

}


input {

    flex: 1;

    border: none;

    outline: none;

    background: transparent;

    color: white;

    padding: 12px;

    font-size: 15px;

}


input::placeholder {

    color: #64748b;

}


button.ask {

    border: none;

    background: #2563eb;

    color: white;

    padding: 0 20px;

    border-radius: 9px;

    font-weight: 600;

    cursor: pointer;

    transition: 0.2s;

}


button.ask:hover {

    background: #3b82f6;

}


button.ask:disabled {

    opacity: 0.5;

    cursor: not-allowed;

}


/* FOOTER */

.footer {

    text-align: center;

    color: #526176;

    font-size: 12px;

    margin-top: 18px;

}


/* MOBILE */

@media (max-width: 700px) {

    .container {

        padding: 20px 10px;

    }


    .title {

        font-size: 30px;

    }


    #chat {

        height: 55vh;

    }


    .message {

        max-width: 90%;

    }


    .suggestion-buttons {

        flex-direction: column;

    }


    .suggestion {

        width: 100%;

        text-align: left;

    }


    button.ask {

        padding: 0 15px;

    }

}

</style>

</head>


<body>


<div class="container">


    <!-- HEADER -->

    <div class="header">

        <div class="logo">⚙️</div>

        <h1 class="title">Mech AI Mentor</h1>

        <p class="subtitle">
            Your AI assistant for Mechanical Engineering
        </p>

    </div>


    <!-- CHAT CARD -->

    <div class="chat-card">


        <!-- TOP BAR -->

        <div class="top-bar">

            <div class="status">

                <span class="status-dot"></span>

                Sarvam AI Online

            </div>


            <div class="model">

                sarvam-105b-conversations

            </div>

        </div>


        <!-- CHAT -->

        <div id="chat">


            <div class="message bot">

                <div class="message-label">
                    🤖 Sarvam
                </div>

                Hello! I'm your Mechanical Engineering AI mentor.

                Ask me about thermodynamics, fluid mechanics,
                heat transfer, materials, CAD, or other
                engineering concepts.

            </div>


        </div>


        <!-- SUGGESTIONS -->

        <div class="suggestions">

            <div class="suggestions-title">
                Try asking
            </div>


            <div class="suggestion-buttons">


                <button
                    class="suggestion"
                    onclick="useQuestion('Explain the first law of thermodynamics')"
                >
                    First law of thermodynamics
                </button>


                <button
                    class="suggestion"
                    onclick="useQuestion('What is Reynolds number?')"
                >
                    Reynolds number
                </button>


                <button
                    class="suggestion"
                    onclick="useQuestion('Explain forced convection')"
                >
                    Forced convection
                </button>


                <button
                    class="suggestion"
                    onclick="useQuestion('What is the difference between stress and strain?')"
                >
                    Stress vs strain
                </button>


            </div>

        </div>


        <!-- INPUT -->

        <div class="input-section">


            <div class="input-box">


                <input

                    id="question"

                    type="text"

                    placeholder="Ask a Mechanical Engineering question..."

                    autocomplete="off"

                >


                <button
                    class="ask"
                    id="askButton"
                    onclick="askQuestion()"
                >
                    Ask
                </button>


            </div>


        </div>


    </div>


    <div class="footer">

        Built with Python · Flask · Sarvam AI

    </div>


</div>



<script>


const input =
    document.getElementById("question");


const button =
    document.getElementById("askButton");


const chat =
    document.getElementById("chat");



function useQuestion(question) {

    input.value = question;

    input.focus();

}



input.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {

        askQuestion();

    }

});



async function askQuestion() {


    const question =
        input.value.trim();


    if (!question) {

        return;

    }


    // USER MESSAGE

    const userMessage =
        document.createElement("div");


    userMessage.className =
        "message user";


    userMessage.innerHTML =
        '<div class="message-label">👤 You</div>';


    userMessage.appendChild(
        document.createTextNode(question)
    );


    chat.appendChild(userMessage);


    input.value = "";


    button.disabled = true;

    button.innerText = "Thinking...";


    // BOT MESSAGE

    const botMessage =
        document.createElement("div");


    botMessage.className =
        "message bot";


    botMessage.innerHTML =
        '<div class="message-label">🤖 Sarvam</div>Thinking...';


    chat.appendChild(botMessage);


    chat.scrollTop =
        chat.scrollHeight;


    try {


        const response =
            await fetch("/ask", {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body: JSON.stringify({

                    question: question

                })

            });


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error || "Server error"
            );

        }


        botMessage.innerHTML =
            '<div class="message-label">🤖 Sarvam</div>';


        botMessage.appendChild(
            document.createTextNode(data.answer)
        );


    }


    catch (error) {


        botMessage.innerHTML =
            '<div class="message-label">❌ Error</div>';


        botMessage.appendChild(
            document.createTextNode(error.message)
        );

    }


    button.disabled = false;

    button.innerText = "Ask";


    chat.scrollTop =
        chat.scrollHeight;

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
