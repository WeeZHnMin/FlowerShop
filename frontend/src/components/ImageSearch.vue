<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-lg-10 col-xl-8">
        <div class="card shadow-lg custom-card">
          <div class="card-header">
            <h3 class="mb-0 text-center">AI 识花</h3>
            <p class="text-center text-muted mb-0">上传或拍摄一张花卉照片，让我来告诉你它是什么！</p>
          </div>
          <div class="card-body p-4">
            <!-- 上传方式选择 -->
            <div class="row g-3 text-center mb-4">
              <div class="col-md-6">
                <label class="btn btn-outline-primary btn-lg w-100 d-flex flex-column align-items-center justify-content-center h-100">
                  <i class="bi bi-image fs-1 mb-2"></i>
                  <span>从相册选择</span>
                  <input type="file" @change="onFileChange" accept="image/*" class="d-none">
                </label>
              </div>
              <div class="col-md-6">
                <button class="btn btn-outline-secondary btn-lg w-100 d-flex flex-column align-items-center justify-content-center h-100" @click="showCamera = true">
                  <i class="bi bi-camera fs-1 mb-2"></i>
                  <span>拍照上传</span>
                </button>
              </div>
            </div>

            <!-- 预览与识别 -->
            <div v-if="imagePreviewUrl" class="preview-section my-4 p-3 border rounded">
              <h5 class="text-center mb-3">图片预览</h5>
              <div class="text-center">
                <img :src="imagePreviewUrl" class="img-fluid rounded shadow-sm" style="max-height: 300px;" alt="Image Preview">
              </div>
              <div class="d-grid mt-3">
                <button class="btn btn-primary btn-lg" @click="recognizeImage" :disabled="!selectedFile || isLoading">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>
                  {{ isLoading ? ' 识别中...' : '开始识别' }}
                </button>
              </div>
            </div>

            <!-- 识别结果 -->
            <div v-if="result" class="mt-4 result-wrapper">
              <h4 class="text-center mb-3">识别结果: <span class="text-success fw-bold">{{ result.recognized_name }}</span></h4>
              <div v-if="result.matching_flowers && result.matching_flowers.length > 0">
                <h5 class="text-center mb-3">本店在售的“{{ result.recognized_name }}”：</h5>
                <div class="list-group result-list">
                  <a href="#" v-for="flower in result.matching_flowers" :key="flower.id" @click.prevent="goToFlower(flower.id)" class="list-group-item list-group-item-action d-flex align-items-center result-item">
                    <img v-if="flower.image" :src="backendUrl + flower.image" :alt="flower.name" class="me-3 rounded" style="width: 80px; height: 80px; object-fit: cover;">
                    <div class="flex-grow-1">
                      <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-1">{{ flower.name }}</h5>
                        <small class="text-muted">库存: {{ flower.stock }}</small>
                      </div>
                      <p class="mb-1 text-danger fw-bold">价格: ¥{{ flower.price }}</p>
                    </div>
                  </a>
                </div>
              </div>
              <div v-else class="alert alert-light text-center mt-3 not-found-alert">
                <p class="mb-0">抱歉，本店暂无“{{ result.recognized_name }}”或相关花卉在售。</p>
                <p class="mb-0"><small>您可以逛逛我们的<router-link to="/market">花卉市场</router-link>，发现更多美丽的花卉。</small></p>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
    <CameraCapture v-if="showCamera" @photo-captured="handlePhotoCaptured" @close="showCamera = false" />
  </div>
</template>

<script>
import api from '../services/api';
import CameraCapture from './CameraCapture.vue';
import { useRouter } from 'vue-router';

export default {
  components: {
    CameraCapture
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  data() {
    return {
      selectedFile: null,
      imagePreviewUrl: null,
      isLoading: false,
      result: null,
      showCamera: false,
      backendUrl: 'http://127.0.0.1:8000', // Re-add backend URL for images
    };
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.handleFile(file);
      }
    },
    handlePhotoCaptured(file) {
      this.showCamera = false;
      this.handleFile(file);
    },
    handleFile(file) {
      this.selectedFile = file;
      if (this.imagePreviewUrl) {
        URL.revokeObjectURL(this.imagePreviewUrl);
      }
      this.imagePreviewUrl = URL.createObjectURL(file);
      this.result = null;
    },
    async recognizeImage() {
      if (!this.selectedFile) return;
      this.isLoading = true;
      this.result = null;

      const formData = new FormData();
      formData.append('image', this.selectedFile);

      try {
        const response = await api.recognizeFlower(formData);
        this.result = response.data;
      } catch (error) {
        console.error("识别失败:", error);
        // 将错误信息发送到后端
        if (error.response) {
          api.logError({ 
            message: 'Flower recognition failed', 
            error: error.response.data 
          });
        } else {
          api.logError({ 
            message: 'Flower recognition failed', 
            error: error.message 
          });
        }
        alert("识别失败，请稍后再试。");
      } finally {
        this.isLoading = false;
      }
    },
    goToFlower(flowerId) {
      this.router.push({ name: 'Market' });
    }
  },
};
</script>

<style scoped>
/* 自定义卡片样式 */
.custom-card {
  background-color: #fff;
  border: none;
  border-radius: 15px;
  box-shadow: 0 8px 25px rgba(155, 89, 182, 0.1); /* 淡紫色辉光效果 */
}

/* 卡片头部样式 */
.card-header {
  background-color: #f4eff6;
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
  padding: 1.5rem;
  color: #8e44ad;
}

/* 预览区域样式 */
.preview-section {
  background-color: #f9f7fb;
  padding: 1rem;
  border-radius: 0.5rem;
}

/* 结果区域包装器样式 */
.result-wrapper {
  background-color: #f9f7fb;
  padding: 1.5rem;
  border-radius: 0.5rem;
}

/* 结果列表项样式 */
.result-list .list-group-item {
  background-color: #fff;
  border: 1px solid #f4eff6;
  margin-bottom: 0.5rem;
  transition: background-color 0.3s ease;
}

.result-list .list-group-item:hover {
  background-color: #f4eff6;
}

/* “未找到”提示框样式 */
.not-found-alert {
  background-color: #fdfbf7;
  border-left: 4px solid #ffc107;
}

/* 主要按钮样式 */
.btn-primary {
  background-color: #9b59b6;
  border-color: #9b59b6;
  transition: background-color 0.2s ease;
}

.btn-primary:hover {
  background-color: #8e44ad;
  border-color: #8e44ad;
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
</style>
