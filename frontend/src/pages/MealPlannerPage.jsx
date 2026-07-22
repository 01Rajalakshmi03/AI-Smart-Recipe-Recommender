import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiCalendar, FiPlus, FiTrash2, FiSearch } from 'react-icons/fi';
import { mealPlanAPI, recipeAPI } from '../services/api';
import { useToast } from '../context/ToastContext';

export default function MealPlannerPage() {
  const toast = useToast();
  const [plans, setPlans] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [showAdd, setShowAdd] = useState(false);
  const [recipes, setRecipes] = useState([]);
  const [search, setSearch] = useState('');

  useEffect(() => {
    mealPlanAPI.getAll(selectedDate).then((res) => setPlans(res.data));
  }, [selectedDate]);

  useEffect(() => {
    if (showAdd) {
      recipeAPI.getAll({ per_page: 20, search }).then((res) => setRecipes(res.data.items));
    }
  }, [showAdd, search]);

  const addPlan = async (recipeId, mealType) => {
    try {
      await mealPlanAPI.create({ date: selectedDate, meal_type: mealType, recipe_id: recipeId });
      const res = await mealPlanAPI.getAll(selectedDate);
      setPlans(res.data);
      setShowAdd(false);
      toast.success('Meal added to plan');
    } catch { toast.error('Failed to add meal'); }
  };

  const removePlan = async (planId) => {
    try {
      await mealPlanAPI.delete(planId);
      setPlans(plans.filter((p) => p.id !== planId));
      toast.success('Meal removed');
    } catch { toast.error('Failed to remove meal'); }
  };

  const mealTypes = ['breakfast', 'lunch', 'dinner', 'snack'];
  const mealIcons = { breakfast: '🌅', lunch: '☀️', dinner: '🌙', snack: '🍿' };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-20 pb-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Meal Planner</h1>
              <p className="text-gray-500 mt-1">Plan your meals for the week</p>
            </div>
            <div className="flex items-center gap-3">
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                className="px-3 py-2 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-sm"
              />
              <button
                onClick={() => setShowAdd(!showAdd)}
                className="flex items-center gap-2 px-4 py-2 bg-primary-500 text-white rounded-xl hover:bg-primary-600 text-sm font-medium"
              >
                <FiPlus size={16} /> Add Meal
              </button>
            </div>
          </div>

          {showAdd && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="bg-white dark:bg-gray-800 rounded-2xl shadow-card p-6 mb-6"
            >
              <div className="relative mb-4">
                <FiSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search recipes..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-sm"
                />
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-h-64 overflow-y-auto">
                {recipes.map((recipe) => (
                  <div key={recipe.id} className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-xl">
                    <img src={recipe.image} alt="" className="w-12 h-12 rounded-lg object-cover" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-800 dark:text-white truncate">{recipe.title}</p>
                      <p className="text-xs text-gray-500">{recipe.cooking_time} min</p>
                    </div>
                    <div className="flex gap-1">
                      {mealTypes.map((type) => (
                        <button
                          key={type}
                          onClick={() => addPlan(recipe.id, type)}
                          className="px-2 py-1 text-xs bg-primary-100 dark:bg-primary-900/30 text-primary-600 rounded-lg hover:bg-primary-200"
                          title={`Add as ${type}`}
                        >
                          {mealIcons[type]}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          <div className="space-y-4">
            {mealTypes.map((type) => {
              const typePlans = plans.filter((p) => p.meal_type === type);
              return (
                <div key={type} className="bg-white dark:bg-gray-800 rounded-2xl shadow-card p-6">
                  <h3 className="font-semibold text-gray-800 dark:text-white mb-4 flex items-center gap-2">
                    <span className="text-xl">{mealIcons[type]}</span> {type.charAt(0).toUpperCase() + type.slice(1)}
                  </h3>
                  {typePlans.length === 0 ? (
                    <p className="text-sm text-gray-400">No meals planned</p>
                  ) : (
                    <div className="space-y-3">
                      {typePlans.map((plan) => (
                        <div key={plan.id} className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-xl">
                          {plan.recipe?.image && (
                            <img src={plan.recipe.image} alt="" className="w-12 h-12 rounded-lg object-cover" />
                          )}
                          <div className="flex-1">
                            <p className="font-medium text-sm text-gray-800 dark:text-white">{plan.recipe?.title}</p>
                            <p className="text-xs text-gray-500">{plan.recipe?.calories} cal | {plan.recipe?.cooking_time} min</p>
                          </div>
                          <button onClick={() => removePlan(plan.id)} className="text-red-400 hover:text-red-500">
                            <FiTrash2 size={16} />
                          </button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
