<template>
  <div>
    <!-- 英雄区：占据屏幕大部分的欢迎区域 -->
    <div class="hero-section text-center text-white d-flex justify-content-center align-items-center">
      <div class="container">
        <h1 class="display-4 fw-bold">用自然之美，点亮您的生活瞬间</h1>
        <p class="lead my-3">从浪漫的婚礼到温馨的家居，我们为您提供最鲜活、最动人的花卉选择。</p>
        <router-link to="/market" class="btn btn-lg btn-light">探索花卉市场</router-link>
      </div>
    </div>

    <!-- 特色功能区 -->
    <div class="container my-5">
      <!-- 特色一：AI专家 -->
      <div class="row feature-item align-items-center styled-section">
        <div class="col-md-7">
          <h2 class="feature-heading">您的私人花卉顾问</h2>
          <p class="lead">遇到养护难题？只需拍照或提问，我们的AI专家就能为您提供专业的养护建议和病虫害解决方案。无论是叶子发黄还是花期短暂，我们都能帮您找到答案。</p>
          <router-link to="/ask-expert" class="btn btn-outline-primary">立即咨询</router-link>
        </div>
        <div class="col-md-5">
          <img src="../assets/花卉2.jpg" class="img-fluid rounded shadow-lg" alt="AI Expert Feature">
        </div>
      </div>

      <!-- 特色二：社区 -->
      <div class="row feature-item align-items-center styled-section">
        <div class="col-md-5">
          <img src="../assets/花卉1.jpg" class="img-fluid rounded shadow-lg" alt="Community Feature">
        </div>
        <div class="col-md-7 text-md-end">
          <h2 class="feature-heading">分享与交流的家园</h2>
          <p class="lead">加入我们的社区，与成千上万的花卉爱好者分享您的养护心得、晒出您的美丽花园。在这里，每一次分享都可能收获赞美，每一次提问都能得到热心回应。</p>
          <router-link to="/community" class="btn btn-outline-success">进入社区</router-link>
        </div>
      </div>

      <!-- 特色三：品质保证 -->
      <div class="row feature-item align-items-center styled-section">
        <div class="col-md-7">
          <h2 class="feature-heading">从田间到花瓶的匠心</h2>
          <p class="lead">我们与顶尖的种植者合作，确保每一束花都拥有最饱满的色泽和最持久的生命力。从玫瑰的浪漫到向日葵的阳光，我们为您精选全球的优质花卉。</p>
        </div>
        <div class="col-md-5">
           <div class="text-center">
              <i class="bi bi-truck display-1 text-primary"></i>
              <i class="bi bi-award display-1 text-warning"></i>
              <i class="bi bi-shield-check display-1 text-success"></i>
              <p class="mt-2">快速配送 · 品质保证 · 安全支付</p>
           </div>
        </div>
      </div>
    </div>

    <!-- 行动号召区 -->
    <div class="cta-section text-center py-5">
      <div class="container">
        <h2>准备好开启您的芬芳之旅了吗？</h2>
        <p class="lead my-3">立即进入我们的花卉市场，发现那些能触动您心弦的美丽花卉。</p>
        <router-link to="/market" class="btn btn-primary btn-lg">立即选购</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  // 组件名称
  name: 'Home',
};
</script>

<style scoped>
/* 英雄区样式 */
.hero-section {
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('../assets/花卉1.jpg');
  height: 60vh;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}

/* 特色项间距 */
.feature-item {
  margin-bottom: 3rem;
}

/* 特色区块统一样式 */
.styled-section {
  background-color: rgba(228, 219, 234, 0.55); /* 淡紫色半透明背景 */
  padding: 3rem;
  border-radius: 15px;
  box-shadow: 0 8px 15px rgba(0,0,0,0.05);
}

/* 特色区块图片样式 */
.feature-item img {
  max-height: 400px;
  object-fit: cover;
}

/* 特色区块标题样式 */
.feature-heading {
  color: #8e44ad; /* 深紫色 */
  font-weight: bold;
  margin-bottom: 1rem;
}

/* 行动号召区样式 */
.cta-section {
  background-color: rgba(228, 219, 234, 0.43);
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
}

.cta-section h2 {
  font-weight: bold;
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

/* 主要文本颜色 */
.text-primary {
    color: #9b59b6 !important;
}
</style>
