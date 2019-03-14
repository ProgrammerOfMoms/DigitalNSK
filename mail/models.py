from django.db import models
from user.models import User

class RecoveryLink(models.Model):
    id          = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = "id", related_name = "recoveryLink", primary_key = True)
    link        = models.URLField(max_length = 200) #add unique = True!!!
    # create_time = models.TextField(default="0000-00-00 00:00:00")
        
    class Meta:
        verbose_name        = "Ссылка на восстановление"
        verbose_name_plural = "Ссылки на восстановление"
 
