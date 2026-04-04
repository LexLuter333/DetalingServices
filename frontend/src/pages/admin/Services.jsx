import { useState, useEffect } from 'react';
import AdminLayout from '../../components/admin/AdminLayout';
import { useAuth } from '../../context/AuthContext';
import { servicesAPI } from '../../api/api';
import './Services.css';

const Services = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingService, setEditingService] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
  });
  const { logout } = useAuth();

  useEffect(() => {
    fetchServices();
  }, []);

  const fetchServices = async () => {
    try {
      const response = await servicesAPI.getAdminAll();
      setServices(response.data.services || []);
    } catch (err) {
      setError('Failed to load services');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    window.location.href = '/admin/login';
  };

  const handleAddNew = () => {
    setEditingService(null);
    setFormData({
      name: '',
      description: '',
      price: '',
    });
    setShowAddForm(true);
  };

  const handleEdit = (service) => {
    setEditingService(service);
    setFormData({
      name: service.name,
      description: service.description || '',
      price: service.price.toString(),
    });
    setShowAddForm(true);
  };

  const handleDelete = async (id) => {
    if (!confirm('Вы уверены, что хотите удалить эту услугу?')) return;
    try {
      await servicesAPI.delete(id);
      await fetchServices();
    } catch (err) {
      alert('Ошибка при удалении услуги');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const serviceData = {
        name: formData.name,
        description: formData.description,
        price: parseFloat(formData.price) || 0,
      };

      if (editingService) {
        await servicesAPI.update(editingService.id, serviceData);
      } else {
        await servicesAPI.create(serviceData);
      }

      setShowAddForm(false);
      setEditingService(null);
      await fetchServices();
    } catch (err) {
      alert('Ошибка при сохранении услуги');
    }
  };

  if (loading) {
    return (
      <AdminLayout onLogout={handleLogout}>
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Загрузка услуг...</p>
        </div>
      </AdminLayout>
    );
  }

  if (error) {
    return (
      <AdminLayout onLogout={handleLogout}>
        <div className="error-container">
          <p className="error-message">{error}</p>
          <button onClick={fetchServices} className="retry-btn">Retry</button>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout onLogout={handleLogout}>
      <div className="services-page">
        <div className="page-header">
          <h1>🔧 Управление услугами</h1>
          <button className="add-service-btn" onClick={handleAddNew}>
            + Добавить услугу
          </button>
        </div>

        {/* Add/Edit Form Modal */}
        {showAddForm && (
          <div className="modal-overlay" onClick={() => setShowAddForm(false)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <h2>{editingService ? 'Редактировать услугу' : 'Новая услуга'}</h2>
              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label>Название *</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Описание</label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    rows="3"
                  />
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Цена (₽) *</label>
                    <input
                      type="number"
                      value={formData.price}
                      onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                      required
                      min="0"
                    />
                  </div>
                </div>
                <div className="form-actions">
                  <button type="button" className="cancel-btn" onClick={() => setShowAddForm(false)}>
                    Отмена
                  </button>
                  <button type="submit" className="save-btn">
                    {editingService ? 'Сохранить' : 'Создать'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Services Table */}
        <div className="services-table-container">
          <table className="services-table">
            <thead>
              <tr>
                <th>Название</th>
                <th>Описание</th>
                <th>Цена</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              {services.map((service) => (
                <tr key={service.id}>
                  <td className="name-cell">{service.name}</td>
                  <td className="desc-cell">{service.description || '—'}</td>
                  <td className="price-cell">{service.price.toLocaleString('ru-RU')} ₽</td>
                  <td className="actions-cell">
                    <button
                      className="edit-btn"
                      onClick={() => handleEdit(service)}
                      title="Редактировать"
                    >
                      ✏️
                    </button>
                    <button
                      className="delete-btn"
                      onClick={() => handleDelete(service.id)}
                      title="Удалить"
                    >
                      🗑️
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AdminLayout>
  );
};

export default Services;
