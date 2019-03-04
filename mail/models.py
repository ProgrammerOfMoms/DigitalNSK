from django.db import models

# Create your models here.

class RecoveryLink(models.Model):
    id      = models.OneToOneField(user, on_delete = models.CASCADE, verbose_name = "id")
    link    = models.URLField(max_length = 200)
        
        class Meta:
            verbose_name        = "Ссылка на восстановление"
            verbose_name_prulal = "Ссылки на восстановление"
 
