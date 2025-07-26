from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlowerViewSet, RecognizeFlowerView, AskQwenView, LogJsonErrorView, PostViewSet

router = DefaultRouter()
router.register(r'flowers', FlowerViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recognize/', RecognizeFlowerView.as_view(), name='recognize-flower'),
    path('ask-qwen/', AskQwenView.as_view(), name='ask-qwen'),
    path('log-error/', LogJsonErrorView.as_view(), name='log-error'),
]