from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import openai
from django.conf import settings
from .models import Category, Book, Review, AIImage
from .serializers import (
    CategorySerializer, BookSerializer, 
    ReviewSerializer, AIImageSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def generate_image(self, request, pk=None):
        """카테고리에 대한 AI 이미지 생성"""
        category = self.get_object()
        prompt = request.data.get('prompt', '')
        
        try:
            # OpenAI API를 사용하여 이미지 생성
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            
            # 생성된 이미지 URL 저장
            image_url = response['data'][0]['url']
            ai_image = AIImage.objects.create(
                category=category,
                image_url=image_url,
                prompt=prompt
            )
            
            return Response(AIImageSerializer(ai_image).data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Book.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # 리뷰 작성 시 감정 분석 수행
        content = self.request.data.get('content', '')
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Analyze the emotion in this review. Return only a number between -1 (very negative) and 1 (very positive):\n{content}",
                max_tokens=10
            )
            emotion_score = float(response.choices[0].text.strip())
        except:
            emotion_score = 0.0
            
        serializer.save(
            user=self.request.user,
            emotion_score=emotion_score
        )
