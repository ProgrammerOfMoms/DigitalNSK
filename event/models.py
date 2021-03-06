from django.db import models
from testing.models import Group

class MainCompetence(models.Model):
    name   = models.CharField(max_length = 50, verbose_name = "Название")
    isBase = models.BooleanField(verbose_name = "Базовая?", default = False)

    class Meta:
        verbose_name        = "Основная компетенция"
        verbose_name_plural = "Основные компетенции"

    def __str__(self):
        return "id: {}, name: {}, base: {}".format(self.id, self.name, self.isBase)

class SideCompetenceAdd(models.Model):
    name            = models.CharField(max_length = 50, verbose_name = "Название")
    overCompetence = models.ForeignKey(MainCompetence, on_delete = models.CASCADE, verbose_name = "Компетенция 1 уровня", related_name = "side", null = True)

    class Meta:
        verbose_name        = "Субкомпетенция 2 уровня"
        verbose_name_plural = "Субкомпетенции 2 уровня"

    def __str__(self):
        return "id: {}, name: {}".format(self.id, self.name)


class SideCompetence(models.Model):
    name   = models.CharField(max_length = 50, verbose_name = "Название")
    overCompetence = models.ForeignKey(SideCompetenceAdd, on_delete = models.CASCADE, verbose_name = "Компетенция 2 уровня", related_name = "side", null = True)

    class Meta:
        verbose_name        = "Субкомпетенция 3 уровня"
        verbose_name_plural = "Субкомпетенции 3 уровня"

    def __str__(self):
        return "id: {}, name: {}".format(self.id, self.name)

class Competence(models.Model):
    """Компетенция"""
    name   = models.CharField(max_length = 80, verbose_name = "Название")
    level  = models.IntegerField(verbose_name = "Уровень", default = 1)
    parent = models.IntegerField(verbose_name = "Родитель(id)", blank = True, default = 0)
    class Meta:
        verbose_name        = "Копметенция"
        verbose_name_plural = "Компетенции"

    def __str__(self):
        return "id: {}, name: {}, level: {}, parent: {}".format(self.id, self.name, self.level, self.parent)

class Point(models.Model):
    """Балл за участие в мероприятии"""
    competence = models.ForeignKey(SideCompetence, on_delete = models.CASCADE, verbose_name = "Компетенция", related_name = "point", null = True)
    value      = models.IntegerField(verbose_name = "Кол-во баллов")
    
    class Meta:
        verbose_name        = "Балл за участие в мероприятии"
        verbose_name_plural = "Баллы за участие в мероприятии"

    def __str__(self):
        return "id: {}, value: {}".format(self.id, self.value)

class Event(models.Model):
    """Мероприятие"""
    name                = models.CharField(max_length = 150, verbose_name = "Название")
    img                 = models.ImageField(upload_to = "Events", blank = True, verbose_name = "Изображение")
    description         = models.TextField(verbose_name = "Описание", blank = True, null = True)
    mainCompetence      = models.ForeignKey(MainCompetence, verbose_name = "Основная компетенция", related_name = "event", blank = True, on_delete = models.CASCADE, null = True)
    competence          = models.ManyToManyField(SideCompetence, verbose_name = "Полезно знать до мероприятия", related_name = "event", blank = True)
    points              = models.ManyToManyField(Point, verbose_name = "Навыки, которые будем прокачивать", related_name = "event_add", blank = True)
    date                = models.CharField(max_length = 10, null = True, verbose_name = "Дата проведения")
    time                = models.CharField(max_length = 5, null = True, verbose_name = "Время проведения")
    venue               = models.TextField(verbose_name = "Место проведения", null = True)
    format_event        = models.CharField(max_length = 50, verbose_name = "Формат мероприятия", blank = True)
    max_partiсipants    = models.IntegerField(verbose_name = "Максимальное количестьво учатников", default = 0)
    partiсipants        = models.IntegerField(verbose_name = "Количестьво учатников", default = 0)
    active              = models.BooleanField(default = True, verbose_name = "Активно?")
    #Партнер
    partner             = models.CharField(max_length = 50, verbose_name = "Партнер", blank = True)
    manager_name        = models.CharField(max_length = 200, verbose_name = "Имя организатора", blank = True)
    manager_position    = models.CharField(max_length = 200, verbose_name = "Должность организатора", blank = True)
    phonenumber         = models.CharField(max_length = 20, verbose_name = "Номер телефона", blank = True)
    class Meta:
        verbose_name        = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return "id: {}, name: {}".format(self.id, self.name)