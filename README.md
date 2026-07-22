# AI Smart Recipe Recommender

An AI-powered recipe recommendation web application built with React, FastAPI, SQLite, and Google Gemini AI.

## Tech Stack

**Frontend:** React 19, Vite, Tailwind CSS, React Router DOM, Framer Motion, Axios, React Hook Form, Chart.js

**Backend:** Python, FastAPI, SQLAlchemy ORM, Pydantic, JWT Authentication, Passlib (bcrypt)

**Database:** SQLite

**AI:** Google Gemini API

## Features

- AI recipe generation from text prompts
- Recipe browsing with filters (cuisine, meal type, difficulty, dietary)
- User authentication (register, login, JWT)
- Favorites and saved recipes
- Meal planner with weekly view
- Shopping list management
- Recipe ratings and comments
- Admin dashboard with analytics
- Dark mode support
- Responsive design
- Toast notifications
- Page animations with Framer Motion

## Installation

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

Create a `.env` file in the backend folder:

```
JWT_SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-google-gemini-api-key
```

Run the backend:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login |
| GET | /api/auth/me | Get current user |
| PUT | /api/auth/me | Update profile |
| GET | /api/recipes | List recipes |
| GET | /api/recipes/:id | Get recipe detail |
| POST | /api/recipes | Create recipe |
| PUT | /api/recipes/:id | Update recipe |
| DELETE | /api/recipes/:id | Delete recipe |
| GET | /api/categories | List categories |
| POST | /api/favorites | Toggle favorite |
| GET | /api/favorites | Get favorites |
| POST | /api/comments | Add comment |
| GET | /api/comments/:id | Get recipe comments |
| POST | /api/ratings | Add rating |
| POST | /api/meal-planner | Create meal plan |
| GET | /api/meal-planner | Get meal plans |
| DELETE | /api/meal-planner/:id | Delete meal plan |
| POST | /api/shopping-list | Add item |
| GET | /api/shopping-list | Get shopping list |
| PUT | /api/shopping-list/:id/toggle | Toggle item |
| DELETE | /api/shopping-list/:id | Delete item |
| POST | /api/ai/generate | Generate recipe with AI |
| POST | /api/ai/explain | Explain recipe with AI |
| GET | /api/ai/recommendations | Get AI recommendations |
| GET | /api/admin/stats | Admin statistics |
| GET | /api/admin/users | List all users |
| DELETE | /api/admin/users/:id | Delete user |

## Database Schema

- **Users** - id, username, email, hashed_password, full_name, role, is_active, dark_mode
- **Recipes** - id, title, description, instructions, image, cooking_time, difficulty, cuisine, nutrition info
- **Categories** - id, name, slug, icon
- **Ingredients** - id, name, category, unit
- **RecipeIngredients** - recipe_id, ingredient_id, quantity, unit
- **Favorites** - user_id, recipe_id
- **Comments** - user_id, recipe_id, content
- **Ratings** - user_id, recipe_id, score
- **MealPlans** - user_id, recipe_id, date, meal_type
- **ShoppingLists** - user_id, item, quantity, is_checked
- **SearchHistories** - user_id, query

## Testing

```bash
cd backend
pytest
```

## Demo Credentials

- **Admin:** admin@example.com / admin123
- Register a new user through the signup page

## Future Improvements

- Recipe image upload
- Social sharing
- Nutritional tracking dashboard
- Shopping list sharing
- Recipe collections/cookbooks
- Voice-based recipe search
- Multi-language support
- Email notifications
- Recipe import from URLs
