<template>
  <div class="shopping-cart-container">
    <!-- Jumbotron Header -->
    <div class="p-5 mb-4 rounded-3 jumbotron-with-bg text-white">
      <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">我的购物车</h1>
        <p class="col-md-8 fs-4">确认您的选择，然后轻松完成结算。</p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="card shadow-sm custom-card">
            <div class="card-body p-4">
              <div class="alert alert-success d-flex justify-content-between align-items-center">
                <strong>当前余额:</strong> <span class="fw-bold fs-5">¥{{ formattedBalance }}</span>
              </div>
              <div v-if="cartItems.length === 0" class="text-center py-5">
                <div class="alert alert-light not-found-alert">
                  <h3>您的购物车是空的</h3>
                  <p class="lead">快去市场逛逛吧！</p>
                </div>
              </div>
              <div v-else>
                <ul class="list-group list-group-flush mb-3">
                  <li v-for="item in cartItems" :key="item.id" class="list-group-item d-flex justify-content-between align-items-center">
                    <div class="d-flex align-items-center">
                      <img :src="item.image" :alt="item.name" class="me-3 rounded" style="width: 80px; height: 80px; object-fit: cover;" v-if="item.image">
                      <div>
                        <h5 class="mb-1">{{ item.name }}</h5>
                        <span class="text-muted">¥{{ item.price }}</span>
                      </div>
                    </div>
                    <div class="d-flex align-items-center">
                      <button class="btn btn-sm btn-outline-secondary me-2" @click="decrementQuantity(item.id)">-</button>
                      <span class="fw-bold">{{ item.quantity }}</span>
                      <button class="btn btn-sm btn-outline-secondary ms-2" @click="incrementQuantity(item.id)">+</button>
                      <button class="btn btn-sm btn-outline-danger ms-3" @click="removeFromCart(item.id)"><i class="bi bi-trash"></i></button>
                    </div>
                  </li>
                </ul>
                <hr>
                <div class="text-end">
                  <h4>总计: <span class="text-danger fw-bold">¥{{ totalPrice.toFixed(2) }}</span></h4>
                </div>
              </div>
            </div>
            <div class="card-footer text-end bg-transparent" v-if="cartItems.length > 0">
              <router-link to="/checkout" class="btn btn-primary btn-lg">去结算</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import store from '../store';
import { computed } from 'vue';

export default {
  setup() {
    const cartItems = computed(() => store.state.cart);
    const balance = computed(() => store.state.balance);

    const formattedBalance = computed(() => {
      const numBalance = parseFloat(balance.value);
      return isNaN(numBalance) ? '0.00' : numBalance.toFixed(2);
    });

    const totalPrice = computed(() => {
      return cartItems.value.reduce((total, item) => total + parseFloat(item.price) * item.quantity, 0);
    });

    const incrementQuantity = (itemId) => {
      const product = cartItems.value.find(item => item.id === itemId);
      if (product) {
        store.addToCart(product);
      }
    };

    const decrementQuantity = (itemId) => {
      store.decrementQuantity(itemId);
    };

    const removeFromCart = (itemId) => {
      store.removeFromCart(itemId);
    };

    return {
      cartItems,
      totalPrice,
      formattedBalance,
      incrementQuantity,
      decrementQuantity,
      removeFromCart,
    };
  },
};
</script>

<style scoped>
.shopping-cart-container {
  background-color: #f4eff6;
  min-height: 100vh;
}

.jumbotron-with-bg {
  background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.6)), url('../assets/花卉1.jpg');
  background-size: cover;
  background-position: center;
}

.custom-card {
  background-color: #fff;
  border: none;
}

.list-group-item {
  background-color: transparent;
}

.not-found-alert {
  background-color: rgba(255, 255, 255, 0.7);
  border: none;
  padding: 2rem;
}

.btn-primary {
    background-color: #9b59b6;
    border-color: #9b59b6;
}
</style>
