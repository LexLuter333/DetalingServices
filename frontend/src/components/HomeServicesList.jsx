import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/services.css';

const categoryServices = [
  {
    id: 1,
    title: 'Мойка и Чистка',
    description: 'Мы предоставляем трехфазную мойку кузова, очистку подкапотного пространства, озонацию и комплексную мойку с салоном.'
  },
  {
    id: 2,
    title: 'Защита и Полировка',
    description: 'Включает полировку кузова, ремонт сколов, нанесение антидождя и оклейку зон риска или полного кузова защитной пленкой.'
  },
  {
    id: 3,
    title: 'Стекла и Оптика',
    description: 'Предлагаем тонировку стекол, полировку и шлифовку стекла, а также восстановление и оклейку фар для лучшей видимости.'
  },
  {
    id: 4,
    title: 'Салон и Комфорт',
    description: 'Делаем глубокую химчистку салона, шумоизоляцию кузова, реставрацию и перешив сидений для максимального уюта.'
  },
  {
    id: 5,
    title: 'Кузов и Тюнинг',
    description: 'Выполняем удаление вмятин без покраски (PDR), установку обвесов и услугу «антихром» для стайлинга деталей.'
  },
  {
    id: 6,
    title: 'Оборудование и Подготовка',
    description: 'Устанавливаем магнитолы и дополнительное оборудование, проводим полную предпродажную подготовку автомобиля.'
  }
];

function HomeServicesList() {
  return (
    <section className="services-list home-specific">
      <div className="container">
        <h2>Наши услуги</h2>
        <div className="services-grid">
          {categoryServices.map(service => (
            <Link
              key={service.id}
              to="/services"
              className="service-card-link"
            >
              <div className="service-card category-card">
                <div className="service-header">
                  <h3>{service.title}</h3>
                </div>
                <p className="service-description">{service.description}</p>
                <div className="service-card-footer">
                  <span>Подробнее →</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
        
        <div className="services-cta">
          <Link to="/services" className="cta-button">
            Перейти к услугам
          </Link>
        </div>
      </div>
    </section>
  );
}

export default HomeServicesList;
