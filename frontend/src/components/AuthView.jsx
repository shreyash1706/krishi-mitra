import { useState } from 'react';
import axios from 'axios';
import { Leaf, User } from 'lucide-react';
import { motion } from 'framer-motion';

const DISTRICTS = [
  "Ahmednagar", "Akola", "Amravati", "Beed", "Bhandara", "Buldhana", "Chandrapur", 
  "Chhatrapati Sambhajinagar", "Dharashiv", "Dhule", "Gadchiroli", "Gondia", "Hingoli", 
  "Jalgaon", "Jalna", "Kolhapur", "Latur", "Mumbai City", "Mumbai Suburban", "Nagpur", 
  "Nanded", "Nandurbar", "Nashik", "Palghar", "Parbhani", "Pune", "Raigad", "Ratnagiri", 
  "Sangli", "Satara", "Sindhudurg", "Solapur", "Thane", "Wardha", "Washim", "Yavatmal"
];

export default function AuthView({ onLogin }) {
  const [formData, setFormData] = useState({
    user_id: '',
    name: '',
    district: DISTRICTS[0],
    village: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await axios.post('http://127.0.0.1:8000/register', formData);
      onLogin(formData);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to connect to backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center p-4 overflow-hidden bg-slate-900">
      {/* Dynamic Background */}
      <div 
        className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1625246333195-78d9c38ad449?q=80&w=2670&auto=format&fit=crop')] bg-cover bg-center opacity-40 scale-105"
        style={{ filter: "brightness(0.6)" }}
      />
      <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-900/60 to-transparent" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-emerald-500/20 rounded-full blur-3xl" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-teal-500/20 rounded-full blur-3xl animate-pulse" />

      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="glass-panel w-full max-w-md rounded-3xl p-8 sm:p-10 relative z-10 premium-shadow border border-white/10 bg-slate-900/60 backdrop-blur-2xl"
      >
        <div className="text-center mb-8">
          <motion.div 
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0.2 }}
            className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 text-white mb-6 shadow-lg shadow-emerald-500/30 floating-icon"
          >
            <Leaf size={36} strokeWidth={2.5} />
          </motion.div>
          <h1 className="text-4xl font-extrabold tracking-tight text-white mb-2 font-sans">
            Krishi <span className="text-gradient">Mitra</span>
          </h1>
          <p className="text-emerald-100/80 font-medium text-lg">Your AI Farming Assistant</p>
        </div>

        {error && (
          <motion.div 
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            className="mb-6 bg-red-500/10 border border-red-500/50 text-red-200 text-sm p-4 rounded-xl text-center"
          >
            {error}
          </motion.div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-1.5 ml-1">User ID</label>
            <div className="relative">
              <input 
                required
                type="text" 
                value={formData.user_id}
                onChange={e => setFormData({...formData, user_id: e.target.value})}
                className="w-full bg-slate-800/50 border border-slate-600/50 rounded-xl px-4 py-3.5 pl-11 text-white outline-none focus:border-emerald-500 focus:bg-slate-800 focus:ring-4 focus:ring-emerald-500/20 transition-all font-medium"
                placeholder="e.g. kisan_123"
              />
              <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-1.5 ml-1">Name</label>
            <input 
              required
              type="text" 
              value={formData.name}
              onChange={e => setFormData({...formData, name: e.target.value})}
              className="w-full bg-slate-800/50 border border-slate-600/50 rounded-xl px-4 py-3.5 text-white outline-none focus:border-emerald-500 focus:bg-slate-800 focus:ring-4 focus:ring-emerald-500/20 transition-all font-medium"
              placeholder="e.g. Ramesh"
            />
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-1.5 ml-1">District</label>
            <select 
              value={formData.district}
              onChange={e => setFormData({...formData, district: e.target.value})}
              className="w-full bg-slate-800/50 border border-slate-600/50 rounded-xl px-4 py-3.5 text-white outline-none focus:border-emerald-500 focus:bg-slate-800 focus:ring-4 focus:ring-emerald-500/20 transition-all font-medium appearance-none cursor-pointer"
            >
              {DISTRICTS.map(d => <option key={d} value={d} className="bg-slate-800 text-white">{d}</option>)}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-1.5 ml-1">Village / Taluka <span className="text-slate-500 font-normal">(Optional)</span></label>
            <input 
              type="text" 
              value={formData.village}
              onChange={e => setFormData({...formData, village: e.target.value})}
              className="w-full bg-slate-800/50 border border-slate-600/50 rounded-xl px-4 py-3.5 text-white outline-none focus:border-emerald-500 focus:bg-slate-800 focus:ring-4 focus:ring-emerald-500/20 transition-all font-medium"
              placeholder="Your village name"
            />
          </div>

          <motion.button 
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            disabled={loading}
            type="submit" 
            className="w-full mt-8 farmer-gradient text-white font-bold py-4 rounded-xl transition-all shadow-lg shadow-emerald-500/30 flex items-center justify-center gap-2 disabled:opacity-70 text-lg"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Connecting...
              </>
            ) : "Enter Chat"}
          </motion.button>
        </form>
      </motion.div>
    </div>
  );
}

