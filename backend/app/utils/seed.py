from app.database.database import SessionLocal
from app.models.user import User
from app.models.recipe import Recipe, Category, Ingredient, RecipeIngredient, Favorite, Comment, Rating, MealPlan, ShoppingList, SearchHistory
from app.utils.security import hash_password


def seed_data():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@example.com",
                hashed_password=hash_password("admin123"),
                full_name="Admin User",
                role="admin",
            )
            db.add(admin)
            db.flush()

        existing_count = db.query(Category).count()
        if existing_count >= 15:
            db.commit()
            return

        if existing_count > 0:
            db.query(RecipeIngredient).delete()
            db.query(Favorite).delete()
            db.query(Comment).delete()
            db.query(Rating).delete()
            db.query(MealPlan).delete()
            db.query(ShoppingList).delete()
            db.query(SearchHistory).delete()
            db.query(Ingredient).delete()
            db.query(Recipe).delete()
            db.query(Category).delete()
            db.flush()

        categories = [
            Category(name="Breakfast", slug="breakfast", icon="🍳", description="Start your day right"),
            Category(name="Lunch", slug="lunch", icon="🥗", description="Midday meals"),
            Category(name="Dinner", slug="dinner", icon="🍽️", description="Evening feasts"),
            Category(name="Snacks", slug="snacks", icon="🍿", description="Quick bites"),
            Category(name="Desserts", slug="desserts", icon="🍰", description="Sweet treats"),
            Category(name="Beverages", slug="beverages", icon="🥤", description="Refreshing drinks"),
            Category(name="Seafood", slug="seafood", icon="🦐", description="Ocean flavors"),
            Category(name="BBQ & Grill", slug="bbq-grill", icon="🔥", description="Smoky grilled goodness"),
            Category(name="Pasta & Noodles", slug="pasta-noodles", icon="🍝", description="Noodle and pasta delights"),
            Category(name="Soups & Stews", slug="soups-stews", icon="🍲", description="Warm and comforting"),
            Category(name="Salads", slug="salads", icon="🥬", description="Fresh and healthy greens"),
            Category(name="Indian", slug="indian", icon="🍛", description="Authentic Indian cuisine"),
            Category(name="Mexican", slug="mexican", icon="🌮", description="Bold Mexican flavors"),
            Category(name="Thai", slug="thai", icon="🍜", description="Aromatic Thai dishes"),
            Category(name="Quick Meals", slug="quick-meals", icon="⚡", description="Ready in 15 minutes"),
        ]
        db.add_all(categories)
        db.flush()

        sample_recipes = [
            # ── BREAKFAST ──
            {
                "title": "Classic Pancakes",
                "description": "Fluffy golden pancakes perfect for a weekend breakfast",
                "instructions": "1. Mix dry ingredients in a bowl. 2. Whisk wet ingredients separately. 3. Combine until just mixed. 4. Heat a non-stick pan. 5. Pour 1/4 cup batter per pancake. 6. Cook until bubbles form, then flip. 7. Serve with maple syrup and fresh berries.",
                "image": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=500",
                "cooking_time": 20, "prep_time": 10, "servings": 4,
                "difficulty": "Easy", "cuisine": "American", "meal_type": "breakfast",
                "calories": 350, "protein": 8, "carbs": 45, "fat": 12,
                "is_vegetarian": 1, "category_id": 1,
                "ingredients": [
                    ("All-purpose flour", 1.5, "cups", ""), ("Sugar", 2, "tbsp", ""),
                    ("Baking powder", 2, "tsp", ""), ("Salt", 0.5, "tsp", ""),
                    ("Milk", 1.25, "cups", ""), ("Egg", 1, "large", ""),
                    ("Butter", 3, "tbsp", "melted"),
                ],
            },
            {
                "title": "Eggs Benedict",
                "description": "Classic brunch dish with poached eggs and hollandaise sauce",
                "instructions": "1. Toast English muffins. 2. Poach eggs in simmering water with vinegar. 3. Make hollandaise: whisk egg yolks and lemon juice over double boiler. 4. Slowly add melted butter while whisking. 5. Season with salt and cayenne. 6. Layer muffin, ham, egg, and sauce.",
                "image": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=500",
                "cooking_time": 15, "prep_time": 15, "servings": 2,
                "difficulty": "Hard", "cuisine": "American", "meal_type": "breakfast",
                "calories": 480, "protein": 24, "carbs": 28, "fat": 30,
                "is_vegetarian": 1, "category_id": 1,
                "ingredients": [
                    ("English muffin", 2, "halves", ""), ("Egg", 4, "large", ""),
                    ("Ham", 4, "slices", ""), ("Butter", 0.5, "cup", "melted"),
                    ("Lemon juice", 1, "tbsp", ""), ("White vinegar", 1, "tbsp", ""),
                ],
            },
            {
                "title": "Avocado Toast with Eggs",
                "description": "Crispy toast topped with creamy avocado and perfectly fried eggs",
                "instructions": "1. Toast sourdough bread until golden. 2. Mash avocado with salt, pepper, and lemon juice. 3. Fry eggs sunny-side up. 4. Spread avocado on toast. 5. Top with fried egg. 6. Sprinkle with chili flakes and everything bagel seasoning.",
                "image": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=500",
                "cooking_time": 5, "prep_time": 5, "servings": 1,
                "difficulty": "Easy", "cuisine": "American", "meal_type": "breakfast",
                "calories": 380, "protein": 16, "carbs": 30, "fat": 24,
                "is_vegetarian": 1, "is_dairy_free": 1, "category_id": 1,
                "ingredients": [
                    ("Sourdough bread", 2, "slices", ""), ("Avocado", 1, "large", "ripe"),
                    ("Egg", 2, "large", ""), ("Lemon juice", 1, "tsp", ""),
                    ("Chili flakes", 0.5, "tsp", ""),
                ],
            },
            {
                "title": "Chicken & Cheese Omelette",
                "description": "Fluffy omelette loaded with grilled chicken and melted cheese",
                "instructions": "1. Whisk eggs with salt and pepper. 2. Cook diced chicken in a pan until golden. 3. Pour egg mixture into the pan. 4. Let it set, add shredded cheese on one half. 5. Fold and cook until cheese melts. 6. Serve with toast.",
                "image": "https://images.unsplash.com/photo-1510693206972-df098062cb71?w=500",
                "cooking_time": 10, "prep_time": 10, "servings": 1,
                "difficulty": "Easy", "cuisine": "American", "meal_type": "breakfast",
                "calories": 420, "protein": 34, "carbs": 2, "fat": 30,
                "is_vegetarian": 0, "is_non_veg": 1, "category_id": 1,
                "ingredients": [
                    ("Egg", 3, "large", ""), ("Chicken breast", 100, "g", "diced"),
                    ("Cheddar cheese", 0.25, "cup", "shredded"), ("Butter", 1, "tbsp", ""),
                    ("Salt", 0.25, "tsp", ""), ("Black pepper", 0.25, "tsp", ""),
                ],
            },

            # ── LUNCH ──
            {
                "title": "Mediterranean Quinoa Bowl",
                "description": "A healthy and colorful bowl packed with Mediterranean flavors",
                "instructions": "1. Cook quinoa according to package directions. 2. Dice cucumber, tomatoes, and red onion. 3. Crumble feta cheese. 4. Mix all ingredients in a bowl. 5. Drizzle with olive oil and lemon juice. 6. Season with salt, pepper, and oregano.",
                "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500",
                "cooking_time": 25, "prep_time": 15, "servings": 2,
                "difficulty": "Easy", "cuisine": "Mediterranean", "meal_type": "lunch",
                "calories": 420, "protein": 15, "carbs": 52, "fat": 18,
                "is_vegetarian": 1, "category_id": 2,
                "ingredients": [
                    ("Quinoa", 1, "cup", ""), ("Cucumber", 1, "medium", "diced"),
                    ("Cherry tomatoes", 1, "cup", "halved"), ("Red onion", 0.5, "medium", "diced"),
                    ("Feta cheese", 0.5, "cup", "crumbled"), ("Olive oil", 2, "tbsp", ""),
                    ("Lemon juice", 1, "tbsp", ""),
                ],
            },
            {
                "title": "Caesar Salad",
                "description": "Classic Caesar salad with crispy croutons and parmesan",
                "instructions": "1. Wash and chop romaine lettuce. 2. Make dressing with mayo, lemon, garlic, anchovy, and parmesan. 3. Toast bread cubes with olive oil for croutons. 4. Toss lettuce with dressing. 5. Top with croutons, shaved parmesan, and black pepper.",
                "image": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?w=500",
                "cooking_time": 10, "prep_time": 15, "servings": 2,
                "difficulty": "Easy", "cuisine": "Italian", "meal_type": "lunch",
                "calories": 310, "protein": 12, "carbs": 18, "fat": 22,
                "is_vegetarian": 1, "category_id": 11,
                "ingredients": [
                    ("Romaine lettuce", 1, "head", "chopped"), ("Parmesan cheese", 0.25, "cup", "shaved"),
                    ("Bread", 2, "slices", "cubed"), ("Olive oil", 2, "tbsp", ""),
                    ("Lemon juice", 2, "tbsp", ""), ("Mayonnaise", 3, "tbsp", ""),
                ],
            },
            {
                "title": "Chicken Caesar Wrap",
                "description": "Grilled chicken wrapped in a tortilla with Caesar dressing",
                "instructions": "1. Season and grill chicken breast until cooked through. 2. Slice chicken into strips. 3. Lay out tortilla and spread Caesar dressing. 4. Add romaine lettuce, parmesan, and chicken. 5. Roll tightly and slice in half.",
                "image": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=500",
                "cooking_time": 15, "prep_time": 10, "servings": 2,
                "difficulty": "Easy", "cuisine": "American", "meal_type": "lunch",
                "calories": 450, "protein": 32, "carbs": 34, "fat": 20,
                "is_vegetarian": 0, "is_non_veg": 1, "category_id": 2,
                "ingredients": [
                    ("Chicken breast", 200, "g", ""), ("Flour tortilla", 2, "large", ""),
                    ("Romaine lettuce", 2, "cups", "chopped"), ("Caesar dressing", 3, "tbsp", ""),
                    ("Parmesan cheese", 2, "tbsp", "shaved"),
                ],
            },
            {
                "title": "Tuna Salad Sandwich",
                "description": "Creamy tuna salad with crisp celery on toasted bread",
                "instructions": "1. Drain canned tuna and flake into a bowl. 2. Mix with mayo, diced celery, red onion, and lemon juice. 3. Season with salt and pepper. 4. Toast bread slices. 5. Spread tuna salad on bread. 6. Add lettuce and tomato. 7. Close and serve.",
                "image": "https://images.unsplash.com/photo-1553909489-cd47e0907980?w=500",
                "cooking_time": 0, "prep_time": 10, "servings": 2,
                "difficulty": "Easy", "cuisine": "American", "meal_type": "lunch",
                "calories": 380, "protein": 28, "carbs": 30, "fat": 16,
                "is_vegetarian": 0, "is_non_veg": 1, "category_id": 2,
                "ingredients": [
                    ("Canned tuna", 2, "cans", "drained"), ("Mayonnaise", 2, "tbsp", ""),
                    ("Celery", 2, "stalks", "diced"), ("Red onion", 2, "tbsp", "diced"),
                    ("Bread", 4, "slices", ""), ("Lettuce", 2, "leaves", ""),
                ],
            },

            # ── DINNER ──
            {
                "title": "Grilled Chicken Breast",
                "description": "Juicy, perfectly seasoned grilled chicken breast",
                "instructions": "1. Marinate chicken with olive oil, garlic, herbs for 30 minutes. 2. Preheat grill to medium-high. 3. Grill chicken 6-7 minutes per side. 4. Rest for 5 minutes before slicing. 5. Serve with your favorite sides.",
                "image": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=500",
                "cooking_time": 15, "prep_time": 35, "servings": 2,
                "difficulty": "Medium", "cuisine": "American", "meal_type": "dinner",
                "calories": 280, "protein": 35, "carbs": 2, "fat": 14,
                "is_vegetarian": 0, "is_non_veg": 1, "is_gluten_free": 1, "category_id": 8,
                "ingredients": [
                    ("Chicken breast", 2, "pieces", ""), ("Olive oil", 2, "tbsp", ""),
                    ("Garlic", 3, "cloves", "minced"), ("Italian herbs", 1, "tsp", ""),
                    ("Salt", 1, "tsp", ""), ("Black pepper", 0.5, "tsp", ""),
                ],
            },
            {
                "title": "Vegetable Stir Fry",
                "description": "Quick and colorful vegetable stir fry with savory sauce",
                "instructions": "1. Cut all vegetables into bite-sized pieces. 2. Heat oil in a wok over high heat. 3. Add vegetables starting with hardest first. 4. Stir fry for 3-4 minutes. 5. Add sauce and toss to coat. 6. Serve over steamed rice.",
                "image": "https://images.unsplash.com/photo-1543339308-d595c4f4cbb0?w=500",
                "cooking_time": 10, "prep_time": 15, "servings": 3,
                "difficulty": "Easy", "cuisine": "Asian", "meal_type": "dinner",
                "calories": 180, "protein": 6, "carbs": 22, "fat": 8,
                "is_vegetarian": 1, "is_vegan": 1, "category_id": 3,
                "ingredients": [
                    ("Broccoli", 2, "cups", "florets"), ("Bell pepper", 1, "large", "sliced"),
                    ("Carrot", 1, "medium", "julienned"), ("Snap peas", 1, "cup", ""),
                    ("Soy sauce", 2, "tbsp", ""), ("Sesame oil", 1, "tbsp", ""),
                    ("Ginger", 1, "tbsp", "minced"),
                ],
            },
            {
                "title": "Spicy Indian Curry",
                "description": "Rich and aromatic Indian curry with tender vegetables",
                "instructions": "1. Heat oil and sauté onions until golden. 2. Add garlic and ginger, cook 1 minute. 3. Add spices and toast for 30 seconds. 4. Add tomatoes and cook down. 5. Add vegetables and coconut milk. 6. Simmer 15-20 minutes. 7. Garnish with cilantro and serve with rice.",
                "image": "https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=500",
                "cooking_time": 30, "prep_time": 15, "servings": 4,
                "difficulty": "Medium", "cuisine": "Indian", "meal_type": "dinner",
                "calories": 320, "protein": 10, "carbs": 28, "fat": 20,
                "is_vegetarian": 1, "is_vegan": 1, "category_id": 12,
                "ingredients": [
                    ("Onion", 2, "large", "diced"), ("Garlic", 4, "cloves", "minced"),
                    ("Ginger", 1, "tbsp", "grated"), ("Curry powder", 2, "tbsp", ""),
                    ("Coconut milk", 1, "can", ""), ("Chickpeas", 1, "can", "drained"),
                    ("Spinach", 2, "cups", ""),
                ],
            },
            {
                "title": "Butter Chicken",
                "description": "Creamy, mildly spiced tomato-based chicken curry",
                "instructions": "1. Marinate chicken in yogurt and spices for 1 hour. 2. Grill or pan-fry chicken until charred. 3. Sauté onions, garlic, ginger. 4. Add tomato puree and simmer. 5. Add cream and butter. 6. Add cooked chicken. 7. Simmer 10 minutes. 8. Garnish with cream and cilantro.",
                "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=500",
                "cooking_time": 40, "prep_time": 60, "servings": 4,
                "difficulty": "Medium", "cuisine": "Indian", "meal_type": "dinner",
                "calories": 450, "protein": 32, "carbs": 18, "fat": 30,
                "is_vegetarian": 0, "is_non_veg": 1, "is_gluten_free": 1, "category_id": 12,
                "ingredients": [
                    ("Chicken thighs", 500, "g", ""), ("Yogurt", 0.5, "cup", ""),
                    ("Butter", 3, "tbsp", ""), ("Tomato puree", 1, "cup", ""),
                    ("Heavy cream", 0.5, "cup", ""), ("Garam masala", 1, "tbsp", ""),
                    ("Kashmiri chili", 1, "tsp", ""), ("Garlic", 4, "cloves", "minced"),
                ],
            },
            {
                "title": "Fish Tacos",
                "description": "Crispy battered fish in warm tortillas with slaw and lime",
                "instructions": "1. Cut fish into strips and season with spices. 2. Dip in beer batter and fry until golden. 3. Make slaw with cabbage, lime, and mayo. 4. Warm tortillas. 5. Assemble tacos with fish, slaw, and avocado. 6. Squeeze lime on top.",
                "image": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=500",
                "cooking_time": 15, "prep_time": 20, "servings": 4,
                "difficulty": "Medium", "cuisine": "Mexican", "meal_type": "dinner",
                "calories": 380, "protein": 24, "carbs": 36, "fat": 16,
                "is_vegetarian": 0, "is_non_veg": 1, "category_id": 13,
                "ingredients": [
                    ("White fish fillets", 400, "g", ""), ("Corn tortillas", 8, "small", ""),
                    ("Cabbage", 2, "cups", "shredded"), ("Lime", 2, "medium", ""),
                    ("Mayonnaise", 2, "tbsp", ""), ("Avocado", 1, "large", ""),
                    ("Beer", 0.5, "cup", "for batter"),
                ],
            },
            {
                "title": "Spaghetti Bolognese",
                "description": "Rich meat sauce over perfectly cooked spaghetti",
                "instructions": "1. Cook spaghetti according to package directions. 2. Brown ground beef in a pan. 3. Add onions, garlic, carrots, celery. 4. Add crushed tomatoes and tomato paste. 5. Season with Italian herbs, salt, and pepper. 6. Simmer 30 minutes. 7. Serve sauce over spaghetti with parmesan.",
                "image": "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=500",
                "cooking_time": 30, "prep_time": 15, "servings": 4,
                "difficulty": "Easy", "cuisine": "Italian", "meal_type": "dinner",
                "calories": 520, "protein": 28, "carbs": 60, "fat": 18,
                "is_vegetarian": 0, "is_non_veg": 1, "category_id": 9,
                "ingredients": [
                    ("Spaghetti", 400, "g", ""), ("Ground beef", 400, "g", ""),
                    ("Onion", 1, "large", "diced"), ("Garlic", 3, "cloves", "minced"),
                    ("Crushed tomatoes", 1, "can", ""), ("Carrot", 1, "medium", "diced"),
                    ("Italian herbs", 1, "tbsp", ""),
                ],
            },
            {
                "title": "Chicken Tikka Masala",
                "description": "Tender chicken in a rich, creamy tomato-spice sauce",
                "instructions": "1. Marinate chicken in yogurt and tikka spices for 1 hour. 2. Grill chicken until slightly charred. 3. Sauté onions, garlic, ginger. 4. Add tomato sauce and spices. 5. Add cream and grilled chicken. 6. Simmer 15 minutes. 7. Serve with naan or rice.",
                "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=500",
                "cooking_time": 35, "prep_time": 60, "servings": 4,
                "difficulty": "Medium", "cuisine": "Indian", "meal_type": "dinner",
                "calories": 480, "protein": 34, "carbs": 22, "fat": 28,
                "is_vegetarian": 0, "is_non_veg": 1, "is_gluten_free": 1, "category_id": 12,
                "ingredients": [
                    ("Chicken breast", 500, "g", "cubed"), ("Yogurt", 0.5, "cup", ""),
                    ("Tomato sauce", 1, "cup", ""), ("Heavy cream", 0.25, "cup", ""),
                    ("Garam masala", 1, "tbsp", ""), ("Turmeric", 1, "tsp", ""),
                    ("Garlic", 3, "cloves", "minced"), ("Onion", 1, "large", "diced"),
                ],
            },
            {
                "title": "Grilled Salmon",
                "description": "Perfectly grilled salmon with lemon herb butter",
                "instructions": "1. Pat salmon dry and season with salt and pepper. 2. Heat grill to medium-high. 3. Oil the grates well. 4. Grill salmon skin-side down for 4-5 minutes. 5. Flip carefully and grill 3-4 more minutes. 6. Top with lemon herb butter and serve.",
                "image": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=500",
                "cooking_time": 10, "prep_time": 10, "servings": 2,
                "difficulty": "Medium", "cuisine": "American", "meal_type": "dinner",
                "calories": 360, "protein": 34, "carbs": 0, "fat": 24,
                "is_vegetarian": 0, "is_non_veg": 1, "is_gluten_free": 1, "is_keto": 1,
                "category_id": 7,
                "ingredients": [
                    ("Salmon fillets", 2, "pieces", ""), ("Butter", 2, "tbsp", "softened"),
                    ("Lemon", 1, "medium", "juiced"), ("Fresh dill", 1, "tbsp", "chopped"),
                    ("Garlic", 1, "clove", "minced"), ("Salt", 0.5, "tsp", ""),
                ],
            },
            {
                "title": "Shrimp Scampi",
                "description": "Succulent shrimp in a garlic butter white wine sauce over pasta",
                "instructions": "1. Cook linguine according to package. 2. Sauté garlic in butter and olive oil. 3. Add shrimp and cook 2 minutes per side. 4. Add white wine and lemon juice. 5. Simmer 2 minutes. 6. Toss with pasta and parsley.",
                "image": "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=500",
                "cooking_time": 15, "prep_time": 10, "servings": 2,
                "difficulty": "Easy", "cuisine": "Italian", "meal_type": "dinner",
                "calories": 520, "protein": 30, "carbs": 54, "fat": 18,
                "is_vegetarian": 0, "is_non_veg": 1, "category_id": 9,
                "ingredients": [
                    ("Linguine", 200, "g", ""), ("Shrimp", 300, "g", "peeled"),
                    ("Butter", 3, "tbsp", ""), ("Garlic", 4, "cloves", "minced"),
                    ("White wine", 0.25, "cup", ""), ("Lemon", 1, "medium", "juiced"),
                    ("Parsley", 2, "tbsp", "chopped"),
                ],
            },
            {
                "title": "Chicken Alfredo",
                "description": "Creamy alfredo pasta with grilled chicken and parmesan",
                "instructions": "1. Cook fettuccine according to package. 2. Season and grill chicken breast. 3. Slice chicken. 4. Make alfredo sauce: melt butter, add cream, parmesan, garlic. 5. Toss pasta in sauce. 6. Top with sliced chicken and parsley.",
                "image": "https://images.unsplash.com/photo-1645112411341-6c4fd023714a?w=500",
                "cooking_time": 20, "prep_time": 15, "servings": 4,
                "difficulty": "Easy", "cuisine": "Italian", "meal_type": "dinner",
                "calories": 620, "protein": 38, "carbs": 52, "fat": 30,
                "is_vegetarian": 0, "is_non_veg": 1, "category_id": 9,
                "ingredients": [
                    ("Fettuccine", 400, "g", ""), ("Chicken breast", 2, "pieces", ""),
                    ("Butter", 4, "tbsp", ""), ("Heavy cream", 1, "cup", ""),
                    ("Parmesan cheese", 1, "cup", "grated"), ("Garlic", 2, "cloves", "minced"),
                ],
            },
            {
                "title": "BBQ Pulled Pork Sandwich",
                "description": "Slow-cooked pulled pork with tangy BBQ sauce on a brioche bun",
                "instructions": "1. Season pork shoulder with dry rub. 2. Slow cook at 225°F for 8 hours. 3. Shred the pork with forks. 4. Mix with BBQ sauce. 5. Toast brioche buns. 6. Pile pulled pork on buns. 7. Top with coleslaw.",
                "image": "https://images.unsplash.com/photo-1529006557810-274b9b2fc783?w=500",
                "cooking_time": 480, "prep_time": 20, "servings": 8,
                "difficulty": "Medium", "cuisine": "American", "meal_type": "dinner",
                "calories": 550, "protein": 32, "carbs": 48, "fat": 24,
                "is_vegetarian": 0, "is_non_veg": 1, "category_id": 8,
                "ingredients": [
                    ("Pork shoulder", 1.5, "kg", ""), ("BBQ sauce", 1, "cup", ""),
                    ("Brioche buns", 8, "pieces", ""), ("Brown sugar", 2, "tbsp", ""),
                    ("Smoked paprika", 1, "tbsp", ""), ("Coleslaw", 2, "cups", ""),
                ],
            },
            {
                "title": "Lamb Gyros",
                "description": "Greek-style seasoned lamb with tzatziki in warm pita",
                "instructions": "1. Season lamb slices with oregano, garlic, lemon. 2. Grill lamb until cooked. 3. Make tzatziki: mix yogurt, cucumber, dill, garlic. 4. Warm pita bread. 5. Fill pita with lamb, tzatziki, tomatoes, onions. 6. Wrap and serve.",
                "image": "https://images.unsplash.com/photo-1529006557810-274b9b2fc783?w=500",
                "cooking_time": 15, "prep_time": 30, "servings": 4,
                "difficulty": "Medium", "cuisine": "Mediterranean", "meal_type": "dinner",
                "calories": 480, "protein": 28, "carbs": 38, "fat": 22,
                "is_vegetarian": 0, "is_non_veg": 1, "category_id": 3,
                "ingredients": [
                    ("Lamb leg slices", 400, "g", ""), ("Pita bread", 4, "pieces", ""),
                    ("Greek yogurt", 1, "cup", ""), ("Cucumber", 0.5, "medium", "grated"),
                    ("Dill", 1, "tbsp", "chopped"), ("Tomato", 1, "medium", "sliced"),
                    ("Red onion", 0.5, "medium", "sliced"),
                ],
            },
            {
                "title": "Paneer Butter Masala",
                "description": "Creamy tomato-based curry with soft paneer cubes",
                "instructions": "1. Sauté onions, garlic, ginger until golden. 2. Add tomatoes and cook down. 3. Blend into smooth sauce. 4. Add butter, cream, and spices. 5. Add paneer cubes. 6. Simmer 10 minutes. 7. Garnish with cream and kasuri methi.",
                "image": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=500",
                "cooking_time": 25, "prep_time": 15, "servings": 4,
                "difficulty": "Medium", "cuisine": "Indian", "meal_type": "dinner",
                "calories": 380, "protein": 16, "carbs": 20, "fat": 28,
                "is_vegetarian": 1, "category_id": 12,
                "ingredients": [
                    ("Paneer", 250, "g", "cubed"), ("Butter", 3, "tbsp", ""),
                    ("Tomatoes", 4, "medium", ""), ("Onion", 1, "large", "diced"),
                    ("Heavy cream", 0.25, "cup", ""), ("Garam masala", 1, "tsp", ""),
                    ("Kasuri methi", 1, "tsp", ""),
                ],
            },
            {
                "title": "Beef Tacos",
                "description": "Seasoned ground beef in crispy taco shells with toppings",
                "instructions": "1. Brown ground beef and drain fat. 2. Add taco seasoning and water. 3. Simmer until thickened. 4. Warm taco shells. 5. Fill shells with beef. 6. Top with lettuce, cheese, tomato, sour cream.",
                "image": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=500",
                "cooking_time": 15, "prep_time": 10, "servings": 4,
                "difficulty": "Easy", "cuisine": "Mexican", "meal_type": "dinner",
                "calories": 420, "protein": 22, "carbs": 32, "fat": 24,
                "is_vegetarian": 0, "is_non_veg": 1, "category_id": 13,
                "ingredients": [
                    ("Ground beef", 400, "g", ""), ("Taco shells", 12, "pieces", ""),
                    ("Lettuce", 1, "cup", "shredded"), ("Cheddar cheese", 1, "cup", "shredded"),
                    ("Tomato", 1, "medium", "diced"), ("Sour cream", 4, "tbsp", ""),
                    ("Taco seasoning", 1, "packet", ""),
                ],
            },

            # ── SNACKS ──
            {
                "title": "Chocolate Lava Cake",
                "description": "Decadent chocolate cake with a molten center",
                "instructions": "1. Melt chocolate and butter together. 2. Whisk eggs and sugar until thick. 3. Fold chocolate mixture into eggs. 4. Add flour and fold gently. 5. Pour into greased ramekins. 6. Bake at 425°F for 12-14 minutes. 7. Invert onto plates and serve immediately.",
                "image": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500",
                "cooking_time": 14, "prep_time": 20, "servings": 4,
                "difficulty": "Hard", "cuisine": "French", "meal_type": "snack",
                "calories": 480, "protein": 8, "carbs": 38, "fat": 32,
                "is_vegetarian": 1, "category_id": 5,
                "ingredients": [
                    ("Dark chocolate", 6, "oz", ""), ("Butter", 0.5, "cup", ""),
                    ("Eggs", 2, "large", ""), ("Sugar", 0.25, "cup", ""),
                    ("Flour", 2, "tbsp", ""), ("Vanilla extract", 1, "tsp", ""),
                ],
            },
            {
                "title": "Loaded Nachos",
                "description": "Crispy tortilla chips loaded with cheese, beans, and toppings",
                "instructions": "1. Spread tortilla chips on a baking sheet. 2. Top with refried beans, jalapeños, and cheese. 3. Bake at 375°F for 10 minutes. 4. Top with sour cream, salsa, and guacamole. 5. Serve immediately.",
                "image": "https://images.unsplash.com/photo-1513456852971-30c0b8199d4d?w=500",
                "cooking_time": 10, "prep_time": 10, "servings": 4,
                "difficulty": "Easy", "cuisine": "Mexican", "meal_type": "snack",
                "calories": 380, "protein": 14, "carbs": 36, "fat": 22,
                "is_vegetarian": 1, "category_id": 4,
                "ingredients": [
                    ("Tortilla chips", 300, "g", ""), ("Cheddar cheese", 1, "cup", "shredded"),
                    ("Refried beans", 1, "can", ""), ("Jalapeños", 2, "tbsp", "sliced"),
                    ("Sour cream", 4, "tbsp", ""), ("Salsa", 0.5, "cup", ""),
                ],
            },
            {
                "title": "Chicken Wings",
                "description": "Crispy fried chicken wings with buffalo sauce",
                "instructions": "1. Pat wings dry and season with salt, pepper, baking powder. 2. Bake at 425°F for 45 minutes, flipping halfway. 3. Melt butter and mix with hot sauce for buffalo sauce. 4. Toss wings in buffalo sauce. 5. Serve with ranch and celery sticks.",
                "image": "https://images.unsplash.com/photo-1608039829572-9b5bba1ee183?w=500",
                "cooking_time": 45, "prep_time": 10, "servings": 4,
                "difficulty": "Easy", "cuisine": "American", "meal_type": "snack",
                "calories": 340, "protein": 26, "carbs": 2, "fat": 26,
                "is_vegetarian": 0, "is_non_veg": 1, "is_gluten_free": 1, "category_id": 4,
                "ingredients": [
                    ("Chicken wings", 1, "kg", ""), ("Baking powder", 1, "tbsp", ""),
                    ("Butter", 3, "tbsp", "melted"), ("Hot sauce", 0.25, "cup", ""),
                    ("Ranch dressing", 0.25, "cup", ""), ("Celery", 4, "sticks", ""),
                ],
            },
            {
                "title": "Bruschetta",
                "description": "Toasted bread topped with fresh tomatoes, basil, and balsamic",
                "instructions": "1. Dice tomatoes and mix with minced garlic, basil, olive oil, salt. 2. Let marinate 15 minutes. 3. Slice baguette and brush with olive oil. 4. Toast under broiler until golden. 5. Top tomato mixture on bread. 6. Drizzle with balsamic glaze.",
                "image": "https://images.unsplash.com/photo-1572695157366-5e585ab2b69f?w=500",
                "cooking_time": 5, "prep_time": 20, "servings": 4,
                "difficulty": "Easy", "cuisine": "Italian", "meal_type": "snack",
                "calories": 180, "protein": 4, "carbs": 22, "fat": 8,
                "is_vegetarian": 1, "is_vegan": 1, "category_id": 4,
                "ingredients": [
                    ("Baguette", 1, "large", "sliced"), ("Tomatoes", 3, "medium", "diced"),
                    ("Fresh basil", 8, "leaves", "chopped"), ("Garlic", 2, "cloves", "minced"),
                    ("Olive oil", 3, "tbsp", ""), ("Balsamic glaze", 1, "tbsp", ""),
                ],
            },

            # ── DESSERTS ──
            {
                "title": "Tiramisu",
                "description": "Classic Italian coffee-flavored dessert with mascarpone",
                "instructions": "1. Brew strong coffee and let cool. 2. Mix mascarpone, eggs, and sugar. 3. Dip ladyfingers in coffee. 4. Layer dipped ladyfingers and mascarpone cream. 5. Repeat layers. 6. Dust with cocoa powder. 7. Refrigerate 4 hours.",
                "image": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=500",
                "cooking_time": 0, "prep_time": 30, "servings": 8,
                "difficulty": "Medium", "cuisine": "Italian", "meal_type": "snack",
                "calories": 420, "protein": 8, "carbs": 42, "fat": 26,
                "is_vegetarian": 1, "category_id": 5,
                "ingredients": [
                    ("Mascarpone cheese", 500, "g", ""), ("Eggs", 4, "large", "separated"),
                    ("Sugar", 0.5, "cup", ""), ("Ladyfingers", 24, "pieces", ""),
                    ("Strong coffee", 1, "cup", "cooled"), ("Cocoa powder", 2, "tbsp", ""),
                ],
            },
            {
                "title": "Mango Sticky Rice",
                "description": "Sweet Thai dessert with coconut sticky rice and fresh mango",
                "instructions": "1. Soak sticky rice for 4 hours. 2. Steam rice until tender. 3. Heat coconut milk with sugar and salt. 4. Pour over hot rice and stir. 5. Let rice absorb coconut milk. 6. Slice mango. 7. Serve rice with mango and extra coconut sauce.",
                "image": "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=500",
                "cooking_time": 30, "prep_time": 240, "servings": 4,
                "difficulty": "Medium", "cuisine": "Thai", "meal_type": "snack",
                "calories": 360, "protein": 4, "carbs": 62, "fat": 12,
                "is_vegetarian": 1, "is_vegan": 1, "is_gluten_free": 1, "category_id": 14,
                "ingredients": [
                    ("Sticky rice", 2, "cups", ""), ("Coconut milk", 1, "can", ""),
                    ("Sugar", 0.25, "cup", ""), ("Salt", 0.25, "tsp", ""),
                    ("Ripe mango", 2, "large", "sliced"),
                ],
            },
            {
                "title": "Gulab Jamun",
                "description": "Soft Indian milk-solid dumplings soaked in rose-cardamom syrup",
                "instructions": "1. Make syrup: boil sugar, water, cardamom, rose water. 2. Mix milk powder, flour, baking soda, ghee into soft dough. 3. Roll into small smooth balls. 4. Deep fry on low heat until golden. 5. Soak in warm syrup for 2 hours. 6. Serve warm.",
                "image": "https://images.unsplash.com/photo-1666190463450-57fa2e574452?w=500",
                "cooking_time": 20, "prep_time": 30, "servings": 8,
                "difficulty": "Hard", "cuisine": "Indian", "meal_type": "snack",
                "calories": 280, "protein": 4, "carbs": 48, "fat": 8,
                "is_vegetarian": 1, "category_id": 12,
                "ingredients": [
                    ("Milk powder", 1.5, "cups", ""), ("All-purpose flour", 0.25, "cup", ""),
                    ("Baking soda", 0.25, "tsp", ""), ("Ghee", 2, "tbsp", ""),
                    ("Sugar", 2, "cups", ""), ("Cardamom", 4, "pods", ""),
                    ("Rose water", 1, "tsp", ""),
                ],
            },

            # ── BEVERAGES ──
            {
                "title": "Berry Smoothie Bowl",
                "description": "Thick and creamy smoothie bowl topped with fresh fruits and granola",
                "instructions": "1. Blend frozen berries, banana, and yogurt until thick and smooth. 2. Pour into a bowl. 3. Top with fresh berries, sliced banana, granola, and honey. 4. Add chia seeds and coconut flakes. 5. Enjoy immediately.",
                "image": "https://images.unsplash.com/photo-1590301157890-4810ed352733?w=500",
                "cooking_time": 0, "prep_time": 10, "servings": 1,
                "difficulty": "Easy", "cuisine": "American", "meal_type": "breakfast",
                "calories": 290, "protein": 12, "carbs": 52, "fat": 6,
                "is_vegetarian": 1, "category_id": 6,
                "ingredients": [
                    ("Frozen mixed berries", 1, "cup", ""), ("Banana", 1, "medium", "frozen"),
                    ("Greek yogurt", 0.5, "cup", ""), ("Granola", 0.25, "cup", ""),
                    ("Honey", 1, "tbsp", ""), ("Chia seeds", 1, "tsp", ""),
                ],
            },
            {
                "title": "Mango Lassi",
                "description": "Creamy Indian yogurt drink blended with ripe mango",
                "instructions": "1. Peel and dice ripe mango. 2. Add mango, yogurt, milk, and sugar to blender. 3. Blend until smooth. 4. Add ice and blend again. 5. Pour into glasses. 6. Garnish with saffron strands.",
                "image": "https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=500",
                "cooking_time": 0, "prep_time": 5, "servings": 2,
                "difficulty": "Easy", "cuisine": "Indian", "meal_type": "snack",
                "calories": 180, "protein": 6, "carbs": 34, "fat": 4,
                "is_vegetarian": 1, "is_gluten_free": 1, "category_id": 12,
                "ingredients": [
                    ("Ripe mango", 1, "large", ""), ("Yogurt", 1, "cup", ""),
                    ("Milk", 0.5, "cup", ""), ("Sugar", 2, "tbsp", ""),
                    ("Cardamom", 0.25, "tsp", ""),
                ],
            },
            {
                "title": "Mojito",
                "description": "Refreshing Cuban cocktail with lime, mint, and rum",
                "instructions": "1. Muddle mint leaves with lime juice and sugar. 2. Add ice to glass. 3. Pour in white rum. 4. Top with club soda. 5. Stir gently. 6. Garnish with mint sprig and lime wheel.",
                "image": "https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=500",
                "cooking_time": 0, "prep_time": 5, "servings": 1,
                "difficulty": "Easy", "cuisine": "Mexican", "meal_type": "snack",
                "calories": 180, "protein": 0, "carbs": 18, "fat": 0,
                "is_vegetarian": 1, "is_vegan": 1, "is_gluten_free": 1,
                "category_id": 6,
                "ingredients": [
                    ("Fresh mint", 10, "leaves", ""), ("Lime", 1, "medium", "juiced"),
                    ("Sugar", 2, "tsp", ""), ("White rum", 2, "oz", ""),
                    ("Club soda", 4, "oz", ""), ("Ice", 1, "cup", ""),
                ],
            },

            # ── SEAFOOD ──
            {
                "title": "Garlic Butter Shrimp",
                "description": "Succulent shrimp sautéed in garlic butter with fresh parsley",
                "instructions": "1. Heat olive oil and butter in a skillet. 2. Add minced garlic and cook 30 seconds. 3. Add shrimp in a single layer. 4. Cook 2 minutes per side until pink. 5. Add lemon juice and parsley. 6. Serve immediately with crusty bread.",
                "image": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=500",
                "cooking_time": 8, "prep_time": 5, "servings": 2,
                "difficulty": "Easy", "cuisine": "American", "meal_type": "dinner",
                "calories": 280, "protein": 24, "carbs": 2, "fat": 20,
                "is_vegetarian": 0, "is_non_veg": 1, "is_gluten_free": 1, "is_keto": 1,
                "category_id": 7,
                "ingredients": [
                    ("Shrimp", 400, "g", "peeled"), ("Butter", 3, "tbsp", ""),
                    ("Garlic", 4, "cloves", "minced"), ("Lemon", 1, "medium", "juiced"),
                    ("Fresh parsley", 2, "tbsp", "chopped"), ("Red pepper flakes", 0.25, "tsp", ""),
                ],
            },
            {
                "title": "Fish and Chips",
                "description": "Beer-battered fish with crispy golden chips and tartar sauce",
                "instructions": "1. Cut potatoes into chips and double fry. 2. Make beer batter with flour, beer, and baking powder. 3. Dip fish in batter. 4. Deep fry until golden and crispy. 5. Make tartar sauce with mayo, pickles, lemon. 6. Serve fish with chips, tartar sauce, and mushy peas.",
                "image": "https://images.unsplash.com/photo-1534604973900-c43ab4c2e0ab?w=500",
                "cooking_time": 25, "prep_time": 20, "servings": 2,
                "difficulty": "Medium", "cuisine": "American", "meal_type": "dinner",
                "calories": 580, "protein": 28, "carbs": 56, "fat": 26,
                "is_vegetarian": 0, "is_non_veg": 1, "category_id": 7,
                "ingredients": [
                    ("White fish fillets", 400, "g", ""), ("Potatoes", 4, "large", "for chips"),
                    ("Flour", 1.5, "cups", ""), ("Beer", 1, "cup", "cold"),
                    ("Baking powder", 1, "tsp", ""), ("Mayonnaise", 0.5, "cup", ""),
                    ("Pickles", 2, "tbsp", "chopped"),
                ],
            },
            {
                "title": "Crab Cakes",
                "description": "Crispy golden crab cakes with remoulade sauce",
                "instructions": "1. Mix crab meat with breadcrumbs, mayo, egg, mustard, Old Bay. 2. Form into patties. 3. Chill 30 minutes. 4. Pan-fry in oil until golden on both sides. 5. Make remoulade: mix mayo, Dijon, capers, lemon. 6. Serve with remoulade and lemon wedge.",
                "image": "https://images.unsplash.com/photo-1559737558-2f5a35f4523b?w=500",
                "cooking_time": 10, "prep_time": 40, "servings": 4,
                "difficulty": "Medium", "cuisine": "American", "meal_type": "dinner",
                "calories": 320, "protein": 22, "carbs": 18, "fat": 18,
                "is_vegetarian": 0, "is_non_veg": 1, "category_id": 7,
                "ingredients": [
                    ("Crab meat", 400, "g", "lump"), ("Breadcrumbs", 0.5, "cup", ""),
                    ("Mayonnaise", 3, "tbsp", ""), ("Egg", 1, "large", "beaten"),
                    ("Dijon mustard", 1, "tsp", ""), ("Old Bay seasoning", 1, "tsp", ""),
                    ("Lemon", 1, "medium", ""),
                ],
            },

            # ── BBQ & GRILL ──
            {
                "title": "Grilled Ribeye Steak",
                "description": "Perfectly seared ribeye with herb compound butter",
                "instructions": "1. Bring steak to room temperature. 2. Season generously with salt and pepper. 3. Heat grill to high. 4. Sear 4-5 minutes per side for medium-rare. 5. Make compound butter with herbs. 6. Rest steak 10 minutes. 7. Top with herb butter and serve.",
                "image": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=500",
                "cooking_time": 12, "prep_time": 20, "servings": 2,
                "difficulty": "Medium", "cuisine": "American", "meal_type": "dinner",
                "calories": 580, "protein": 42, "carbs": 0, "fat": 46,
                "is_vegetarian": 0, "is_non_veg": 1, "is_gluten_free": 1, "is_keto": 1,
                "category_id": 8,
                "ingredients": [
                    ("Ribeye steak", 2, "pieces", "1 inch thick"), ("Butter", 3, "tbsp", "softened"),
                    ("Fresh rosemary", 1, "tbsp", "chopped"), ("Garlic", 2, "cloves", "minced"),
                    ("Salt", 1, "tsp", ""), ("Black pepper", 1, "tsp", ""),
                ],
            },
            {
                "title": "Jerk Chicken",
                "description": "Spicy Caribbean jerk-seasoned grilled chicken",
                "instructions": "1. Blend jerk marinade: scotch bonnet, scallions, thyme, allspice, soy sauce. 2. Marinate chicken overnight. 3. Preheat grill to medium. 4. Grill chicken 6-7 minutes per side. 5. Baste with extra marinade. 6. Serve with rice and peas.",
                "image": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=500",
                "cooking_time": 20, "prep_time": 480, "servings": 4,
                "difficulty": "Medium", "cuisine": "American", "meal_type": "dinner",
                "calories": 340, "protein": 32, "carbs": 4, "fat": 22,
                "is_vegetarian": 0, "is_non_veg": 1, "is_gluten_free": 1, "is_dairy_free": 1,
                "category_id": 8,
                "ingredients": [
                    ("Chicken pieces", 800, "g", ""), ("Scotch bonnet", 2, "peppers", ""),
                    ("Scallions", 4, "stalks", ""), ("Allspice", 1, "tsp", ""),
                    ("Thyme", 2, "sprigs", ""), ("Soy sauce", 3, "tbsp", ""),
                    ("Brown sugar", 1, "tbsp", ""),
                ],
            },
            {
                "title": "Grilled Vegetable Platter",
                "description": "Assorted grilled vegetables with balsamic glaze and herbs",
                "instructions": "1. Cut zucchini, bell peppers, eggplant, and mushrooms. 2. Toss with olive oil, salt, pepper, and herbs. 3. Grill on high heat. 4. Grill each vegetable until charred and tender. 5. Arrange on platter. 6. Drizzle with balsamic glaze and fresh basil.",
                "image": "https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=500",
                "cooking_time": 15, "prep_time": 15, "servings": 4,
                "difficulty": "Easy", "cuisine": "Mediterranean", "meal_type": "dinner",
                "calories": 150, "protein": 4, "carbs": 16, "fat": 10,
                "is_vegetarian": 1, "is_vegan": 1, "is_gluten_free": 1,
                "category_id": 8,
                "ingredients": [
                    ("Zucchini", 2, "medium", "sliced"), ("Bell peppers", 2, "large", "quartered"),
                    ("Eggplant", 1, "medium", "sliced"), ("Mushrooms", 2, "cups", "whole"),
                    ("Olive oil", 3, "tbsp", ""), ("Balsamic glaze", 2, "tbsp", ""),
                ],
            },

            # ── SOUPS & STEWS ──
            {
                "title": "Chicken Noodle Soup",
                "description": "Comforting homemade chicken noodle soup with vegetables",
                "instructions": "1. Sauté onions, carrots, and celery. 2. Add chicken broth and bring to boil. 3. Add chicken breasts and simmer until cooked. 4. Remove chicken, shred it. 5. Add noodles to broth and cook. 6. Return chicken to pot. 7. Season with herbs and serve.",
                "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=500",
                "cooking_time": 30, "prep_time": 15, "servings": 6,
                "difficulty": "Easy", "cuisine": "American", "meal_type": "dinner",
                "calories": 250, "protein": 22, "carbs": 28, "fat": 6,
                "is_vegetarian": 0, "is_non_veg": 1, "is_dairy_free": 1,
                "category_id": 10,
                "ingredients": [
                    ("Chicken breast", 300, "g", ""), ("Egg noodles", 2, "cups", ""),
                    ("Carrots", 2, "medium", "diced"), ("Celery", 2, "stalks", "diced"),
                    ("Onion", 1, "medium", "diced"), ("Chicken broth", 6, "cups", ""),
                    ("Thyme", 1, "tsp", ""),
                ],
            },
            {
                "title": "Tom Yum Soup",
                "description": "Spicy and sour Thai soup with shrimp and mushrooms",
                "instructions": "1. Bring chicken broth to boil. 2. Add lemongrass, galangal, kaffir lime leaves. 3. Add mushrooms and shrimp. 4. Cook until shrimp turn pink. 5. Add fish sauce, lime juice, and chili paste. 6. Garnish with cilantro and serve hot.",
                "image": "https://images.unsplash.com/photo-1548943487-a2e4e43b4853?w=500",
                "cooking_time": 15, "prep_time": 10, "servings": 4,
                "difficulty": "Medium", "cuisine": "Thai", "meal_type": "dinner",
                "calories": 180, "protein": 18, "carbs": 8, "fat": 6,
                "is_vegetarian": 0, "is_non_veg": 1, "is_gluten_free": 1,
                "category_id": 14,
                "ingredients": [
                    ("Shrimp", 300, "g", "peeled"), ("Mushrooms", 1, "cup", "sliced"),
                    ("Lemongrass", 2, "stalks", "bruised"), ("Kaffir lime leaves", 4, "leaves", ""),
                    ("Fish sauce", 2, "tbsp", ""), ("Lime juice", 3, "tbsp", ""),
                    ("Chili paste", 1, "tbsp", ""),
                ],
            },
            {
                "title": "Mushroom Soup",
                "description": "Creamy wild mushroom soup with truffle oil",
                "instructions": "1. Sauté onions and garlic in butter. 2. Add sliced mushrooms and cook 10 minutes. 3. Add vegetable broth and simmer. 4. Blend until smooth. 5. Add heavy cream and stir. 6. Season with salt, pepper, and truffle oil. 7. Serve with crusty bread.",
                "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=500",
                "cooking_time": 25, "prep_time": 10, "servings": 4,
                "difficulty": "Easy", "cuisine": "French", "meal_type": "dinner",
                "calories": 220, "protein": 6, "carbs": 14, "fat": 16,
                "is_vegetarian": 1, "is_gluten_free": 1,
                "category_id": 10,
                "ingredients": [
                    ("Mixed mushrooms", 500, "g", "sliced"), ("Onion", 1, "medium", "diced"),
                    ("Garlic", 3, "cloves", "minced"), ("Butter", 3, "tbsp", ""),
                    ("Vegetable broth", 3, "cups", ""), ("Heavy cream", 0.5, "cup", ""),
                    ("Truffle oil", 1, "tsp", ""),
                ],
            },
            {
                "title": "Mulligatawny Soup",
                "description": "Indian-spiced chicken and lentil soup with coconut milk",
                "instructions": "1. Sauté onions, carrots, celery. 2. Add curry powder and cook 1 minute. 3. Add chicken broth, lentils, and rice. 4. Simmer until lentils are tender. 5. Add coconut milk and shredded chicken. 6. Season and serve with naan.",
                "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=500",
                "cooking_time": 35, "prep_time": 15, "servings": 6,
                "difficulty": "Easy", "cuisine": "Indian", "meal_type": "dinner",
                "calories": 310, "protein": 20, "carbs": 36, "fat": 10,
                "is_vegetarian": 0, "is_non_veg": 1, "is_dairy_free": 1,
                "category_id": 12,
                "ingredients": [
                    ("Chicken breast", 300, "g", "shredded"), ("Red lentils", 1, "cup", ""),
                    ("Coconut milk", 0.5, "cup", ""), ("Curry powder", 1, "tbsp", ""),
                    ("Carrots", 2, "medium", "diced"), ("Chicken broth", 4, "cups", ""),
                    ("Basmati rice", 0.25, "cup", ""),
                ],
            },

            # ── SALADS ──
            {
                "title": "Greek Salad",
                "description": "Fresh Greek salad with olives, feta, and oregano dressing",
                "instructions": "1. Chop cucumbers, tomatoes, red onion, and bell pepper. 2. Add Kalamata olives. 3. Crumble feta cheese on top. 4. Make dressing with olive oil, red wine vinegar, oregano. 5. Drizzle dressing over salad. 6. Season with salt and pepper.",
                "image": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=500",
                "cooking_time": 0, "prep_time": 15, "servings": 2,
                "difficulty": "Easy", "cuisine": "Mediterranean", "meal_type": "lunch",
                "calories": 280, "protein": 10, "carbs": 14, "fat": 22,
                "is_vegetarian": 1, "is_gluten_free": 1,
                "category_id": 11,
                "ingredients": [
                    ("Cucumber", 1, "large", "diced"), ("Tomatoes", 2, "large", "chopped"),
                    ("Red onion", 0.5, "medium", "sliced"), ("Kalamata olives", 0.5, "cup", ""),
                    ("Feta cheese", 100, "g", "crumbled"), ("Olive oil", 3, "tbsp", ""),
                    ("Red wine vinegar", 1, "tbsp", ""),
                ],
            },
            {
                "title": "Cobb Salad",
                "description": "Loaded American salad with chicken, bacon, eggs, and blue cheese",
                "instructions": "1. Grill and slice chicken breast. 2. Cook and crumble bacon. 3. Hard boil and slice eggs. 4. Arrange all ingredients in rows on a bed of lettuce. 5. Add avocado and tomatoes. 6. Drizzle with red wine vinaigrette.",
                "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500",
                "cooking_time": 20, "prep_time": 15, "servings": 2,
                "difficulty": "Medium", "cuisine": "American", "meal_type": "lunch",
                "calories": 480, "protein": 38, "carbs": 12, "fat": 34,
                "is_vegetarian": 0, "is_non_veg": 1, "is_gluten_free": 1,
                "category_id": 11,
                "ingredients": [
                    ("Chicken breast", 200, "g", "grilled"), ("Bacon", 4, "slices", "crispy"),
                    ("Eggs", 2, "large", "hard boiled"), ("Avocado", 1, "medium", "sliced"),
                    ("Blue cheese", 0.25, "cup", "crumbled"), ("Romaine lettuce", 4, "cups", "chopped"),
                    ("Tomato", 1, "medium", "diced"),
                ],
            },
            {
                "title": "Thai Papaya Salad",
                "description": "Spicy and tangy green papaya salad with peanuts",
                "instructions": "1. Julienne green papaya. 2. Pound garlic and chilies in mortar. 3. Add green beans, tomatoes. 4. Add fish sauce, lime juice, palm sugar. 5. Add shredded papaya and pound lightly. 6. Top with crushed peanuts. 7. Serve immediately.",
                "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500",
                "cooking_time": 0, "prep_time": 15, "servings": 2,
                "difficulty": "Medium", "cuisine": "Thai", "meal_type": "lunch",
                "calories": 160, "protein": 6, "carbs": 20, "fat": 6,
                "is_vegetarian": 0, "is_non_veg": 1, "is_gluten_free": 1, "is_dairy_free": 1,
                "category_id": 14,
                "ingredients": [
                    ("Green papaya", 2, "cups", "shredded"), ("Cherry tomatoes", 1, "cup", "halved"),
                    ("Green beans", 6, "pieces", "cut"), ("Lime", 1, "medium", "juiced"),
                    ("Fish sauce", 2, "tbsp", ""), ("Peanuts", 2, "tbsp", "crushed"),
                    ("Thai chilies", 2, "pieces", ""),
                ],
            },

            # ── PASTA & NOODLES ──
            {
                "title": "Pad Thai",
                "description": "Classic Thai stir-fried rice noodles with shrimp and peanuts",
                "instructions": "1. Soak rice noodles in warm water. 2. Make sauce: mix tamarind, fish sauce, sugar, lime. 3. Stir fry shrimp until pink. 4. Add noodles and sauce. 5. Toss with bean sprouts, green onions. 6. Serve with crushed peanuts and lime.",
                "image": "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=500",
                "cooking_time": 15, "prep_time": 20, "servings": 2,
                "difficulty": "Medium", "cuisine": "Thai", "meal_type": "dinner",
                "calories": 440, "protein": 22, "carbs": 58, "fat": 14,
                "is_vegetarian": 0, "is_non_veg": 1, "is_dairy_free": 1,
                "category_id": 14,
                "ingredients": [
                    ("Rice noodles", 200, "g", ""), ("Shrimp", 200, "g", "peeled"),
                    ("Tamarind paste", 2, "tbsp", ""), ("Fish sauce", 2, "tbsp", ""),
                    ("Bean sprouts", 1, "cup", ""), ("Peanuts", 3, "tbsp", "crushed"),
                    ("Lime", 1, "medium", ""),
                ],
            },
            {
                "title": "Creamy Mushroom Pasta",
                "description": "Silky pasta in a rich mushroom cream sauce with parmesan",
                "instructions": "1. Cook pasta according to package. 2. Sauté mushrooms in butter until golden. 3. Add garlic and cook 30 seconds. 4. Add heavy cream and simmer. 5. Toss with pasta and parmesan. 6. Season with salt, pepper, and parsley.",
                "image": "https://images.unsplash.com/photo-1595231712325-9e23b8b3c6b8?w=500",
                "cooking_time": 20, "prep_time": 10, "servings": 2,
                "difficulty": "Easy", "cuisine": "Italian", "meal_type": "dinner",
                "calories": 520, "protein": 16, "carbs": 56, "fat": 28,
                "is_vegetarian": 1,
                "category_id": 9,
                "ingredients": [
                    ("Penne pasta", 250, "g", ""), ("Mushrooms", 300, "g", "sliced"),
                    ("Heavy cream", 0.75, "cup", ""), ("Parmesan cheese", 0.5, "cup", "grated"),
                    ("Butter", 2, "tbsp", ""), ("Garlic", 2, "cloves", "minced"),
                    ("Parsley", 2, "tbsp", "chopped"),
                ],
            },
            {
                "title": "Dan Dan Noodles",
                "description": "Spicy Sichuan noodles with ground pork and chili oil",
                "instructions": "1. Cook noodles and drain. 2. Brown ground pork with soy sauce. 3. Make sauce: mix sesame paste, chili oil, soy sauce, vinegar. 4. Toss noodles with sauce. 5. Top with pork, green onions, crushed peanuts. 6. Serve immediately.",
                "image": "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=500",
                "cooking_time": 15, "prep_time": 10, "servings": 2,
                "difficulty": "Medium", "cuisine": "Asian", "meal_type": "dinner",
                "calories": 460, "protein": 20, "carbs": 52, "fat": 18,
                "is_vegetarian": 0, "is_non_veg": 1, "is_dairy_free": 1,
                "category_id": 9,
                "ingredients": [
                    ("Egg noodles", 200, "g", ""), ("Ground pork", 150, "g", ""),
                    ("Sesame paste", 2, "tbsp", ""), ("Chili oil", 1, "tbsp", ""),
                    ("Soy sauce", 2, "tbsp", ""), ("Peanuts", 2, "tbsp", "crushed"),
                    ("Green onions", 2, "stalks", "chopped"),
                ],
            },

            # ── QUICK MEALS ──
            {
                "title": "Garlic Butter Chicken Bites",
                "description": "Tender chicken bites in garlic butter sauce ready in 15 minutes",
                "instructions": "1. Cut chicken into bite-sized pieces. 2. Season with salt, pepper, paprika. 3. Heat olive oil in a skillet. 4. Cook chicken 3-4 minutes until golden. 5. Add butter and garlic, cook 1 minute. 6. Toss chicken in sauce. 7. Garnish with parsley.",
                "image": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=500",
                "cooking_time": 10, "prep_time": 5, "servings": 2,
                "difficulty": "Easy", "cuisine": "American", "meal_type": "dinner",
                "calories": 320, "protein": 30, "carbs": 2, "fat": 22,
                "is_vegetarian": 0, "is_non_veg": 1, "is_gluten_free": 1, "is_keto": 1,
                "category_id": 15,
                "ingredients": [
                    ("Chicken breast", 300, "g", "cubed"), ("Butter", 2, "tbsp", ""),
                    ("Garlic", 4, "cloves", "minced"), ("Olive oil", 1, "tbsp", ""),
                    ("Paprika", 1, "tsp", ""), ("Parsley", 1, "tbsp", "chopped"),
                ],
            },
            {
                "title": "Veggie Quesadilla",
                "description": "Crispy tortilla filled with cheese, peppers, and onions",
                "instructions": "1. Sauté sliced peppers and onions. 2. Lay tortilla in a pan. 3. Add cheese on one half. 4. Add sautéed veggies and more cheese. 5. Fold and cook until golden on both sides. 6. Cut into wedges. 7. Serve with salsa and sour cream.",
                "image": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=500",
                "cooking_time": 8, "prep_time": 7, "servings": 2,
                "difficulty": "Easy", "cuisine": "Mexican", "meal_type": "lunch",
                "calories": 380, "protein": 16, "carbs": 34, "fat": 22,
                "is_vegetarian": 1, "category_id": 15,
                "ingredients": [
                    ("Flour tortilla", 2, "large", ""), ("Cheddar cheese", 1, "cup", "shredded"),
                    ("Bell pepper", 1, "medium", "sliced"), ("Onion", 0.5, "medium", "sliced"),
                    ("Salsa", 4, "tbsp", ""), ("Sour cream", 2, "tbsp", ""),
                ],
            },
            {
                "title": "Egg Fried Rice",
                "description": "Quick and flavorful fried rice with eggs and vegetables",
                "instructions": "1. Cook rice and let cool completely. 2. Heat oil in a wok. 3. Scramble eggs, set aside. 4. Stir fry mixed vegetables. 5. Add rice and soy sauce. 6. Toss with eggs. 7. Season with sesame oil and green onions.",
                "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=500",
                "cooking_time": 10, "prep_time": 5, "servings": 2,
                "difficulty": "Easy", "cuisine": "Asian", "meal_type": "dinner",
                "calories": 380, "protein": 14, "carbs": 52, "fat": 12,
                "is_vegetarian": 1, "is_vegan": 1, "is_dairy_free": 1,
                "category_id": 15,
                "ingredients": [
                    ("Cooked rice", 3, "cups", "cold"), ("Eggs", 3, "large", ""),
                    ("Mixed vegetables", 1, "cup", ""), ("Soy sauce", 2, "tbsp", ""),
                    ("Sesame oil", 1, "tsp", ""), ("Green onions", 2, "stalks", "chopped"),
                ],
            },
            {
                "title": "Caprese Sandwich",
                "description": "Simple Italian sandwich with fresh mozzarella, tomato, and basil",
                "instructions": "1. Slice fresh mozzarella and tomatoes. 2. Layer on ciabatta bread. 3. Add fresh basil leaves. 4. Drizzle with balsamic glaze and olive oil. 5. Season with salt and pepper. 6. Close sandwich and press gently.",
                "image": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=500",
                "cooking_time": 0, "prep_time": 5, "servings": 1,
                "difficulty": "Easy", "cuisine": "Italian", "meal_type": "lunch",
                "calories": 420, "protein": 20, "carbs": 36, "fat": 22,
                "is_vegetarian": 1, "category_id": 15,
                "ingredients": [
                    ("Ciabatta roll", 1, "medium", ""), ("Fresh mozzarella", 100, "g", "sliced"),
                    ("Tomato", 1, "medium", "sliced"), ("Fresh basil", 4, "leaves", ""),
                    ("Balsamic glaze", 1, "tbsp", ""), ("Olive oil", 1, "tbsp", ""),
                ],
            },
            {
                "title": "Teriyaki Salmon Bowl",
                "description": "Glazed salmon over rice with steamed vegetables",
                "instructions": "1. Make teriyaki sauce: mix soy sauce, mirin, sugar, ginger. 2. Cook rice. 3. Pan-sear salmon until crispy skin forms. 4. Pour teriyaki sauce over salmon. 5. Steam broccoli and edamame. 6. Assemble bowl with rice, salmon, veggies, sesame seeds.",
                "image": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=500",
                "cooking_time": 15, "prep_time": 10, "servings": 2,
                "difficulty": "Easy", "cuisine": "Asian", "meal_type": "dinner",
                "calories": 520, "protein": 36, "carbs": 54, "fat": 16,
                "is_vegetarian": 0, "is_non_veg": 1, "is_gluten_free": 1,
                "category_id": 15,
                "ingredients": [
                    ("Salmon fillets", 2, "pieces", ""), ("Sushi rice", 1, "cup", ""),
                    ("Soy sauce", 3, "tbsp", ""), ("Mirin", 2, "tbsp", ""),
                    ("Broccoli", 1, "cup", "florets"), ("Edamame", 0.5, "cup", ""),
                    ("Sesame seeds", 1, "tsp", ""),
                ],
            },
        ]

        for recipe_data in sample_recipes:
            ingredients = recipe_data.pop("ingredients")
            recipe = Recipe(**recipe_data, author_id=admin.id)
            db.add(recipe)
            db.flush()

            for ing_name, qty, unit, notes in ingredients:
                ingredient = db.query(Ingredient).filter(Ingredient.name == ing_name).first()
                if not ingredient:
                    ingredient = Ingredient(name=ing_name)
                    db.add(ingredient)
                    db.flush()

                db.add(RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id,
                    quantity=qty,
                    unit=unit,
                    notes=notes,
                ))

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Seed error: {e}")
    finally:
        db.close()
