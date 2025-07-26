<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <div class="auth-header">
        <h2>创建您的账户</h2>
        <p class="text-muted">加入我们，探索花卉的无限可能</p>
      </div>
      <div class="auth-body">
        <form @submit.prevent="handleRegister">
          <div class="mb-3">
            <label for="username" class="form-label">用户名</label>
            <input type="text" v-model="username" class="form-control auth-input" id="username" required>
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">密码</label>
            <input type="password" v-model="password" class="form-control auth-input" id="password" required>
          </div>
          <div class="mb-3">
            <label for="email" class="form-label">邮箱地址</label>
            <input type="email" v-model="email" class="form-control auth-input" id="email">
          </div>
          <div class="mb-3">
            <label for="phone_number" class="form-label">手机号</label>
            <input type="text" v-model="phone_number" class="form-control auth-input" id="phone_number">
          </div>
          <button type="submit" class="btn auth-btn w-100">创建账户</button>
        </form>
        <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
          {{ errorMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  data() {
    return {
      username: '',
      password: '',
      email: '',
      phone_number: '',
      role: 'customer',
      errorMessage: ''
    };
  },
  methods: {
    async handleRegister() {
      this.errorMessage = '';
      try {
        await api.register({
          username: this.username,
          password: this.password,
          email: this.email,
          phone_number: this.phone_number,
          role: this.role
        });
        this.$router.push('/login');
      } catch (error) {
        this.errorMessage = '注册失败，请检查您的输入。' + (error.response?.data?.username || '');
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
.auth-wrapper {
  min-height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.24)), url('../assets/干花系.jpg');
  background-size: cover;
  background-position: center;
}

.auth-card {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  background-color: rgba(242, 237, 244, 0.85);
  border: 1px solid #d5bcde;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.auth-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.auth-header h2 {
  color: #8e44ad;
  font-weight: bold;
}

.auth-input:focus {
  border-color: #bba2c4;
  box-shadow: 0 0 0 0.25rem rgba(187, 162, 196, 0.5);
}

.auth-btn {
  background-color: #9b59b6;
  border-color: #9b59b6;
  color: #fff;
  font-weight: bold;
  padding: 0.75rem;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.auth-btn:hover {
  background-color: #8e44ad;
  border-color: #8e44ad;
}
</style>
