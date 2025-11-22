import React from "react";
import { Link } from "react-router-dom"; // <-- import Link from react-router-dom
import logo from "./assets/logo.png";
import { useNavigate } from "react-router-dom";


export default function Header() {
      const navigate = useNavigate();

  return (
    <header className="header">
      <div className="header-logo">
        {/* Wrap both logo and text in Link */}
        <Link to="/" style={{ display: "flex", alignItems: "center", textDecoration: "none", color: "inherit" }}>
          <img src={logo} alt="logo" style={{ marginRight: "8px" }} />
          <h1>HealthConnect</h1>
        </Link>
      </div>
      <div className="header-menu">
        <button>ARE YOU A DOCTOR?</button>
        <a href="#">HELP CENTER</a>
        <nav>
            <button className="login-btn" onClick={() => navigate("/login")}>
            Login
            </button>
        </nav>
      </div>
    </header>
  );
}
