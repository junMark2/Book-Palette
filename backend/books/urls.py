from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, GenreViewSet, BookGenreViewSet, UserBookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'book-genres', BookGenreViewSet)
router.register(r'user-books', UserBookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
