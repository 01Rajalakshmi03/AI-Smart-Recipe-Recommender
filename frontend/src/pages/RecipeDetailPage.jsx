import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiClock, FiUsers, FiHeart, FiStar, FiShare2, FiArrowLeft, FiMessageSquare } from 'react-icons/fi';
import { recipeAPI, favoriteAPI, commentAPI, ratingAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import Loading from '../components/common/Loading';

export default function RecipeDetailPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const toast = useToast();
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isFavorite, setIsFavorite] = useState(false);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [userRating, setUserRating] = useState(0);

  useEffect(() => {
    recipeAPI.getById(id).then((res) => {
      setRecipe(res.data);
      setLoading(false);
    });
    commentAPI.getByRecipe(id).then((res) => setComments(res.data));
  }, [id]);

  const toggleFavorite = async () => {
    if (!user) { toast.warning('Please login to add favorites'); return; }
    try {
      const res = await favoriteAPI.toggle(parseInt(id));
      setIsFavorite(res.data.is_favorite);
      toast.success(res.data.message);
    } catch { toast.error('Failed to update favorite'); }
  };

  const submitComment = async (e) => {
    e.preventDefault();
    if (!user) { toast.warning('Please login to comment'); return; }
    if (!newComment.trim()) return;
    try {
      await commentAPI.add({ content: newComment, recipe_id: parseInt(id) });
      const res = await commentAPI.getByRecipe(id);
      setComments(res.data);
      setNewComment('');
      toast.success('Comment added');
    } catch { toast.error('Failed to add comment'); }
  };

  const submitRating = async (score) => {
    if (!user) { toast.warning('Please login to rate'); return; }
    try {
      await ratingAPI.add({ score, recipe_id: parseInt(id) });
      setUserRating(score);
      toast.success('Rating submitted');
    } catch { toast.error('Failed to submit rating'); }
  };

  if (loading) return <Loading />;
  if (!recipe) return <div className="text-center py-20 text-gray-500">Recipe not found</div>;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-20 pb-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <Link to="/recipes" className="inline-flex items-center gap-2 text-gray-500 hover:text-primary-500 mb-6">
          <FiArrowLeft size={18} /> Back to Recipes
        </Link>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="relative h-64 sm:h-96 rounded-2xl overflow-hidden mb-8">
            <img
              src={recipe.image || 'https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=500'}
              alt={recipe.title}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
            <div className="absolute bottom-6 left-6 right-6 text-white">
              <div className="flex items-center gap-2 mb-2 flex-wrap">
                {recipe.category && (
                  <span className="px-3 py-1 bg-white/20 backdrop-blur rounded-full text-sm">
                    {recipe.category.icon} {recipe.category.name}
                  </span>
                )}
                {recipe.is_ai_generated === 1 && (
                  <span className="px-3 py-1 bg-purple-500/80 backdrop-blur rounded-full text-sm">✨ AI Generated</span>
                )}
                {recipe.is_vegetarian === 1 && (
                  <span className="px-3 py-1 bg-green-500/80 backdrop-blur rounded-full text-sm">🥬 Vegetarian</span>
                )}
                {recipe.is_non_veg === 1 && (
                  <span className="px-3 py-1 bg-red-500/80 backdrop-blur rounded-full text-sm">🍗 Non-Veg</span>
                )}
                {recipe.is_vegan === 1 && (
                  <span className="px-3 py-1 bg-emerald-500/80 backdrop-blur rounded-full text-sm">🌱 Vegan</span>
                )}
                {recipe.is_gluten_free === 1 && (
                  <span className="px-3 py-1 bg-amber-500/80 backdrop-blur rounded-full text-sm">🌾 Gluten-Free</span>
                )}
                {recipe.is_keto === 1 && (
                  <span className="px-3 py-1 bg-teal-500/80 backdrop-blur rounded-full text-sm">🥑 Keto</span>
                )}
                {recipe.is_dairy_free === 1 && (
                  <span className="px-3 py-1 bg-blue-500/80 backdrop-blur rounded-full text-sm">🥛 Dairy-Free</span>
                )}
              </div>
              <h1 className="text-3xl font-bold">{recipe.title}</h1>
            </div>

            <div className="absolute top-4 right-4 flex gap-2">
              <button
                onClick={toggleFavorite}
                className={`p-3 rounded-full backdrop-blur ${isFavorite ? 'bg-red-500 text-white' : 'bg-white/20 text-white hover:bg-white/30'}`}
              >
                <FiHeart size={20} fill={isFavorite ? 'currentColor' : 'none'} />
              </button>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
            {[
              { icon: <FiClock />, label: 'Cook Time', value: `${recipe.cooking_time} min` },
              { icon: <FiUsers />, label: 'Servings', value: recipe.servings },
              { icon: <FiStar />, label: 'Difficulty', value: recipe.difficulty },
              { icon: <span className="text-lg">🔥</span>, label: 'Calories', value: `${recipe.calories} kcal` },
            ].map((item, i) => (
              <div key={i} className="bg-white dark:bg-gray-800 rounded-xl p-4 text-center shadow-card">
                <div className="text-primary-500 flex justify-center mb-1">{item.icon}</div>
                <p className="text-xs text-gray-500">{item.label}</p>
                <p className="font-semibold text-gray-800 dark:text-white">{item.value}</p>
              </div>
            ))}
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-card p-6 mb-8">
            <h2 className="text-xl font-bold text-gray-800 dark:text-white mb-3">Description</h2>
            <p className="text-gray-600 dark:text-gray-400">{recipe.description}</p>
          </div>

          {recipe.protein > 0 && (
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-card p-6 mb-8">
              <h2 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Nutrition Facts</h2>
              <div className="grid grid-cols-4 gap-4">
                {[
                  { label: 'Calories', value: recipe.calories, color: 'text-red-500' },
                  { label: 'Protein', value: `${recipe.protein}g`, color: 'text-blue-500' },
                  { label: 'Carbs', value: `${recipe.carbs}g`, color: 'text-green-500' },
                  { label: 'Fat', value: `${recipe.fat}g`, color: 'text-yellow-500' },
                ].map((n, i) => (
                  <div key={i} className="text-center">
                    <p className={`text-2xl font-bold ${n.color}`}>{n.value}</p>
                    <p className="text-sm text-gray-500">{n.label}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="grid md:grid-cols-2 gap-8 mb-8">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-card p-6">
              <h2 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Ingredients</h2>
              <ul className="space-y-2">
                {recipe.ingredients?.map((ri, i) => (
                  <li key={i} className="flex items-center gap-3 text-gray-600 dark:text-gray-400">
                    <span className="w-2 h-2 bg-primary-400 rounded-full flex-shrink-0" />
                    <span>{ri.quantity} {ri.unit} {ri.ingredient?.name || ri.name}</span>
                    {ri.notes && <span className="text-xs text-gray-400">({ri.notes})</span>}
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-card p-6">
              <h2 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Instructions</h2>
              <div className="space-y-3">
                {recipe.instructions?.split(/\d+\.\s*/).filter(Boolean).map((step, i) => (
                  <div key={i} className="flex gap-3">
                    <span className="w-6 h-6 bg-primary-500 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">
                      {i + 1}
                    </span>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">{step.trim()}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {user && (
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-card p-6 mb-8">
              <h2 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Rate This Recipe</h2>
              <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map((score) => (
                  <button
                    key={score}
                    onClick={() => submitRating(score)}
                    className={`p-2 rounded-lg transition-colors ${
                      userRating >= score ? 'text-yellow-400' : 'text-gray-300 hover:text-yellow-300'
                    }`}
                  >
                    <FiStar size={28} fill={userRating >= score ? 'currentColor' : 'none'} />
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-card p-6">
            <h2 className="text-xl font-bold text-gray-800 dark:text-white mb-4">
              Comments ({comments.length})
            </h2>

            {user && (
              <form onSubmit={submitComment} className="flex gap-3 mb-6">
                <input
                  type="text"
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  placeholder="Add a comment..."
                  className="flex-1 px-4 py-2 rounded-xl bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 text-sm"
                />
                <button
                  type="submit"
                  className="px-4 py-2 bg-primary-500 text-white rounded-xl hover:bg-primary-600 text-sm font-medium"
                >
                  Post
                </button>
              </form>
            )}

            <div className="space-y-4">
              {comments.map((comment) => (
                <div key={comment.id} className="flex gap-3">
                  <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 text-sm font-medium flex-shrink-0">
                    {comment.user?.username?.[0]?.toUpperCase() || '?'}
                  </div>
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-medium text-sm text-gray-800 dark:text-white">{comment.user?.username}</span>
                      <span className="text-xs text-gray-400">{new Date(comment.created_at).toLocaleDateString()}</span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">{comment.content}</p>
                  </div>
                </div>
              ))}
              {comments.length === 0 && (
                <p className="text-gray-400 text-sm text-center py-4">No comments yet. Be the first to comment!</p>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
