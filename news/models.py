from django.db import models

# Create your models here.

class News(models.Model):

    html_code       = models.TextField(verbose_name = "html код новости")
    photo           = models.URLField(verbose_name = "Картинка к новости")
    date            = models.DateField(verbose_name = "Дата публикации", auto_now=True)

    class Meta:
        verbose_name        = "Новость"
        verbose_name_plural = "Новости"