import React, { useEffect, useState } from "react";
import Header from "../header"; 
import MiniCalendar from "../calendar/MiniCalendar";
import "./specialties.css";

export default function Cardio() {
  const [doctors, setDoctors] = useState([]);

  useEffect(() => {
      fetch("http://localhost:5000/api/cardiology")
      .then(res => res.json())
      .then(data => setDoctors(data))
      .catch(err => console.error("Fetch error:", err));
  }, []);

  return (
    <div className="page-container">
      <Header />

      <h1 className="title">Cardiologists</h1>

      {doctors.length === 0 ? (
        <p>Loading…</p>
      ) : (
        doctors.map(doc => (
          <div key={doc.id} className="doctor-card">
            <div className="doctor-info">
              <img src={doc.image} alt={doc.name} className="doc-img" />
              <div>
                <h3>{doc.name}</h3>
                <p>{doc.specialty}</p>
                <p>{doc.address}</p>
                <button className="btn-appoint">Make an appointment</button>
              </div>
            </div>

            <MiniCalendar />
          </div>
        ))
      )}
    </div>
  );
}
