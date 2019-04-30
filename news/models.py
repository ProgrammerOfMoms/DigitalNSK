from django.db import models
import datetime

# Create your models here.

class News(models.Model):

    html_code       = models.TextField(verbose_name = "html код новости")
    title           = models.TextField(verbose_name= "Заголовок", default = "title")
    photo           = models.TextField(verbose_name = "Картинка к новости")
    date            = models.DateField(verbose_name = "Дата публикации", default = datetime.datetime.now().date())

    class Meta:
        verbose_name        = "Новость"
        verbose_name_plural = "Новости"
