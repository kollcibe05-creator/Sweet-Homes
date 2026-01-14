import { Navigate } from "react-router-dom";

function ProtectedRoute({ user, isLoading, children, adminOnly = false }) {
  // Show loader while session is being verified
  if (isLoading) {
    return <div className="loader">Verifying session...</div>;
  }

  // Redirect if not logged in
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Redirect if not admin and adminOnly
  if (adminOnly && user.role?.name !== "Admin") {
    return <Navigate to="/" replace />;
  }

  return children;
}

export default ProtectedRoute;
