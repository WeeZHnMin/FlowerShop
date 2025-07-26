<template>
  <div class="order-history-container">
    <!-- Jumbotron Header -->
    <div class="p-5 mb-4 rounded-3 jumbotron-with-bg text-white">
      <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">我的订单</h1>
        <p class="col-md-8 fs-4">在这里查看您所有的订单历史记录。</p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div v-if="isLoading" class="text-center py-5">
            <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
          <div v-else-if="orders.length === 0" class="text-center py-5">
            <div class="alert alert-light not-found-alert">
              <h3>您还没有任何订单</h3>
              <p class="lead">快去市场逛逛吧！</p>
            </div>
          </div>
          <div v-else class="accordion" id="ordersAccordion">
            <div v-for="order in orders" :key="order.id" class="accordion-item custom-card shadow-sm mb-3">
              <h2 class="accordion-header" :id="'heading' + order.id">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" :data-bs-target="'#collapse' + order.id">
                  <span class="fw-bold me-3">订单 #{{ order.id }}</span>
                  <span :class="statusClass(order.status)">{{ formatStatus(order.status) }}</span>
                  <small class="ms-auto text-muted">{{ new Date(order.created_at).toLocaleString() }}</small>
                </button>
              </h2>
              <div :id="'collapse' + order.id" class="accordion-collapse collapse" data-bs-parent="#ordersAccordion">
                <div class="accordion-body">
                  <p><strong>总金额:</strong> <span class="text-danger fw-bold">¥{{ order.total_price }}</span></p>
                  <p><strong>收货地址:</strong> {{ order.shipping_address }}</p>
                  <hr>
                  <h5>订单商品:</h5>
                  <ul class="list-group list-group-flush">
                    <li v-for="item in order.items" :key="item.id" class="list-group-item d-flex justify-content-between align-items-center">
                      <span>{{ item.flower.name }}</span>
                      <span>{{ item.quantity }} x ¥{{ item.price }}</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import api from '../services/api';

export default {
  setup() {
    const orders = ref([]);
    const isLoading = ref(true);

    const statusMap = {
      pending: '待支付',
      processing: '处理中',
      shipped: '已发货',
      completed: '已完成',
      cancelled: '已取消',
    };

    const formatStatus = (status) => statusMap[status] || status;

    const statusClass = (status) => {
      switch (status) {
        case 'completed': return 'badge bg-success';
        case 'shipped': return 'badge bg-primary';
        case 'processing': return 'badge bg-info text-dark';
        case 'cancelled': return 'badge bg-danger';
        default: return 'badge bg-secondary';
      }
    };

    onMounted(async () => {
      try {
        const response = await api.getOrders();
        orders.value = response.data;
      } catch (error) {
        console.error("获取订单失败:", error);
        alert('无法加载您的订单历史。');
      } finally {
        isLoading.value = false;
      }
    });

    return { orders, isLoading, formatStatus, statusClass };
  },
};
</script>

<style scoped>
.order-history-container {
  background-color: #f4eff6;
  min-height: 100vh;
}

.jumbotron-with-bg {
  background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.6)), url('../assets/花卉1.jpg');
  background-size: cover;
  background-position: center;
}

.custom-card, .accordion-item {
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0,0,0,0.08);
}

.accordion-button {
  background-color: #fff;
  color: #333;
}

.accordion-button:not(.collapsed) {
  background-color: #f4eff6;
  box-shadow: inset 0 -1px 0 rgba(0,0,0,.125);
}

.accordion-body {
  background-color: #fdfdfd;
}

.not-found-alert {
  background-color: rgba(255, 255, 255, 0.7);
  border: none;
  padding: 2rem;
}

.badge.bg-primary {
    background-color: #9b59b6 !important;
}
</style>