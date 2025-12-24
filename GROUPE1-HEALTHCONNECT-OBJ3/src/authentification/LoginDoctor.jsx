import React from "react";
import "../styles/LoginDoctor.css";
import { Link } from "react-router-dom";



const LoginDoctor = () => {
  return (
    <div className="login-doctor-page">
      <div className="login-card">
        <h2>Doctor Login</h2>

        <div className="form-section">
          <div className="form-group">
            <input
              type="text"
              placeholder="Username or Email"
            />
          </div>

          <div className="form-group">
            <input
              type="password"
              placeholder="Password"
            />
          </div>
        </div>

        <div className="login-options">
          <label>
            <input type="checkbox" /> Remember me
          </label>

          <span className="forgot-password">
            Forgot password?
          </span>
        </div>

        <button className="login-btn">LOGIN</button>

        <p className="register-link">
  Don’t have an account?{" "}
  <Link to="/register-doctor">Create one</Link>
</p>

      </div>
    </div>
  );
};

export default LoginDoctor;
