from django.db import models
from testing.models import Group
class Event(models.Model):
    """Мероприятие"""
    name            = models.CharField(max_length = 50, verbose_name = "Название")
    image           = models.URLField(verbose_name = "Изображение", blank = True, null = True)

    description     = models.TextField(verbose_name = "Описание", blank = True)
    competence      = models.CharField(max_length = 50, verbose_name = "Компетенция", blank = True)
    #competence  = models.ManyToManyField(Group, verbose_name = "Компетенция", related_name = "event")
    date            = models.DateField(null = True, verbose_name = "Дата проведения")
    time            = models.TimeField(null = True, verbose_name = "Время проведения")
    duration        = models.IntegerField(verbose_name = "Длительность", blank = True, default = 0)
    venue           = models.TextField(verbose_name = "Место проведения", null = True)
    format_event    = models.CharField(max_length = 50, verbose_name = "Формат мероприятия", blank = True)
    format_task     = models.CharField(max_length = 50, verbose_name = "Формат задания", blank = True)
    max_partiсipant = models.IntegerField(verbose_name = "Максимальное количестьво учатников", default = 0)

    class Meta:
        verbose_name        = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return "id: {}, name: {}".format(self.id, self.name)