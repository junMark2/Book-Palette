from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Thread, Comment
from .serializers import ThreadSerializer, CommentSerializer

class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Thread.objects.all()
        book_id = self.request.query_params.get('book', None)
        thread_type = self.request.query_params.get('type', None)
        
        if book_id:
            queryset = queryset.filter(book_id=book_id)
        if thread_type:
            queryset = queryset.filter(thread_type=thread_type)
            
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        thread = self.get_object()
        user = request.user
        
        if thread.likes.filter(id=user.id).exists():
            thread.likes.remove(user)
            return Response({'status': 'unliked'})
        else:
            thread.likes.add(user)
            return Response({'status': 'liked'})

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Comment.objects.filter(parent=None)  # 최상위 댓글만 반환
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        
        if comment.likes.filter(id=user.id).exists():
            comment.likes.remove(user)
            return Response({'status': 'unliked'})
        else:
            comment.likes.add(user)
            return Response({'status': 'liked'})
