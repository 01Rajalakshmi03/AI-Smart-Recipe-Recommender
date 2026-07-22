import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiHeart } from 'react-icons/fi';
import { favoriteAPI } from '../services/api';
import RecipeCard from '../components/recipes/RecipeCard';
import RecipeSkeleton from '../components/common/RecipeSkeleton';

export default function FavoritesPage() {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    favoriteAPI.getAll()
      .then((res) => setFavorites(res.data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-20 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">My Favorites</h1>
          <p className="text-gray-500 mb-8">Recipes you have saved</p>

          {loading ? (
            <RecipeSkeleton count={6} />
          ) : favorites.length === 0 ? (
            <div className="text-center py-20">
              <FiHeart size={64} className="mx-auto text-gray-300 mb-4" />
              <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">No favorites yet</h3>
              <p className="text-gray-500">Start exploring recipes and save your favorites!</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {favorites.map((fav, i) => fav.recipe && (
                <RecipeCard key={fav.id} recipe={fav.recipe} index={i} />
              ))}
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
