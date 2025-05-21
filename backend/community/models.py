from django.db import models
from django.contrib.auth import get_user_model
from backend.books.models import Book, Genre

class Thread(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Thread by {self.user.username} on {self.book.title if self.book else 'General'}"

class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.thread.id}"

class Like(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"Like by {self.user.username} on {self.thread.id}"

class ColorHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.genre.name} - {self.count}"
