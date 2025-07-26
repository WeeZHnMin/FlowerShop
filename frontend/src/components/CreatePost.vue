<template>
  <!-- 创建新帖子页面的主容器 -->
  <div class="create-post-container">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <!-- 使用卡片样式来包裹表单 -->
          <div class="card shadow-lg custom-card">
            <div class="card-body p-4 p-md-5">
              <!-- 头部：标题和返回按钮 -->
              <div class="d-flex justify-content-between align-items-center mb-4">
                <h2 class="mb-0">发布新帖</h2>
                <router-link to="/community" class="btn btn-outline-secondary">返回社区</router-link>
              </div>
              <!-- 表单，提交时调用submitPost方法 -->
              <form @submit.prevent="submitPost">
                <!-- 标题输入字段 -->
                <div class="mb-3">
                  <label for="title" class="form-label">标题</label>
                  <input type="text" id="title" v-model="title" class="form-control form-control-lg" required>
                </div>
                <!-- 内容输入字段 -->
                <div class="mb-3">
                  <label for="content" class="form-label">内容</label>
                  <textarea id="content" v-model="content" class="form-control form-control-lg" rows="10" required></textarea>
                </div>
                <!-- 提交按钮 -->
                <div class="d-grid">
                  <button type="submit" class="btn btn-primary btn-lg">发布</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// 导入Vue的Composition API函数、路由和API服务
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

export default {
  // 使用Vue 3 Composition API
  setup() {
    const router = useRouter(); // 获取路由实例
    // 定义响应式数据来绑定表单输入
    const title = ref('');
    const content = ref('');

    // 异步方法：提交新帖子
    const submitPost = async () => {
      try {
        // 调用API创建帖子
        await api.createPost({ title: title.value, content: content.value });
        // 成功后跳转回社区页面
        router.push('/community');
      } catch (error) {
        console.error("发布帖子失败:", error);
      }
    };

    // 返回需要在模板中使用的数据和方法
    return { title, content, submitPost };
  },
};
</script>

<style scoped>
/* 页面主容器样式 */
.create-post-container {
  background-image: linear-gradient(rgba(235, 227, 239, 0.85), rgba(228, 219, 234, 0.85)), url('../assets/干花系.jpg');
  background-size: cover;
  background-attachment: fixed;
  min-height: 100vh;
}

/* 自定义卡片样式 */
.custom-card {
  background-color: rgba(242, 237, 244, 0.9); /* 淡紫色半透明背景 */
  border: 1px solid rgba(0,0,0,0.08);
  backdrop-filter: blur(5px);
}

/* 增大表单控件的字体大小 */
.form-control-lg {
  font-size: 1rem;
}

/* 主要按钮样式 */
.btn-primary {
    background-color: #9b59b6;
    border-color: #9b59b6;
}
</style>
