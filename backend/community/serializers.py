from rest_framework import serializers
from .models import Thread, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    replies = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'thread', 'author', 'content', 'parent',
                 'created_at', 'updated_at', 'replies', 'likes_count']
        read_only_fields = ['author']
    
    def get_replies(self, obj):
        if obj.parent is None:  # Only get replies for parent comments
            replies = obj.replies.all()
            return CommentSerializer(replies, many=True).data
        return []
    
    def get_likes_count(self, obj):
        return obj.likes.count()

class ThreadSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Thread
        fields = ['id', 'title', 'content', 'author', 'book',
                 'thread_type', 'created_at', 'updated_at',
                 'comments_count', 'likes_count']
        read_only_fields = ['author']
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_likes_count(self, obj):
        return obj.likes.count()
