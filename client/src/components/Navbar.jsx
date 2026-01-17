
import { NavLink, Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

function Navbar({ user, setUser }) {
  const navigate = useNavigate();

  function handleLogout() {
    fetch("/logout", { method: "DELETE" }).then(() => {
      setUser(null);
      navigate("/login");
    });
  }

  //  active links styling
  const linkStyles = ({ isActive }) => ({
    color: isActive ? "#FF385C" : "#484848",
    fontWeight: isActive ? "bold" : "normal",
    borderBottom: isActive ? "2px solid #FF385C" : "none"
  });

  return (
    <nav className="navbar-container">
      <Link to="/" className="brand-logo">🏘️ Sweet Homes</Link>

      <div className="nav-links">
        <NavLink to="/houses" style={linkStyles}>Explore</NavLink>

        {user ? (
          <>
            <NavLink to="/favorites" style={linkStyles}>Favorites</NavLink>
            <NavLink to="/my-bookings" style={linkStyles}>My Trips</NavLink>

            {user.role?.name === "Admin" && (
              <NavLink to="/admin" className="admin-pill" style={linkStyles}>
                Admin Dashboard
              </NavLink>
            )}

            <div className="user-profile">
              <span className="welcome-text">Hello, <strong>{user.username}</strong></span>
              <button className="logout-btn" onClick={handleLogout}>Logout</button>
            </div>
          </>
        ) : (
          <div className="auth-buttons">
            <NavLink to="/login" className="login-link">Login</NavLink>
            <NavLink to="/signup" className="signup-btn">Signup</NavLink>
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;