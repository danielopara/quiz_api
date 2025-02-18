import logging

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.models import Question
from api.serializers import QuizSerializer


class QuestionView():
    
    @permission_classes([IsAuthenticated])
    @api_view(['POST'])
    def create_question(request):
        if not request.user.is_authenticated:
            return Response({'success': False, "data": "user is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = QuizSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data':serializer.data}, status=200)
        return Response({'success': False, 'data': serializer.errors}, status=400)
    