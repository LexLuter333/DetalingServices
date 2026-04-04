import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Hero from '../components/Hero';
import ServicesList from '../components/HomeServicesList';
import BookingForm from '../components/BookingForm';

function Home() {
  const location = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const serviceName = params.get('service');

    if (serviceName) {
      // Прокручиваем к форме записи
      const bookingSection = document.getElementById('booking-section');
      if (bookingSection) {
        bookingSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  }, [location.search]);

  return (
    <main>
      <Hero />
      <ServicesList />
      <BookingForm />
    </main>
  );
}

export default Home;
