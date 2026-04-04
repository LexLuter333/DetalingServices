import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './AdminLayout.css';

const AdminLayout = ({ children, onLogout }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isMobile, setIsMobile] = useState(false);
  const location = useLocation();

  const menuItems = [
    { path: '/admin/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/admin/bookings', label: 'Бронирования', icon: '📋' },
    { path: '/admin/services', label: 'Услуги', icon: '🔧' },
    { path: '/admin/reviews', label: 'Отзывы', icon: '💬' },
  ];

  const isActive = (path) => location.pathname === path;

  useEffect(() => {
    const checkMobile = () => {
      const mobile = window.innerWidth <= 768;
      setIsMobile(mobile);
      if (mobile) {
        setSidebarOpen(false);
      } else {
        setSidebarOpen(true);
      }
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const handleNavClick = () => {
    if (isMobile) {
      setSidebarOpen(false);
    }
  };

  return (
    <div className="admin-layout">
      <aside className={`sidebar ${sidebarOpen && !isMobile ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <Link to="/admin/dashboard" className="sidebar-logo">
          </Link>
        </div>

        <nav className="sidebar-nav">
          {menuItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${isActive(item.path) ? 'active' : ''}`}
              onClick={handleNavClick}
            >
              <span className="nav-icon">{item.icon}</span>
              {sidebarOpen && !isMobile && <span className="nav-label">{item.label}</span>}
            </Link>
          ))}
        </nav>

        <div className="sidebar-footer">
          <button onClick={onLogout} className="logout-btn">
            <span className="nav-icon">🚪</span>
            {sidebarOpen && !isMobile && <span>Выйти</span>}
          </button>
        </div>
      </aside>

      <div className="main-content">
        <header className="top-header">
          <button
            className="menu-toggle"
            onClick={toggleSidebar}
            aria-label="Toggle menu"
          >
            ☰
          </button>
        </header>

        <main className="content">
          {children}
        </main>
      </div>
    </div>
  );
};

export default AdminLayout;
