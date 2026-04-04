import React from 'react';
import '../styles/about.css';

function About() {
  return (
    <section className="about">
      <div className="container">
        <h2>Ваш автомобиль заслуживает лучшего ухода</h2>
        <p>
          Мы предлагаем профессиональный уход за автомобилем с использованием передовых технологий и качественных материалов. 
          Наш опыт работы с 2019 года гарантирует высокое качество услуг и индивидуальный подход к каждому клиенту.
        </p>
        <div className="stats">
          <div className="stat">
            <h3>5+</h3>
            <p>лет опыта</p>
          </div>
          <div className="stat">
            <h3>500+</h3>
            <p>довольных клиентов</p>
          </div>
          <div className="stat">
            <h3>100%</h3>
            <p>качество гарантировано</p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default About;
