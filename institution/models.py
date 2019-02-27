from django.db import models

class Institution(models.Model):
    name = models.CharField(max_length = 100, verbose_name = "Название")
    class Meta:
        verbose_name        = "Образовательное учреждение"
        verbose_name_plural = "Образовательные учреждения" 
