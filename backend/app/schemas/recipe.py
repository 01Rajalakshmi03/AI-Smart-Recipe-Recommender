from datetime import datetime
from pydantic import BaseModel

from app.schemas.user import UserResponse


class IngredientBase(BaseModel):
    name: str
    category: str = ""
    unit: str = ""


class IngredientResponse(IngredientBase):
    id: int

    class Config:
        from_attributes = True


class RecipeIngredientBase(BaseModel):
    ingredient_id: int
    quantity: float = 0
    unit: str = ""
    notes: str = ""


class RecipeIngredientCreate(BaseModel):
    name: str
    quantity: float = 0
    unit: str = ""
    notes: str = ""


class RecipeIngredientResponse(BaseModel):
    id: int
    ingredient_id: int
    ingredient: IngredientResponse
    quantity: float
    unit: str
    notes: str

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str
    slug: str
    icon: str = ""
    image: str = ""
    description: str = ""


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RecipeBase(BaseModel):
    title: str
    description: str = ""
    instructions: str = ""
    image: str = ""
    cooking_time: int = 0
    prep_time: int = 0
    servings: int = 2
    difficulty: str = "Medium"
    cuisine: str = ""
    meal_type: str = ""
    calories: float = 0
    protein: float = 0
    carbs: float = 0
    fat: float = 0
    is_vegetarian: int = 0
    is_vegan: int = 0
    is_gluten_free: int = 0
    is_non_veg: int = 0
    is_keto: int = 0
    is_dairy_free: int = 0
    category_id: int | None = None


class RecipeCreate(RecipeBase):
    ingredients: list[RecipeIngredientCreate] = []


class RecipeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    instructions: str | None = None
    image: str | None = None
    cooking_time: int | None = None
    prep_time: int | None = None
    servings: int | None = None
    difficulty: str | None = None
    cuisine: str | None = None
    meal_type: str | None = None
    calories: float | None = None
    protein: float | None = None
    carbs: float | None = None
    fat: float | None = None
    is_vegetarian: int | None = None
    is_vegan: int | None = None
    is_gluten_free: int | None = None
    is_non_veg: int | None = None
    is_keto: int | None = None
    is_dairy_free: int | None = None
    category_id: int | None = None


class RecipeResponse(RecipeBase):
    id: int
    is_ai_generated: int
    author_id: int | None
    category: CategoryResponse | None = None
    ingredients: list[RecipeIngredientResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RecipeListResponse(BaseModel):
    id: int
    title: str
    description: str
    image: str
    cooking_time: int
    difficulty: str
    cuisine: str
    meal_type: str
    calories: float
    is_vegetarian: int
    is_vegan: int
    is_gluten_free: int
    is_non_veg: int
    is_keto: int
    is_dairy_free: int
    is_ai_generated: int
    category: CategoryResponse | None = None
    average_rating: float = 0
    rating_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    recipe_id: int


class CommentResponse(CommentBase):
    id: int
    user_id: int
    recipe_id: int
    user: UserResponse
    created_at: datetime

    class Config:
        from_attributes = True


class RatingBase(BaseModel):
    score: int


class RatingCreate(RatingBase):
    recipe_id: int


class RatingResponse(RatingBase):
    id: int
    user_id: int
    recipe_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FavoriteCreate(BaseModel):
    recipe_id: int


class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    recipe_id: int
    recipe: RecipeListResponse | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class MealPlanCreate(BaseModel):
    date: str
    meal_type: str
    recipe_id: int


class MealPlanResponse(BaseModel):
    id: int
    date: str
    meal_type: str
    user_id: int
    recipe_id: int
    recipe: RecipeListResponse | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class ShoppingListCreate(BaseModel):
    item: str
    quantity: str = ""


class ShoppingListResponse(BaseModel):
    id: int
    item: str
    quantity: str
    is_checked: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SearchHistoryResponse(BaseModel):
    id: int
    query: str
    created_at: datetime

    class Config:
        from_attributes = True


class AIGenerateRequest(BaseModel):
    prompt: str
    meal_type: str = ""
    cuisine: str = ""
    dietary: str = ""


class AIGenerateResponse(BaseModel):
    recipe: RecipeResponse
    explanation: str = ""


class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    per_page: int
    pages: int
