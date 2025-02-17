import logging

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import AppUser
from api.serializers import AppUserSerializer

logger = logging.getLogger(__name__)
class UserView():
    @api_view(['POST'])
    def register(request):
        try:
            email = request.data['user']['email']
            if AppUser.objects.filter(email=email).exists():
                return Response({'success': False, 'data': "email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            serializer=AppUserSerializer(data=request.data)
            if serializer.is_valid():
                app_user = serializer.save()
                profiles = [
                {"games_amount": profile.games_amount,
                 "games_won": profile.games_won,
                 "games_lost": profile.games_lost}
                for profile in app_user.userquizprofile_set.all()
            ]
                return Response({'success': True,
                                 'data': {
                                     'email': app_user.email,
                                     'profile':  profiles
                                     }},
                                status=status.HTTP_201_CREATED)
            
            return Response({"success": False, 
                            'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in register user: {str(e)}")
            return Response({'success': False, 'data': "an error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    @api_view(['POST'])
    def login( request):
        try:
            email = request.data['email']
            password = request.data['password']
            
            if not email or not password:
                return Response({"success": False, "data": "email and password are required"})
            
            user = authenticate(username=email, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                
                return Response({"success": True,
                                "data": {
                                    "access_token": access_token,
                                    "refresh_token": str(refresh)
                                }},
                                status=status.HTTP_200_OK)
            return Response({"success": False, "data": "invalid credentials"})
        except Exception as e :
            logger.error(f"Error in login endpoint: {str(e)}")
            return Response({"success": False, "data": "internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )