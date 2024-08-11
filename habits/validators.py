from rest_framework.exceptions import ValidationError

from habits.models import Habit


class LeadTimeValidator:
    """Проверка времени на выполнение привычки"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val > 120:
            raise ValidationError('Время на выполнение должно быть не больше 120 минут')


class PeriodicityValidator:
    """Проверка периодичности выполнения в днях"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val > 7:
            raise ValidationError('Периодичность выполнения должна быть не реже, чем 1 раз за 7 дней')


class AssociatedHabitOrRewardValidator:
    """Проверка, что вознаграждени и связанная привычка не назначены одновременно"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        associated_habit = dict(value).get('associated_habit')
        reward = dict(value).get(self.field)
        if associated_habit is not None and reward is not None:
            raise ValidationError('Нельзя назначить вознаграждение и связанную привычку одновременно')


class PleasurableHabitValidator:
    """Проверка, что у приятной привычки не назначено вознаграждение или связанная привычка"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        is_pleasurable = dict(value).get('is_pleasurable')
        tmp_val = dict(value).get(self.field)
        if is_pleasurable and tmp_val is not None:
            raise ValidationError('Нельзя назначить вознаграждение или связанную привычку для приятной привычки')


class AssociatedHabitIsPleasurableHabitValidator:
    """Проверка, что связанная привычка является приятной"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        associated_habit = dict(value).get(self.field)
        if associated_habit is not None:
            habit = Habit.objects.get(pk=associated_habit.pk)

            if not habit.is_pleasurable:
                raise ValidationError('Связанная привычка должна быть приятной')
