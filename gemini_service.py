import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)


def generate_comic_story(prompt, character="", setting="", tone=""):
    full_prompt = f"""
Create a creative comic book story based on the following details.

Story Prompt: {prompt}
Main Character: {character}
Setting: {setting}
Tone: {tone}

Generate:
1. Comic title
2. Short story
3. Panel-by-panel scenes
4. Dialogue for each panel

Keep the story suitable for a general audience.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    return response.text