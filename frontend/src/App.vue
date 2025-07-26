<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">FlowerShop</a>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link to="/" class="nav-link">首页</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/market" class="nav-link">花卉市场</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <router-link to="/bouquet-booking" class="nav-link">花束预订</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <router-link to="/ask-expert" class="nav-link">AI 专家与拍照识花</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <router-link to="/community" class="nav-link">社区</router-link>
            </li>
            <li class="nav-item" v-if="isOwner">
              <router-link to="/customers" class="nav-link">客户管理</router-link>
            </li>
            <li class="nav-item" v-if="isOwner">
              <router-link to="/product-management" class="nav-link">商品管理</router-link>
            </li>
            <li class="nav-item" v-if="isOwner">
              <router-link to="/order-management" class="nav-link">订单管理</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn && !isOwner">
              <router-link to="/order-history" class="nav-link">我的订单</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item" v-if="isLoggedIn && !isOwner">
              <router-link to="/cart" class="nav-link">
                购物车
                <span class="badge bg-primary rounded-pill">{{ cartItemCount }}</span>
              </router-link>
            </li>
            <li class="nav-item" v-if="!isLoggedIn">
              <router-link to="/register" class="nav-link">注册</router-link>
            </li>
            <li class="nav-item" v-if="!isLoggedIn">
              <router-link to="/login" class="btn btn-primary">登录</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <button class="btn btn-outline-danger" @click="handleLogout">登出</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <main class="container mt-4">
      <router-view/>
    </main>
  </div>
</template>

<script>
import store from './store.js';
import api from './services/api';
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'App',
  setup() {
    const router = useRouter();
    const isLoggedIn = computed(() => store.state.isLoggedIn);
    const isOwner = computed(() => store.state.role === 'owner');
    const cartItemCount = computed(() => store.state.cart.reduce((count, item) => count + item.quantity, 0));

    const handleLogout = () => {
      store.logout();
      router.push('/login');
    };

    onMounted(async () => {
      if (isLoggedIn.value) {
        try {
          const response = await api.getCurrentUser();
          store.setBalance(response.data.balance);
        } catch (error) {
          console.error("Failed to fetch user details:", error);
          if (error.response && error.response.status === 401) {
            store.logout();
            router.push('/login');
          }
        }
      }
    });

    return { isLoggedIn, isOwner, cartItemCount, handleLogout };
  }
};
</script>

<style>
body {
  background-color: #d5bcde; /* Or a color that complements the navbar */
}
.navbar {
  background-color: #d5bcde !important;
}
.navbar-brand {
  font-weight: bold;
}
</style>
