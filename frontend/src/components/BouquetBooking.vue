<template>
  <div class="container">
    <!-- 页面标题 -->
    <div class="p-5 mb-4 rounded-3 jumbotron-with-bg text-white">
      <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">花束预订服务</h1>
        <p class="col-md-8 fs-4">选择您心仪的花束类型和大小，预约配送时间，让美丽准时到达。</p>
      </div>
    </div>

    <!-- 筛选控制栏 -->
    <div class="d-flex justify-content-between align-items-center mb-4 p-3 rounded shadow-sm controls-bar">
      <!-- 花束类型筛选 -->
      <div class="btn-group" role="group">
        <div class="btn-group">
          <button type="button" class="btn btn-outline-primary dropdown-toggle" data-bs-toggle="dropdown">
            {{ selectedBouquetType ? getBouquetTypeLabel(selectedBouquetType) : '所有类型' }}
          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#" @click.prevent="filterByBouquetType(null)">所有类型</a></li>
            <li v-if="bouquetTypes.length === 0"><span class="dropdown-item-text">加载中...</span></li>
            <li v-for="type in bouquetTypes" :key="type.value">
              <a class="dropdown-item" href="#" @click.prevent="filterByBouquetType(type.value)">{{ type.label }}</a>
            </li>
          </ul>
        </div>

        <!-- 花束大小筛选 -->
        <div class="btn-group">
          <button type="button" class="btn btn-outline-primary dropdown-toggle" data-bs-toggle="dropdown">
            {{ selectedSize ? getSizeLabel(selectedSize) : '所有大小' }}
          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#" @click.prevent="filterBySize(null)">所有大小</a></li>
            <li v-if="sizes.length === 0"><span class="dropdown-item-text">加载中...</span></li>
            <li v-for="size in sizes" :key="size.value">
              <a class="dropdown-item" href="#" @click.prevent="filterBySize(size.value)">{{ size.label }}</a>
            </li>
          </ul>
        </div>
      </div>

      <!-- 搜索框 -->
      <div class="w-50">
        <div class="input-group">
          <input type="text" v-model="searchQuery" @keyup.enter="triggerSearch" class="form-control" placeholder="搜索花束名称...">
          <button class="btn btn-primary" type="button" @click="triggerSearch">搜索</button>
          <button class="btn btn-outline-secondary" type="button" @click="clearSearch">清除</button>
        </div>
      </div>
    </div>

    <!-- 花束列表 -->
    <div class="row">
      <div v-for="flower in filteredFlowers" :key="flower.id" class="col-md-4 mb-4">
        <div class="card h-100 card-hover">
          <img :src="flower.image || 'https://via.placeholder.com/300x200'" class="card-img-top" :alt="flower.name">
          <div class="card-body">
            <h5 class="card-title">{{ flower.name }}</h5>
            <div class="mb-2">
              <span class="badge bg-primary me-1">{{ getBouquetTypeLabel(flower.bouquet_type) }}</span>
              <span class="badge bg-warning text-dark me-1">{{ getSizeLabel(flower.size) }}</span>
              <span class="badge bg-success">{{ flower.origin }}</span>
            </div>
            <p class="card-text text-muted">{{ flower.flower_language }}</p>
            <p class="card-text"><small class="text-muted">{{ flower.usage }}</small></p>
          </div>
          <div class="card-footer d-flex justify-content-between align-items-center bg-transparent border-top-0">
            <span class="fw-bold text-danger fs-5">¥{{ flower.price }}</span>
            <button 
              class="btn btn-outline-primary"
              data-bs-toggle="modal" 
              data-bs-target="#bookingModal"
              @click="openBookingModal(flower)"
              :disabled="!flower.is_available_for_booking"
            >
              {{ flower.is_available_for_booking ? '立即预订' : '暂不可订' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 预订模态框 -->
    <div class="modal fade" id="bookingModal" tabindex="-1" ref="bookingModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">预订花束 - {{ selectedFlower?.name }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitBooking">
              <div class="row">
                <!-- 左侧：花束信息 -->
                <div class="col-md-6">
                  <img :src="selectedFlower?.image || 'https://via.placeholder.com/300x200'" 
                       class="img-fluid rounded mb-3" :alt="selectedFlower?.name">
                  <h6>花束详情</h6>
                  <p><strong>类型：</strong>{{ getBouquetTypeLabel(selectedFlower?.bouquet_type) }}</p>
                  <p><strong>大小：</strong>{{ getSizeLabel(selectedFlower?.size) }}</p>
                  <p><strong>价格：</strong><span class="text-danger fw-bold">¥{{ selectedFlower?.price }}</span></p>
                  <p><strong>花语：</strong>{{ selectedFlower?.flower_language }}</p>
                </div>
                
                <!-- 右侧：预订信息 -->
                <div class="col-md-6">
                  <h6>预订信息</h6>
                  
                  <div class="mb-3">
                    <label class="form-label">数量</label>
                    <input type="number" v-model="bookingForm.quantity" class="form-control" min="1" required>
                  </div>
                  
                  <div class="mb-3">
                    <label class="form-label">预订日期</label>
                    <input type="datetime-local" v-model="bookingForm.booking_date" class="form-control" required>
                  </div>
                  
                  <div class="mb-3">
                    <label class="form-label">配送日期</label>
                    <input type="datetime-local" v-model="bookingForm.delivery_date" class="form-control" required>
                  </div>
                  
                  <div class="mb-3">
                    <label class="form-label">收件人姓名</label>
                    <input type="text" v-model="bookingForm.recipient_name" class="form-control" required>
                  </div>
                  
                  <div class="mb-3">
                    <label class="form-label">收件人电话</label>
                    <input type="tel" v-model="bookingForm.recipient_phone" class="form-control" required>
                  </div>
                  
                  <div class="mb-3">
                    <label class="form-label">收货地址</label>
                    <textarea v-model="bookingForm.shipping_address" class="form-control" rows="3" required></textarea>
                  </div>
                  
                  <div class="mb-3">
                    <label class="form-label">特殊要求</label>
                    <textarea v-model="bookingForm.special_requirements" class="form-control" rows="2" placeholder="如有特殊要求请在此说明"></textarea>
                  </div>
                </div>
              </div>
              
              <div class="row mt-3">
                <div class="col-12">
                  <div class="alert alert-info">
                    <strong>总价：¥{{ totalPrice }}</strong>
                    <br><small>预订成功后，我们将在配送日期准时为您送达。</small>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" ref="cancelButton">取消</button>
            <button type="button" class="btn btn-primary" @click="submitBooking" :disabled="isSubmitting">
              {{ isSubmitting ? '提交中...' : '确认预订' }}
            </button>
          </div>
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
      allFlowers: [],
      searchQuery: '',
      activeSearchTerm: '',
      selectedBouquetType: null,
      selectedSize: null,
      selectedFlower: null,
      isSubmitting: false,
      bookingModal: null,
      bookingForm: {
        quantity: 1,
        booking_date: '',
        delivery_date: '',
        recipient_name: '',
        recipient_phone: '',
        shipping_address: '',
        special_requirements: ''
      },
      bouquetTypes: [
        { value: 'single', label: '单支花' },
        { value: 'small', label: '小花束' },
        { value: 'medium', label: '中花束' },
        { value: 'large', label: '大花束' },
        { value: 'luxury', label: '豪华花束' }
      ],
      sizes: [
        { value: 'mini', label: '迷你型' },
        { value: 'small', label: '小型' },
        { value: 'medium', label: '中型' },
        { value: 'large', label: '大型' },
        { value: 'extra_large', label: '特大型' }
      ]
    };
  },
  computed: {
    filteredFlowers() {
      let flowers = this.allFlowers.filter(f => f.is_available_for_booking);
      
      if (this.activeSearchTerm) {
        const query = this.activeSearchTerm.toLowerCase();
        flowers = flowers.filter(f => 
          f.name && f.name.toLowerCase().includes(query)
        );
      }
      
      if (this.selectedBouquetType) {
        flowers = flowers.filter(f => f.bouquet_type === this.selectedBouquetType);
      }
      
      if (this.selectedSize) {
        flowers = flowers.filter(f => f.size === this.selectedSize);
      }
      
      return flowers;
    },
    totalPrice() {
      if (!this.selectedFlower || !this.bookingForm.quantity) return 0;
      return (parseFloat(this.selectedFlower.price) * parseInt(this.bookingForm.quantity)).toFixed(2);
    }
  },
  async created() {
    await this.fetchFlowers();
    this.setDefaultDates();
    // 如果URL中有flowerId参数，预选择该花卉
    const flowerId = this.$route.query.flowerId;
    if (flowerId) {
      this.preSelectFlower(parseInt(flowerId));
    }
  },
  
  methods: {
    async fetchFlowers() {
      try {
        const response = await api.getFlowers();
        this.allFlowers = response.data;
      } catch (error) {
        console.error('无法加载花卉列表:', error);
      }
    },
    filterByBouquetType(type) {
      this.selectedBouquetType = type;
    },
    filterBySize(size) {
      this.selectedSize = size;
    },
    triggerSearch() {
      this.activeSearchTerm = this.searchQuery;
    },
    clearSearch() {
      this.searchQuery = '';
      this.activeSearchTerm = '';
    },
    getBouquetTypeLabel(type) {
      const found = this.bouquetTypes.find(t => t.value === type);
      return found ? found.label : type;
    },
    getSizeLabel(size) {
      const found = this.sizes.find(s => s.value === size);
      return found ? found.label : size;
    },
    setDefaultDates() {
      const now = new Date();
      const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000);
      
      // 设置默认预订时间为当前时间
      this.bookingForm.booking_date = now.toISOString().slice(0, 16);
      // 设置默认配送时间为明天
      this.bookingForm.delivery_date = tomorrow.toISOString().slice(0, 16);
    },
    openBookingModal(flower) {
      this.selectedFlower = flower;
      this.resetBookingForm();
    },
    resetBookingForm() {
      this.bookingForm = {
        quantity: 1,
        booking_date: this.bookingForm.booking_date,
        delivery_date: this.bookingForm.delivery_date,
        recipient_name: '',
        recipient_phone: '',
        shipping_address: '',
        special_requirements: ''
      };
    },
    // 预选择花卉
    preSelectFlower(flowerId) {
      const flower = this.allFlowers.find(f => f.id === flowerId);
      if (flower) {
        this.selectedFlower = flower;
        this.openBookingModal(flower);
      }
    },
    async submitBooking() {
      if (this.isSubmitting) return;
      
      this.isSubmitting = true;
      try {
        const orderData = {
          order_type: 'booking',
          booking_date: this.bookingForm.booking_date,
          delivery_date: this.bookingForm.delivery_date,
          recipient_name: this.bookingForm.recipient_name,
          recipient_phone: this.bookingForm.recipient_phone,
          shipping_address: this.bookingForm.shipping_address,
          special_requirements: this.bookingForm.special_requirements,
          items: [{
            flower_id: this.selectedFlower.id,
            quantity: parseInt(this.bookingForm.quantity),
            price: this.selectedFlower.price
          }]
        };
        
        await api.createOrder(orderData);
        alert('预订成功！我们将按时为您配送。');
        if (this.$refs.cancelButton) {
          this.$refs.cancelButton.click();
        }
        this.$router.push('/order-history');
      } catch (error) {
        console.error('预订失败:', error);
        alert('预订失败，请重试。');
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
.jumbotron-with-bg {
  background-image: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.55)), url('../assets/油菜田.jpg');
  background-size: cover;
  background-position: center;
}

.controls-bar {
  background-color: rgba(228, 219, 234, 0.65);
}

.card {
  background-color: rgba(242, 237, 244, 0.8);
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}

.card-hover {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-hover:hover {
  transform: scale(1.05);
  box-shadow: 0 1rem 3rem rgba(0,0,0,.175)!important;
}

.btn-primary {
  background-color: #9b59b6;
  border-color: #9b59b6;
}

.btn-outline-primary {
  --bs-btn-color: #9b59b6;
  --bs-btn-border-color: #9b59b6;
  --bs-btn-hover-color: #fff;
  --bs-btn-hover-bg: #9b59b6;
  --bs-btn-hover-border-color: #9b59b6;
  --bs-btn-active-color: #fff;
  --bs-btn-active-bg: #9b59b6;
  --bs-btn-active-border-color: #9b59b6;
}

.badge.bg-primary {
  background-color: #9b59b6 !important;
}
</style>