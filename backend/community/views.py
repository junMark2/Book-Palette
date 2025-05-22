from rest_framework import viewsets, permissions
from .models import Thread, Comment, Like, ColorHistory
from .serializers import ThreadSerializer, CommentSerializer, LikeSerializer, ColorHistorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum

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

    @action(detail=True, methods=['get'])
    def represent_color(self, request, pk=None):
        user = self.get_object()
        color_history = ColorHistory.objects.filter(user=user)
        total_count = color_history.aggregate(Sum('count'))['count__sum'] or 0

        if total_count == 0:
            return Response({"represent_color": None})

        color_weights = {}
        for entry in color_history:
            color_weights[entry.genre.color] = color_weights.get(entry.genre.color, 0) + entry.count

        represent_color = max(color_weights, key=color_weights.get)
        return Response({"represent_color": represent_color})
