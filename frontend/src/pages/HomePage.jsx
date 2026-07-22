import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiSearch, FiArrowRight, FiTrendingUp, FiStar, FiZap } from 'react-icons/fi';
import { recipeAPI, categoryAPI } from '../services/api';
import RecipeCard from '../components/recipes/RecipeCard';
import RecipeSkeleton from '../components/common/RecipeSkeleton';

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i) => ({ opacity: 1, y: 0, transition: { delay: i * 0.1, duration: 0.5 } }),
};

export default function HomePage() {
  const [recipes, setRecipes] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    Promise.all([
      recipeAPI.getAll({ per_page: 6 }),
      categoryAPI.getAll(),
    ]).then(([recipeRes, catRes]) => {
      setRecipes(recipeRes.data.items);
      setCategories(catRes.data);
    }).finally(() => setLoading(false));
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/recipes?search=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <div className="min-h-screen">
      <section className="relative bg-gradient-to-br from-primary-50 via-white to-orange-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 pt-24 pb-16 overflow-hidden">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-float" />
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-orange-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-float" style={{ animationDelay: '1s' }} />
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <motion.div
            initial="hidden"
            animate="visible"
            className="text-center max-w-3xl mx-auto"
          >
            <motion.div variants={fadeUp} custom={0} className="inline-flex items-center gap-2 px-4 py-2 bg-primary-100 dark:bg-primary-900/30 rounded-full text-primary-600 text-sm font-medium mb-6">
              <FiZap size={16} /> Powered by AI
            </motion.div>

            <motion.h1 variants={fadeUp} custom={1} className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
              Discover Recipes with{' '}
              <span className="gradient-text">AI Intelligence</span>
            </motion.h1>

            <motion.p variants={fadeUp} custom={2} className="text-lg text-gray-600 dark:text-gray-400 mb-8">
              Get personalized recipe recommendations powered by artificial intelligence.
              Search thousands of recipes, create meal plans, and explore new cuisines.
            </motion.p>

            <motion.form variants={fadeUp} custom={3} onSubmit={handleSearch} className="flex items-center max-w-xl mx-auto mb-8">
              <div className="relative flex-1">
                <FiSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search for recipes, ingredients, cuisines..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-4 rounded-l-xl bg-white dark:bg-gray-800 border border-r-0 border-gray-200 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-primary-500 text-gray-800 dark:text-white"
                />
              </div>
              <button
                type="submit"
                className="px-8 py-4 bg-primary-500 text-white rounded-r-xl hover:bg-primary-600 transition-colors font-medium"
              >
                Search
              </button>
            </motion.form>

            <motion.div variants={fadeUp} custom={4} className="flex flex-wrap items-center justify-center gap-4 text-sm text-gray-500">
              <span className="flex items-center gap-1"><FiTrendingUp size={14} /> Trending:</span>
              {['Chicken', 'Pasta', 'Curry', 'Tacos', 'Salmon', 'Paneer', 'BBQ', 'Smoothie'].map((tag) => (
                <Link
                  key={tag}
                  to={`/recipes?search=${tag}`}
                  className="px-3 py-1 bg-white dark:bg-gray-800 rounded-full border border-gray-200 dark:border-gray-700 hover:border-primary-400 hover:text-primary-500 transition-colors"
                >
                  {tag}
                </Link>
              ))}
            </motion.div>
          </motion.div>
        </div>
      </section>

      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Popular Categories</h2>
              <p className="text-gray-500 mt-1">Explore recipes by category</p>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
            {categories.map((cat, i) => (
              <motion.div
                key={cat.id}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.05 }}
              >
                <Link
                  to={`/recipes?category_id=${cat.id}`}
                  className="block p-6 bg-white dark:bg-gray-800 rounded-2xl shadow-card hover:shadow-card-hover hover:-translate-y-1 transition-all text-center"
                >
                  <span className="text-4xl mb-3 block">{cat.icon}</span>
                  <h3 className="font-semibold text-gray-800 dark:text-white text-sm">{cat.name}</h3>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Featured Recipes</h2>
              <p className="text-gray-500 mt-1">Handpicked recipes for you</p>
            </div>
            <Link
              to="/recipes"
              className="flex items-center gap-2 text-primary-500 hover:text-primary-600 font-medium"
            >
              View All <FiArrowRight size={16} />
            </Link>
          </div>

          {loading ? (
            <RecipeSkeleton count={6} />
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {recipes.map((recipe, i) => (
                <RecipeCard key={recipe.id} recipe={recipe} index={i} />
              ))}
            </div>
          )}
        </div>
      </section>

      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="bg-gradient-to-r from-primary-500 to-orange-500 rounded-3xl p-8 md:p-12 text-white relative overflow-hidden"
          >
            <div className="absolute inset-0 overflow-hidden">
              <div className="absolute -top-20 -right-20 w-64 h-64 bg-white/10 rounded-full" />
              <div className="absolute -bottom-20 -left-20 w-64 h-64 bg-white/10 rounded-full" />
            </div>

            <div className="relative max-w-2xl">
              <h2 className="text-3xl font-bold mb-4">Let AI Create Your Perfect Recipe</h2>
              <p className="text-white/80 mb-6">
                Tell us what ingredients you have or what you are craving, and our AI will generate a
                personalized recipe just for you.
              </p>
              <Link
                to="/ai-generator"
                className="inline-flex items-center gap-2 px-6 py-3 bg-white text-primary-500 rounded-xl font-semibold hover:bg-gray-100 transition-colors"
              >
                <FiZap size={18} /> Try AI Generator
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      <section className="py-16 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-8">What Our Users Say</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { name: 'Sarah M.', text: 'The AI suggestions are spot on! I have discovered so many new recipes.', rating: 5 },
              { name: 'John D.', text: 'Meal planning has never been easier. This app changed my cooking routine.', rating: 5 },
              { name: 'Priya K.', text: 'Love the Indian recipe collection. The AI generates authentic flavors.', rating: 5 },
            ].map((t, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-card"
              >
                <div className="flex gap-1 justify-center mb-3">
                  {Array.from({ length: t.rating }).map((_, j) => (
                    <FiStar key={j} size={16} className="text-yellow-400 fill-yellow-400" />
                  ))}
                </div>
                <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">"{t.text}"</p>
                <p className="font-semibold text-gray-800 dark:text-white">{t.name}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
