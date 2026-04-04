import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { servicesAPI, bookingsAPI } from '../api/api';
import '../styles/booking.css';

// Резервный список услуг (если API не доступен) - совпадает с данными в базе
const FALLBACK_SERVICES = [
  { id: 'svc_1', name: 'Трехфазная мойка кузова', price: 1500 },
  { id: 'svc_2', name: 'Трехфазная мойка кузова + салон', price: 2200 },
  { id: 'svc_3', name: 'Химчистка салона', price: 6500 },
  { id: 'svc_4', name: 'Полировка кузова', price: 10000 },
  { id: 'svc_5', name: 'Мойка подкапотного пространства', price: 2500 },
  { id: 'svc_6', name: 'Озонация', price: 1500 },
  { id: 'svc_7', name: 'Антихром', price: 1500 },
  { id: 'svc_8', name: 'PDR (Удаление вмятин)', price: 3000 },
  { id: 'svc_9', name: 'Антидождь', price: 1000 },
  { id: 'svc_10', name: 'Предпродажная подготовка', price: 15000 },
  { id: 'svc_11', name: 'Оклейка зон риска', price: 45000 },
  { id: 'svc_12', name: 'Полная оклейка кузова', price: 200000 },
  { id: 'svc_13', name: 'Оклейка фар', price: 3000 },
  { id: 'svc_14', name: 'Тонировка стекол', price: 3000 },
  { id: 'svc_15', name: 'Доработка и восстановление оптики', price: 5000 },
  { id: 'svc_16', name: 'Шумоизоляция', price: 3000 },
  { id: 'svc_17', name: 'Ремонт сколов', price: 2000 },
  { id: 'svc_18', name: 'Реставрация / перешив салона', price: 3000 },
  { id: 'svc_19', name: 'Установка магнитол и доп. оборудования', price: 1000 },
  { id: 'svc_20', name: 'Установка обвесов', price: 1000 },
  { id: 'svc_21', name: 'Полировка / Шлифовка стекол', price: 7000 }
];

function BookingForm() {
  const location = useLocation();
  const [services, setServices] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    carBrand: '',
    carModel: '',
    phone: '',
    service: '',
    comment: ''
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  // Загрузка услуг при монтировании компонента
  useEffect(() => {
    const loadServices = async () => {
      try {
        console.log('📦 Loading services from API...');
        const response = await servicesAPI.getAll();
        console.log('✅ Services loaded from API:', response.data.services);

        const servicesList = response.data.services || [];

        if (servicesList.length > 0) {
          setServices(servicesList);
          console.log('✅ Using API services, first service ID:', servicesList[0].id);
        } else {
          // Если API вернул пустой список, используем резервный
          console.warn('⚠️ API returned empty services list, using fallback');
          setServices(FALLBACK_SERVICES);
        }
      } catch (err) {
        console.error('❌ Failed to load services from API:', err);
        console.warn('⚠️ Using fallback services');
        // Используем резервный список при ошибке
        setServices(FALLBACK_SERVICES);
      }
    };
    loadServices();
  }, []); // Загружаем услуги только при монтировании

  // Обработка URL параметров и установка выбранной услуги
  useEffect(() => {
    if (services.length > 0) {
      const params = new URLSearchParams(location.search);
      const serviceNameFromUrl = params.get('service');

      if (serviceNameFromUrl) {
        // Декодируем URL и ищем услугу по названию
        const decodedServiceName = decodeURIComponent(serviceNameFromUrl);
        const matchedService = services.find(s =>
          s.name.toLowerCase() === decodedServiceName.toLowerCase()
        );

        if (matchedService) {
          setFormData(prev => ({
            ...prev,
            service: matchedService.id
          }));
          console.log('✅ Service selected from URL:', matchedService.name);
        } else {
          console.warn('⚠️ Service not found in list:', decodedServiceName);
          // Если не нашли, оставляем текущую выбранную услугу или первую
          if (!formData.service && services.length > 0) {
            setFormData(prev => ({
              ...prev,
              service: services[0].id
            }));
          }
        }
      } else {
        // Если параметра нет, выбираем первую услугу (только если ничего не выбрано)
        if (!formData.service && services.length > 0) {
          setFormData(prev => ({
            ...prev,
            service: services[0].id
          }));
        }
      }
    }
  }, [location.search, services]);

  // Форматирование телефона: +7 (___) ___-__-__
  const formatPhone = (value) => {
    const digits = value.replace(/\D/g, '');
    
    if (!digits) return '+7 (';
    
    let cleanDigits = digits;
    if (digits.startsWith('8')) {
      cleanDigits = '7' + digits.slice(1);
    } else if (!digits.startsWith('7')) {
      cleanDigits = '7' + digits;
    }

    const limited = cleanDigits.slice(0, 11);

    let formatted = '+7 (';
    if (limited.length > 1) {
      formatted += limited.slice(1, 4);
    }
    if (limited.length >= 4) {
      formatted += ') ' + limited.slice(4, 7);
    }
    if (limited.length >= 7) {
      formatted += '-' + limited.slice(7, 9);
    }
    if (limited.length >= 9) {
      formatted += '-' + limited.slice(9, 11);
    }

    return formatted;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    if (name === 'phone') {
      const formatted = formatPhone(value);
      setFormData({ ...formData, [name]: formatted });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);

    console.log('📤 Submitting booking form...');
    console.log('Form data:', formData);
    console.log('Available services:', services);

    try {
      // Проверяем что телефон заполнен (11 цифр)
      const phoneDigits = formData.phone.replace(/\D/g, '');
      console.log('Phone digits:', phoneDigits);
      
      if (phoneDigits.length !== 11) {
        setError('Введите корректный номер телефона (11 цифр)');
        setLoading(false);
        return;
      }

      // Проверяем что услуга выбрана
      console.log('Selected service:', formData.service);
      if (!formData.service) {
        setError('Выберите услугу из списка');
        setLoading(false);
        return;
      }

      // Проверяем что услуга существует в списке
      const serviceExists = services.find(s => s.id === formData.service);
      console.log('Service exists in list:', serviceExists);
      
      if (!serviceExists) {
        setError('Выбранная услуга не найдена');
        setLoading(false);
        return;
      }

      // Формируем данные для отправки
      const bookingData = {
        customer_name: formData.name,
        customer_phone: formData.phone,
        car_brand: formData.carBrand,
        car_model: formData.carModel,
        service_id: formData.service,
        comment: formData.comment
      };

      console.log('📤 Sending booking data:', bookingData);

      const response = await bookingsAPI.createBooking(bookingData);
      console.log('✅ Booking created:', response.data);

      setSuccess(true);
      setFormData({ name: '', carBrand: '', carModel: '', phone: '', service: '', comment: '' });

      setTimeout(() => setSuccess(false), 5000);
    } catch (err) {
      console.error('❌ Booking error:', err);
      console.error('Error response:', err.response?.data);
      console.error('Error status:', err.response?.status);
      
      // Показываем более подробную ошибку
      let errorMessage = 'Ошибка при отправке заявки';
      if (err.response?.data?.error) {
        errorMessage = err.response.data.error;
        
        // Если услуга не найдена, показываем какие ID доступны
        if (err.response.data.error === 'service not found') {
          const availableIds = services.map(s => s.id).join(', ');
          errorMessage = `Услуга не найдена. Доступные ID: ${availableIds}`;
        }
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="booking" id="booking-section">
      <div className="container">
        <h2>Запишитесь на бесплатную консультацию</h2>

        {success && (
          <div className="success-message">
            ✓ Заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.
          </div>
        )}

        {error && (
          <div className="error-message">
            ✗ {error}
          </div>
        )}

        <form className="booking-form" onSubmit={handleSubmit}>
          <input
            type="text"
            name="name"
            placeholder="Ваше имя"
            value={formData.name}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="carBrand"
            placeholder="Марка автомобиля"
            value={formData.carBrand}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="carModel"
            placeholder="Модель автомобиля"
            value={formData.carModel}
            onChange={handleChange}
          />
          <select
            name="service"
            value={formData.service}
            onChange={handleChange}
            required
          >
            <option value="">Выберите услугу</option>
            {services.length === 0 ? (
              <option disabled>Загрузка услуг...</option>
            ) : (
              services.map(service => (
                <option key={service.id} value={service.id}>
                  {service.name}
                </option>
              ))
            )}
          </select>
          <input
            type="tel"
            name="phone"
            placeholder="+7 (___) ___-__-__"
            value={formData.phone}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="comment"
            placeholder="Комментарий (необязательно)"
            value={formData.comment}
            onChange={handleChange}
          />
          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Отправка...' : 'Записаться'}
          </button>
        </form>
      </div>
    </section>
  );
}

export default BookingForm;
