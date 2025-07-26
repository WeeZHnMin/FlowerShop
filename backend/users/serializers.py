from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone_number', 'role', 'balance']
        extra_kwargs = {
            'password': {'write_only': True},
            'balance': {'read_only': True}
        }

    def create(self, validated_data):
        # Manually create the user to ensure balance is set on creation
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            role='customer',
            balance=1000  # Set balance directly on the instance
        )
        user.set_password(validated_data['password']) # Hash the password
        user.save() # Save the complete user object once
        return user
