import { useState, useEffect } from 'react';
import { adminAPI } from '../../api/api';
import { useAuth } from '../../context/AuthContext';
import AdminLayout from '../../components/admin/AdminLayout';
import './Bookings.css';

const Bookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all');
  const { logout } = useAuth();

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      const response = await adminAPI.getAllBookings();
      setBookings(response.data.bookings);
    } catch (err) {
      setError('Failed to load bookings');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    window.location.href = '/admin/login';
  };

  const handleStatusChange = async (id, newStatus) => {
    try {
      await adminAPI.updateBookingStatus(id, newStatus);
      fetchBookings();
    } catch (err) {
      alert('Failed to update status');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this booking?')) return;
    
    try {
      await adminAPI.deleteBooking(id);
      fetchBookings();
    } catch (err) {
      alert('Failed to delete booking');
    }
  };

  const filteredBookings = filter === 'all' 
    ? bookings 
    : bookings.filter(b => b.status === filter);

  return (
    <AdminLayout onLogout={handleLogout}>
      <div className="bookings-page">
        <div className="page-header">
          <h1>📋 Бронирования</h1>
          <div className="filter-group">
            <select value={filter} onChange={(e) => setFilter(e.target.value)}>
              <option value="all">Все</option>
              <option value="pending">Ожидают</option>
              <option value="confirmed">Подтверждено</option>
              <option value="completed">Завершено</option>
              <option value="cancelled">Отменено</option>
            </select>
          </div>
        </div>

        {loading && <div className="loading">Загрузка...</div>}
        {error && <div className="error">{error}</div>}

        {!loading && !error && (
          <div className="bookings-list">
            {filteredBookings.length === 0 ? (
              <div className="empty-state">
                <p>Нет бронирований</p>
              </div>
            ) : (
              filteredBookings.map((booking) => (
                <div key={booking.id} className="booking-card">
                  <div className="booking-header">
                    <div className="booking-id">#{booking.id.slice(0, 8)}</div>
                    <span className={`status-badge status-${booking.status}`}>
                      {getStatusText(booking.status)}
                    </span>
                  </div>

                  <div className="booking-body">
                    <div className="booking-info">
                      <div className="info-row">
                        <label>Клиент:</label>
                        <span>{booking.customer_name}</span>
                      </div>
                      <div className="info-row">
                        <label>Телефон:</label>
                        <span>{booking.customer_phone}</span>
                      </div>
                      <div className="info-row">
                        <label>Автомобиль:</label>
                        <span>{booking.car_brand} {booking.car_model}</span>
                      </div>
                      <div className="info-row">
                        <label>Услуга:</label>
                        <span>{booking.service_name}</span>
                      </div>
                      <div className="info-row">
                        <label>Цена:</label>
                        <span className="price">{booking.price.toLocaleString('ru-RU')} ₽</span>
                      </div>
                      {booking.comment && (
                        <div className="info-row comment">
                          <label>Комментарий:</label>
                          <span>{booking.comment}</span>
                        </div>
                      )}
                    </div>

                    <div className="booking-actions">
                      <select
                        value={booking.status}
                        onChange={(e) => handleStatusChange(booking.id, e.target.value)}
                        className="status-select"
                      >
                        <option value="pending">Ожидает</option>
                        <option value="confirmed">Подтверждено</option>
                        <option value="completed">Завершено</option>
                        <option value="cancelled">Отменено</option>
                      </select>

                      <button
                        onClick={() => handleDelete(booking.id)}
                        className="delete-btn"
                      >
                        🗑️ Удалить
                      </button>
                    </div>
                  </div>

                  <div className="booking-footer">
                    <small>
                      Создано: {new Date(booking.created_at).toLocaleString('ru-RU')}
                    </small>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </AdminLayout>
  );
};

function getStatusText(status) {
  const statusMap = {
    pending: 'Ожидает',
    confirmed: 'Подтверждено',
    completed: 'Завершено',
    cancelled: 'Отменено',
  };
  return statusMap[status] || status;
}

export default Bookings;
