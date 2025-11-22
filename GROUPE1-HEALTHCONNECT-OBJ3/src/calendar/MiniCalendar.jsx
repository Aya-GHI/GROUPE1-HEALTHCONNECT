import React, { useState } from "react";
import "./MiniCalendar.css";

export default function MiniCalendar() {
  const today = new Date();
  const [currentMonth, setCurrentMonth] = useState(today.getMonth());
  const [currentYear, setCurrentYear] = useState(today.getFullYear());

  const monthName = new Date(currentYear, currentMonth)
    .toLocaleString("default", { month: "long" });

  const firstDay = new Date(currentYear, currentMonth, 1).getDay();
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

  const prevMonth = () => {
    if (currentMonth === 0) {
      setCurrentMonth(11);
      setCurrentYear(currentYear - 1);
    } else {
      setCurrentMonth(currentMonth - 1);
    }
  };

  const nextMonth = () => {
    if (currentMonth === 11) {
      setCurrentMonth(0);
      setCurrentYear(currentYear + 1);
    } else {
      setCurrentMonth(currentMonth + 1);
    }
  };

  const days = [];
  for (let i = 0; i < firstDay; i++) days.push(null);
  for (let i = 1; i <= daysInMonth; i++) days.push(i);

  return (
    <div className="mini-calendar">
      <div className="calendar-header">
        <button onClick={prevMonth}>{"<"}</button>
        <span>{monthName} {currentYear}</span>
        <button onClick={nextMonth}>{">"}</button>
      </div>

      <div className="weekday-row">
        {["S","M","T","W","T","F","S"].map((d) => (
          <div key={d}>{d}</div>
        ))}
      </div>

      <div className="days-grid">
        {days.map((day, i) => (
          <div key={i} className={day === today.getDate() && currentMonth === today.getMonth() ? "today" : ""}>
            {day}
          </div>
        ))}
      </div>
    </div>
  );
}
