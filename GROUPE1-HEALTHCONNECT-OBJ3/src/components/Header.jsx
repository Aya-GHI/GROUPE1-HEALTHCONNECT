import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import axios from "axios";
import "../styles/App.css";
import Login from "./authentification/Login";
import Register from "./authentification/Register.jsx";
import LoginDoctor from "./authentification/LoginDoctor";




import doctorsImg from "./assets/doc.png";
import Dentists from "./specialties/Dentistry";
import Cardiology from "./specialties/cardio";
import Ophthalmology from "./specialties/ophtalmo";
import Dermatology from "./specialties/Dermatology";
import Pediatrics from "./specialties/Pediatrics";
import Header from "./components/Header";

// ======= SPECIALTIES COMPONENT =======
function Specialties() {
  const navigate = useNavigate();

  const specialties = [
    { icon: "favorite", label: "Cardiology", route: "/cardio" },
    { icon: "spa", label: "Dermatology", route: "/dermatology" },
    { icon: "child_care", label: "Pediatrics", route: "/pediatrics" },
    { icon: "visibility", label: "Ophthalmology", route: "/ophthalmology" },
    { icon: "masks", label: "Dentistry", route: "/dentists" },
  ];

  return (
    <section className="specialties">
      <h2>Browse by Specialty</h2>
      <div className="specialties-grid">
        {specialties.map((item, idx) => (
          <button
            key={idx}
            type="button"
            className="specialty-item"
            onClick={() => item.route && navigate(item.route)}
          >
            <div className="specialty-icon">
              <span className="material-symbols-outlined">{item.icon}</span>
            </div>
            <p>{item.label}</p>
          </button>
        ))}
      </div>
    </section>
  );
}

// ======= SEARCH BAR COMPONENT =======
function SearchBar() {
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      let url = `http://localhost:5000/doctors?`;
      if (name) url += `name_like=${name}&`;
      if (location) url += `location_like=${location}&`;

      const response = await axios.get(url);
      setResults(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="search-bar-container">
      <div className="search-bar">
        <span className="material-symbols-outlined">search</span>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <span className="material-symbols-outlined">location_on</span>
        <input
          type="text"
          placeholder="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      <div className="search-results">
        {results.map((doctor) => (
          <div key={doctor.id} className="doctor-card">
            <h4>{doctor.name}</h4>
            <p>
              {doctor.specialty} — {doctor.location}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

// ======= HOME PAGE CONTENT =======
function AppContent() {
  return (
    <div className="app">
      <Header />

      {/* HERO SECTION */}
      <section className="hero">
        <div className="hero-content">
          <div className="hero-text">
            <h1>Connecting you to trusted doctors —</h1>
            <h3>anytime, anywhere!</h3>
            <p>
              HealthConnect helps you reach verified medical professionals,
              explore their specialties, and access personalized healthcare
              services from the comfort of your home.
            </p>
          </div>
          <div className="hero-image">
            <img src={doctorsImg} alt="Doctors" />
          </div>
        </div>
      </section>

      {/* SEARCH BAR */}
      <SearchBar />

      {/* SPECIALTIES */}
      <Specialties />
    </div>
  );
}

// ======= ROOT APP WITH ROUTING =======
export default function App() {
  return (
    <Router>*
      
      <Routes>
        <Route path="/" element={<AppContent />} />
        <Route path="/login-doctor" element={<LoginDoctor />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} /> 
        <Route path="/dentists" element={<Dentists />} />
        <Route path="/cardio" element={<Cardiology />} />
        <Route path="/dermatology" element={<Dermatology />} />
        <Route path="/pediatrics" element={<Pediatrics />} />
        <Route path="/ophthalmology" element={<Ophthalmology />} />
      </Routes>
    </Router>
  );
}
