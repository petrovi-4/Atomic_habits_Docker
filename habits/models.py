from users.models import User
from django.db import models

from config.settings import NULLABLE


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='пользователь', **NULLABLE)
    place = models.CharField(max_length=150, verbose_name='место', **NULLABLE)
    time = models.TimeField(verbose_name='время', **NULLABLE)
    periodicity = models.PositiveIntegerField(verbose_name='периодичность в днях', default=1)
    action = models.CharField(max_length=150, verbose_name='действие')
    is_pleasurable = models.BooleanField(default=False, verbose_name='приятная привычка')
    associated_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='связанная привычка', **NULLABLE)
    reward = models.CharField(verbose_name='вознаграждени', **NULLABLE)
    lead_time = models.IntegerField(verbose_name='время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='публичная привычка')
    date_of_next_reminder_sending = models.DateField(verbose_name='дата отправки следуюзего напоминания', **NULLABLE)

    def __str__(self):
        return f'Я буду {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-time']

