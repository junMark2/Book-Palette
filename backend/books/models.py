from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)  # HEX color code
    image = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=100)
    pub_date = models.DateField()
    description = models.TextField()
    isbn = models.CharField(max_length=13, unique=True)
    cover_image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    emotion_score = models.FloatField(default=0.0)  # 감정 분석 점수 (-1.0 ~ 1.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s review on {self.book}"

class AIImage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ai_images')
    image_url = models.URLField()
    prompt = models.TextField()  # AI 이미지 생성에 사용된 프롬프트
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Image for {self.category}"
