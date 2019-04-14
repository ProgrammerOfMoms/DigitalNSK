from django.db import models
from testing.models import Group

class SideCompetence(models.Model):
    name            = models.CharField(max_length = 50, verbose_name = "Название")

    class Meta:
        verbose_name        = "Субкомпетенция 3 уровня"
        verbose_name_plural = "Субкомпетенции 3 уровня"

    def __str__(self):
        return "id: {}, name: {}".format(self.id, self.name)

class SideCompetenceAdd(models.Model):
    name            = models.CharField(max_length = 50, verbose_name = "Название")
    subCompetence   = models.ManyToManyField(SideCompetence, verbose_name = "Субкомпетенции 3 уровня", related_name = "sideCompAdd")

    class Meta:
        verbose_name        = "Субкомпетенция 2 уровня"
        verbose_name_plural = "Субкомпетенции 2 уровня"

    def __str__(self):
        return "id: {}, name: {}".format(self.id, self.name)

class BaseCompetence(models.Model):
    name            = models.CharField(max_length = 50, verbose_name = "Название")
    subCompetence   = models.ManyToManyField(SideCompetenceAdd, verbose_name = "Субкомпетенции 2 уровня", related_name = "baseComp")

    class Meta:
        verbose_name        = "Базовая компетенция"
        verbose_name_plural = "Базовые компетенции"

    def __str__(self):
        return "id: {}, name: {}".format(self.id, self.name)

class MainCompetence(models.Model):
    name            = models.CharField(max_length = 50, verbose_name = "Название")
    subCompetence   = models.ManyToManyField(SideCompetenceAdd, verbose_name = "Субкомпетенции 2 уровня", related_name = "mainComp", blank = True)

    class Meta:
        verbose_name        = "Основная компетенция"
        verbose_name_plural = "Основные компетенции"

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
        return "id: {}, competence: {}, value: {}".format(self.id, self.competence.name, self.value)

class Event(models.Model):
    """Мероприятие"""
    name                = models.CharField(max_length = 50, verbose_name = "Название")
    img                 = models.URLField(verbose_name = "Изображение", blank = True, null = True)
    description         = models.TextField(verbose_name = "Описание", blank = True, null = True)
    competence          = models.ManyToManyField(SideCompetence, verbose_name = "Полезно знать до мероприятия", related_name = "event", blank = True)
    points              = models.ManyToManyField(Point, verbose_name = "Навыки, которые будем прокачивать", related_name = "event_add", blank = True)
    date                = models.CharField(max_length = 10, null = True, verbose_name = "Дата проведения")
    time                = models.CharField(max_length = 5, null = True, verbose_name = "Время проведения")
    venue               = models.TextField(verbose_name = "Место проведения", null = True)
    format_event        = models.CharField(max_length = 50, verbose_name = "Формат мероприятия", blank = True)
    max_partiсipants    = models.IntegerField(verbose_name = "Максимальное количестьво учатников", default = 0)
    partiсipants        = models.IntegerField(verbose_name = "Количестьво учатников", default = 0)

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