// yourfit-saas/frontend/src/components/Dashboard.jsx
import React from 'react';
import { useAuth } from '../App';

function Dashboard() {
  const { token } = useAuth(); // Access the token from context

  return (
    <div className="dashboard-container">
      <h2>Welcome to YourFit Dashboard!</h2>
      <p>You are authenticated.</p>
      <p>Your Token: <code style={{ wordBreak: 'break-all' }}>{token ? token : 'No token found'}</code></p>
      <p>This is where your personalized fitness content will go.</p>
    </div>
  );
}

export default Dashboard;