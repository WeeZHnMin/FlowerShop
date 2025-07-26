<template>
  <div class="product-management-container">
    <!-- Jumbotron Header -->
    <div class="p-5 mb-4 rounded-3 jumbotron-with-bg text-white">
      <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">商品管理</h1>
        <p class="col-md-8 fs-4">在这里添加、编辑或删除您的花卉商品。</p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container">
      <div class="card shadow-sm custom-card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h4 class="mb-0">花卉列表</h4>
          <button class="btn btn-primary" @click="openModal()">
            <i class="bi bi-plus-circle"></i> 添加花卉
          </button>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead class="table-light">
                <tr>
                  <th>图片</th>
                  <th>名称</th>
                  <th>用途</th>
                  <th>季节</th>
                  <th>价格</th>
                  <th>库存</th>
                  <th class="text-center">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="flower in flowers" :key="flower.id">
                  <td><img :src="flower.image || 'https://via.placeholder.com/100x75'" class="img-thumbnail" style="width: 100px;"></td>
                  <td>{{ flower.name }}</td>
                  <td>{{ flower.usage }}</td>
                  <td>{{ flower.season }}</td>
                  <td class="fw-bold">¥{{ flower.price }}</td>
                  <td>{{ flower.stock }}</td>
                  <td class="text-center">
                    <button class="btn btn-outline-primary btn-sm me-2" @click="openModal(flower)">编辑</button>
                    <button class="btn btn-outline-danger btn-sm" @click="handleDeleteFlower(flower.id)">删除</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Flower Modal -->
    <div class="modal fade" :class="{ 'show d-block': showModal }" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingFlower ? '编辑花卉' : '添加花卉' }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleSaveFlower">
              <div class="row">
                <div class="col-md-6">
                  <div class="mb-3">
                    <label class="form-label">名称</label>
                    <input type="text" v-model="form.name" class="form-control" required>
                  </div>
                  <div class="mb-3">
                    <label class="form-label">价格</label>
                    <input type="number" step="0.01" v-model="form.price" class="form-control" required>
                  </div>
                  <div class="mb-3">
                    <label class="form-label">库存</label>
                    <input type="number" v-model="form.stock" class="form-control" required>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="mb-3">
                    <label class="form-label">用途</label>
                    <input type="text" v-model="form.usage" class="form-control">
                  </div>
                  <div class="mb-3">
                    <label class="form-label">季节</label>
                    <input type="text" v-model="form.season" class="form-control">
                  </div>
                  <div class="mb-3">
                    <label class="form-label">产地</label>
                    <input type="text" v-model="form.origin" class="form-control">
                  </div>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">花语</label>
                <input type="text" v-model="form.flower_language" class="form-control">
              </div>
              <div class="mb-3">
                <label class="form-label">养护要求</label>
                <textarea v-model="form.care_requirements" class="form-control"></textarea>
              </div>
              <div class="mb-3">
                <label for="flowerImage" class="form-label">花卉图片</label>
                <input class="form-control" type="file" id="flowerImage" @change="handleImageUpload">
                <div v-if="form.image_url" class="mt-2">
                  <img :src="form.image_url" class="img-thumbnail" style="max-width: 150px;" alt="Image preview"/>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeModal">取消</button>
                <button type="submit" class="btn btn-primary">保存</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showModal" class="modal-backdrop fade show"></div>

  </div>
</template>

<script>
import api from '../services/api';

export default {
  data() {
    return {
      flowers: [],
      showModal: false,
      editingFlower: null,
      form: {
        name: '',
        usage: '',
        season: '',
        price: 0,
        stock: 0,
        origin: '',
        flower_language: '',
        care_requirements: '',
        image: null,
        image_url: null
      }
    };
  },
  created() {
    this.fetchFlowers();
  },
  methods: {
    async fetchFlowers() {
      try {
        const response = await api.getFlowers();
        this.flowers = response.data;
      } catch (error) {
        console.error("无法加载花卉列表:", error);
      }
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.form.image = file;
        this.form.image_url = URL.createObjectURL(file);
      }
    },
    openModal(flower = null) {
      if (flower) {
        this.editingFlower = flower;
        this.form = { 
          ...flower, 
          image: null,
          image_url: flower.image
        };
      } else {
        this.editingFlower = null;
        this.form = { name: '', usage: '', season: '', price: 0, stock: 0, origin: '', flower_language: '', care_requirements: '', image: null, image_url: null };
      }
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    async handleSaveFlower() {
      const formData = new FormData();
      for (const key in this.form) {
        if (key === 'image' && this.form.image) {
          formData.append('image', this.form.image);
        } else if (key !== 'image' && key !== 'image_url' && this.form[key] !== null) {
          formData.append(key, this.form[key]);
        }
      }

      try {
        if (this.editingFlower) {
          await api.updateFlower(this.editingFlower.id, formData);
        } else {
          await api.addFlower(formData);
        } 
        this.fetchFlowers();
        this.closeModal();
      } catch (error) {
        console.error("保存花卉失败:", error.response ? error.response.data : error);
      }
    },
    async handleDeleteFlower(id) {
      if (confirm('您确定要删除这个花卉吗？')) {
        try {
          await api.deleteFlower(id);
          this.fetchFlowers();
        } catch (error) {
          console.error("删除花卉失败:", error);
        }
      }
    }
  }
};
</script>

<style scoped>
.product-management-container {
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

.table-hover tbody tr:hover {
  background-color: #e8ddee;
}

.modal-content {
  border-radius: 0.5rem;
  background-color: #f4eff6;
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
</style>
