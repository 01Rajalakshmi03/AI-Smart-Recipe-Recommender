import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiFilter, FiX } from 'react-icons/fi';
import { recipeAPI, categoryAPI } from '../services/api';
import RecipeCard from '../components/recipes/RecipeCard';
import RecipeSkeleton from '../components/common/RecipeSkeleton';

export default function RecipesPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [recipes, setRecipes] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [totalPages, setTotalPages] = useState(1);
  const [showFilters, setShowFilters] = useState(false);

  const [filters, setFilters] = useState({
    search: searchParams.get('search') || '',
    category_id: searchParams.get('category_id') || '',
    cuisine: searchParams.get('cuisine') || '',
    meal_type: searchParams.get('meal_type') || '',
    difficulty: searchParams.get('difficulty') || '',
    is_vegetarian: searchParams.get('is_vegetarian') || '',
    is_vegan: searchParams.get('is_vegan') || '',
    is_gluten_free: searchParams.get('is_gluten_free') || '',
    is_non_veg: searchParams.get('is_non_veg') || '',
    is_keto: searchParams.get('is_keto') || '',
    is_dairy_free: searchParams.get('is_dairy_free') || '',
    page: 1,
  });

  useEffect(() => {
    categoryAPI.getAll().then((res) => setCategories(res.data));
  }, []);

  useEffect(() => {
    setLoading(true);
    const params = {};
    Object.entries(filters).forEach(([key, val]) => {
      if (val) params[key] = val;
    });

    recipeAPI.getAll(params)
      .then((res) => {
        setRecipes(res.data.items);
        setTotalPages(res.data.pages);
      })
      .finally(() => setLoading(false));
  }, [filters]);

  const updateFilter = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value, ...(key !== 'page' && { page: 1 }) }));
  };

  const clearFilters = () => {
    setFilters({ search: '', category_id: '', cuisine: '', meal_type: '', difficulty: '', is_vegetarian: '', is_vegan: '', is_gluten_free: '', is_non_veg: '', is_keto: '', is_dairy_free: '', page: 1 });
  };

  const activeFilterCount = Object.values(filters).filter((v) => v && v !== 1).length;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-20 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Browse Recipes</h1>
          <p className="text-gray-500 mt-1">Discover delicious recipes for every occasion</p>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="lg:hidden flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-800 rounded-xl shadow-card"
          >
            <FiFilter size={18} /> Filters {activeFilterCount > 0 && `(${activeFilterCount})`}
          </button>

          <div className={`lg:w-64 flex-shrink-0 ${showFilters ? 'block' : 'hidden lg:block'}`}>
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-card p-6 space-y-6 sticky top-24">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-gray-800 dark:text-white">Filters</h3>
                {activeFilterCount > 0 && (
                  <button onClick={clearFilters} className="text-sm text-primary-500 hover:text-primary-600">
                    Clear all
                  </button>
                )}
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">Category</label>
                <select
                  value={filters.category_id}
                  onChange={(e) => updateFilter('category_id', e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-sm focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">All Categories</option>
                  {categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>{cat.icon} {cat.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">Meal Type</label>
                <select
                  value={filters.meal_type}
                  onChange={(e) => updateFilter('meal_type', e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-sm focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">All Types</option>
                  <option value="breakfast">🍳 Breakfast</option>
                  <option value="lunch">🥗 Lunch</option>
                  <option value="dinner">🍽️ Dinner</option>
                  <option value="snack">🍿 Snack</option>
                </select>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">Difficulty</label>
                <select
                  value={filters.difficulty}
                  onChange={(e) => updateFilter('difficulty', e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-sm focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">Any Difficulty</option>
                  <option value="Easy">Easy</option>
                  <option value="Medium">Medium</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">Cuisine</label>
                <select
                  value={filters.cuisine}
                  onChange={(e) => updateFilter('cuisine', e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-sm focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">All Cuisines</option>
                  <option value="Indian">Indian</option>
                  <option value="Italian">Italian</option>
                  <option value="American">American</option>
                  <option value="Asian">Asian</option>
                  <option value="Mediterranean">Mediterranean</option>
                  <option value="French">French</option>
                  <option value="Mexican">Mexican</option>
                  <option value="Thai">Thai</option>
                </select>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">Dietary</label>
                <div className="space-y-2">
                  {[
                    { key: 'is_vegetarian', label: '🥬 Vegetarian', value: '1' },
                    { key: 'is_vegan', label: '🌱 Vegan', value: '1' },
                    { key: 'is_non_veg', label: '🍗 Non-Veg', value: '1' },
                    { key: 'is_gluten_free', label: '🌾 Gluten-Free', value: '1' },
                    { key: 'is_keto', label: '🥑 Keto', value: '1' },
                    { key: 'is_dairy_free', label: '🥛 Dairy-Free', value: '1' },
                  ].map((diet) => (
                    <label key={diet.key} className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={filters[diet.key] === diet.value}
                        onChange={(e) => updateFilter(diet.key, e.target.checked ? diet.value : '')}
                        className="rounded border-gray-300 text-primary-500 focus:ring-primary-500"
                      />
                      <span className="text-sm text-gray-700 dark:text-gray-300">{diet.label}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="flex-1">
            {loading ? (
              <RecipeSkeleton count={6} />
            ) : recipes.length === 0 ? (
              <div className="text-center py-20">
                <span className="text-6xl mb-4 block">🔍</span>
                <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">No recipes found</h3>
                <p className="text-gray-500 mb-4">Try adjusting your filters or search terms</p>
                <button
                  onClick={clearFilters}
                  className="px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600"
                >
                  Clear Filters
                </button>
              </div>
            ) : (
              <>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {recipes.map((recipe, i) => (
                    <RecipeCard key={recipe.id} recipe={recipe} index={i} />
                  ))}
                </div>

                {totalPages > 1 && (
                  <div className="flex justify-center gap-2 mt-8">
                    {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                      <button
                        key={page}
                        onClick={() => updateFilter('page', page)}
                        className={`w-10 h-10 rounded-lg font-medium transition-colors ${
                          filters.page === page
                            ? 'bg-primary-500 text-white'
                            : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-primary-50'
                        }`}
                      >
                        {page}
                      </button>
                    ))}
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
