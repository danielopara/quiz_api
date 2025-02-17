from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import AppUser, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required':True}
        }
    
    def create(self, validated_data):
        try:
            return User.objects.create_user(
                email = validated_data['email'],
                username=validated_data['email'],
                password= validated_data['password']
            )
        except Exception as e:
            raise serializers.ValidationError({"error": f"Failed to create user: {str(e)}"})
        
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "email already exists"})
        return email
    

class AppUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = AppUser
        fields = ('user',)
        
    def create(self, validated_data):
        try:
            user_data = validated_data.pop('user')  
            
            serializer = UserSerializer(data = user_data)
            serializer.is_valid(raise_exception=True)
            
            user = serializer.save()
            
            app_user = AppUser.objects.create(user = user, email = user.email)
            return app_user
        except Exception as e:
            raise serializers.ValidationError({"error": f"failed to create app user: {str(e)}"})