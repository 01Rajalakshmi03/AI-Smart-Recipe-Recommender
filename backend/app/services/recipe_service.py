from math import ceil

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.recipe import (
    Recipe,
    Category,
    Ingredient,
    RecipeIngredient,
    Favorite,
    Comment,
    Rating,
    MealPlan,
    ShoppingList,
    SearchHistory,
)
from app.schemas.recipe import (
    RecipeCreate,
    RecipeUpdate,
    CommentCreate,
    RatingCreate,
    FavoriteCreate,
    MealPlanCreate,
    ShoppingListCreate,
    CategoryCreate,
)


def get_recipes(
    db: Session,
    page: int = 1,
    per_page: int = 12,
    search: str = "",
    category_id: int = None,
    cuisine: str = "",
    meal_type: str = "",
    difficulty: str = "",
    is_vegetarian: int = None,
    is_vegan: int = None,
    is_gluten_free: int = None,
    is_non_veg: int = None,
    is_keto: int = None,
    is_dairy_free: int = None,
):
    query = db.query(Recipe)

    if search:
        query = query.filter(
            Recipe.title.ilike(f"%{search}%") | Recipe.description.ilike(f"%{search}%")
        )
    if category_id:
        query = query.filter(Recipe.category_id == category_id)
    if cuisine:
        query = query.filter(Recipe.cuisine.ilike(f"%{cuisine}%"))
    if meal_type:
        query = query.filter(Recipe.meal_type == meal_type)
    if difficulty:
        query = query.filter(Recipe.difficulty == difficulty)
    if is_vegetarian is not None:
        query = query.filter(Recipe.is_vegetarian == is_vegetarian)
    if is_vegan is not None:
        query = query.filter(Recipe.is_vegan == is_vegan)
    if is_gluten_free is not None:
        query = query.filter(Recipe.is_gluten_free == is_gluten_free)
    if is_non_veg is not None:
        query = query.filter(Recipe.is_non_veg == is_non_veg)
    if is_keto is not None:
        query = query.filter(Recipe.is_keto == is_keto)
    if is_dairy_free is not None:
        query = query.filter(Recipe.is_dairy_free == is_dairy_free)

    total = query.count()
    pages = ceil(total / per_page) if per_page else 1
    recipes = query.offset((page - 1) * per_page).limit(per_page).all()

    result = []
    for recipe in recipes:
        avg_rating = db.query(func.avg(Rating.score)).filter(Rating.recipe_id == recipe.id).scalar() or 0
        rating_count = db.query(Rating).filter(Rating.recipe_id == recipe.id).count()
        recipe_dict = {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "image": recipe.image,
            "cooking_time": recipe.cooking_time,
            "difficulty": recipe.difficulty,
            "cuisine": recipe.cuisine,
            "meal_type": recipe.meal_type,
            "calories": recipe.calories,
            "is_vegetarian": recipe.is_vegetarian,
            "is_vegan": recipe.is_vegan,
            "is_gluten_free": recipe.is_gluten_free,
            "is_non_veg": recipe.is_non_veg,
            "is_keto": recipe.is_keto,
            "is_dairy_free": recipe.is_dairy_free,
            "is_ai_generated": recipe.is_ai_generated,
            "category": recipe.category,
            "average_rating": round(float(avg_rating), 1),
            "rating_count": rating_count,
            "created_at": recipe.created_at,
        }
        result.append(recipe_dict)

    return {
        "items": result,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
    }


def get_recipe(db: Session, recipe_id: int) -> Recipe:
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise ValueError("Recipe not found")
    return recipe


def create_recipe(db: Session, recipe_data: RecipeCreate, author_id: int = None) -> Recipe:
    recipe = Recipe(
        title=recipe_data.title,
        description=recipe_data.description,
        instructions=recipe_data.instructions,
        image=recipe_data.image,
        cooking_time=recipe_data.cooking_time,
        prep_time=recipe_data.prep_time,
        servings=recipe_data.servings,
        difficulty=recipe_data.difficulty,
        cuisine=recipe_data.cuisine,
        meal_type=recipe_data.meal_type,
        calories=recipe_data.calories,
        protein=recipe_data.protein,
        carbs=recipe_data.carbs,
        fat=recipe_data.fat,
        is_vegetarian=recipe_data.is_vegetarian,
        is_vegan=recipe_data.is_vegan,
        is_gluten_free=recipe_data.is_gluten_free,
        is_non_veg=recipe_data.is_non_veg,
        is_keto=recipe_data.is_keto,
        is_dairy_free=recipe_data.is_dairy_free,
        category_id=recipe_data.category_id,
        author_id=author_id,
    )
    db.add(recipe)
    db.flush()

    for ing_data in recipe_data.ingredients:
        ingredient = db.query(Ingredient).filter(
            Ingredient.name.ilike(ing_data.name)
        ).first()
        if not ingredient:
            ingredient = Ingredient(name=ing_data.name)
            db.add(ingredient)
            db.flush()

        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            quantity=ing_data.quantity,
            unit=ing_data.unit,
            notes=ing_data.notes,
        )
        db.add(recipe_ingredient)

    db.commit()
    db.refresh(recipe)
    return recipe


def update_recipe(db: Session, recipe_id: int, update_data: RecipeUpdate) -> Recipe:
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise ValueError("Recipe not found")

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(recipe, key, value)

    db.commit()
    db.refresh(recipe)
    return recipe


def delete_recipe(db: Session, recipe_id: int):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise ValueError("Recipe not found")
    db.delete(recipe)
    db.commit()


def toggle_favorite(db: Session, user_id: int, recipe_id: int) -> bool:
    existing = db.query(Favorite).filter(
        Favorite.user_id == user_id, Favorite.recipe_id == recipe_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return False
    else:
        favorite = Favorite(user_id=user_id, recipe_id=recipe_id)
        db.add(favorite)
        db.commit()
        return True


def get_user_favorites(db: Session, user_id: int):
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()


def add_comment(db: Session, user_id: int, data: CommentCreate) -> Comment:
    comment = Comment(content=data.content, user_id=user_id, recipe_id=data.recipe_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_recipe_comments(db: Session, recipe_id: int):
    return db.query(Comment).filter(Comment.recipe_id == recipe_id).order_by(Comment.created_at.desc()).all()


def add_rating(db: Session, user_id: int, data: RatingCreate) -> Rating:
    existing = db.query(Rating).filter(
        Rating.user_id == user_id, Rating.recipe_id == data.recipe_id
    ).first()
    if existing:
        existing.score = data.score
        db.commit()
        db.refresh(existing)
        return existing

    rating = Rating(score=data.score, user_id=user_id, recipe_id=data.recipe_id)
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating


def create_meal_plan(db: Session, user_id: int, data: MealPlanCreate) -> MealPlan:
    plan = MealPlan(
        date=data.date,
        meal_type=data.meal_type,
        user_id=user_id,
        recipe_id=data.recipe_id,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def get_user_meal_plans(db: Session, user_id: int, date: str = None):
    query = db.query(MealPlan).filter(MealPlan.user_id == user_id)
    if date:
        query = query.filter(MealPlan.date == date)
    return query.order_by(MealPlan.date).all()


def delete_meal_plan(db: Session, plan_id: int, user_id: int):
    plan = db.query(MealPlan).filter(MealPlan.id == plan_id, MealPlan.user_id == user_id).first()
    if plan:
        db.delete(plan)
        db.commit()


def add_shopping_item(db: Session, user_id: int, data: ShoppingListCreate) -> ShoppingList:
    item = ShoppingList(item=data.item, quantity=data.quantity, user_id=user_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_user_shopping_list(db: Session, user_id: int):
    return db.query(ShoppingList).filter(ShoppingList.user_id == user_id).all()


def toggle_shopping_item(db: Session, item_id: int, user_id: int) -> ShoppingList:
    item = db.query(ShoppingList).filter(
        ShoppingList.id == item_id, ShoppingList.user_id == user_id
    ).first()
    if item:
        item.is_checked = 1 - item.is_checked
        db.commit()
        db.refresh(item)
    return item


def delete_shopping_item(db: Session, item_id: int, user_id: int):
    item = db.query(ShoppingList).filter(
        ShoppingList.id == item_id, ShoppingList.user_id == user_id
    ).first()
    if item:
        db.delete(item)
        db.commit()


def add_search_history(db: Session, user_id: int, query: str):
    history = SearchHistory(query=query, user_id=user_id)
    db.add(history)
    db.commit()


def get_categories(db: Session):
    return db.query(Category).all()


def create_category(db: Session, data: CategoryCreate) -> Category:
    category = Category(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()


def get_admin_stats(db: Session):
    from app.models.user import User
    return {
        "total_users": db.query(User).count(),
        "total_recipes": db.query(Recipe).count(),
        "total_categories": db.query(Category).count(),
        "total_comments": db.query(Comment).count(),
        "ai_generated": db.query(Recipe).filter(Recipe.is_ai_generated == 1).count(),
    }


def get_all_users(db: Session):
    return db.query(User).all()


def delete_user(db: Session, user_id: int):
    from app.models.user import User
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()


def get_all_recipes_admin(db: Session):
    return db.query(Recipe).all()


def get_all_comments_admin(db: Session):
    return db.query(Comment).all()


def delete_comment(db: Session, comment_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
