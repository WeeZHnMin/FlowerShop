from django.urls import path
from .views import RegisterView, LoginView, CustomerListView, CurrentUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
]
