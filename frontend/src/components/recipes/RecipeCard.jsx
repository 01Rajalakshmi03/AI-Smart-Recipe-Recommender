import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiClock, FiHeart, FiStar, FiUsers } from 'react-icons/fi';

export default function RecipeCard({ recipe, index = 0 }) {
  const difficultyColor = {
    Easy: 'bg-green-100 text-green-700',
    Medium: 'bg-yellow-100 text-yellow-700',
    Hard: 'bg-red-100 text-red-700',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05, duration: 0.4 }}
      whileHover={{ y: -5 }}
      className="group"
    >
      <Link to={`/recipes/${recipe.id}`}>
        <div className="bg-white dark:bg-gray-800 rounded-2xl overflow-hidden shadow-card hover:shadow-card-hover transition-all duration-300">
          <div className="relative h-48 overflow-hidden">
            <img
              src={recipe.image || 'https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=500'}
              alt={recipe.title}
              className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
            />
            {recipe.is_ai_generated === 1 && (
              <div className="absolute top-3 left-3 px-2 py-1 bg-purple-500 text-white text-xs font-medium rounded-full flex items-center gap-1">
                <span>✨</span> AI
              </div>
            )}
            {recipe.is_vegetarian === 1 && (
              <div className="absolute top-3 right-3 px-2 py-1 bg-green-500 text-white text-xs font-medium rounded-full">
                🥬 Veg
              </div>
            )}
            {recipe.is_non_veg === 1 && (
              <div className="absolute top-3 right-3 px-2 py-1 bg-red-500 text-white text-xs font-medium rounded-full">
                🍗 Non-Veg
              </div>
            )}
            {recipe.is_vegan === 1 && (
              <div className={`absolute ${recipe.is_vegetarian === 1 || recipe.is_non_veg === 1 ? 'top-10 right-3' : 'top-3 right-3'} px-2 py-1 bg-emerald-500 text-white text-xs font-medium rounded-full`}>
                🌱 Vegan
              </div>
            )}
            {recipe.is_gluten_free === 1 && (
              <div className={`absolute ${recipe.is_vegetarian === 1 || recipe.is_non_veg === 1 || recipe.is_vegan === 1 ? 'top-[5.5rem] right-3' : 'top-3 right-3'} px-2 py-1 bg-amber-500 text-white text-xs font-medium rounded-full`}>
                🌾 GF
              </div>
            )}
          </div>

          <div className="p-4">
            <div className="flex items-center gap-2 mb-2">
              {recipe.category && (
                <span className="text-xs text-primary-500 font-medium">
                  {recipe.category.icon} {recipe.category.name}
                </span>
              )}
              <span className={`text-xs px-2 py-0.5 rounded-full ${difficultyColor[recipe.difficulty] || ''}`}>
                {recipe.difficulty}
              </span>
            </div>

            <h3 className="font-semibold text-gray-800 dark:text-white mb-1 group-hover:text-primary-500 transition-colors line-clamp-1">
              {recipe.title}
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-2 mb-3">
              {recipe.description}
            </p>

            <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
              <div className="flex items-center gap-3">
                <span className="flex items-center gap-1">
                  <FiClock size={14} /> {recipe.cooking_time}m
                </span>
                <span className="flex items-center gap-1">
                  <FiUsers size={14} /> {recipe.servings || 2}
                </span>
              </div>
              {recipe.average_rating > 0 && (
                <span className="flex items-center gap-1 text-yellow-500">
                  <FiStar size={14} /> {recipe.average_rating}
                </span>
              )}
            </div>

            {recipe.calories > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700">
                <span className="text-xs text-gray-500">{recipe.calories} cal</span>
              </div>
            )}
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
