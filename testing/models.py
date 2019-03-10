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
    answers     = models.ForeignKey(Answer, on_delete = models.CASCADE, verbose_name = "Ответы", null = True, related_name="question")

    class Meta:
        verbose_name        = "Вопрос"
        verbose_name_plural = "Вопросы"
   
    def __str__(self):
        return "id: {}, content: {}".format(self.id, self.content)

class Test(models.Model):
    name        = models.CharField(max_length = 200, verbose_name = "Название")
    desciption  = models.TextField(verbose_name="Описание", blank=True, null = True)
    question    = models.ForeignKey(Answer, on_delete = models.CASCADE, verbose_name = "Вопросы", null = True, related_name="test")

    class Meta:
        verbose_name        = "Тест"
        verbose_name_plural = "Тесты"
    
    def __str__(self):
        return "id: {}, description: {}".format(self.id, self.desciption)
    
