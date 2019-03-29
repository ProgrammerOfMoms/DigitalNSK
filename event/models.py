from django.db import models
from testing.models import Group

class EventStage(models.Model):
    """Этап мероприятия"""
    name = models.CharField(max_length = 50, verbose_name = "Название")

    class Meta:
        verbose_name        = "Этап мероприятия"
        verbose_name_plural = "Этапы мероприятия"

    def __str__(self):
        return "id: {}, name: {}".format(self.id, self.name)

class Competence(models.Model):
    """Компетенция"""
    name = models.CharField(max_length = 50, verbose_name = "Название")

    class Meta:
        verbose_name        = "Копметенция"
        verbose_name_plural = "Компетенции"

    def __str__(self):
        return "id: {}, name: {}".format(self.id, self.name)

class Event(models.Model):
    """Мероприятие"""
    name                = models.CharField(max_length = 50, verbose_name = "Название")
    img                 = models.URLField(verbose_name = "Изображение", blank = True, null = True)
    description         = models.ManyToManyField(EventStage, verbose_name = "Описание", blank = True, related_name = "event")
    #competence      = models.CharField(max_length = 50, verbose_name = "Компетенция", blank = True)
    competence          = models.ManyToManyField(Competence, verbose_name = "Компетенция", related_name = "event")
    inherent_competence = models.ManyToManyField(Competence, verbose_name = "Компетенция", related_name = "event_add")
    date                = models.CharField(max_length = 10, null = True, verbose_name = "Дата проведения")
    time                = models.CharField(max_length = 5, null = True, verbose_name = "Время проведения")
    duration            = models.CharField(max_length = 15, verbose_name = "Длительность", blank = True, null = True)
    venue               = models.TextField(verbose_name = "Место проведения", null = True)
    format_event        = models.CharField(max_length = 50, verbose_name = "Формат мероприятия", blank = True)
    format_task         = models.CharField(max_length = 50, verbose_name = "Формат задания", blank = True)
    max_partiсipants    = models.IntegerField(verbose_name = "Максимальное количестьво учатников", default = 0)
    partiсipants        = models.IntegerField(verbose_name = "Количестьво учатников", default = 0)
    count               = models.IntegerField(verbose_name = "Вес мероприятия", default = 0)
    partner             = models.CharField(max_length = 50, verbose_name = "Партнер", blank = True)
    manager_name        = models.CharField(max_length = 200, verbose_name = "Имя организатора", blank = True)
    manager_position    = models.CharField(max_length = 200, verbose_name = "Должность организатора", blank = True)
    phonenumber         = models.CharField(max_length = 20, verbose_name = "Номер телефона", blank = True)

    class Meta:
        verbose_name        = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return "id: {}, name: {}".format(self.id, self.name)

