import React from 'react';
import '../styles/hero.css';

function Hero() {
  const handleScrollToBooking = () => {
    const bookingSection = document.getElementById('booking-section');
    if (bookingSection) {
      bookingSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <section className="hero">
      <video
        className="hero-video"
        autoPlay
        muted
        loop
        playsInline
      >
        <source src="/IMG_2145.webm" type="video/webm" />
      </video>

      <div className="hero-overlay" />

      <div className="hero-content">
        <h1>Детейлинг в Екатеринбурге</h1>
        <p>Мы преобразим Ваш автомобиль до неузнаваемости</p>
        <button className="hero-btn" onClick={handleScrollToBooking}>
          Записаться на консультацию
        </button>
      </div>
    </section>
  );
}

export default Hero;
