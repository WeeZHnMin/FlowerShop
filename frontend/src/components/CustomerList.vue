<template>
  <!-- 客户列表页面主容器 -->
  <div class="customer-list-container">
    <!-- 页面顶部Jumbotron -->
    <div class="p-5 mb-4 rounded-3 jumbotron-with-bg text-white">
      <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">客户管理</h1>
        <p class="col-md-8 fs-4">查看和管理您的客户信息。</p>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-10">
          <!-- 包裹表格的卡片 -->
          <div class="card shadow-sm custom-card">
            <div class="card-body">
              <!-- 错误信息提示 -->
              <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
              <!-- 客户信息表格 -->
              <div v-if="customers.length" class="table-responsive">
                <table class="table table-hover align-middle">
                  <thead class="table-light">
                    <tr>
                      <th scope="col">#</th>
                      <th scope="col">用户名</th>
                      <th scope="col">邮箱</th>
                      <th scope="col">手机号</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="customer in customers" :key="customer.id">
                      <th scope="row">{{ customer.id }}</th>
                      <td>{{ customer.username }}</td>
                      <td>{{ customer.email || '-' }}</td>
                      <td>{{ customer.phone_number || '-' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!-- 无客户信息时的提示 -->
              <p v-else-if="!errorMessage" class="text-center text-muted py-4">暂无客户信息。</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// 导入API服务
import api from '../services/api';

export default {
  // 使用Options API
  data() {
    return {
      customers: [], // 存储客户列表
      errorMessage: '' // 存储错误信息
    };
  },
  // Vue生命周期钩子：组件创建后调用
  async created() {
    try {
      // 调用API获取客户列表
      const response = await api.getCustomers();
      this.customers = response.data;
    } catch (error) { 
      // 如果出错，设置错误信息
      this.errorMessage = '无法加载客户列表。请确保您是店主并已登录。';
      console.error(error);
    }
  }
};
</script>

<style scoped>
/* 页面主容器样式 */
.customer-list-container {
  background-color: #f4eff6; /* 淡紫色背景 */
  min-height: 100vh;
}

/* Jumbotron背景图片 */
.jumbotron-with-bg {
  background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.6)), url('../assets/花卉2.jpg');
  background-size: cover;
  background-position: center;
}

/* 自定义卡片样式 */
.custom-card {
  background-color: #fff;
  border: none;
}

/* 表格样式 */
.table {
  margin-bottom: 0;
}

/* 表格行悬停效果 */
.table-hover tbody tr:hover {
  background-color: #e8ddee; /* 淡紫色悬停背景 */
}

/* 表格头部样式 */
.table-light {
  --bs-table-bg: #f4eff6; /* 表头使用淡紫色背景 */
}
</style>
