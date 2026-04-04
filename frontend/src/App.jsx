import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import ServicesPage from './pages/Services';
import Contacts from './pages/Contacts';
import ReviewsPublic from './pages/Reviews';
import Login from './pages/admin/Login';
import Dashboard from './pages/admin/Dashboard';
import Bookings from './pages/admin/Bookings';
import Services from './pages/admin/Services';
import Reviews from './pages/admin/Reviews';
import './styles/index.css';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, isAdmin, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/admin/login" replace />;
  }

  if (!isAdmin) {
    return <Navigate to="/admin/login" replace />;
  }

  return children;
};

// Public Route Component (redirect to dashboard if already logged in)
const PublicRoute = ({ children }) => {
  const { isAuthenticated, isAdmin, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  if (isAuthenticated && isAdmin) {
    return <Navigate to="/admin/dashboard" replace />;
  }

  return children;
};

function AppRoutes() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<><Header /><Home /><Footer /></>} />
      <Route path="/services" element={<><Header /><ServicesPage /><Footer /></>} />
      <Route path="/contacts" element={<><Header /><Contacts /><Footer /></>} />
      <Route path="/reviews" element={<><Header /><ReviewsPublic /><Footer /></>} />

      {/* Admin Auth Routes */}
      <Route path="/admin/login" element={<PublicRoute><Login /></PublicRoute>} />

      {/* Protected Admin Routes */}
      <Route path="/admin/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/admin/bookings" element={<ProtectedRoute><Bookings /></ProtectedRoute>} />
      <Route path="/admin/services" element={<ProtectedRoute><Services /></ProtectedRoute>} />
      <Route path="/admin/reviews" element={<ProtectedRoute><Reviews /></ProtectedRoute>} />

      {/* Redirect unknown routes */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

export default App;
