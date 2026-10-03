from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(_name_)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


@app.route("/", methods=["GET", "POST"])
def home():

    story = ""

    if request.method == "POST":

        prompt = request.form.get("prompt")
        character = request.form.get("character")
        setting = request.form.get("setting")
        tone = request.form.get("tone")

        user_prompt = f"""
        Create a creative comic story.

        Story idea: {prompt}
        Main character: {character}
        Setting: {setting}
        Tone: {tone}

        Create a 5-panel comic story.
        For each panel provide:
        1. Scene description
        2. Character action
        3. Dialogue

        Give the story a suitable title.
        Keep the language simple and creative.
        """

        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=user_prompt
            )

            story = response.text

        except Exception as e:
            story = "Error: " + str(e)

    return render_template("index.html", story=story)


if _name_ == "_main_":
    app.run(debug=True)