import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export const authApi = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  me: () => api.get('/auth/me'),
};

export const locationsApi = {
  getAll: (category) => api.get('/locations/', { params: category ? { category } : {} }),
  getById: (id) => api.get(`/locations/${id}`),
  create: (data) => api.post('/locations/', data),
  update: (id, data) => api.put(`/locations/${id}`, data),
  delete: (id) => api.delete(`/locations/${id}`),
  uploadImage: (id, file, isPrimary = false) => {
    const form = new FormData();
    form.append('file', file);
    return api.post(`/locations/${id}/images?is_primary=${isPrimary}`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  deleteImage: (imageId) => api.delete(`/locations/images/${imageId}`),
};

export const slotsApi = {
  getByLocation: (locationId) => api.get(`/slots/location/${locationId}`),
  getAvailable: (locationId) => api.get(`/slots/location/${locationId}/available`),
  create: (data) => api.post('/slots/', data),
  delete: (id) => api.delete(`/slots/${id}`),
};

export const bookingsApi = {
  create: (data) => api.post('/bookings/', data),
  getMy: () => api.get('/bookings/my'),
  getAll: () => api.get('/bookings/'),
  getOne: (id) => api.get(`/bookings/${id}`),
  pay: (id) => api.post(`/bookings/${id}/pay`),
  cancel: (id) => api.post(`/bookings/${id}/cancel`),
  updateStatus: (id, status) => api.put(`/bookings/${id}/status`, { status }),
};

export const usersApi = {
  getAll: () => api.get('/users/'),
  deactivate: (id) => api.put(`/users/${id}/deactivate`),
};

export default api;
