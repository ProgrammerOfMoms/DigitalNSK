from django.db import models

class Answer(models.Model):
    content     = models.TextField(verbose_name="Ответ")
    group       = models.IntegerField(verbose_name="Группа")

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

class Group(models.Model):
    """Группа"""

    key  = models.IntegerField(verbose_name = "Номер группы")
    name = models.CharField(max_length = 200, verbose_name = "Название", unique = True)


class Test(models.Model):
    TEST_1 = "Тест №1"
    TEST_2 = "Тест №2"
    TEST_3 = "Тест №3"

    CHOICES_OF_TEST = (
        (TEST_1, "Тест №1"),
        (TEST_2, "Тест №2"),
        (TEST_3, "Тест №3")
    )

    name                = models.CharField(max_length = 200, verbose_name = "Название", unique = True)
    description         = models.TextField(verbose_name="Описание", blank=True, null = True)
    questions           = models.ManyToManyField(Question, verbose_name = "Вопросы", related_name="test")
    mode                = models.CharField(choices = CHOICES_OF_TEST, default = TEST_1, verbose_name = "Тип теста", max_length = 50)
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