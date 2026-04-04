import React from 'react';
import '../styles/reviews.css';



function Reviews() {
  return (
    <section className="reviews">
      <div className="container">
        <h2>Отзывы клиентов</h2>
        <div className="reviews-grid">
          {reviewsData.map(review => (
            <div key={review.id} className="review-card">
              <p className="review-text">"{review.text}"</p>
              <p className="review-author">{review.author}</p>
              <p className="review-car">{review.carModel}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default Reviews;
