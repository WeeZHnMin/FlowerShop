from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import UserSerializer

# Custom Permission
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to only allow owners to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'owner'

# Views
class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    """
    API view for user login. Returns an auth token.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "username": user.username,
                "role": user.role,
                "balance": user.balance
            })
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class CustomerListView(generics.ListAPIView):
    """
    API view to list all customers. Only accessible by owners.
    """
    queryset = User.objects.filter(role='customer')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class CurrentUserView(APIView):
    """
    API view to get current user details.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)