import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Header from "./components/Header";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import RegisterDoctor from "./pages/RegisterDoctor";
import LoginDoctor from "./pages/LoginDoctor";
function App() {
  return (
    <Router>
      <Header />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/register-doctor" element={<RegisterDoctor />} />
        <Route path="/doctor-login" element={<LoginDoctor />} />
      </Routes>
    </Router>
  );
}

export default App;
