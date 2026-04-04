import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { servicesAPI } from '../api/api';
import '../styles/services.css';

// Резервный список услуг (если API не доступен)
const FALLBACK_SERVICES = [
  { id: 'svc_1', name: 'Трехфазная мойка кузова', price: 1500, description: 'Способ бесконтактной очистки автомобиля, при котором химия наносится в три этапа для максимально безопасного и глубокого удаления грязи.' },
  { id: 'svc_2', name: 'Трехфазная мойка кузова + салон', price: 2200, description: 'Комплексная мойка кузова и салона в три этапа.' },
  { id: 'svc_3', name: 'Химчистка салона', price: 6500, description: 'Комплексная глубокая очистка внутренних поверхностей автомобиля с использованием специальной химии и оборудования.' },
  { id: 'svc_4', name: 'Полировка кузова', price: 10000, description: 'Процесс восстановления лакокрасочного покрытия (ЛКП) и придания ему глубокого зеркального блеска.' },
  { id: 'svc_5', name: 'Мойка подкапотного пространства', price: 2500, description: 'Очистка подкапотного пространства от масляных потеков, пыли, грязи и реагентов.' },
  { id: 'svc_6', name: 'Озонация', price: 1500, description: 'Обработка салона озоном (O₃) — активной формой кислорода для удаления запахов.' },
  { id: 'svc_7', name: 'Антихром', price: 1500, description: 'Покрытие хромированных деталей кузова пленкой или краской для придания автомобилю более яркого вида.' },
  { id: 'svc_8', name: 'PDR (Удаление вмятин)', price: 3000, description: 'Технология, позволяющая удалять вмятины с кузова автомобиля без перекраски. Метод основан на аккуратном выравнивании металла изнутри.' },
  { id: 'svc_9', name: 'Антидождь', price: 1000, description: 'Нанесение специального гидрофобного покрытия на стекла автомобиля. Отталкивает воду, обеспечивая улучшенную видимость в дождь.' },
  { id: 'svc_10', name: 'Предпродажная подготовка', price: 15000, description: 'Легкая полировка кузова + легкая химчистка салона.' },
  { id: 'svc_11', name: 'Оклейка зон риска', price: 45000, description: 'Нанесение защитной пленки на наиболее уязвимые участки кузова: бамперы, капот, дверные ручки и пороги.' },
  { id: 'svc_12', name: 'Полная оклейка кузова', price: 200000, description: 'Оклейка авто в цветную или бронепленку для защиты от сколов, царапин или изменения цвета.' },
  { id: 'svc_13', name: 'Оклейка фар', price: 3000, description: 'Нанесение специальной защитной пленки на фары автомобиля для защиты от повреждений.' },
  { id: 'svc_14', name: 'Тонировка стекол', price: 3000, description: 'Нанесение специальной пленки на окна автомобиля для уменьшения проникновения солнечного света (цена за полусферу).' },
  { id: 'svc_15', name: 'Доработка и восстановление оптики', price: 5000, description: 'Услуги по улучшению состояния фар и фонарей. Включает полировку, удаление потемнений и царапин.' },
  { id: 'svc_16', name: 'Шумоизоляция', price: 3000, description: 'Процесс снижения уровня шума в салоне с использованием специальных материалов, поглощающих звук и вибрации.' },
  { id: 'svc_17', name: 'Ремонт сколов', price: 2000, description: 'Процесс восстановления лакокрасочного покрытия на кузове автомобиля после появления повреждений.' },
  { id: 'svc_18', name: 'Реставрация / перешив салона', price: 3000, description: 'Восстановление или замена обивки сидений, дверных панелей и других элементов интерьера.' },
  { id: 'svc_19', name: 'Установка магнитол и доп. оборудования', price: 1000, description: 'Установка магнитол, динамиков, усилителей, камер заднего вида, навигаторов и систем безопасности.' },
  { id: 'svc_20', name: 'Установка обвесов', price: 1000, description: 'Установка спойлеров, порогов и бамперов для улучшения внешнего вида и аэродинамики.' },
  { id: 'svc_21', name: 'Полировка / Шлифовка стекол', price: 7000, description: 'Процесс удаления мелких царапин и дефектов с поверхности стекол автомобиля.' }
];

function ServicesList() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadServices = async () => {
      try {
        const response = await servicesAPI.getAll();
        const servicesList = response.data.services || [];
        setServices(servicesList);
      } catch (err) {
        console.warn('Failed to load services from API, using fallback:', err);
        setServices(FALLBACK_SERVICES);
      } finally {
        setLoading(false);
      }
    };

    loadServices();
  }, []);

  if (loading) {
    return (
      <section className="services-list">
        <div className="container">
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Загрузка услуг...</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="services-list">
      <div className="container">
        <div className="services-grid">
          {services.map(service => (
            <Link
              key={service.id}
              to={`/?service=${encodeURIComponent(service.name)}`}
              className="service-card-link"
            >
              <div className="service-card">
                <div className="service-header">
                  <h3>{service.name}</h3>
                </div>
                {service.price && (
                  <span className="service-price">
                    Цена от {service.price.toLocaleString('ru-RU')} ₽
                  </span>
                )}
                {service.description && <p>{service.description}</p>}
                <div className="service-card-footer">
                  <span>Записаться →</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}

export default ServicesList;
