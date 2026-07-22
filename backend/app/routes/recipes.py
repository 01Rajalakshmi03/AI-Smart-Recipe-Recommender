from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.schemas.recipe import (
    RecipeCreate,
    RecipeUpdate,
    FavoriteCreate,
    CommentCreate,
    RatingCreate,
    MealPlanCreate,
    ShoppingListCreate,
    CategoryCreate,
)
from app.services import recipe_service
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.recipe import Rating

router = APIRouter(prefix="/api", tags=["Recipes"])


@router.get("/recipes")
def list_recipes(
    page: int = Query(1, ge=1),
    per_page: int = Query(12, ge=1, le=50),
    search: str = Query("", max_length=200),
    category_id: int = Query(None),
    cuisine: str = Query("", max_length=50),
    meal_type: str = Query("", max_length=30),
    difficulty: str = Query("", max_length=20),
    is_vegetarian: int = Query(None),
    is_vegan: int = Query(None),
    is_gluten_free: int = Query(None),
    is_non_veg: int = Query(None),
    is_keto: int = Query(None),
    is_dairy_free: int = Query(None),
    db: Session = Depends(get_db),
):
    return recipe_service.get_recipes(
        db, page, per_page, search, category_id, cuisine, meal_type, difficulty,
        is_vegetarian, is_vegan, is_gluten_free, is_non_veg, is_keto, is_dairy_free
    )


@router.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    try:
        recipe = recipe_service.get_recipe(db, recipe_id)
        avg_rating = db.query(func.avg(Rating.score)).filter(Rating.recipe_id == recipe_id).scalar() or 0
        rating_count = db.query(Rating).filter(Rating.recipe_id == recipe_id).count()

        return {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "instructions": recipe.instructions,
            "image": recipe.image,
            "cooking_time": recipe.cooking_time,
            "prep_time": recipe.prep_time,
            "servings": recipe.servings,
            "difficulty": recipe.difficulty,
            "cuisine": recipe.cuisine,
            "meal_type": recipe.meal_type,
            "calories": recipe.calories,
            "protein": recipe.protein,
            "carbs": recipe.carbs,
            "fat": recipe.fat,
            "is_vegetarian": recipe.is_vegetarian,
            "is_vegan": recipe.is_vegan,
            "is_gluten_free": recipe.is_gluten_free,
            "is_non_veg": recipe.is_non_veg,
            "is_keto": recipe.is_keto,
            "is_dairy_free": recipe.is_dairy_free,
            "is_ai_generated": recipe.is_ai_generated,
            "author_id": recipe.author_id,
            "category": recipe.category,
            "ingredients": recipe.ingredients,
            "average_rating": round(float(avg_rating), 1),
            "rating_count": rating_count,
            "created_at": recipe.created_at,
            "updated_at": recipe.updated_at,
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/recipes")
def create_recipe(
    recipe_data: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe = recipe_service.create_recipe(db, recipe_data, current_user.id)
    return {"id": recipe.id, "message": "Recipe created successfully"}


@router.put("/recipes/{recipe_id}")
def update_recipe(
    recipe_id: int,
    recipe_data: RecipeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        recipe_service.update_recipe(db, recipe_id, recipe_data)
        return {"message": "Recipe updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/recipes/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        recipe_service.delete_recipe(db, recipe_id)
        return {"message": "Recipe deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/favorites")
def toggle_favorite(
    data: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    is_favorite = recipe_service.toggle_favorite(db, current_user.id, data.recipe_id)
    return {"is_favorite": is_favorite, "message": "Added to favorites" if is_favorite else "Removed from favorites"}


@router.get("/favorites")
def get_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return recipe_service.get_user_favorites(db, current_user.id)


@router.post("/comments")
def add_comment(
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = recipe_service.add_comment(db, current_user.id, data)
    return {"id": comment.id, "message": "Comment added successfully"}


@router.get("/comments/{recipe_id}")
def get_comments(recipe_id: int, db: Session = Depends(get_db)):
    return recipe_service.get_recipe_comments(db, recipe_id)


@router.post("/ratings")
def add_rating(
    data: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rating = recipe_service.add_rating(db, current_user.id, data)
    return {"id": rating.id, "message": "Rating added successfully"}


@router.post("/meal-planner")
def create_meal_plan(
    data: MealPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plan = recipe_service.create_meal_plan(db, current_user.id, data)
    return {"id": plan.id, "message": "Meal plan created successfully"}


@router.get("/meal-planner")
def get_meal_plans(
    date: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return recipe_service.get_user_meal_plans(db, current_user.id, date)


@router.delete("/meal-planner/{plan_id}")
def delete_meal_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe_service.delete_meal_plan(db, plan_id, current_user.id)
    return {"message": "Meal plan deleted"}


@router.post("/shopping-list")
def add_shopping_item(
    data: ShoppingListCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = recipe_service.add_shopping_item(db, current_user.id, data)
    return {"id": item.id, "message": "Item added to shopping list"}


@router.get("/shopping-list")
def get_shopping_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return recipe_service.get_user_shopping_list(db, current_user.id)


@router.put("/shopping-list/{item_id}/toggle")
def toggle_shopping_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = recipe_service.toggle_shopping_item(db, item_id, current_user.id)
    return {"is_checked": item.is_checked if item else False}


@router.delete("/shopping-list/{item_id}")
def delete_shopping_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe_service.delete_shopping_item(db, item_id, current_user.id)
    return {"message": "Item deleted"}


@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    return recipe_service.get_categories(db)


@router.post("/categories")
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = recipe_service.create_category(db, data)
    return {"id": category.id, "message": "Category created"}


@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe_service.delete_category(db, category_id)
    return {"message": "Category deleted"}
