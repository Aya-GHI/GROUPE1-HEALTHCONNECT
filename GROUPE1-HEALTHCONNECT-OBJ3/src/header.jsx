import React from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "./assets/logo.png";
import "./styles/Header.css";

export default function Header() {
  const navigate = useNavigate();

  return (
    <header className="header">
      <div className="header-top">

        {/* LOGO */}
        <div className="logo-container">
          <Link
            to="/"
            style={{ display: "flex", alignItems: "center", textDecoration: "none" }}
          >
            <img src={logo} alt="logo" className="logo-image" />
            <span className="logo-text">HealthConnect</span>
          </Link>
        </div>

        {/* LINKS */}
        <div className="header-links">
          <Link to="/register-doctor" className="doctor-btn">
            ARE YOU A DOCTOR?
          </Link>

          <Link to="/help" className="header-link">
            HELP CENTER
          </Link>

          <button className="login-btn" onClick={() => navigate("/login")}>
            Login
          </button>
        </div>

      </div>
    </header>
  );
}
