<template>
  <!-- 花卉市场页面主容器 -->
  <div class="container">
    <!-- 页面顶部Jumbotron -->
    <div class="p-5 mb-4 rounded-3 jumbotron-with-bg text-white">
      <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">我们的花卉市场</h1>
        <p class="col-md-8 fs-4">探索由我们的店主精心培育和挑选的各式花卉。无论您是寻找一份特别的礼物，还是想为您的家增添一抹自然的色彩，都能在这里找到心仪之选。</p>
      </div>
    </div>

    <!-- 控制栏：包含搜索和筛选功能 -->
    <div class="d-flex justify-content-between align-items-center mb-4 p-3 rounded shadow-sm controls-bar">
      <!-- 搜索框 -->
      <div class="w-50">
        <div class="input-group">
          <input type="text" v-model="searchQuery" @keyup.enter="triggerSearch" class="form-control" placeholder="搜索花卉名称、用途、花语...">
          <button class="btn btn-primary" type="button" @click="triggerSearch">搜索</button>
          <button class="btn btn-outline-secondary" type="button" @click="clearSearch"><i class="bi bi-x-lg"></i>清除</button>
        </div>
      </div>
      <!-- 筛选按钮组 -->
      <div class="btn-group" role="group" aria-label="Filter buttons">
        <!-- 按用途筛选 -->
        <div class="btn-group">
          <button type="button" class="btn btn-outline-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
            {{ selectedUsage ? `用途: ${selectedUsage}` : '所有用途' }}
          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#" @click.prevent="filterBy('usage', null)">所有</a></li>
            <li v-if="uniqueUsages.length === 0"><span class="dropdown-item-text">加载中...</span></li>
            <li v-for="usage in uniqueUsages" :key="usage"><a class="dropdown-item" href="#" @click.prevent="filterBy('usage', usage)">{{ usage }}</a></li>
          </ul>
        </div>

        <!-- 按季节筛选 -->
        <div class="btn-group">
          <button type="button" class="btn btn-outline-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
            {{ selectedSeason ? `季节: ${selectedSeason}` : '所有季节' }}
          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#" @click.prevent="filterBy('season', null)">所有</a></li>
            <li v-if="uniqueSeasons.length === 0"><span class="dropdown-item-text">加载中...</span></li>
            <li v-for="season in uniqueSeasons" :key="season"><a class="dropdown-item" href="#" @click.prevent="filterBy('season', season)">{{ season }}</a></li>
          </ul>
        </div>

        <!-- 按产地筛选 -->
        <div class="btn-group">
          <button type="button" class="btn btn-outline-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
            {{ selectedOrigin ? `产地: ${selectedOrigin}` : '所有产地' }}
          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#" @click.prevent="filterBy('origin', null)">所有</a></li>
            <li v-if="uniqueOrigins.length === 0"><span class="dropdown-item-text">加载中...</span></li>
            <li v-for="origin in uniqueOrigins" :key="origin"><a class="dropdown-item" href="#" @click.prevent="filterBy('origin', origin)">{{ origin }}</a></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 花卉商品列表 -->
    <div class="row">
      <div v-for="flower in filteredFlowers" :key="flower.id" class="col-md-4 mb-4">
        <div class="card h-100 card-hover">
          <img :src="flower.image || 'https://via.placeholder.com/300x200'" class="card-img-top" :alt="flower.name">
          <div class="card-body">
            <h5 class="card-title">{{ flower.name }}</h5>
            <!-- 花卉标签 -->
            <p class="card-text">
              <span class="badge bg-primary me-1">{{ flower.usage }}</span>
              <span class="badge bg-warning text-dark me-1">{{ flower.season }}</span>
              <span class="badge bg-success">{{ flower.origin }}</span>
            </p>
            <!-- 花束信息 -->
            <p class="card-text" v-if="flower.bouquet_type || flower.size">
              <span class="badge bg-info text-dark me-1" v-if="flower.bouquet_type">{{ getBouquetTypeLabel(flower.bouquet_type) }}</span>
              <span class="badge bg-secondary me-1" v-if="flower.size">{{ getSizeLabel(flower.size) }}</span>
            </p>
            <p class="card-text text-muted">{{ flower.flower_language }}</p>
          </div>
          <!-- 卡片底部：价格和按钮 -->
          <div class="card-footer bg-transparent border-top-0">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="fw-bold text-danger fs-5">¥{{ flower.price }}</span>
            </div>
            <div class="d-flex gap-2">
              <button 
                class="btn btn-sm flex-fill"
                :class="justAddedId === flower.id ? 'btn-success' : 'btn-outline-success'"
                @click="handleAddToCart(flower)"
                :disabled="justAddedId === flower.id"
              >
                <span v-if="justAddedId === flower.id">已添加 ✓</span>
                <span v-else>加入购物车</span>
              </button>
              <button 
                class="btn btn-sm btn-outline-primary flex-fill"
                @click="goToBooking(flower)"
                v-if="flower.is_available_for_booking"
              >
                预订
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
// 导入API服务和Vuex store
import api from '../services/api';
import store from '../store';

export default {
  // 使用Options API
  data() {
    return {
      allFlowers: [], // 存储从后端获取的所有花卉数据
      searchQuery: '', // 绑定搜索输入框的实时输入
      activeSearchTerm: '', // 实际用于执行搜索的关键词
      selectedUsage: null, // 当前选中的用途筛选条件
      selectedSeason: null, // 当前选中的季节筛选条件
      selectedOrigin: null, // 当前选中的产地筛选条件
      justAddedId: null, // 用于跟踪刚刚被添加到购物车的商品ID，以实现按钮状态的临时变化
    };
  },
  // 计算属性
  computed: {
    // 从所有花卉数据中提取并去重“用途”
    uniqueUsages() {
      const usages = this.allFlowers.map(f => f.usage).filter(Boolean).flatMap(u => u.split(/[,\s，]+/));
      return [...new Set(usages)];
    },
    // 从所有花卉数据中提取并去重“季节”
    uniqueSeasons() {
      const seasons = this.allFlowers.map(f => f.season).filter(Boolean).flatMap(s => s.split(/[,\s，]+/));
      return [...new Set(seasons)];
    },
    // 从所有花卉数据中提取并去重“产地”
    uniqueOrigins() {
      const origins = this.allFlowers.map(f => f.origin).filter(Boolean).flatMap(o => o.split(/[,\s，]+/));
      return [...new Set(origins)];
    },
    // 根据搜索和筛选条件计算最终要显示的花卉列表
    filteredFlowers() {
      let flowers = this.allFlowers;

      // 应用搜索过滤
      if (this.activeSearchTerm) {
        const query = this.activeSearchTerm.toLowerCase();
        flowers = flowers.filter(f => 
          (f.name && f.name.toLowerCase().includes(query)) ||
          (f.usage && f.usage.toLowerCase().includes(query)) ||
          (f.flower_language && f.flower_language.toLowerCase().includes(query))
        );
      }

      // 应用分类筛选
      if (this.selectedUsage) {
        flowers = flowers.filter(f => f.usage && f.usage.includes(this.selectedUsage));
      }
      if (this.selectedSeason) {
        flowers = flowers.filter(f => f.season && f.season.includes(this.selectedSeason));
      }
      if (this.selectedOrigin) {
        flowers = flowers.filter(f => f.origin === this.selectedOrigin);
      }
      return flowers;
    }
  },
  // Vue生命周期钩子：组件创建后调用
  async created() {
    await this.fetchFlowers();
  },
  // 组件方法
  methods: {
    // 异步从后端获取所有花卉数据
    async fetchFlowers() {
      try {
        const response = await api.getFlowers();
        this.allFlowers = response.data;
      } catch (error) {
        console.error("无法加载花卉列表:", error);
      }
    },
    // 根据类型和值设置筛选条件
    filterBy(type, value) {
      if (type === 'usage') {
        this.selectedUsage = value;
      }
      if (type === 'season') {
        this.selectedSeason = value;
      }
      if (type === 'origin') {
        this.selectedOrigin = value;
      }
    },
    // 触发搜索，将实时输入的值赋给activeSearchTerm
    triggerSearch() {
      this.activeSearchTerm = this.searchQuery;
    },
    // 清除搜索条件
    clearSearch() {
      this.searchQuery = '';
      this.activeSearchTerm = '';
    },
    // 处理"加入购物车"逻辑
    handleAddToCart(flower) {
      store.addToCart(flower); // 调用store action
      this.justAddedId = flower.id; // 设置刚刚添加的ID
      // 2秒后重置按钮状态
      setTimeout(() => {
        this.justAddedId = null;
      }, 2000);
    },
    // 获取花束类型标签
    getBouquetTypeLabel(type) {
      const types = {
        'wedding': '婚礼花束',
        'birthday': '生日花束',
        'anniversary': '纪念日花束',
        'graduation': '毕业花束',
        'sympathy': '慰问花束',
        'congratulations': '祝贺花束',
        'romantic': '浪漫花束',
        'custom': '定制花束'
      };
      return types[type] || type;
    },
    // 获取尺寸标签
    getSizeLabel(size) {
      const sizes = {
        'small': '小束',
        'medium': '中束',
        'large': '大束',
        'extra_large': '特大束'
      };
      return sizes[size] || size;
    },
    // 跳转到预订页面
    goToBooking(flower) {
      this.$router.push({
        path: '/bouquet-booking',
        query: { flowerId: flower.id }
      });
    }
  }
};
</script>

<style scoped>
/* Jumbotron背景图片 */
.jumbotron-with-bg {
  background-image: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.55)), url('../assets/油菜田.jpg');
  background-size: cover;
  background-position: center;
}

/* 控制栏背景色 */
.controls-bar {
  background-color: rgba(228, 219, 234, 0.65);
}

/* 卡片背景色 */
.card {
  background-color: rgba(242, 237, 244, 0.8);
}

/* 卡片图片样式 */
.card-img-top {
    height: 200px;
    object-fit: cover;
}

/* 卡片悬停效果 */
.card-hover {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-hover:hover {
  transform: scale(1.05);
  box-shadow: 0 1rem 3rem rgba(0,0,0,.175)!important;
}

/* 主要按钮样式 */
.btn-primary {
    background-color: #9b59b6;
    border-color: #9b59b6;
}

/* 轮廓按钮样式 */
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

/* 主要徽章样式 */
.badge.bg-primary {
    background-color: #9b59b6 !important;
}
</style>