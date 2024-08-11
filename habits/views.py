from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginator import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, HabitPublicSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """Эндпоинт создания привычки"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()


class HabitListAPIView(generics.ListAPIView):
    """Эндпоинт списка привычек"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitPublicListAPIView(generics.ListAPIView):
    """Эндпоинт списка публичных привычек"""
    serializer_class = HabitPublicSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPaginator
    queryset = Habit.objects.filter(is_public=True)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Эндпоинт просмотра привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт редактирования привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт удаления привычки"""
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
