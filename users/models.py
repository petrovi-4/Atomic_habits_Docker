from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    telegram_chat_id = models.CharField(max_length=35, verbose_name='ID чата Telegram', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
