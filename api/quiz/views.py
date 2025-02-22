import logging

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.models import Question
from api.serializers import QuizSerializer

logger = logging.getLogger(__name__)

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
    
    @permission_classes([IsAuthenticated])
    @api_view(['GET'])
    def get_question(request):
        try:
            question = Question.objects.order_by('?').first()
            
            if not question:
                return Response({'success': False, 'data': 'no questions found'}, status=status.HTTP_400_BAD_REQUEST)
            
            question_list = {
                'id': question.id,
                'creator': question.creator.email,
                'question': question.question,
                'option_a': question.option_a,
                'option_b': question.option_b,
                'option_c': question.option_c,
                'option_d': question.option_d,
            }
            
            return Response({'success': True, 'data': question_list}, status=200)
        except Exception as e:
            logger.error(f"get_question error,  {str(e)}")
            return Response({'success': False, 'data': "Internal server error" },  status=status.HTTP_500_INTERNAL_SERVER_ERROR)