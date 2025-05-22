from rest_framework import serializers
from .models import Category, Book, Review, AIImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color', 'image']

class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publisher', 'pub_date', 
                 'description', 'isbn', 'cover_image', 'category', 'price']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'content', 'emotion_score', 
                 'created_at', 'updated_at']
        read_only_fields = ['emotion_score']

class AIImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIImage
        fields = ['id', 'category', 'image_url', 'prompt', 'created_at']
        read_only_fields = ['image_url']  # 이미지 URL은 AI 생성 후 자동으로 설정
