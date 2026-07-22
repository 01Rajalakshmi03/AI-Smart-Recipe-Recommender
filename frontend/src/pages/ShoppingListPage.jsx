import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiPlus, FiTrash2, FiCheck } from 'react-icons/fi';
import { shoppingListAPI } from '../services/api';
import { useToast } from '../context/ToastContext';

export default function ShoppingListPage() {
  const toast = useToast();
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState('');
  const [newQty, setNewQty] = useState('');

  useEffect(() => {
    shoppingListAPI.getAll().then((res) => setItems(res.data));
  }, []);

  const addItem = async (e) => {
    e.preventDefault();
    if (!newItem.trim()) return;
    try {
      const res = await shoppingListAPI.add({ item: newItem, quantity: newQty });
      setItems([...items, res.data]);
      setNewItem('');
      setNewQty('');
      toast.success('Item added');
    } catch { toast.error('Failed to add item'); }
  };

  const toggleItem = async (id) => {
    try {
      const res = await shoppingListAPI.toggle(id);
      setItems(items.map((item) => item.id === id ? { ...item, is_checked: res.data.is_checked } : item));
    } catch { toast.error('Failed to toggle item'); }
  };

  const removeItem = async (id) => {
    try {
      await shoppingListAPI.delete(id);
      setItems(items.filter((item) => item.id !== id));
      toast.success('Item removed');
    } catch { toast.error('Failed to remove item'); }
  };

  const unchecked = items.filter((i) => !i.is_checked);
  const checked = items.filter((i) => i.is_checked);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-20 pb-12">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Shopping List</h1>
          <p className="text-gray-500 mb-8">Keep track of ingredients you need</p>

          <form onSubmit={addItem} className="flex gap-2 mb-8">
            <input
              type="text"
              value={newItem}
              onChange={(e) => setNewItem(e.target.value)}
              placeholder="Add an item..."
              className="flex-1 px-4 py-2.5 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-sm focus:ring-2 focus:ring-primary-500"
            />
            <input
              type="text"
              value={newQty}
              onChange={(e) => setNewQty(e.target.value)}
              placeholder="Qty"
              className="w-24 px-3 py-2.5 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-sm focus:ring-2 focus:ring-primary-500"
            />
            <button
              type="submit"
              className="px-4 py-2.5 bg-primary-500 text-white rounded-xl hover:bg-primary-600"
            >
              <FiPlus size={18} />
            </button>
          </form>

          {unchecked.length > 0 && (
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-500 mb-3">To Buy ({unchecked.length})</h3>
              <div className="space-y-2">
                {unchecked.map((item) => (
                  <motion.div
                    key={item.id}
                    layout
                    className="flex items-center gap-3 p-3 bg-white dark:bg-gray-800 rounded-xl shadow-card"
                  >
                    <button onClick={() => toggleItem(item.id)} className="w-6 h-6 border-2 border-gray-300 rounded-full hover:border-primary-500 flex items-center justify-center">
                      {item.is_checked ? <FiCheck size={14} className="text-primary-500" /> : null}
                    </button>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-800 dark:text-white">{item.item}</p>
                      {item.quantity && <p className="text-xs text-gray-500">{item.quantity}</p>}
                    </div>
                    <button onClick={() => removeItem(item.id)} className="text-gray-400 hover:text-red-500">
                      <FiTrash2 size={16} />
                    </button>
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {checked.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-3">Got ({checked.length})</h3>
              <div className="space-y-2">
                {checked.map((item) => (
                  <motion.div
                    key={item.id}
                    layout
                    className="flex items-center gap-3 p-3 bg-gray-100 dark:bg-gray-700 rounded-xl opacity-60"
                  >
                    <button onClick={() => toggleItem(item.id)} className="w-6 h-6 bg-primary-500 rounded-full flex items-center justify-center">
                      <FiCheck size={14} className="text-white" />
                    </button>
                    <p className="flex-1 text-sm line-through text-gray-500">{item.item}</p>
                    <button onClick={() => removeItem(item.id)} className="text-gray-400 hover:text-red-500">
                      <FiTrash2 size={16} />
                    </button>
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {items.length === 0 && (
            <div className="text-center py-20">
              <span className="text-6xl mb-4 block">🛒</span>
              <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">Shopping list is empty</h3>
              <p className="text-gray-500">Add items you need to buy</p>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
