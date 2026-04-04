import axios from 'axios';

// Use environment variable for API URL, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  login: (password) =>
    api.post('/auth/login', { password }),
  register: (email, password, role = 'user') =>
    api.post('/auth/register', { email, password, role }),
};

// Bookings API
export const bookingsAPI = {

  createBooking: (bookingData) =>
    api.post('/bookings/', bookingData),
  getAllBookings: () =>
    api.get('/bookings/'),
  getBooking: (id) =>
    api.get(`/bookings/${id}`),
};
// Services API
export const servicesAPI = {
  getAll: () =>
    api.get('/services/'),
  getAdminAll: () =>
    api.get('/admin/services'),
  create: (data) =>
    api.post('/admin/services', data),
  update: (id, data) =>
    api.put(`/admin/services/${id}`, data),
  delete: (id) =>
    api.delete(`/admin/services/${id}`),
};

// Reviews API
export const reviewsAPI = {
  // Public
  getPublic: (limit = 50) =>
    api.get(`/reviews/?limit=${limit}`),
  // Admin
  getAll: () =>
    api.get('/admin/reviews'),
  create: (review) =>
    api.post('/admin/reviews', review),
  update: (id, review) =>
    api.put(`/admin/reviews/${id}`, review),
  delete: (id) =>
    api.delete(`/admin/reviews/${id}`),
  getStats: () =>
    api.get('/admin/reviews/stats'),
};

// Admin API
export const adminAPI = {
  getDashboard: () =>
    api.get('/admin/dashboard'),
  getAllBookings: () =>
    api.get('/admin/bookings'),
  updateBookingStatus: (id, status) =>
    api.put(`/admin/bookings/${id}/status`, { status }),
  deleteBooking: (id) =>
    api.delete(`/admin/bookings/${id}`),
  getStats: () =>
    api.get('/admin/stats'),
};

export default api;
