<template>
  <div class="order-management-container">
    <!-- Jumbotron Header -->
    <div class="p-5 mb-4 rounded-3 jumbotron-with-bg text-white">
      <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">订单管理</h1>
        <p class="col-md-8 fs-4">在这里查看和管理所有客户订单。</p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-12">
          <div class="card shadow-sm custom-card">
            <div class="card-body">
              <div v-if="isLoading" class="text-center py-5">
                <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>
              <div v-else-if="orders.length === 0" class="text-center py-5">
                <div class="alert alert-light not-found-alert">
                  <h3>当前没有订单</h3>
                </div>
              </div>
              <div v-else class="table-responsive">
                <table class="table table-hover align-middle">
                  <thead class="table-light">
                    <tr>
                      <th>订单ID</th>
                      <th>客户</th>
                      <th>下单时间</th>
                      <th>总金额</th>
                      <th>状态</th>
                      <th class="text-center">操作</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="order in orders" :key="order.id">
                      <td>#{{ order.id }}</td>
                      <td>{{ order.user.username }}</td>
                      <td>{{ new Date(order.created_at).toLocaleString() }}</td>
                      <td class="fw-bold">¥{{ order.total_price }}</td>
                      <td>
                        <span :class="statusClass(order.status)">{{ formatStatus(order.status) }}</span>
                      </td>
                      <td>
                        <select class="form-select form-select-sm" @change="updateStatus(order, $event)">
                          <option :selected="order.status === 'pending'" value="pending">待支付</option>
                          <option :selected="order.status === 'processing'" value="processing">处理中</option>
                          <option :selected="order.status === 'shipped'" value="shipped">已发货</option>
                          <option :selected="order.status === 'completed'" value="completed">已完成</option>
                          <option :selected="order.status === 'cancelled'" value="cancelled">已取消</option>
                        </select>
                      </td>
                    </tr>
                  </tbody>
                </table>
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

    const fetchOrders = async () => {
      try {
        isLoading.value = true;
        const response = await api.getOrders();
        orders.value = response.data;
      } catch (error) {
        console.error("获取订单失败:", error);
        alert('无法加载订单列表。');
      } finally {
        isLoading.value = false;
      }
    };

    const updateStatus = async (order, event) => {
      const newStatus = event.target.value;
      try {
        await api.updateOrder(order.id, { status: newStatus });
        order.status = newStatus;
        alert(`订单 #${order.id} 的状态已更新为 ${formatStatus(newStatus)}`);
      } catch (error) {
        console.error("更新订单状态失败:", error);
        // Create a serializable object from the error
        const errorLog = {
          message: error.message,
          name: error.name,
          stack: error.stack,
          config: error.config,
          code: error.code,
          response: error.response ? {
            data: error.response.data,
            status: error.response.status,
            headers: error.response.headers
          } : null
        };
        api.logError(errorLog).catch(err => console.error("Failed to log error:", err));
        alert('更新订单状态失败。');
      }
    };

    onMounted(fetchOrders);

    return { orders, isLoading, formatStatus, statusClass, updateStatus };
  },
};
</script>

<style scoped>
.order-management-container {
  background-color: #f4eff6;
  min-height: 100vh;
}

.jumbotron-with-bg {
  background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.6)), url('../assets/花卉2.jpg');
  background-size: cover;
  background-position: center;
}

.custom-card {
  background-color: #fff;
  border: none;
}

.table {
  margin-bottom: 0;
}

.table-hover tbody tr:hover {
  background-color: #e8ddee;
}

.table-light {
  --bs-table-bg: #f4eff6;
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