<template>
  <!-- 摄像头模态框的背景遮罩 -->
  <div class="camera-modal-backdrop">
    <!-- 模态框内容区域 -->
    <div class="camera-modal-content shadow-lg">
      <!-- 头部：包含标题和关闭按钮 -->
      <div class="camera-header">
        <h4 class_="modal-title">摄像头拍照</h4>
        <button type="button" class="btn-close" @click="closeCamera" aria-label="Close"></button>
      </div>

      <!-- 主体：显示摄像头视频流或拍摄的照片预览 -->
      <div class="camera-body">
        <!-- 视频容器，当没有拍摄照片时显示 -->
        <div v-if="!imageCaptureUrl" class="video-container">
          <video ref="videoPlayer" class="camera-video" autoplay playsinline></video>
        </div>
        <!-- 预览容器，当已拍摄照片时显示 -->
        <div v-if="imageCaptureUrl" class="preview-container">
          <img :src="imageCaptureUrl" class="camera-preview" alt="Photo preview" />
        </div>
      </div>

      <!-- 底部：包含操作按钮 -->
      <div class="camera-footer">
        <!-- “拍照”按钮，仅在视频模式下显示 -->
        <button v-if="!imageCaptureUrl" class="btn btn-primary btn-lg" @click="captureImage">拍照</button>
        <!-- “重拍”按钮，仅在预览模式下显示 -->
        <button v-if="imageCaptureUrl" class="btn btn-outline-secondary" @click="retake">重拍</button>
        <!-- “使用照片”按钮，仅在预览模式下显示 -->
        <button v-if="imageCaptureUrl" class="btn btn-success" @click="usePhoto">使用照片</button>
        <!-- “取消”按钮，始终显示 -->
        <button type="button" class="btn btn-secondary" @click="closeCamera">取消</button>
      </div>
      <!-- 用于绘制和转换图像的Canvas元素，在页面上不可见 -->
      <canvas ref="canvas" style="display: none;"></canvas>
    </div>
  </div>
</template>

<script>
export default {
  // 定义组件可以向父组件触发的自定义事件
  emits: ['photo-captured', 'close'],
  // 组件的响应式数据
  data() {
    return {
      stream: null, // 存储摄像头媒体流对象
      imageCaptureUrl: null, // 存储拍摄照片的Data URL，用于预览
    };
  },
  // Vue生命周期钩子：组件挂载后调用
  mounted() {
    this.startCamera(); // 启动摄像头
  },
  // Vue生命周期钩子：组件卸载前调用
  beforeUnmount() {
    this.stopStream(); // 停止摄像头数据流，释放资源
  },
  // 组件方法
  methods: {
    // 异步方法：启动摄像头
    async startCamera() {
      try {
        // 检查浏览器是否支持摄像头API
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
          alert('您的浏览器不支持摄像头功能。');
          this.closeCamera();
          return;
        }
        // 请求访问摄像头视频
        this.stream = await navigator.mediaDevices.getUserMedia({ video: true });
        // 将视频流附加到video元素上进行播放
        this.$refs.videoPlayer.srcObject = this.stream;
      } catch (error) {
        console.error("Error accessing camera:", error);
        alert('无法访问摄像头。请确保您已授权，并且没有其他应用正在使用摄像头。');
        this.closeCamera();
      }
    },
    // 拍摄照片
    captureImage() {
      const video = this.$refs.videoPlayer; // 获取video元素
      const canvas = this.$refs.canvas; // 获取canvas元素
      // 设置canvas尺寸与视频流尺寸一致
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      // 在canvas上绘制当前视频帧
      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      // 将canvas内容转换为JPEG格式的Data URL
      this.imageCaptureUrl = canvas.toDataURL('image/jpeg');
      // 停止视频流
      this.stopStream();
    },
    // 重新拍摄
    retake() {
      this.imageCaptureUrl = null; // 清除已拍摄的照片
      this.startCamera(); // 重新启动摄像头
    },
    // 使用拍摄的照片
    usePhoto() {
      // 将canvas内容转换为Blob对象
      this.$refs.canvas.toBlob(blob => {
        // 将Blob对象转换为File对象
        const file = new File([blob], "camera-photo.jpg", { type: "image/jpeg" });
        // 触发'photo-captured'事件，并将文件作为参数传递给父组件
        this.$emit('photo-captured', file);
      }, 'image/jpeg');
    },
    // 停止视频流
    stopStream() {
      if (this.stream) {
        // 遍历并停止所有轨道（视频、音频）
        this.stream.getTracks().forEach(track => track.stop());
        this.stream = null; // 清空stream对象
      }
    },
    // 关闭摄像头模态框
    closeCamera() {
      this.stopStream(); // 确保摄像头已关闭
      this.$emit('close'); // 触发'close'事件通知父组件关闭模态框
    },
  },
};
</script>

<style scoped>
/* 模态框背景遮罩 */
.camera-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
  transition: opacity 0.3s ease;
}

/* 模态框内容 */
.camera-modal-content {
  background-color: #f4eff6; /* 淡紫色背景 */
  border-radius: 12px;
  padding: 1.5rem;
  max-width: 640px;
  width: 95%;
  border: 1px solid rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
}

/* 模态框头部 */
.camera-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid #d5bcde; /* 紫色系边框 */
}

.modal-title {
  font-weight: 500;
}

/* 模态框主体 */
.camera-body {
  margin-bottom: 1rem;
}

/* 视频和预览容器，用于保持宽高比 */
.video-container, .preview-container {
  background-color: #000;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  width: 100%;
  padding-top: 75%; /* 4:3 宽高比 */
}

/* 视频和预览图像的样式 */
.camera-video, .camera-preview {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持图像比例，覆盖整个容器 */
}

/* 模态框底部 */
.camera-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem; /* 按钮间距 */
  padding-top: 1rem;
  border-top: 1px solid #d5bcde; /* 紫色系边框 */
}

/* 主要按钮样式 */
.btn-primary {
    background-color: #9b59b6;
    border-color: #9b59b6;
}
</style>
