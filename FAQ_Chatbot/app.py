from flask import Flask, render_template, request, jsonify
from faq_chatbot import get_answer

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "")

    if not isinstance(question, str):
        return jsonify({"answer": "Please enter a valid question."}), 400

    answer = get_answer(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    print("Starting FAQ Chatbot...")
    app.run(debug=True)