import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles/Header.css';
import logo from '../assets/logo.png';

const Header = () => {
  const location = useLocation();
  const isLoginPage =
    location.pathname === '/' || location.pathname === '/login';

  return (
    <header className="header">
      <div className="header-top">
        
        {/* LOGO + TITLE clickable */}
        <Link to="/" className="logo-container">
          <img
            src={logo}
            alt="Health Connect Logo"
            className="logo-image"
          />
          <h1 className="logo-text">HEALTH CONNECT</h1>
        </Link>

        <div className="header-links">
          <Link to="/register-doctor" className="header-link">
  ARE YOU A DOCTOR?
</Link>


          <Link to="/help" className="header-link">
            HELP CENTER
          </Link>

          {isLoginPage ? (
            <Link to="/register" className="create-account-btn">
              Create account
            </Link>
          ) : (
            <Link to="/login" className="login-btn">
              Login
            </Link>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
