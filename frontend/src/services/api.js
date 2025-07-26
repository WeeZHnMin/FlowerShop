import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export default {
  // 用户认证
  register(userData) {
    return apiClient.post('/users/register/', userData);
  },
  login(credentials) {
    return apiClient.post('/users/login/', credentials);
  },
  logout() {
    return apiClient.post('/users/logout/');
  },
  getCustomers() {
    return apiClient.get('/users/customers/');
  },

  // 花卉
  getFlowers() {
    return apiClient.get('/products/flowers/');
  },
  addFlower(formData) {
    return apiClient.post('/products/flowers/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
  updateFlower(id, formData) {
    return apiClient.put(`/products/flowers/${id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
  deleteFlower(id) {
    return apiClient.delete(`/products/flowers/${id}/`);
  },

  // 订单
  createOrder(orderData) {
    return apiClient.post('/orders/', orderData);
  },
  getOrders() {
    return apiClient.get('/orders/');
  },
  updateOrder(id, data) {
    return apiClient.patch(`/orders/${id}/`, data);
  },

  // 社区
  getPosts() {
    return apiClient.get('/products/posts/');
  },
  getPost(id) {
    return apiClient.get(`/products/posts/${id}/`);
  },
  createPost(postData) {
    return apiClient.post('/products/posts/', postData);
  },
  likePost(postId) {
    return apiClient.post(`/products/posts/${postId}/likes/`);
  },
  addComment(postId, commentData) {
    return apiClient.post(`/products/posts/${postId}/comments/`, commentData);
  },

  // 识别
  recognizeFlower(formData) {
    return apiClient.post('/products/recognize/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // 错误日志
  logError(errorData) {
    return apiClient.post('/products/log-error/', errorData);
  }
};