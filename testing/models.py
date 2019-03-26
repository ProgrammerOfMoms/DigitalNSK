from django.db import models


class Group(models.Model):
    """Группа"""

    key  = models.IntegerField(verbose_name = "Номер группы")
    name = models.CharField(max_length = 200, verbose_name = "Название", unique = True)

    class Meta:
        verbose_name        = "Группа"
        verbose_name_plural = "Группы"
    
    def __str__(self):
        return "id: {}, key: {}, name: {}".format(self.id, self.key, self.name)

class Answer(models.Model):
    content     = models.TextField(verbose_name="Ответ")
    group       = models.ForeignKey(Group, verbose_name = "Группа", related_name = "answer", on_delete=models.SET_NULL, null = True)

    class Meta:
        verbose_name        = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return "id: {}, content: {}".format(self.id, self.content)

class Question(models.Model):
    content     = models.TextField(verbose_name="Вопрос")
    answers     = models.ManyToManyField(Answer, verbose_name = "Ответы", related_name="question")

    class Meta:
        verbose_name        = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return "id: {}, content: {}".format(self.id, self.content)

class Test(models.Model):
    name                = models.CharField(max_length = 200, verbose_name = "Название", unique = True)
    description         = models.TextField(verbose_name="Описание", blank=True, null = True)
    questions           = models.ManyToManyField(Question, verbose_name = "Вопросы", related_name="test")
    mode                = models.IntegerField(verbose_name = "Тип теста", unique = False)
    groups              = models.ManyToManyField(Group, verbose_name = "Группы", related_name="test", blank = True)
    additionalQuestion  = models.OneToOneField(Question, verbose_name = "Дополнительный вопрос", related_name="test_add", on_delete = models.SET_NULL, blank = True, null = True)
    class Meta:
        verbose_name        = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return "id: {}, description: {}".format(self.id, self.description)

class ResultOfTest(models.Model):
    competence  = models.TextField(verbose_name="Компетенция", blank=True, null = True)
    test        = models.ForeignKey(Test, verbose_name="Тест", related_name = "result", on_delete=models.CASCADE)

    class Meta:
        verbose_name        = "Результат теста"
        verbose_name_plural = "Результаты теста"

    def __str__(self):
        return "id: {}, test: {}".format(self.id, self.test.mode)