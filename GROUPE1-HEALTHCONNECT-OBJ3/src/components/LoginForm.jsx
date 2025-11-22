import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/LoginForm.css';

const LoginForm = () => {
  const [formData, setFormData] = useState({
    emailUsername: '',
    password: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Données de connexion:', formData);
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>WELCOME BACK!</h2>
        <p className="login-subtitle">Log in to continue to your account</p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="emailUsername">Email/Username</label>
            <input
              type="text"
              id="emailUsername"
              name="emailUsername"
              placeholder="Enter your email or username"
              value={formData.emailUsername}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              placeholder="Enter your password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          <button type="submit" className="login-btn">
            LOGIN
          </button>
        </form>

        <p className="register-link">
          Don't have an account? <Link to="/register">Create an account</Link>
        </p>
      </div>
    </div>
  );
};

export default LoginForm;