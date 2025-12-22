import React from "react";
import "../styles/RegisterDoctor.css";
import { Link } from "react-router-dom";
const RegisterDoctor = () => {
  return (
    <div className="register-doctor-page">
      <div className="register-card">
        <h2>Create Doctor account</h2>

        {/* Personal Information */}
        <div className="form-section">
          <h4>Personal Information</h4>

          <div className="form-group">
            <input type="text" placeholder="Enter your full name" />
          </div>

          <div className="form-group">
            <input type="email" placeholder="Enter your email address" />
          </div>

          <div className="form-group">
            <input type="text" placeholder="Enter your phone number" />
          </div>
        </div>

        {/* Professional Information */}
        <div className="form-section">
          <h4>Professional Information</h4>

          <div className="form-group">
            <select>
              <option>Select your specialty</option>
              <option>Cardiology</option>
              <option>Dermatology</option>
              <option>Pediatrics</option>
            </select>
          </div>

          <div className="form-group">
            <select>
              <option>Name / type of diploma</option>
              <option>Doctorate</option>
              <option>Master</option>
            </select>
          </div>

          <div className="form-group">
            <input type="text" placeholder="Clinic / Office name" />
          </div>

          <div className="form-group">
            <input type="text" placeholder="Exact location" />
          </div>

          <div className="form-group">
            <input type="number" placeholder="Years of experience" />
          </div>
        </div>

        {/* Account Information */}
        <div className="form-section">
          <h4>Account Information</h4>

          <div className="form-group">
            <input type="text" placeholder="Username" />
          </div>

          <div className="form-group">
            <input
              type="password"
              placeholder="Password (at least 8 characters)"
            />
          </div>
        </div>

        <div className="terms">
          <input type="checkbox" />
          <span>I agree to the Terms of Use</span>
        </div>

        <button className="register-btn">REGISTER</button>
        <p className="login-link">
  Already have an account?{" "}
  <Link to="/doctor-login">Log in</Link>
</p>

      </div>
    </div>
  );
};

export default RegisterDoctor;
