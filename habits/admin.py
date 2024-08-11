from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'time', 'periodicity', 'is_pleasurable',
                    'associated_habit', 'reward', 'is_public',)
