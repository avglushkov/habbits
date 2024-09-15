from rest_framework import serializers

from habits.models import Habit
from habits.validators import (HabitTimeValidator,
                               HabitPeriodValidator,
                               IsRelatedHabitPleasant,
                               RelationOrPrizeValidator,
                               HabitExecutionValidator)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [HabitExecutionValidator(),
                      HabitTimeValidator(),
                      HabitPeriodValidator(),
                      IsRelatedHabitPleasant(),
                      RelationOrPrizeValidator()]
