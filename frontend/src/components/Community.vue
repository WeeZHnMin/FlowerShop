<template>
  <!-- 社区页面主容器 -->
  <div class="community-container">
    <!-- 页面顶部Jumbotron -->
    <div class="p-5 mb-4 rounded-3 jumbotron-with-bg text-white">
      <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">加入我们的花卉社区</h1>
        <p class="col-md-8 fs-4">分享您的花卉故事，交流养护心得，发现更多关于花的美好。</p>
        <router-link to="/create-post" class="btn btn-primary btn-lg mt-3">发布新帖</router-link>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="container">
      <!-- 加载状态提示 -->
      <div v-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <!-- 无帖子时的提示信息 -->
      <div v-else-if="posts.length === 0" class="text-center py-5">
        <div class="alert alert-light not-found-alert">
          <h3>还没有人发帖</h3>
          <p class="lead">快来成为第一个分享者吧！</p>
        </div>
      </div>
      <!-- 帖子列表 -->
      <div v-else class="row">
        <div v-for="post in posts" :key="post.id" class="col-lg-12 mb-4">
          <div class="card h-100 card-hover custom-card">
            <div class="card-body">
              <h4 class="card-title">
                <!-- 帖子标题，点击可跳转到详情页 -->
                <router-link :to="{ name: 'PostDetail', params: { id: post.id } }" class="text-decoration-none text-dark stretched-link">{{ post.title }}</router-link>
              </h4>
              <!-- 帖子元数据：作者和发布时间 -->
              <p class="card-subtitle mb-2 text-muted">
                <span class="me-3"><i class="bi bi-person-circle"></i> {{ post.author.username }}</span>
                <span><i class="bi bi-clock"></i> {{ new Date(post.created_at).toLocaleString() }}</span>
              </p>
              <!-- 帖子统计：点赞和评论数 -->
              <div class="d-flex justify-content-end align-items-center mt-3">
                <span class="badge bg-primary rounded-pill me-3 fs-6"><i class="bi bi-hand-thumbs-up"></i> {{ post.likes_count }}</span>
                <span class="badge bg-secondary rounded-pill fs-6"><i class="bi bi-chat-dots"></i> {{ post.comments.length }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// 导入Vue的Composition API函数和自定义的API服务
import { ref, onMounted } from 'vue';
import api from '../services/api';

export default {
  // 使用Vue 3 Composition API
  setup() {
    // 定义响应式数据
    const posts = ref([]); // 存储帖子列表
    const isLoading = ref(true); // 加载状态标志

    // 异步方法：从后端获取帖子列表
    const fetchPosts = async () => {
      try {
        const response = await api.getPosts();
        posts.value = response.data; // 将获取到的数据赋值给posts
      } catch (error) {
        console.error("获取帖子列表失败:", error);
      } finally {
        isLoading.value = false; // 结束加载状态
      }
    };

    // 在组件挂载后调用fetchPosts方法
    onMounted(fetchPosts);

    // 返回需要在模板中使用的数据和方法
    return { posts, isLoading };
  },
};
</script>

<style scoped>
/* 页面主容器样式 */
.community-container {
  background-image: linear-gradient(rgba(235, 227, 239, 0.85), rgba(228, 219, 234, 0.85)), url('../assets/干花系.jpg');
  background-size: cover;
  background-attachment: fixed; /* 背景图固定，不随滚动条滚动 */
  padding-top: 1rem;
  padding-bottom: 3rem;
  min-height: 100vh;
}

/* Jumbotron背景图片 */
.jumbotron-with-bg {
  background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.6)), url('../assets/郁金香花田.jpg');
  background-size: cover;
  background-position: center;
}

/* 自定义卡片样式 */
.custom-card {
  background-color: rgba(242, 237, 244, 0.85); /* 淡紫色半透明背景 */
  border: 1px solid rgba(0,0,0,0.08);
  backdrop-filter: blur(5px); /* 模糊效果 */
}

/* 卡片悬停效果 */
.card-hover {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-hover:hover {
  transform: translateY(-5px); /* 向上移动 */
  box-shadow: 0 1rem 3rem rgba(0,0,0,.175)!important;
}

/* 卡片标题链接样式 */
.card-title a {
  color: #333;
}
.card-title a:hover {
  color: #9b59b6; /* 悬停时变为主题紫色 */
}

/* “未找到”提示框样式 */
.not-found-alert {
  background-color: rgba(242, 237, 244, 0.7);
  border: none;
  padding: 2rem;
}

/* 深度选择器，修改子组件或v-html中的按钮样式 */
:deep(.btn-primary) {
    background-color: #9b59b6;
    border-color: #9b59b6;
}

/* 深度选择器，修改子组件或v-html中的徽章样式 */
:deep(.badge.bg-primary) {
    background-color: #9b59b6 !important;
}
</style>
