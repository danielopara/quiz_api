from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers

from .models import AppUser, Question, User, UserQuizProfile


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('creator',)
        
    def create(self, validated_data):
        try:
            request = self.context.get('request')
           
            app_user = User.objects.get(id=request.user.id)
            user = AppUser.objects.get(email=app_user.email)
                
            validated_data['creator'] = user

                
            return Question.objects.create(creator=validated_data['creator']
                                           , question=validated_data['question'],
                                           option_a=validated_data['option_a'],
                                           option_b=validated_data['option_b'],
                                           option_c=validated_data['option_c'],
                                           option_d=validated_data['option_d'],
                                           correct_answer=validated_data['correct_answer'])
            
        except Exception as e:
            raise serializers.ValidationError({"error": f"failed to create question: {str(e)}"})

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

class UserQuizProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuizProfile
        fields = ('games_amount', 'games_won', 'games_lost')    
    

class AppUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    profile = UserQuizProfileSerializer(source='userquizprofile_set', many=True, read_only=True)  # Returns multiple profiles

    class Meta:
        model = AppUser
        fields = ('user','profile')
        
    def create(self, validated_data):
        try:
            with transaction.atomic():
                user_data = validated_data.pop('user')  
                
                serializer = UserSerializer(data = user_data)
                serializer.is_valid(raise_exception=True)
                
                user = serializer.save()
                
                app_user = AppUser.objects.create(user = user, email = user.email)
                UserQuizProfile.objects.create(usr_id=app_user)
            
            
                return app_user
        except Exception as e:
            raise serializers.ValidationError({"error": f"failed to create app user: {str(e)}"})
        