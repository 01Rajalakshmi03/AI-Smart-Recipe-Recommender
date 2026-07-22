from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.recipe import AIGenerateRequest, RecipeCreate
from app.services import ai_service, recipe_service
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.recipe import SearchHistory

router = APIRouter(prefix="/api/ai", tags=["AI"])


@router.post("/generate")
def generate_recipe(
    data: AIGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        result = ai_service.generate_recipe_with_ai(
            data.prompt, data.meal_type, data.cuisine, data.dietary
        )

        recipe_data = RecipeCreate(
            title=result.get("title", "AI Generated Recipe"),
            description=result.get("description", ""),
            instructions=result.get("instructions", ""),
            cooking_time=result.get("cooking_time", 30),
            prep_time=result.get("prep_time", 15),
            servings=result.get("servings", 2),
            difficulty=result.get("difficulty", "Medium"),
            cuisine=result.get("cuisine", ""),
            meal_type=result.get("meal_type", ""),
            calories=result.get("calories", 0),
            protein=result.get("protein", 0),
            carbs=result.get("carbs", 0),
            fat=result.get("fat", 0),
            is_vegetarian=result.get("is_vegetarian", 0),
            is_vegan=result.get("is_vegan", 0),
            is_gluten_free=result.get("is_gluten_free", 0),
            ingredients=[
                {"name": ing.get("name", ""), "quantity": ing.get("quantity", 0), "unit": ing.get("unit", ""), "notes": ing.get("notes", "")}
                for ing in result.get("ingredients", [])
            ],
        )

        recipe = recipe_service.create_recipe(db, recipe_data, current_user.id)
        recipe.is_ai_generated = 1
        db.commit()
        db.refresh(recipe)

        return {"recipe_id": recipe.id, "message": "Recipe generated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recipe: {str(e)}",
        )


@router.post("/explain")
def explain_recipe(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        explanation = ai_service.explain_recipe_with_ai(
            data.get("title", ""),
            data.get("description", ""),
        )
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate explanation: {str(e)}",
        )


@router.get("/recommendations")
def get_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        histories = (
            db.query(SearchHistory)
            .filter(SearchHistory.user_id == current_user.id)
            .order_by(SearchHistory.created_at.desc())
            .limit(10)
            .all()
        )

        queries = [h.query for h in histories]
        recommendations = ai_service.get_ai_recommendations(queries)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recommendations: {str(e)}",
        )
