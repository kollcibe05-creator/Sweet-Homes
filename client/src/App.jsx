import React, { useState, useEffect } from "react";
import { Routes, Route } from "react-router-dom";

// Components
import Navbar from "./Components/Navbar";
import HouseGalleryWithRating from "./Components/HouseGalleryWithRating";
import HouseDetail from "./Components/HouseDetail";
import Login from "./Components/Login";
import Signup from "./Components/Signup";
import AdminDashboard from "./Components/AdminDashboard";
import MyBookings from "./Components/BookingForm";       // Ensure BookingForm.jsx default exports MyBookings
import Favourites from "./Components/Favourites";       // Ensure Favourites.jsx default exports Favourites
import ProtectedRoute from "./Components/ProtectedRoute"; // Ensure default export

function App() {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Auto-login: Check if user session exists on refresh
  useEffect(() => {
    fetch("/check_session")
      .then((res) => {
        if (res.ok) {
          res.json().then((user) => setUser(user));
        }
      })
      .finally(() => setIsLoading(false)); // Stop loading after fetch
  }, []);

  if (isLoading) {
    return <div className="loader">Loading...</div>; // Show loader while checking session
  }

  return (
    <div className="App">
      <Navbar user={user} setUser={setUser} />
      <main>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<HouseGalleryWithRating />} />
          <Route path="/houses/:id" element={<HouseDetail user={user} />} />
          <Route path="/login" element={<Login setUser={setUser} />} />
          <Route path="/signup" element={<Signup setUser={setUser} />} />

          {/* User Protected Routes */}
          <Route
            path="/my-bookings"
            element={
              <ProtectedRoute user={user}>
                <MyBookings user={user} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/favorites"
            element={
              <ProtectedRoute user={user}>
                <Favourites user={user} />
              </ProtectedRoute>
            }
          />

          {/* Admin Only Route */}
          <Route
            path="/admin"
            element={
              <ProtectedRoute user={user} adminOnly={true}>
                <AdminDashboard user={user} />
              </ProtectedRoute>
            }
          />
        </Routes>
      </main>
    </div>
  );
}

export default App;
