from flask import Blueprint, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

comic_routes = Blueprint("comic_routes", _name_)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


@comic_routes.route("/generate", methods=["POST"])
def generate_story():

    data = request.get_json()

    prompt = data.get("prompt", "")
    character = data.get("character", "")
    setting = data.get("setting", "")
    tone = data.get("tone", "")

    comic_prompt = f"""
    Create a creative comic story.

    Story idea: {prompt}
    Main character: {character}
    Setting: {setting}
    Tone: {tone}

    Create a 5-panel comic story.

    For each panel include:
    - Scene description
    - Character action
    - Dialogue

    Give the comic a suitable title.
    Use simple and creative English.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=comic_prompt
        )

        return jsonify({
            "success": True,
            "story": response.text
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500