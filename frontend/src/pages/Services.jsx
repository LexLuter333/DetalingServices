import React from 'react';
import ServicesList from '../components/ServicesList';
import '../styles/page.css';

function Services() {
  return (
    <main>
      <div className="page-header">
        <h1>Наши услуги</h1>
      </div>
      <ServicesList />
    </main>
  );
}

export default Services;
