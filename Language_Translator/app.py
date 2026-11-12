
from flask import Flask, render_template, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "kn": "Kannada",
    "ta": "Tamil",
    "te": "Telugu"
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/languages")
def get_languages():
    return jsonify([
        {"code": code, "name": name}
        for code, name in LANGUAGES.items()
    ])


@app.route("/translate", methods=["POST"])
def translate():
    try:
        data = request.get_json(silent=True) or {}

        text = data.get("text", "").strip()
        source = data.get("source", "en")
        target = data.get("target", "hi")

        if not text:
            return jsonify({"error": "Please enter some text."}), 400

        if source not in LANGUAGES or target not in LANGUAGES:
            return jsonify({"error": "Please select valid languages."}), 400

        if source == target:
            return jsonify({"error": "Please select different languages."}), 400

        result = translator.translate(
            text,
            src=source,
            dest=target
        )

        return jsonify({
            "translated_text": result.text
        })

    except Exception as e:
        print("TRANSLATION ERROR:", str(e))
        return jsonify({
            "error": "Translation failed. Please check your internet connection and try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
