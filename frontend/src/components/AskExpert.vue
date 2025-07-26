<template>
  <!-- 主容器，包含整个页面的背景和布局 -->
  <div class="ask-expert-container">
    <!-- 页面顶部的巨幕，展示背景图片和标题 -->
    <div class="p-5 mb-4 rounded-3 jumbotron-with-bg text-white">
      <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">AI 专家 & 拍照识花</h1>
        <p class="col-md-8 fs-4">无论是养花难题，还是偶遇不识的花朵，我们都能为您解答。</p>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="container py-5">
      <!-- 标签页导航：用于在“AI问答”和“拍照识花”之间切换 -->
      <ul class="nav nav-pills justify-content-center mb-4">
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'qa' }" href="#" @click.prevent="activeTab = 'qa'">AI 专家问答</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'image' }" href="#" @click.prevent="activeTab = 'image'">拍照识花</a>
        </li>
      </ul>

      <!-- 标签页内容 -->
      <div class="tab-content">
        <!-- AI专家问答标签页 -->
        <div class="tab-pane fade" :class="{ 'show active': activeTab === 'qa' }">
          <div class="row justify-content-center">
            <div class="col-lg-8">
              <!-- 问答功能的卡片式布局 -->
              <div class="card shadow-sm custom-card">
                <div class="card-body p-4">
                  <h3 class="card-title text-center mb-4">AI 花卉养护与病害虫专家</h3>
                  <!-- 问题输入框和提问按钮 -->
                  <div class="input-group mb-3">
                    <input type="text" v-model="currentQuestion" class="form-control form-control-lg" placeholder="输入您的问题，例如：婚礼用什么花或叶子发黄该使用什么药品" @keyup.enter="askAIExpert">
                    <button class="btn btn-primary btn-lg" @click="askAIExpert" :disabled="isAsking">
                      <!-- 加载动画，仅在请求期间显示 -->
                      <span v-if="isAsking" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                      {{ isAsking ? ' 思考中...' : '提问' }}
                    </button>
                  </div>
                  <!-- 显示AI回答的区域 -->
                  <div v-if="lastAnswer" class="mt-4 p-3 rounded answer-box" v-html="formattedAnswer"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 拍照识花标签页 -->
        <div class="tab-pane fade" :class="{ 'show active': activeTab === 'image' }">
          <!-- 引入并显示ImageSearch组件 -->
          <ImageSearch />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// 导入必要的库和组件
import { marked } from 'marked'; // 用于将Markdown格式的文本转换为HTML
import store from '../store'; // 引入Vuex store，用于状态管理
import ImageSearch from './ImageSearch.vue'; // 引入拍照识花组件

export default {
  // 注册子组件
  components: {
    ImageSearch
  },
  // 组件的响应式数据
  data() {
    return {
      activeTab: 'qa', // 当前激活的标签页，默认为'qa' (问答)
      currentQuestion: '', // 用户在输入框中输入的问题
      isAsking: false, // 标志位，表示是否正在向AI请求答案
    };
  },
  // 计算属性，用于从store中获取数据或进行格式化
  computed: {
    // 从store获取上一个问题
    lastQuestion() {
      return store.state.lastQuestion;
    },
    // 从store获取最新的AI回答
    lastAnswer() {
      return store.state.lastAnswer;
    },
    // 将Markdown格式的AI回答转换为HTML，以便在页面上正确显示
    formattedAnswer() {
      return marked(this.lastAnswer);
    }
  },
  // 组件方法
  methods: {
    // 异步方法，用于向AI专家提问
    async askAIExpert() {
      // 如果输入为空或正在请求中，则不执行任何操作
      if (!this.currentQuestion.trim() || this.isAsking) return;
      
      const question = this.currentQuestion; // 保存当前问题
      store.setNewQuestion(question); // 将新问题存入store
      this.currentQuestion = ''; // 清空输入框
      this.isAsking = true; // 设置为请求中状态

      try {
        // 使用fetch API向后端发送POST请求
        const response = await fetch('http://127.0.0.1:8000/api/products/ask-qwen/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}` // 包含用户认证token
          },
          body: JSON.stringify({ question: question }) // 将问题数据转换为JSON字符串
        });

        // 如果响应失败，则抛出错误
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        // 处理流式响应
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        // 循环读取数据流
        while (true) {
          const { done, value } = await reader.read();
          if (done) break; // 如果数据流结束，则跳出循环
          
          const chunk = decoder.decode(value, { stream: true }); // 解码数据块
          const lines = chunk.split('\n'); // 按行分割
          for (const line of lines) {
            if (line.startsWith('data:')) { // 处理SSE (Server-Sent Events) 数据
              try {
                const json_data = JSON.parse(line.substring(5)); // 解析JSON数据
                if (json_data.error) {
                  store.setAnswer(`\n**后端错误:** ${json_data.error}`);
                  throw new Error(json_data.error);
                }
                if (json_data.choices && json_data.choices[0].delta.content) {
                  // 将增量内容追加到store的回答中
                  store.appendToAnswer(json_data.choices[0].delta.content);
                }
              } catch (e) { 
                // 忽略空的JSON解析错误
                if (!(e instanceof SyntaxError)) {
                  console.error("Error processing stream data:", e);
                }
              }
            }
          }
        }
      } catch (error) {
        // 捕获并处理请求过程中的任何错误
        if (!store.state.lastAnswer.includes("后端错误")) {
            store.setAnswer(`\n**出现错误:** ${error.message}`);
        }
        console.error("AI问答失败:", error);
      } finally {
        // 无论成功或失败，最终都将请求状态设置为false
        this.isAsking = false;
      }
    },
  }
};
</script>

<style scoped>
/* 容器样式 */
.ask-expert-container {
  background-color: #f9f7fb; /* 淡紫色背景 */
  min-height: 100vh;
}

/* 巨幕样式 */
.jumbotron-with-bg {
  background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.5)), url('../assets/花卉2.jpg');
  background-size: cover;
  background-position: center;
  border-radius: 0 !important; /* 移除圆角，使其充满宽度 */
}

/* 内容区域包装器，提供上下内边距 */
.content-wrapper {
  padding-top: 3rem;
  padding-bottom: 3rem;
}

/* 标签页导航按钮样式 */
.nav-pills .nav-link {
  color: #8e44ad; /* 深紫色文字 */
  background-color: #e5d9ea; /* 淡紫色背景 */
  margin: 0 10px;
  border-radius: 50px; /* 圆形胶囊按钮 */
  padding: 0.75rem 1.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

/* 激活状态的标签页按钮 */
.nav-pills .nav-link.active {
  color: #fff;
  background-color: #9b59b6; /* 主题紫色 */
  box-shadow: 0 4px 15px rgba(155, 89, 182, 0.4); /* 添加紫色阴影 */
}

/* 自定义卡片样式 */
.custom-card {
  background-color: #fff;
  border: none;
  border-radius: 15px;
  box-shadow: 0 8px 25px rgba(155, 89, 182, 0.1); /* 淡紫色辉光效果 */
}

/* 卡片头部样式 */
.card-header {
  background-color: #f4eff6; /* 更淡的紫色背景 */
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
  padding: 1.5rem;
  color: #8e44ad;
}

/* 输入框聚焦时的样式 */
.form-control:focus {
  border-color: #d5bcde;
  box-shadow: 0 0 0 0.25rem rgba(155, 89, 182, 0.25); /* 紫色光晕 */
}

/* AI回答框样式 */
.answer-box {
  background-color: #f9f7fb;
  border-left: 4px solid #9b59b6; /* 左侧紫色边框 */
}

/* 深度选择器，用于修改v-html渲染内容的样式 */
.answer-box :deep(h1),
.answer-box :deep(h2),
.answer-box :deep(h3) {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.answer-box :deep(ul),
.answer-box :deep(ol) {
  padding-left: 1.5rem;
}

.answer-box :deep(code) {
  background-color: #e9ecef;
  padding: 0.2rem 0.4rem;
  border-radius: 0.2rem;
}

.answer-box :deep(pre) {
  background-color: #e9ecef;
  padding: 1rem;
  border-radius: 0.3rem;
  white-space: pre-wrap;
}

/* 主要按钮样式 */
.btn-primary {
  background-color: #9b59b6;
  border-color: #9b59b6;
  transition: background-color 0.2s ease;
}

/* 主要按钮悬停样式 */
.btn-primary:hover {
  background-color: #8e44ad;
  border-color: #8e44ad;
}
</style>
