import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return axios(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export const authAPI = {
  login: async (username, password) => {
    const response = await axios.post(`${API_BASE_URL}/auth/login/`, {
      username,
      password,
    });
    return response.data;
  },

  register: async (username, email, password) => {
    const response = await api.post('/auth/register/', {
      username,
      email,
      password,
      password2: password,
    });
    return response.data;
  },

  getProfile: async () => {
    const response = await api.get('/user/profile/');
    return response.data;
  },
};

export const categoryAPI = {
  getAll: async () => {
    const response = await api.get('/categories/');
    return response.data;
  },

  getQuestions: async (slug, params = {}) => {
    const response = await api.get(`/categories/${slug}/questions/`, { params });
    return response.data;
  },
};

export const questionAPI = {
  getById: async (id) => {
    const response = await api.get(`/questions/${id}/`);
    return response.data;
  },

  submitAnswer: async (id, data) => {
    const response = await api.post(`/questions/${id}/submit/`, data);
    return response.data;
  },
};

export const leaderboardAPI = {
  get: async (period = 'overall') => {
    const response = await api.get('/leaderboard/', { params: { period } });
    return response.data;
  },
};

export const challengeAPI = {
  create: async (data) => {
    const response = await api.post('/challenges/', data);
    return response.data;
  },

  getStatus: async (id) => {
    const response = await api.get(`/challenges/${id}/status/`);
    return response.data;
  },

  getAll: async () => {
    const response = await api.get('/challenges/');
    return response.data;
  },
};

export default api;
