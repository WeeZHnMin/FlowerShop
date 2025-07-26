<template>
  <!-- 结算页面主容器 -->
  <div class="checkout-container">
    <!-- 页面顶部Jumbotron -->
    <div class="p-5 mb-4 rounded-3 jumbotron-with-bg text-white">
      <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">结算</h1>
        <p class="col-md-8 fs-4">请确认您的订单信息并完成支付。</p>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="container">
      <div class="row g-5">
        <!-- 左侧：收货信息表单 -->
        <div class="col-md-7">
          <div class="card shadow-sm custom-card">
            <div class="card-header"><h4>收货信息</h4></div>
            <div class="card-body p-4">
              <form @submit.prevent="handleCheckout">
                <!-- 收货地址输入框 -->
                <div class="mb-3">
                  <label for="shippingAddress" class="form-label">收货地址</label>
                  <textarea id="shippingAddress" v-model="shippingAddress" class="form-control" rows="3" required></textarea>
                </div>
                <!-- 支付方式选择 -->
                <div class="mb-3">
                  <label for="paymentMethod" class="form-label">支付方式</label>
                  <select id="paymentMethod" v-model="paymentMethod" class="form-select" required>
                    <option value="balance">余额支付</option>
                    <option value="alipay">支付宝</option>
                    <option value="wechat">微信支付</option>
                    <option value="cod">货到付款</option>
                  </select>
                </div>
                <!-- 提交订单按钮 -->
                <div class="d-grid">
                  <button type="submit" class="btn btn-primary btn-lg" :disabled="isSubmitting || (paymentMethod === 'balance' && totalPrice > balance)">
                    <span v-if="isSubmitting" class="spinner-border spinner-border-sm"></span>
                    <!-- 根据不同情况显示不同文本 -->
                    <span v-if="paymentMethod === 'balance' && totalPrice > balance">余额不足</span>
                    <span v-else>{{ isSubmitting ? '正在提交...' : '提交订单' }}</span>
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <!-- 右侧：订单摘要 -->
        <div class="col-md-5">
          <div class="card shadow-sm custom-card">
            <div class="card-header"><h5>订单摘要</h5></div>
            <div class="card-body p-4">
              <!-- 显示用户当前余额 -->
              <div class="alert alert-success">
                <strong>当前余额:</strong> <span class="fw-bold">¥{{ formattedBalance }}</span>
              </div>
              <!-- 订单项目列表 -->
              <ul class="list-group list-group-flush">
                <li v-for="item in cartItems" :key="item.id" class="list-group-item d-flex justify-content-between">
                  <span>{{ item.name }} x {{ item.quantity }}</span>
                  <span>¥{{ (item.price * item.quantity).toFixed(2) }}</span>
                </li>
              </ul>
            </div>
            <!-- 订单总计 -->
            <div class="card-footer">
              <strong>总计: <span class="text-danger fw-bold">¥{{ totalPrice.toFixed(2) }}</span></strong>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 支付二维码模态框 -->
    <PaymentQRCodeModal 
      v-if="showPaymentModal"
      :payment-type="paymentMethod"
      :amount="totalPrice"
      @close="showPaymentModal = false"
      @payment-successful="handleSuccessfulPayment"
    />
  </div>
</template>

<script>
// 导入必要的模块和组件
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import store from '../store'; // Vuex store
import api from '../services/api'; // API服务
import PaymentQRCodeModal from './PaymentQRCodeModal.vue'; // 支付模态框组件

export default {
  components: {
    PaymentQRCodeModal
  },
  // 使用Vue 3 Composition API
  setup() {
    const router = useRouter(); // 获取路由实例
    // 从store计算购物车项目和用户余额
    const cartItems = computed(() => store.state.cart);
    const balance = computed(() => store.state.balance);
    // 定义响应式数据
    const shippingAddress = ref('');
    const paymentMethod = ref('balance');
    const isSubmitting = ref(false); // 订单提交状态
    const showPaymentModal = ref(false); // 控制支付模态框的显示

    // 计算格式化后的余额，保留两位小数
    const formattedBalance = computed(() => {
      const numBalance = parseFloat(balance.value);
      return isNaN(numBalance) ? '0.00' : numBalance.toFixed(2);
    });

    // 计算购物车总价
    const totalPrice = computed(() => 
      cartItems.value.reduce((total, item) => total + item.price * item.quantity, 0)
    );

    // 处理结算逻辑
    const handleCheckout = () => {
      // 如果是支付宝或微信支付，显示二维码模态框
      if (paymentMethod.value === 'alipay' || paymentMethod.value === 'wechat') {
        showPaymentModal.value = true;
      } else {
        // 否则直接提交订单
        submitOrder();
      }
    };

    // 模拟支付成功后的处理
    const handleSuccessfulPayment = () => {
      showPaymentModal.value = false; // 关闭模态框
      submitOrder(); // 提交订单
    };

    // 异步提交订单到后端
    const submitOrder = async () => {
      if (cartItems.value.length === 0) {
        alert('您的购物车是空的！');
        return;
      }
      // 再次校验余额
      if (paymentMethod.value === 'balance' && totalPrice.value > balance.value) {
        alert('您的余额不足以完成支付。');
        return;
      }

      isSubmitting.value = true;
      try {
        // 构造订单数据
        const orderData = {
          shipping_address: shippingAddress.value,
          items: cartItems.value.map(item => ({
            flower_id: item.id,
            quantity: item.quantity,
            price: item.price
          })),
        };
        // 调用API创建订单
        const response = await api.createOrder(orderData);
        store.clearCart(); // 清空购物车
        // 如果后端返回了新的用户信息，则更新store中的余额
        if (response.data.user && response.data.user.balance !== undefined) {
            store.setBalance(response.data.user.balance);
        }
        alert('订单已成功提交！');
        router.push('/order-history'); // 跳转到订单历史页面
      } catch (error) {
        console.error('订单提交失败:', error);
        // 记录错误日志
        const errorLog = {
          message: error.message,
          name: error.name,
          stack: error.stack,
          config: error.config,
          code: error.code,
          response: error.response ? { data: error.response.data, status: error.response.status, headers: error.response.headers } : null
        };
        api.logError(errorLog).catch(err => console.error("Failed to log error:", err));
        const errorMessage = error.response?.data?.detail || '订单提交失败，请稍后再试。';
        alert(errorMessage);
      } finally {
        isSubmitting.value = false; // 结束提交状态
      }
    };

    // 返回所有需要在模板中使用的数据和方法
    return { 
      cartItems, 
      totalPrice, 
      balance,
      formattedBalance,
      shippingAddress, 
      paymentMethod, 
      handleCheckout, 
      submitOrder, 
      isSubmitting, 
      showPaymentModal,
      handleSuccessfulPayment
    };
  },
};
</script>

<style scoped>
/* 页面容器样式 */
.checkout-container {
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
  height: 100%;
}

/* 卡片头部样式 */
.card-header {
  background-color: #f4eff6;
  font-weight: bold;
}

/* 列表组项目样式 */
.list-group-item {
  background-color: transparent;
}

/* 主要按钮样式 */
.btn-primary {
    background-color: #9b59b6;
    border-color: #9b59b6;
}
</style>
