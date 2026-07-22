import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiZap, FiLoader } from 'react-icons/fi';
import { aiAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';

const quickPrompts = [
  { label: '🍳 Breakfast', prompt: 'Give me a quick and healthy breakfast recipe' },
  { label: '🥗 Healthy Lunch', prompt: 'Suggest a nutritious low-calorie lunch' },
  { label: '🍛 Indian Curry', prompt: 'Create an authentic Indian curry recipe' },
  { label: '🍝 Italian Pasta', prompt: 'Suggest a classic Italian pasta dish' },
  { label: '💪 High Protein', prompt: 'Generate a high protein meal for muscle building' },
  { label: '🥬 Vegetarian', prompt: 'Create a delicious vegetarian dinner' },
  { label: '🌱 Vegan', prompt: 'Suggest a satisfying vegan meal' },
  { label: '🍗 Non-Veg', prompt: 'Create a delicious non-vegetarian chicken or meat recipe' },
  { label: '🦐 Seafood', prompt: 'Suggest a fresh seafood recipe with shrimp or fish' },
  { label: '🔥 BBQ & Grill', prompt: 'Create a smoky grilled or BBQ recipe' },
  { label: '👶 Kids Friendly', prompt: 'Create a meal that kids will love' },
  { label: '🏋️ Weight Loss', prompt: 'Generate a weight loss friendly dinner under 400 calories' },
  { label: '🥑 Keto', prompt: 'Create a low-carb keto-friendly meal' },
  { label: '⚡ Quick Meal', prompt: 'Suggest a meal ready in under 15 minutes' },
];

export default function AIGeneratorPage() {
  const { user } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();
  const [prompt, setPrompt] = useState('');
  const [mealType, setMealType] = useState('');
  const [cuisine, setCuisine] = useState('');
  const [dietary, setDietary] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!user) { toast.warning('Please login to use AI Generator'); navigate('/login'); return; }
    if (!prompt.trim()) { toast.warning('Please enter a prompt'); return; }

    setLoading(true);
    try {
      const res = await aiAPI.generate({ prompt, meal_type: mealType, cuisine, dietary });
      toast.success('Recipe generated successfully!');
      navigate(`/recipes/${res.data.recipe_id}`);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to generate recipe. Make sure GEMINI_API_KEY is configured.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-20 pb-12">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="text-center mb-10">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-100 dark:bg-purple-900/30 rounded-full text-purple-600 text-sm font-medium mb-4">
              <FiZap size={16} /> AI Powered
            </div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-3">AI Recipe Generator</h1>
            <p className="text-gray-500">Tell us what you want and let AI create the perfect recipe for you</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-card p-6 mb-8">
            <h3 className="font-semibold text-gray-800 dark:text-white mb-3">Quick Prompts</h3>
            <div className="flex flex-wrap gap-2">
              {quickPrompts.map((qp) => (
                <button
                  key={qp.label}
                  onClick={() => setPrompt(qp.prompt)}
                  className="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 rounded-full hover:bg-primary-50 hover:text-primary-600 transition-colors"
                >
                  {qp.label}
                </button>
              ))}
            </div>
          </div>

          <form onSubmit={handleGenerate} className="bg-white dark:bg-gray-800 rounded-2xl shadow-card p-6 space-y-6">
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
                What do you want to cook?
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="e.g., A spicy Thai chicken dish with vegetables..."
                rows={4}
                className="w-full px-4 py-3 rounded-xl bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 resize-none"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">Meal Type</label>
                <select
                  value={mealType}
                  onChange={(e) => setMealType(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-sm"
                >
                  <option value="">Any</option>
                  <option value="breakfast">Breakfast</option>
                  <option value="lunch">Lunch</option>
                  <option value="dinner">Dinner</option>
                  <option value="snack">Snack</option>
                </select>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">Cuisine</label>
                <select
                  value={cuisine}
                  onChange={(e) => setCuisine(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-sm"
                >
                  <option value="">Any</option>
                  <option value="Indian">Indian</option>
                  <option value="Italian">Italian</option>
                  <option value="Chinese">Chinese</option>
                  <option value="Mexican">Mexican</option>
                  <option value="Thai">Thai</option>
                  <option value="Japanese">Japanese</option>
                  <option value="American">American</option>
                  <option value="Mediterranean">Mediterranean</option>
                  <option value="French">French</option>
                  <option value="Korean">Korean</option>
                  <option value="Vietnamese">Vietnamese</option>
                </select>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">Dietary</label>
                <select
                  value={dietary}
                  onChange={(e) => setDietary(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-sm"
                >
                  <option value="">None</option>
                  <option value="vegetarian">Vegetarian</option>
                  <option value="vegan">Vegan</option>
                  <option value="gluten-free">Gluten Free</option>
                  <option value="keto">Keto</option>
                  <option value="diabetic">Diabetic Friendly</option>
                </select>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading || !prompt.trim()}
              className="w-full py-3 bg-gradient-to-r from-primary-500 to-orange-500 text-white rounded-xl font-semibold hover:from-primary-600 hover:to-orange-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <><FiLoader className="animate-spin" size={18} /> Generating Recipe...</>
              ) : (
                <><FiZap size={18} /> Generate Recipe</>
              )}
            </button>
          </form>
        </motion.div>
      </div>
    </div>
  );
}
