import { Link } from 'react-router-dom';
import { FiGithub, FiTwitter, FiInstagram, FiMail } from 'react-icons/fi';

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-8">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <span className="text-2xl">🍳</span>
              <span className="text-xl font-bold text-white">RecipeAI</span>
            </div>
            <p className="text-sm text-gray-400">
              AI-powered recipe recommendations for every occasion. Discover, cook, and enjoy.
            </p>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li><Link to="/recipes" className="hover:text-primary-400 transition-colors">Browse Recipes</Link></li>
              <li><Link to="/ai-generator" className="hover:text-primary-400 transition-colors">AI Generator</Link></li>
              <li><Link to="/meal-planner" className="hover:text-primary-400 transition-colors">Meal Planner</Link></li>
              <li><Link to="/shopping-list" className="hover:text-primary-400 transition-colors">Shopping List</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-4">Categories</h3>
            <ul className="space-y-2 text-sm">
              <li><Link to="/recipes?meal_type=breakfast" className="hover:text-primary-400 transition-colors">🍳 Breakfast</Link></li>
              <li><Link to="/recipes?meal_type=lunch" className="hover:text-primary-400 transition-colors">🥗 Lunch</Link></li>
              <li><Link to="/recipes?meal_type=dinner" className="hover:text-primary-400 transition-colors">🍽️ Dinner</Link></li>
              <li><Link to="/recipes?category_id=7" className="hover:text-primary-400 transition-colors">🦐 Seafood</Link></li>
              <li><Link to="/recipes?category_id=8" className="hover:text-primary-400 transition-colors">🔥 BBQ & Grill</Link></li>
              <li><Link to="/recipes?category_id=9" className="hover:text-primary-400 transition-colors">🍝 Pasta</Link></li>
              <li><Link to="/recipes?category_id=12" className="hover:text-primary-400 transition-colors">🍛 Indian</Link></li>
              <li><Link to="/recipes?category_id=13" className="hover:text-primary-400 transition-colors">🌮 Mexican</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-4">Dietary</h3>
            <ul className="space-y-2 text-sm">
              <li><Link to="/recipes?is_vegetarian=1" className="hover:text-primary-400 transition-colors">🥬 Vegetarian</Link></li>
              <li><Link to="/recipes?is_vegan=1" className="hover:text-primary-400 transition-colors">🌱 Vegan</Link></li>
              <li><Link to="/recipes?is_non_veg=1" className="hover:text-primary-400 transition-colors">🍗 Non-Veg</Link></li>
              <li><Link to="/recipes?is_gluten_free=1" className="hover:text-primary-400 transition-colors">🌾 Gluten-Free</Link></li>
              <li><Link to="/recipes?is_keto=1" className="hover:text-primary-400 transition-colors">🥑 Keto</Link></li>
              <li><Link to="/recipes?is_dairy_free=1" className="hover:text-primary-400 transition-colors">🥛 Dairy-Free</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-4">Connect</h3>
            <div className="flex gap-4">
              <a href="#" className="hover:text-primary-400 transition-colors"><FiGithub size={20} /></a>
              <a href="#" className="hover:text-primary-400 transition-colors"><FiTwitter size={20} /></a>
              <a href="#" className="hover:text-primary-400 transition-colors"><FiInstagram size={20} /></a>
              <a href="#" className="hover:text-primary-400 transition-colors"><FiMail size={20} /></a>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
          <p>&copy; 2024 AI Smart Recipe Recommender. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
