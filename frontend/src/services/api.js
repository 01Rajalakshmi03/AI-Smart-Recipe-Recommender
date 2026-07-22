import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  getMe: () => api.get('/auth/me'),
  updateMe: (data) => api.put('/auth/me', data),
};

export const recipeAPI = {
  getAll: (params) => api.get('/recipes', { params }),
  getById: (id) => api.get(`/recipes/${id}`),
  create: (data) => api.post('/recipes', data),
  update: (id, data) => api.put(`/recipes/${id}`, data),
  delete: (id) => api.delete(`/recipes/${id}`),
};

export const favoriteAPI = {
  toggle: (recipeId) => api.post('/favorites', { recipe_id: recipeId }),
  getAll: () => api.get('/favorites'),
};

export const commentAPI = {
  add: (data) => api.post('/comments', data),
  getByRecipe: (recipeId) => api.get(`/comments/${recipeId}`),
};

export const ratingAPI = {
  add: (data) => api.post('/ratings', data),
};

export const mealPlanAPI = {
  create: (data) => api.post('/meal-planner', data),
  getAll: (date) => api.get('/meal-planner', { params: { date } }),
  delete: (id) => api.delete(`/meal-planner/${id}`),
};

export const shoppingListAPI = {
  add: (data) => api.post('/shopping-list', data),
  getAll: () => api.get('/shopping-list'),
  toggle: (id) => api.put(`/shopping-list/${id}/toggle`),
  delete: (id) => api.delete(`/shopping-list/${id}`),
};

export const categoryAPI = {
  getAll: () => api.get('/categories'),
  create: (data) => api.post('/categories', data),
  delete: (id) => api.delete(`/categories/${id}`),
};

export const aiAPI = {
  generate: (data) => api.post('/ai/generate', data),
  explain: (data) => api.post('/ai/explain', data),
  recommendations: () => api.get('/ai/recommendations'),
};

export const adminAPI = {
  getStats: () => api.get('/admin/stats'),
  getUsers: () => api.get('/admin/users'),
  deleteUser: (id) => api.delete(`/admin/users/${id}`),
  getRecipes: () => api.get('/admin/recipes'),
  getComments: () => api.get('/admin/comments'),
  deleteComment: (id) => api.delete(`/admin/comments/${id}`),
};

export default api;
