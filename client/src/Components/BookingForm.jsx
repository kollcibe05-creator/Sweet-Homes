import React, { useState, useEffect } from "react";

function MyBookings({ user }) {
  const [bookings, setBookings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
  ackend
    fetch("/my-bookings")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch bookings");
        return res.json();
      })
      .then((data) => setBookings(data))
      .catch((err) => console.error("Error fetching bookings:", err))
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) {
    return <div className="loader">Loading your bookings...</div>;
  }

  return (
    <div className="container">
      <h2>My Bookings 📖</h2>
      {bookings.length === 0 ? (
        <p>You have no bookings yet.</p>
      ) : (
        <div className="booking-grid">
          {bookings.map((booking) => (
            <div key={booking.id} className="booking-card">
              <h3>{booking.house?.location || "Unknown location"}</h3>
              <p>Check-in: {booking.start_date}</p>
              <p>Check-out: {booking.end_date}</p>
              <p>Total: ${booking.total_price}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}


export default MyBookings;
