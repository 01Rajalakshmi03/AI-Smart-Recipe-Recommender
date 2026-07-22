import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiUsers, FiBook, FiMessageSquare, FiTrash2, FiBarChart2 } from 'react-icons/fi';
import { adminAPI } from '../services/api';
import { useToast } from '../context/ToastContext';

export default function AdminDashboardPage() {
  const toast = useToast();
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [recipes, setRecipes] = useState([]);
  const [comments, setComments] = useState([]);
  const [activeTab, setActiveTab] = useState('stats');

  useEffect(() => {
    adminAPI.getStats().then((res) => setStats(res.data));
    adminAPI.getUsers().then((res) => setUsers(res.data));
    adminAPI.getRecipes().then((res) => setRecipes(res.data));
    adminAPI.getComments().then((res) => setComments(res.data));
  }, []);

  const deleteUser = async (id) => {
    if (!confirm('Are you sure?')) return;
    try {
      await adminAPI.deleteUser(id);
      setUsers(users.filter((u) => u.id !== id));
      toast.success('User deleted');
    } catch { toast.error('Failed to delete user'); }
  };

  const deleteComment = async (id) => {
    try {
      await adminAPI.deleteComment(id);
      setComments(comments.filter((c) => c.id !== id));
      toast.success('Comment deleted');
    } catch { toast.error('Failed to delete comment'); }
  };

  const tabs = [
    { id: 'stats', label: 'Overview', icon: <FiBarChart2 size={18} /> },
    { id: 'users', label: 'Users', icon: <FiUsers size={18} /> },
    { id: 'recipes', label: 'Recipes', icon: <FiBook size={18} /> },
    { id: 'comments', label: 'Comments', icon: <FiMessageSquare size={18} /> },
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-20 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">Admin Dashboard</h1>

          <div className="flex gap-2 mb-8 overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium whitespace-nowrap transition-colors ${
                  activeTab === tab.id
                    ? 'bg-primary-500 text-white'
                    : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-100'
                }`}
              >
                {tab.icon} {tab.label}
              </button>
            ))}
          </div>

          {activeTab === 'stats' && stats && (
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
              {[
                { label: 'Total Users', value: stats.total_users, icon: <FiUsers />, color: 'bg-blue-500' },
                { label: 'Total Recipes', value: stats.total_recipes, icon: <FiBook />, color: 'bg-green-500' },
                { label: 'Total Comments', value: stats.total_comments, icon: <FiMessageSquare />, color: 'bg-yellow-500' },
                { label: 'AI Generated', value: stats.ai_generated, icon: <FiBarChart2 />, color: 'bg-purple-500' },
              ].map((stat, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="bg-white dark:bg-gray-800 rounded-2xl shadow-card p-6"
                >
                  <div className={`w-12 h-12 ${stat.color} rounded-xl flex items-center justify-center text-white mb-3`}>
                    {stat.icon}
                  </div>
                  <p className="text-3xl font-bold text-gray-800 dark:text-white">{stat.value}</p>
                  <p className="text-sm text-gray-500">{stat.label}</p>
                </motion.div>
              ))}
            </div>
          )}

          {activeTab === 'users' && (
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-card overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th className="px-6 py-3 text-left font-medium text-gray-500">User</th>
                      <th className="px-6 py-3 text-left font-medium text-gray-500">Email</th>
                      <th className="px-6 py-3 text-left font-medium text-gray-500">Role</th>
                      <th className="px-6 py-3 text-left font-medium text-gray-500">Joined</th>
                      <th className="px-6 py-3 text-right font-medium text-gray-500">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                    {users.map((user) => (
                      <tr key={user.id}>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center text-white text-sm font-medium">
                              {user.username[0].toUpperCase()}
                            </div>
                            <span className="font-medium text-gray-800 dark:text-white">{user.username}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-gray-500">{user.email}</td>
                        <td className="px-6 py-4">
                          <span className={`px-2 py-0.5 text-xs font-medium rounded-full ${
                            user.role === 'admin' ? 'bg-purple-100 text-purple-700' : 'bg-gray-100 text-gray-700'
                          }`}>{user.role}</span>
                        </td>
                        <td className="px-6 py-4 text-gray-500">{new Date(user.created_at).toLocaleDateString()}</td>
                        <td className="px-6 py-4 text-right">
                          <button onClick={() => deleteUser(user.id)} className="text-red-400 hover:text-red-500">
                            <FiTrash2 size={16} />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'recipes' && (
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-card overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th className="px-6 py-3 text-left font-medium text-gray-500">Recipe</th>
                      <th className="px-6 py-3 text-left font-medium text-gray-500">Cuisine</th>
                      <th className="px-6 py-3 text-left font-medium text-gray-500">Difficulty</th>
                      <th className="px-6 py-3 text-left font-medium text-gray-500">AI</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                    {recipes.map((recipe) => (
                      <tr key={recipe.id}>
                        <td className="px-6 py-4 font-medium text-gray-800 dark:text-white">{recipe.title}</td>
                        <td className="px-6 py-4 text-gray-500">{recipe.cuisine}</td>
                        <td className="px-6 py-4">
                          <span className={`px-2 py-0.5 text-xs font-medium rounded-full ${
                            recipe.difficulty === 'Easy' ? 'bg-green-100 text-green-700' :
                            recipe.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                            'bg-red-100 text-red-700'
                          }`}>{recipe.difficulty}</span>
                        </td>
                        <td className="px-6 py-4">{recipe.is_ai_generated ? '✨' : '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'comments' && (
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-card overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th className="px-6 py-3 text-left font-medium text-gray-500">User</th>
                      <th className="px-6 py-3 text-left font-medium text-gray-500">Comment</th>
                      <th className="px-6 py-3 text-left font-medium text-gray-500">Date</th>
                      <th className="px-6 py-3 text-right font-medium text-gray-500">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                    {comments.map((comment) => (
                      <tr key={comment.id}>
                        <td className="px-6 py-4 text-gray-800 dark:text-white">User #{comment.user_id}</td>
                        <td className="px-6 py-4 text-gray-500 max-w-xs truncate">{comment.content}</td>
                        <td className="px-6 py-4 text-gray-500">{new Date(comment.created_at).toLocaleDateString()}</td>
                        <td className="px-6 py-4 text-right">
                          <button onClick={() => deleteComment(comment.id)} className="text-red-400 hover:text-red-500">
                            <FiTrash2 size={16} />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
