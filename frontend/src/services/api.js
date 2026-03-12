import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const auth = {
  register: (data) => api.post('/auth/register', data),
  login: (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    return api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
  },
  logout: () => api.post('/auth/logout'),
  me: () => api.get('/auth/users/me'),
};

export const feed = {
  get: (params) => api.get('/api/feed', { params }),
};

export const articles = {
  get: (id) => api.get(`/api/articles/${id}`),
  interact: (id, type) => api.post(`/api/articles/${id}/interact`, {
    interaction_type: type
  }),
  getSaved: () => api.get('/api/articles/saved/list'),
  getLiked: () => api.get('/api/articles/liked/list'),
};

export const preferences = {
  set: (topics) => api.post('/api/preferences', { topics }),
  get: () => api.get('/api/preferences'),
};

export default api;