import json
import google.generativeai as genai

from app.config.settings import settings

genai.configure(api_key=settings.GEMINI_API_KEY)


def generate_recipe_with_ai(prompt: str, meal_type: str = "", cuisine: str = "", dietary: str = "") -> dict:
    system_prompt = """You are a professional chef and nutritionist. Generate a detailed recipe in JSON format.
Return ONLY a valid JSON object with these fields:
{
    "title": "Recipe Title",
    "description": "Short description",
    "instructions": "Step by step cooking instructions",
    "cooking_time": 30,
    "prep_time": 15,
    "servings": 2,
    "difficulty": "Easy|Medium|Hard",
    "cuisine": "cuisine type",
    "meal_type": "breakfast|lunch|dinner|snack",
    "calories": 350,
    "protein": 25,
    "carbs": 40,
    "fat": 12,
    "is_vegetarian": 0,
    "is_vegan": 0,
    "is_gluten_free": 0,
    "ingredients": [
        {"name": "ingredient name", "quantity": 1, "unit": "cup", "notes": "optional notes"}
    ]
}"""

    full_prompt = f"{system_prompt}\n\nUser request: {prompt}"
    if meal_type:
        full_prompt += f"\nMeal type: {meal_type}"
    if cuisine:
        full_prompt += f"\nCuisine: {cuisine}"
    if dietary:
        full_prompt += f"\nDietary preference: {dietary}"

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(full_prompt)

    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0]

    return json.loads(text)


def explain_recipe_with_ai(recipe_title: str, recipe_description: str) -> str:
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""Explain this recipe in a friendly, engaging way. Include tips, variations, and interesting facts:

Recipe: {recipe_title}
Description: {recipe_description}

Provide a 2-3 paragraph explanation that would help a home cook understand and appreciate this recipe."""

    response = model.generate_content(prompt)
    return response.text.strip()


def get_ai_recommendations(search_history: list[str]) -> str:
    model = genai.GenerativeModel("gemini-pro")
    history_text = ", ".join(search_history[-10:]) if search_history else "No search history"
    prompt = f"""Based on these recent recipe searches: {history_text}

Suggest 5 recipe ideas with brief descriptions. Format as a numbered list."""

    response = model.generate_content(prompt)
    return response.text.strip()
