import React from 'react';
import '../styles/footer.css';

function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>Контакты</h3>
            <p>Екатеринбург, пер. Автоматики 2И</p>
            <p>Телефон: 8 (995) 495-53-51</p>
            <p>Email: osg.detailing@yandex.ru</p>
          </div>
          <div className="footer-section">
            <h3>Социальные сети</h3>
            <ul className="social-links">
              <li><a href="https://t.me/novicars" target="_blank" rel="noopener noreferrer">Telegram</a></li>
              <li><a href="https://www.instagram.com/novicars_detailing_ekb" target="_blank" rel="noopener noreferrer">Instagram</a></li>
              <li><a href="https://vk.ru/novicars_detailing_ekb" target="_blank" rel="noopener noreferrer">VK</a></li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
