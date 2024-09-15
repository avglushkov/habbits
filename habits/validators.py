from rest_framework.exceptions import ValidationError


class RelationOrPrizeValidator:
    """Проверка на корректность указания связей и вознаграждений"""
    def __init__(self):
        pass

    def __call__(self, value, *args, **kwargs):
        if value.get('is_pleasant'):
            if value.get('prize') or value.get('related_habit'):
                raise ValidationError('Для приятной привычки не может быть указано вознаграждение или связанные привычки')
        else:
            if value.get('prize') and value.get('related_habit'):
                raise ValidationError('Нужно выбрать или вознаграждение или приятную привычку')
            if value.get('related_habit') is None and value.get('prize') is None:
                raise ValidationError('Нужно выбрать или вознаграждение или приятную привычку')


class HabitExecutionValidator:
    """Проверка корректности заполнения времени выполнения привычки"""
    def __init__(self):
        pass

    def __call__(self, value, *args, **kwargs):
        if value.get('is_pleasant'):
            if value.get('execution_time'):
                raise ValidationError('Для приятной привычки не нужно указывать время выполнения')
        else:
            if value.get('execution_time'):
                if value.get('execution_time') > 120:
                    raise ValidationError('Время выполнения привычки не должно быть больше 120 секунд')
                if value.get('execution_time') < 1:
                    raise ValidationError('Время выполнения привычки должно быть больше 1 секунды')
            else:
                raise ValidationError('Вы не заполнили поле с временем выполнения привычки (execution_time)')


class IsRelatedHabitPleasant:
    """Проверка на корректность привязки к полезным привычкам только приятных"""
    def __init__(self):
        pass

    def __call__(self, value, *args, **kwargs):
        if value.get('related_habit') and not value.get('is_pleasant'):
            if not value.get('related_habit').is_pleasant:
                raise ValidationError('Полезные привычки можно связывать только с приятными')


class HabitPeriodValidator:
    """Проверка корректности заданного периода повторения привычки"""
    def __init__(self):
        pass

    def __call__(self, value, *args, **kwargs):
        if value.get('is_pleasant'):
            if value.get('period'):
                raise ValidationError('Для приятных привычек не нужна периодичность')
        else:
            if value.get('period'):
                if value.get('period') > 7:
                    raise ValidationError('Привычку нужно повторять не реже раза в неделю')
                if value.get('period') < 1:
                    raise ValidationError('Периодичность указана некорректно, она должна быть от одного до 7 дней')
            else:
                raise ValidationError('Вы не указали периодичность')


class HabitTimeValidator:
    """Проверка корректности ввода времени для привычки"""
    def __init__(self):
        pass

    def __call__(self, value, *args, **kwargs):
        if value.get('is_pleasant'):
            if value.get('habit_time'):
                raise ValidationError("Приятная привычка  приятной привычки не требуется время (time)")
        else:
            if not value.get('habit_time'):
                raise ValidationError("Вы не заполнили время привычки (habit_time)")
