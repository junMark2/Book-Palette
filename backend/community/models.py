from django.db import models
from django.contrib.auth import get_user_model
from books.models import Book

User = get_user_model()

class Thread(models.Model):
    THREAD_TYPES = [
        ('BOOK', '도서 스레드'),
        ('FREE', '자유 스레드'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, related_name='threads')
    thread_type = models.CharField(max_length=4, choices=THREAD_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_threads', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.thread}"
