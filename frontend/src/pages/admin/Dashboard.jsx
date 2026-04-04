import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { adminAPI } from '../../api/api';
import { useAuth } from '../../context/AuthContext';
import AdminLayout from '../../components/admin/AdminLayout';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      console.log('📊 Fetching dashboard data...');
      console.log('User:', user);
      console.log('Token exists:', !!localStorage.getItem('token'));
      
      const response = await adminAPI.getDashboard();
      console.log('✅ Dashboard data loaded:', response.data);
      
      setStats(response.data.stats);
      setError('');
    } catch (err) {
      console.error('❌ Dashboard error:', err);
      console.error('Error response:', err.response);
      console.error('Error status:', err.response?.status);
      
      let errorMessage = 'Failed to load dashboard data';
      
      // Проверяем тип ошибки
      if (err.response) {
        // Backend ответил ошибкой
        if (err.response.status === 401) {
          errorMessage = 'Сессия истекла. Пожалуйста, войдите снова.';
          // Автоматический редирект на login через 2 секунды
          setTimeout(() => {
            logout();
            navigate('/admin/login');
          }, 2000);
        } else if (err.response.status === 403) {
          errorMessage = 'Недостаточно прав для доступа';
        } else if (err.response.status === 500) {
          errorMessage = 'Ошибка сервера: ' + (err.response.data?.error || 'Неизвестная ошибка');
        } else if (err.response.data?.error) {
          errorMessage = err.response.data.error;
        }
      } else if (err.request) {
        // Запрос ушёл но нет ответа
        errorMessage = 'Нет ответа от сервера. Проверьте что backend запущен.';
      } else {
        // Другая ошибка
        errorMessage = err.message || 'Неизвестная ошибка';
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/admin/login');
  };

  if (loading) {
    return (
      <AdminLayout onLogout={handleLogout}>
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Загрузка статистики...</p>
        </div>
      </AdminLayout>
    );
  }

  if (error) {
    return (
      <AdminLayout onLogout={handleLogout}>
        <div className="error-container">
          <p className="error-message">{error}</p>
          <button onClick={fetchDashboard} className="retry-btn">
            🔄 Повторить
          </button>
          {error.includes('Сессия истекла') && (
            <Link to="/admin/login" className="login-btn">
              🔐 Войти снова
            </Link>
          )}
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout onLogout={handleLogout}>
      <div className="dashboard">
        <div className="dashboard-header">
          <h1>Dashboard</h1>
          <p>Обзор статистики и управления бронированиями</p>
        </div>

        <div className="stats-grid">
          <div className="stat-card total">
            <div className="stat-icon">📋</div>
            <div className="stat-info">
              <span className="stat-value">{stats?.total_bookings || 0}</span>
              <span className="stat-label">Всего бронирований</span>
            </div>
          </div>

          <div className="stat-card pending">
            <div className="stat-icon">⏳</div>
            <div className="stat-info">
              <span className="stat-value">{stats?.pending_bookings || 0}</span>
              <span className="stat-label">Ожидают</span>
            </div>
          </div>

          <div className="stat-card confirmed">
            <div className="stat-icon">✅</div>
            <div className="stat-info">
              <span className="stat-value">{stats?.confirmed_bookings || 0}</span>
              <span className="stat-label">Подтверждено</span>
            </div>
          </div>

          <div className="stat-card completed">
            <div className="stat-icon">🎉</div>
            <div className="stat-info">
              <span className="stat-value">{stats?.completed_bookings || 0}</span>
              <span className="stat-label">Завершено</span>
            </div>
          </div>

          <div className="stat-card revenue">
            <div className="stat-icon">💰</div>
            <div className="stat-info">
              <span className="stat-value">{stats?.total_revenue?.toLocaleString('ru-RU') || 0} ₽</span>
              <span className="stat-label">Выручка</span>
            </div>
          </div>
        </div>

        <div className="dashboard-actions">
          <Link to="/admin/bookings" className="action-btn primary">
            📋 Все бронирования
          </Link>
          <Link to="/admin/services" className="action-btn secondary">
            🔧 Услуги
          </Link>
        </div>

        {stats?.recent_bookings?.length > 0 && (
          <div className="recent-bookings">
            <h2>Последние бронирования</h2>
            <div className="bookings-table-container">
              <table className="bookings-table">
                <thead>
                  <tr>
                    <th>Клиент</th>
                    <th>Автомобиль</th>
                    <th>Услуга</th>
                    <th>Цена</th>
                    <th>Статус</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.recent_bookings.slice(0, 5).map((booking) => (
                    <tr key={booking.id}>
                      <td>{booking.customer_name}</td>
                      <td>{booking.car_brand} {booking.car_model}</td>
                      <td>{booking.service_name}</td>
                      <td>{booking.price.toLocaleString('ru-RU')} ₽</td>
                      <td>
                        <span className={`status-badge status-${booking.status}`}>
                          {getStatusText(booking.status)}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
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

export default Dashboard;
