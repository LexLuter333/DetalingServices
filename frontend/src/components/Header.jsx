import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/header.css';

function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <header className="header">
      <div className="container">
        <Link to="/" className="logo">
          <img src="/Icon_logo.webp" alt="OSG Detailing" className="logo-icon" />
        </Link>
        
        <button 
          className={`burger-menu ${menuOpen ? 'active' : ''}`}
          onClick={toggleMenu}
          aria-label="Меню"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
        
        <nav className={`nav ${menuOpen ? 'nav-open' : ''}`}>
          <Link to="/" className="nav-link" onClick={() => setMenuOpen(false)}>Главная</Link>
          <Link to="/services" className="nav-link" onClick={() => setMenuOpen(false)}>Услуги</Link>
          <Link to="/reviews" className="nav-link" onClick={() => setMenuOpen(false)}>Отзывы</Link>
          <Link to="/contacts" className="nav-link" onClick={() => setMenuOpen(false)}>Контакты</Link>
        </nav>
      </div>
    </header>
  );
}

export default Header;
