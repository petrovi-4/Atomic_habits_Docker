from django.urls import path

from habits.views import HabitCreateAPIView, HabitUpdateAPIView, HabitDestroyAPIView, HabitRetrieveAPIView, HabitListAPIView, \
    HabitPublicListAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name


urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='habit-create'),
    path('<int:pk>/update/', HabitUpdateAPIView.as_view(), name='habit-update'),
    path('<int:pk>/delete/', HabitDestroyAPIView.as_view(), name='habit-delete'),
    path('<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit-get'),
    path('list/', HabitListAPIView.as_view(), name='habits-list'),
    path('public_list/', HabitPublicListAPIView.as_view(), name='habits-public_list'),
]
