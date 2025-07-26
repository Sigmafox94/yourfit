// yourfit-saas/frontend/src/components/Auth/Login.jsx
import React, { useState } from 'react';
import { useAuth } from '../../App'; // Import useAuth context

function Login() {
  const [formData, setFormData] = useState({
    username_or_email: '',
    password: '',
  });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const { setToken } = useAuth(); // Get setToken from context

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/accounts/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess('Login successful!');
        setToken(data.token); // Store token in AuthContext (and localStorage)
      } else {
        // Handle API errors (e.g., invalid credentials)
        setError(data.message || JSON.stringify(data));
      }
    } catch (err) {
      setError('Network error or server unreachable: ' + err.message);
    }
  };

  return (
    <div className="form-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username_or_email">Username or Email:</label>
          <input
            type="text"
            id="username_or_email"
            name="username_or_email"
            value={formData.username_or_email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        {error && <p className="error-message">{error}</p>}
        {success && <p className="success-message">{success}</p>}
        <button type="submit" className="submit-button">Login</button>
      </form>
    </div>
  );
}

export default Login;