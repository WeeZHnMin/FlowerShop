import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import Market from '../components/FlowerList.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import CustomerList from '../components/CustomerList.vue';
import ProductManagement from '../components/ProductManagement.vue';
import AskExpert from '../components/AskExpert.vue';
import ShoppingCart from '../components/ShoppingCart.vue';
import Checkout from '../components/Checkout.vue';
import OrderHistory from '../components/OrderHistory.vue';
import OrderManagement from '../components/OrderManagement.vue';
import Community from '../components/Community.vue';
import PostDetail from '../components/PostDetail.vue';
import CreatePost from '../components/CreatePost.vue';
import BouquetBooking from '../components/BouquetBooking.vue';

import store from '../store';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/market',
        name: 'Market',
        component: Market
    },
    {
        path: '/ask-expert',
        name: 'AskExpert',
        component: AskExpert,
        beforeEnter: (to, from, next) => {
            if (store.state.isLoggedIn) {
                next();
            } else {
                next('/login');
            }
        }
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/customers',
        name: 'CustomerList',
        component: CustomerList,
        beforeEnter: (to, from, next) => {
            const role = localStorage.getItem('role');
            if (role === 'owner') {
                next();
            } else {
                next('/login');
            }
        }
    },
    {
        path: '/product-management',
        name: 'ProductManagement',
        component: ProductManagement,
        beforeEnter: (to, from, next) => {
            const role = localStorage.getItem('role');
            if (role === 'owner') {
                next();
            } else {
                next('/login');
            }
        }
    },
    {
        path: '/cart',
        name: 'ShoppingCart',
        component: ShoppingCart,
        beforeEnter: (to, from, next) => {
            if (store.state.isLoggedIn) {
                next();
            } else {
                next('/login');
            }
        }
    },
    {
        path: '/checkout',
        name: 'Checkout',
        component: Checkout,
        beforeEnter: (to, from, next) => {
            if (store.state.isLoggedIn) {
                next();
            } else {
                next('/login');
            }
        }
    },
    {
        path: '/order-history',
        name: 'OrderHistory',
        component: OrderHistory,
        beforeEnter: (to, from, next) => {
            if (store.state.isLoggedIn && store.state.role === 'customer') {
                next();
            } else {
                next('/login');
            }
        }
    },
    {
        path: '/order-management',
        name: 'OrderManagement',
        component: OrderManagement,
        beforeEnter: (to, from, next) => {
            if (store.state.isLoggedIn && store.state.role === 'owner') {
                next();
            } else {
                next('/login');
            }
        }
    },
    {
        path: '/community',
        name: 'Community',
        component: Community,
        beforeEnter: (to, from, next) => {
            if (store.state.isLoggedIn) {
                next();
            } else {
                next('/login');
            }
        }
    },
    {
        path: '/post/:id',
        name: 'PostDetail',
        component: PostDetail,
        beforeEnter: (to, from, next) => {
            if (store.state.isLoggedIn) {
                next();
            } else {
                next('/login');
            }
        }
    },
    {
        path: '/create-post',
        name: 'CreatePost',
        component: CreatePost,
        beforeEnter: (to, from, next) => {
            if (store.state.isLoggedIn) {
                next();
            } else {
                next('/login');
            }
        }
    },
    {
        path: '/bouquet-booking',
        name: 'BouquetBooking',
        component: BouquetBooking,
        beforeEnter: (to, from, next) => {
            if (store.state.isLoggedIn) {
                next();
            } else {
                next('/login');
            }
        }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;