<template>
  <div class="post-detail-container">
    <div class="container py-5">
      <div v-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div v-else-if="post" class="row justify-content-center">
        <div class="col-lg-8">
          <!-- Post Content Card -->
          <div class="card shadow-sm custom-card mb-4">
            <div class="card-body p-4">
              <h2 class="card-title mb-3">{{ post.title }}</h2>
              <p class="card-subtitle mb-3 text-muted">
                <span class="me-3"><i class="bi bi-person-circle"></i> {{ post.author.username }}</span>
                <span><i class="bi bi-clock"></i> {{ new Date(post.created_at).toLocaleString() }}</span>
              </p>
              <hr>
              <div class="post-content py-3" v-html="post.content"></div>
            </div>
            <div class="card-footer bg-transparent d-flex justify-content-between align-items-center">
              <router-link to="/community" class="btn btn-outline-secondary">返回社区</router-link>
              <button class="btn btn-lg" :class="post.is_liked ? 'btn-primary' : 'btn-outline-primary'" @click="toggleLike">
                <i :class="post.is_liked ? 'bi bi-hand-thumbs-up-fill' : 'bi bi-hand-thumbs-up'"></i>
                {{ post.is_liked ? '已赞' : '点赞' }} ({{ post.likes_count }})
              </button>
            </div>
          </div>

          <!-- Comments Section -->
          <div class="card shadow-sm custom-card">
            <div class="card-body p-4">
              <h4 class="mb-4">评论 ({{ post.comments.length }})</h4>
              
              <!-- Comments List -->
              <div v-if="post.comments.length > 0" class="comments-list mb-4">
                <div v-for="comment in post.comments" :key="comment.id" class="comment-item mb-3">
                  <p class="mb-1">{{ comment.content }}</p>
                  <small class="text-muted">
                    <i class="bi bi-person"></i> {{ comment.author.username }} at {{ new Date(comment.created_at).toLocaleString() }}
                  </small>
                </div>
              </div>
              <p v-else class="text-muted text-center">暂无评论，快来抢沙发吧！</p>

              <!-- New Comment Form -->
              <form @submit.prevent="submitComment">
                <div class="mb-3">
                  <textarea v-model="newComment" class="form-control" rows="3" placeholder="写下你的评论..." required></textarea>
                </div>
                <div class="d-grid">
                  <button type="submit" class="btn btn-primary">提交评论</button>
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
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../services/api';

export default {
  setup() {
    const route = useRoute();
    const post = ref(null);
    const newComment = ref('');
    const isLoading = ref(true);

    const fetchPost = async () => {
      try {
        const response = await api.getPost(route.params.id);
        post.value = response.data;
      } catch (error) {
        console.error("获取帖子详情失败:", error);
      } finally {
        isLoading.value = false;
      }
    };

    const toggleLike = async () => {
      try {
        await api.likePost(post.value.id);
        // Optimistically update UI
        post.value.is_liked = !post.value.is_liked;
        post.value.likes_count += post.value.is_liked ? 1 : -1;
      } catch (error) {
        console.error("点赞失败:", error);
      } 
    };

    const submitComment = async () => {
      try {
        const response = await api.addComment(post.value.id, { content: newComment.value });
        post.value.comments.push(response.data);
        newComment.value = '';
      } catch (error) {
        console.error("提交评论失败:", error);
      }
    };

    onMounted(fetchPost);

    return { post, newComment, isLoading, toggleLike, submitComment };
  },
};
</script>

<style scoped>
.post-detail-container {
  background-image: linear-gradient(rgba(235, 227, 239, 0.85), rgba(228, 219, 234, 0.85)), url('../assets/干花系.jpg');
  background-size: cover;
  background-attachment: fixed;
  min-height: 100vh;
}

.custom-card {
  background-color: rgba(242, 237, 244, 0.9);
  border: 1px solid rgba(0,0,0,0.08);
  backdrop-filter: blur(5px);
}

.post-content {
  white-space: pre-wrap; /* Preserves whitespace and line breaks */
  font-size: 1.1rem;
  line-height: 1.7;
}

.comments-list {
  max-height: 400px;
  overflow-y: auto;
}

.comment-item {
  border-bottom: 1px solid #ddd;
  padding-bottom: 1rem;
}
.comment-item:last-child {
  border-bottom: none;
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
