from rest_framework import serializers
from .models import Thread, Comment, Like, ColorHistory

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['id', 'book', 'user', 'content', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'thread', 'user', 'content', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'thread', 'user']

class ColorHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorHistory
        fields = ['id', 'user', 'genre', 'count']
