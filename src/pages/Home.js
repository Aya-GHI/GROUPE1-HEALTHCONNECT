import React from "react";
import "../styles/Home.css";
import doctorsImg from "../assets/doc.png";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="home">
 
  

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-text">
          <h1>
            Connecting you to <br />
            trusted doctors — <br />
            anytime, anywhere!
          </h1>
          <p>
            HealthConnect helps you reach verified medical professionals,
            explore their specialties, and access personalized healthcare
            services from the comfort of your home.
          </p>
        </div>

        <div className="hero-image">
          <img src={doctorsImg} alt="Doctors" />

        </div>
      </section>

      {/* Search Bar */}
      <div className="search-bar">
        <input type="text" placeholder="Name or Speciality" />
        <input type="text" placeholder="Location" />
        <button>Search</button>
      </div>

      {/* Specialties */}
      <section className="specialties">
        <h2>Browse by Specialty</h2>

        <div className="specialty-list">
          <div className="specialty-item">❤️<p>Cardiology</p></div>
          <div className="specialty-item">😊<p>Dermatology</p></div>
          <div className="specialty-item">👶<p>Pediatrics</p></div>
          <div className="specialty-item">👁️<p>Ophthalmology</p></div>
          <div className="specialty-item">🦷<p>Dentistry</p></div>
        </div>
      </section>
    </div>
  );
};

export default Home;
