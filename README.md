# FlowerShop - 全栈花店Web应用

这是一个功能完善的全栈花店Web应用程序，结合了现代化的前后端技术，提供了一个完整的在线花卉销售和社区互动平台。

## 核心技术栈

*   **后端**: Django, Django REST Framework
*   **前端**: Vue.js 3, Vite, Vue Router, Axios, Bootstrap 5
*   **数据库**: SQLite (用于开发)
*   **AI & API**: 通义千问大模型, 百度植物识别API

## 项目结构

```
.flowerSystem/
├── backend/                    # 后端 Django 项目
│   ├── .venv/                  # Python 虚拟环境
│   ├── flower_shop/            # Django 项目配置
│   │   ├── settings.py         # 项目设置
│   │   └── urls.py             # 根 URL 配置
│   ├── products/               # 商品与社区模块
│   │   ├── models.py           # Flower, Post, Comment, Like 模型
│   │   ├── serializers.py      # 序列化器
│   │   ├── views.py            # 视图集 (API 逻辑)
│   │   └── urls.py             # 模块 URL 配置
│   ├── orders/                 # 订单模块
│   ├── users/                  # 用户模块
│   ├── manage.py               # Django 管理脚本
│   ├── requirements.txt        # 后端依赖
│   └── config.json.template    # API 密钥配置模板
└── frontend/                   # 前端 Vue.js 项目
    ├── public/                 # 公共静态资源 (logo.svg)
    ├── src/
    │   ├── components/         # Vue 组件
    │   │   ├── FlowerList.vue    # 花卉市场
    │   │   ├── ShoppingCart.vue  # 购物车
    │   │   ├── Checkout.vue      # 结算页面
    │   │   ├── OrderHistory.vue  # 客户订单历史
    │   │   ├── OrderManagement.vue # 店主订单管理
    │   │   ├── AskExpert.vue     # AI 专家 & 拍照识花
    │   │   ├── ImageSearch.vue   # 拍照识花组件
    │   │   ├── CameraCapture.vue # 摄像头拍照组件
    │   │   ├── Community.vue     # 社区主页
    │   │   ├── PostDetail.vue    # 帖子详情
    │   │   └── CreatePost.vue    # 创建帖子
    │   ├── router/             # 路由配置
    │   ├── services/           # API 服务
    │   │   └── api.js          # Axios 实例和 API 调用
    │   ├── store.js            # 全局状态管理
    │   └── main.js             # Vue 应用入口
    ├── index.html              # 主 HTML 文件
    ├── package.json            # 前端依赖和脚本
    └── vite.config.js          # Vite 配置
```

## 主要功能亮点

*   **完整的购物流程**: 浏览商品、加入购物车、填写订单、余额支付、模拟第三方支付。
*   **双重用户角色**: 系统区分“客户”和“店主”，提供不同的视图和权限。
*   **订单管理**: 客户可查看订单历史和状态，店主可管理所有订单并更新状态。
*   **AI 智能服务**: 
    *   **AI 专家问答**: 集成通义千问大模型，为用户提供专业花卉养护建议。
    *   **拍照识花**: 用户可通过本地上传或摄像头实时拍照，调用百度API识别花卉，并直接搜索店内相关商品。
*   **用户社区**: 客户可以发布、浏览、点赞和评论帖子，构建互动社区。
*   **用户余额系统**: 新用户注册即送1000元初始余额，用于支付订单。

## 本地运行

### 后端

1.  **进入后端目录**: `cd backend`
2.  **创建并激活虚拟环境**:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```
3.  **安装依赖**: `pip install -r requirements.txt`
4.  **配置API密钥**: 复制 `config.json.template` 为 `config.json`，并填入你自己的API密钥。
5.  **数据库迁移**: `python manage.py migrate`
6.  **创建超级用户 (可选)**: `python manage.py createsuperuser`
7.  **运行服务器**: `python manage.py runserver` (默认运行在 `http://127.0.0.1:8000`)

### 前端

1.  **进入前端目录**: `cd frontend`
2.  **安装依赖**: `npm install`
3.  **运行开发服务器**: `npm run dev` (默认运行在 `http://127.0.0.1:5173`)

现在可以在浏览器中打开 `http://127.0.0.1:5173` 来访问应用。
