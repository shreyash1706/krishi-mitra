import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import AuthView from './components/AuthView';
import MainApp from './components/MainApp';

function App() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('krishi_user');
    return saved ? JSON.parse(saved) : null;
  });

  const handleLogin = (userData) => {
    localStorage.setItem('krishi_user', JSON.stringify(userData));
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('krishi_user');
    setUser(null);
  };

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-950 text-slate-50 selection:bg-emerald-500/30">
        <Routes>
          <Route 
            path="/login" 
            element={!user ? <AuthView onLogin={handleLogin} /> : <Navigate to="/" replace />} 
          />
          <Route 
            path="/" 
            element={user ? <MainApp user={user} onLogout={handleLogout} /> : <Navigate to="/login" replace />} 
          />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
