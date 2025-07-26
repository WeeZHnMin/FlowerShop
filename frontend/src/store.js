import { reactive, readonly, watch } from 'vue';

// Function to get user-specific storage key
const getUserKey = (key) => {
  const userId = state.userId;
  return userId ? `${key}_user${userId}` : null;
};

const initialState = {
  isLoggedIn: !!localStorage.getItem('token'),
  role: localStorage.getItem('role') || null,
  userId: localStorage.getItem('userId') || null,
  balance: parseFloat(localStorage.getItem('balance')) || 0,
  cart: [], // Cart will be loaded on login
  lastQuestion: '',
  lastAnswer: '',
};

const state = reactive(initialState);

// Function to load data for the current user
const loadUserData = () => {
  const cartKey = getUserKey('cart');
  const questionKey = getUserKey('lastQuestion');
  const answerKey = getUserKey('lastAnswer');

  state.cart = cartKey ? JSON.parse(localStorage.getItem(cartKey)) || [] : [];
  state.lastQuestion = questionKey ? localStorage.getItem(questionKey) || '' : '';
  state.lastAnswer = answerKey ? localStorage.getItem(answerKey) || '' : '';
};

// Load data on initial script execution if user is already logged in
if (state.isLoggedIn) {
  loadUserData();
}

// Watchers to persist state
watch(() => state.cart, (newCart) => {
  const key = getUserKey('cart');
  if (key) localStorage.setItem(key, JSON.stringify(newCart));
}, { deep: true });

watch(() => state.lastQuestion, (newQuestion) => {
  const key = getUserKey('lastQuestion');
  if (key) localStorage.setItem(key, newQuestion);
});

watch(() => state.lastAnswer, (newAnswer) => {
  const key = getUserKey('lastAnswer');
  if (key) localStorage.setItem(key, newAnswer);
});

const actions = {
  login(token, role, userId, balance) {
    const numericBalance = parseFloat(balance) || 0;
    localStorage.setItem('token', token);
    localStorage.setItem('role', role);
    localStorage.setItem('userId', userId);
    localStorage.setItem('balance', numericBalance);
    state.isLoggedIn = true;
    state.role = role;
    state.userId = userId;
    state.balance = numericBalance;
    loadUserData(); // Load user-specific data after login
  },
  logout() {
    const cartKey = getUserKey('cart');
    const questionKey = getUserKey('lastQuestion');
    const answerKey = getUserKey('lastAnswer');
    // Clear storage for the logged-out user
    if(cartKey) localStorage.removeItem(cartKey);
    if(questionKey) localStorage.removeItem(questionKey);
    if(answerKey) localStorage.removeItem(answerKey);

    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('userId');
    localStorage.removeItem('balance');
    state.isLoggedIn = false;
    state.role = null;
    state.userId = null;
    state.balance = 0;
    loadUserData(); // This will clear the state arrays/strings
  },
  setBalance(balance) {
      const numericBalance = parseFloat(balance) || 0;
      state.balance = numericBalance;
      localStorage.setItem('balance', numericBalance);
  },
  
  // Cart Actions
  addToCart(product) {
    const cartItem = state.cart.find(item => item.id === product.id);
    if (cartItem) {
      cartItem.quantity++;
    } else {
      // Ensure all necessary properties, including image, are added.
      state.cart.push({ 
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.image, // Explicitly add the image property
        quantity: 1 
      });
    }
  },
  decrementQuantity(productId) {
    const cartItem = state.cart.find(item => item.id === productId);
    if (cartItem && cartItem.quantity > 1) {
      cartItem.quantity--;
    } else if (cartItem) {
      this.removeFromCart(productId);
    }
  },
  removeFromCart(productId) {
    state.cart = state.cart.filter(item => item.id !== productId);
  },
  clearCart() {
    state.cart = [];
  },

  // QA Actions
  setNewQuestion(question) {
    state.lastQuestion = question;
    state.lastAnswer = '';
  },
  appendToAnswer(answerChunk) {
    state.lastAnswer += answerChunk;
  },
  setAnswer(answer) {
    state.lastAnswer = answer;
  }
};

export default {
  state: readonly(state),
  ...actions,
};
