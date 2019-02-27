from django.db import models

class Test(models.Model):
    name = models.CharField(max_length = 200, verbose_name = "Название")

    class Meta:
        verbose_name        = "Тест"
        verbose_name_plural = "Тесты"
    
