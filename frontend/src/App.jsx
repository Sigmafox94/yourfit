// yourfit-saas/frontend/src/App.jsx
import React, { useState, useEffect, createContext, useContext } from 'react';
import Register from './components/Auth/Register';
import Login from './components/Auth/Login';
import Dashboard from './components/Dashboard'; // We will create this
import './App.css'; // Let's bring back a simple CSS for basic styling

// Create an Auth Context
const AuthContext = createContext(null);

// Custom hook to use Auth Context
export const useAuth = () => {
  return useContext(AuthContext);
};

function App() {
  // State to hold the authentication token
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'));
  const [view, setView] = useState('login'); // 'login' or 'register'

  // Update isAuthenticated whenever token changes
  useEffect(() => {
    setIsAuthenticated(!!token);
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }, [token]);

  const logout = () => {
    // In a real app, you'd send a request to the backend /logout endpoint
    // For now, just clear the token from state and local storage
    setToken(null);
    setIsAuthenticated(false);
    setView('login'); // Redirect to login after logout
    alert('Logged out successfully!');
  };

  const authContextValue = {
    token,
    setToken,
    isAuthenticated,
    logout,
  };

  return (
    <AuthContext.Provider value={authContextValue}>
      <div className="app-container">
        <header className="app-header">
          <h1>YourFit SaaS</h1>
          {isAuthenticated ? (
            <button onClick={logout} className="logout-button">Logout</button>
          ) : (
            <nav className="auth-nav">
              <button onClick={() => setView('login')} className={view === 'login' ? 'active' : ''}>Login</button>
              <button onClick={() => setView('register')} className={view === 'register' ? 'active' : ''}>Register</button>
            </nav>
          )}
        </header>
        <main className="app-main">
          {isAuthenticated ? (
            <Dashboard />
          ) : (
            <>
              {view === 'login' && <Login />}
              {view === 'register' && <Register />}
            </>
          )}
        </main>
      </div>
    </AuthContext.Provider>
  );
}

export default App;