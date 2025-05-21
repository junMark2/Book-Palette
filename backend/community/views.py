from rest_framework import viewsets, permissions
from .models import Thread, Comment, Like, ColorHistory
from .serializers import ThreadSerializer, CommentSerializer, LikeSerializer, ColorHistorySerializer

class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ColorHistoryViewSet(viewsets.ModelViewSet):
    queryset = ColorHistory.objects.all()
    serializer_class = ColorHistorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
