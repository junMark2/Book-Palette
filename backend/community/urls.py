from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ThreadViewSet, CommentViewSet, LikeViewSet, ColorHistoryViewSet

router = DefaultRouter()
router.register(r'threads', ThreadViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'color-history', ColorHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
