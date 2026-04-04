import { useState, useEffect } from 'react';
import { reviewsAPI } from '../api/api';
import './ReviewsPublic.css';

const ReviewsPublic = () => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    car_brand: '',
    car_model: '',
    rating: 5,
    text: '',
  });
  const [submitting, setSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState('');

  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
    try {
      const [reviewsRes, statsRes] = await Promise.all([
        reviewsAPI.getPublic(50),
        reviewsAPI.getStats(),
      ]);
      const allReviews = reviewsRes.data.reviews || [];
      setReviews(allReviews);
      setStats(statsRes.data.stats || null);
    } catch (err) {
      console.error('Failed to fetch reviews:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setSubmitMessage('');

    try {
      await reviewsAPI.create(formData);
      setSubmitMessage('✅ Спасибо! Ваш отзыв успешно отправлен!');
      setFormData({
        name: '',
        car_brand: '',
        car_model: '',
        rating: 5,
        text: '',
      });
      setShowForm(false);
      fetchReviews();
    } catch (err) {
      setSubmitMessage('❌ Ошибка при отправке отзыва. Попробуйте позже.');
      console.error('Failed to submit review:', err);
    } finally {
      setSubmitting(false);
      setTimeout(() => setSubmitMessage(''), 5000);
    }
  };

  const getStarRating = (rating) => {
    return '⭐'.repeat(rating);
  };

  if (loading) {
    return (
      <main className="reviews-public-page">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Загрузка отзывов...</p>
        </div>
      </main>
    );
  }

  return (
    <>
    <main className="reviews-public-page">
        <div className="reviews-hero">
          <h1>Отзывы наших клиентов</h1>
          <p>Более {stats?.total_reviews || 0} отзывов со средним рейтингом {stats?.average_rating?.toFixed(1) || '0'} ⭐</p>
        </div>

        {/* Stats */}
        {stats && (
          <div className="reviews-stats-public">
            <div className="stat-item">
              <span className="stat-number">{stats.total_reviews}</span>
              <span className="stat-text">отзывов</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">{stats.average_rating?.toFixed(1) || '0'}</span>
              <span className="stat-text">средний рейтинг</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">{Object.keys(stats.rating_breakdown || {}).filter(r => r >= 4).reduce((acc, r) => acc + (stats.rating_breakdown[r] || 0), 0)}</span>
              <span className="stat-text">положительных</span>
            </div>
          </div>
        )}

        {/* Leave Review Button */}
        <div className="leave-review-section">
          <button className="leave-review-btn" onClick={() => setShowForm(!showForm)}>
            {showForm ? '✕ Закрыть форму' : '✍️ Оставить отзыв'}
          </button>
        </div>

        {/* Review Form Modal */}
        {showForm && (
          <div className="modal-overlay" onClick={() => setShowForm(false)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <h2>Оставить отзыв</h2>
              <p className="form-description">Поделитесь своим опытом работы с нами</p>
              
              {submitMessage && (
                <div className={`submit-message ${submitMessage.includes('✅') ? 'success' : 'error'}`}>
                  {submitMessage}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label>Ваше имя *</label>
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
                    <label>Марка автомобиля *</label>
                    <input
                      type="text"
                      value={formData.car_brand}
                      onChange={(e) => setFormData({ ...formData, car_brand: e.target.value })}
                      required
                      placeholder="Toyota"
                    />
                  </div>
                  <div className="form-group">
                    <label>Модель автомобиля *</label>
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
                  <label>Ваша оценка *</label>
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
                    placeholder="Расскажите о вашем опыте работы с нами..."
                  />
                </div>

                <div className="form-actions">
                  <button 
                    type="button" 
                    className="cancel-btn" 
                    onClick={() => setShowForm(false)}
                  >
                    Отмена
                  </button>
                  <button 
                    type="submit" 
                    className="save-btn"
                    disabled={submitting}
                  >
                    {submitting ? '⏳ Отправка...' : 'Отправить отзыв'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Reviews Grid */}
        <div className="reviews-grid-public">
          {reviews.length === 0 ? (
            <div className="empty-reviews">
              <p>Отзывов пока нет. Будьте первым!</p>
            </div>
          ) : (
            reviews.map((review, index) => (
              <div
                key={review.id}
                className="review-card-public"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="review-header-public">
                  <div className="review-author-public">
                    <span className="author-name">{review.name}</span>
                  </div>
                  <div className="review-rating-public">
                    {getStarRating(review.rating)}
                  </div>
                </div>

                <div className="review-car-info">
                  <span className="car-badge-public">
                    🚗 {review.car_brand} {review.car_model}
                  </span>
                </div>

                <p className="review-text-public">{review.text}</p>

                <div className="review-footer-public">
                  <span className="review-date-public">
                    {new Date(review.created_at).toLocaleDateString('ru-RU', {
                      day: 'numeric',
                      month: 'long',
                      year: 'numeric'
                    })}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>

        {/* CTA Section */}
        <div className="reviews-cta">
          <h2>Почитайте отзывы наших клиентов</h2>
          <p>Мы гордимся качеством наших услуг и довольными клиентами</p>
        </div>
      </main>
    </>
  );
};

export default ReviewsPublic;
