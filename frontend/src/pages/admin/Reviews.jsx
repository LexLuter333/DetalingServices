import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AdminLayout from '../../components/admin/AdminLayout';
import { useAuth } from '../../context/AuthContext';
import { reviewsAPI } from '../../api/api';
import './Reviews.css';

const Reviews = () => {
  const [reviews, setReviews] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    car_brand: '',
    car_model: '',
    rating: 5,
    text: '',
  });
  const { logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [reviewsRes, statsRes] = await Promise.all([
        reviewsAPI.getAll(),
        reviewsAPI.getStats(),
      ]);
      setReviews(reviewsRes.data.reviews || []);
      setStats(statsRes.data.stats || null);
    } catch (err) {
      console.error('Failed to fetch data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/admin/login');
  };

  const handleAddNew = () => {
    setFormData({
      name: '',
      car_brand: '',
      car_model: '',
      rating: 5,
      text: '',
    });
    setShowAddForm(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await reviewsAPI.create(formData);
      setShowAddForm(false);
      await fetchData();
      alert('Отзыв успешно добавлен!');
    } catch (err) {
      alert('Ошибка при добавлении отзыва: ' + (err.response?.data?.error || err.message));
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Вы уверены, что хотите удалить этот отзыв?')) return;
    try {
      await reviewsAPI.delete(id);
      await fetchData();
    } catch (err) {
      alert('Ошибка при удалении отзыва');
    }
  };

  const getStarRating = (rating) => {
    return '⭐'.repeat(rating);
  };

  if (loading) {
    return (
      <AdminLayout onLogout={handleLogout}>
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Загрузка отзывов...</p>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout onLogout={handleLogout}>
      <div className="reviews-page">
        <div className="page-header">
          <h1>💬 Управление отзывами</h1>
          <button className="add-review-btn" onClick={handleAddNew}>
            + Добавить отзыв
          </button>
        </div>

        {/* Stats */}
        {stats && (
          <div className="reviews-stats">
            <div className="stat-card">
              <span className="stat-value">{stats.total_reviews}</span>
              <span className="stat-label">Всего отзывов</span>
            </div>
            <div className="stat-card">
              <span className="stat-value">{stats.average_rating?.toFixed(1) || '0'}</span>
              <span className="stat-label">Средний рейтинг</span>
            </div>
          </div>
        )}

        {/* Add Review Form Modal */}
        {showAddForm && (
          <div className="modal-overlay" onClick={() => setShowAddForm(false)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <h2>Добавить отзыв</h2>
              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label>Имя клиента *</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                    placeholder="Иван Иванов"
                  />
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Марка авто *</label>
                    <input
                      type="text"
                      value={formData.car_brand}
                      onChange={(e) => setFormData({ ...formData, car_brand: e.target.value })}
                      required
                      placeholder="Toyota"
                    />
                  </div>
                  <div className="form-group">
                    <label>Модель авто *</label>
                    <input
                      type="text"
                      value={formData.car_model}
                      onChange={(e) => setFormData({ ...formData, car_model: e.target.value })}
                      required
                      placeholder="Camry"
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label>Рейтинг *</label>
                  <div className="rating-input">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        key={star}
                        type="button"
                        className={`star-btn ${formData.rating >= star ? 'active' : ''}`}
                        onClick={() => setFormData({ ...formData, rating: star })}
                      >
                        ⭐
                      </button>
                    ))}
                    <span className="rating-value">{formData.rating} из 5</span>
                  </div>
                </div>
                <div className="form-group">
                  <label>Текст отзыва *</label>
                  <textarea
                    value={formData.text}
                    onChange={(e) => setFormData({ ...formData, text: e.target.value })}
                    rows="4"
                    required
                    placeholder="Напишите текст отзыва..."
                  />
                </div>
                <div className="form-actions">
                  <button type="button" className="cancel-btn" onClick={() => setShowAddForm(false)}>
                    Отмена
                  </button>
                  <button type="submit" className="save-btn">
                    Добавить отзыв
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Reviews List */}
        <div className="reviews-section">
          <h2>📝 Все отзывы ({reviews.length})</h2>
          <div className="reviews-list">
            {reviews.length === 0 ? (
              <div className="empty-state">
                <p>Отзывов пока нет. Нажмите "Добавить отзыв" чтобы создать первый.</p>
              </div>
            ) : (
              reviews.map((review) => (
                <div key={review.id} className="review-card">
                  <div className="review-header">
                    <div className="review-author">
                      <span className="author-name">{review.name}</span>
                      <span className="review-rating">{getStarRating(review.rating)}</span>
                    </div>
                    <div className="review-car">
                      <span className="car-badge">
                        🚗 {review.car_brand} {review.car_model}
                      </span>
                    </div>
                  </div>
                  <p className="review-text">{review.text}</p>
                  <div className="review-footer">
                    <span className="review-date">
                      {new Date(review.created_at).toLocaleDateString('ru-RU', {
                        day: 'numeric',
                        month: 'long',
                        year: 'numeric',
                      })}
                    </span>
                    <button
                      className="delete-review-btn"
                      onClick={() => handleDelete(review.id)}
                    >
                      🗑️ Удалить
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </AdminLayout>
  );
};

export default Reviews;
