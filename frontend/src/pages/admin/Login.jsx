import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../../api/api';
import { useAuth } from '../../context/AuthContext';
import './Login.css';

const Login = () => {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      console.log('📤 Sending login request...');
      const response = await authAPI.login(password);
      console.log('✅ Login response:', response.data);

      const { token, user } = response.data;

      login(user, token);
      navigate('/admin/dashboard');
    } catch (err) {
      console.error('❌ Login error:', err);
      console.error('Error response:', err.response?.data);

      if (err.response?.status === 401) {
        setError('Неверный пароль');
      } else if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else {
        setError('Ошибка подключения к серверу');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-card">
          <div className="login-logo">
            <img src="/Icon_logo.webp" alt="OSG Detailing" className="login-logo-img" />
            <p>Admin Panel</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <h2>Вход</h2>

            {error && <div className="error-message">{error}</div>}

            <div className="form-group">
              <label htmlFor="password">Пароль администратора</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Введите пароль"
                required
                autoFocus
                autoComplete="current-password"
              />
            </div>

            <button type="submit" className="login-btn" disabled={loading}>
              {loading ? 'Вход...' : 'Войти'}
            </button>

            <div className="login-footer">
              <Link to="/">← На главную</Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
