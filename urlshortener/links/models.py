from django.db import models
from django.contrib.auth.models import User
import random
import string

def generate_short_id():
    return ''.join(random.choices(string.ascii_lowercase, k=8))

class Link(models.Model):
    original_url = models.URLField()  # Длинная ссылка
    short_id = models.CharField(max_length=8, unique=True, default=generate_short_id)  # Короткая ссылка (8 символов)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания ссылки
    last_accessed = models.DateTimeField(auto_now=True)  # Дата последнего обращения
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')  # Связь с пользователем

    def __str__(self):
        return f"{self.original_url} -> {self.short_id}"

    def is_unused(self, days=30):
        """
        Проверка, является ли ссылка неиспользуемой (последний доступ был больше чем X дней назад).
        """
        from django.utils import timezone
        from datetime import timedelta

        return self.last_accessed < timezone.now() - timedelta(days=days)

    @staticmethod
    def generate_short_id(length=8):
        characters = string.ascii_letters
        return ''.join(random.choice(characters) for _ in range(length))