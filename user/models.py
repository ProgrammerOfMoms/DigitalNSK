from django.db import models
from testing.models import Test
from institution.models import Institution



class User(models.Model):
    """Модель пользователя"""

    PARTICIPANT     = "PATICIPANT"
    TUTOR           = "TUTOR"
    UNIVERSITY      = "UNIVERSITY"
    PARTNER         = "PARTNER"
    ADMINISTRATOR   = "ADMINISTRATOR"


    CHOICES_OF_ROLE = (
        (PARTICIPANT,"Участник"),
        (TUTOR, "Тьютор"),
        (UNIVERSITY,"Университет"),
        (PARTNER, "Партнер"),
        (ADMINISTRATOR, "Администратор"),
    )

    firstName       = models.CharField(max_length = 20, verbose_name = "Имя")
    lastName        = models.CharField(max_length = 20, verbose_name = "Фамилия")
    patronymic      = models.CharField(max_length = 20, verbose_name = "Отчество", blank = True, default = "")
    email           = models.EmailField(verbose_name = "Email", blank = True)
    password        = models.TextField(verbose_name = "Пароль", blank = True, default = "")
    photo           = models.URLField(verbose_name="Фото", blank = True)
    phoneNumber     = models.CharField(max_length = 18, blank = True, default = "")
    role            = models.CharField(verbose_name = "Роль", choices = CHOICES_OF_ROLE, default = PARTICIPANT, max_length = 20)
    emailConfirmed  = models.BooleanField(verbose_name = "Email подтвержден", default = False)

    def __str__(self):
        return "{} {} id{}".format(self.firstName, self.lastName, str(self.id))
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"



class Progress(models.Model):
    """Модель прогресса участника"""

    progress = models.IntegerField(verbose_name = "Прогресс", default = 0)

    class Meta:
        verbose_name        = "Прогресс"
        verbose_name_plural = "Прогресс"



class Participant(models.Model):
    """Модель участника"""

    CLASS_8     = "8TH CLASS"
    CLASS_9     = "9TH CLASS"
    CLASS_10    = "10TH CLASS"
    CLASS_11    = "11TH CLASS"
    COURSE_1    = "1TH COURSE"
    COURSE_2    = "2TH COURSE"
    COURSE_3    = "3TH COURSE"
    COURSE_4    = "4TH COURSE"
    COURSE_5    = "5TH COURSE"


    CHOICES_OF_LEVEL = (
        (CLASS_8,"8 класс"), (CLASS_9, "9 класс"), (CLASS_10, "10 класс"),
        (CLASS_11,"11 класс"), (COURSE_1, "1 курс"), (COURSE_2, "2 курс"),
        (COURSE_3, "3 курс"), (COURSE_4, "4 курс"), (COURSE_5, "5 курс"),
    )

    id              = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True, related_name = "participant", verbose_name = "Пользователь")
    eduInstitution  = models.OneToOneField(Institution, on_delete = models.CASCADE, related_name = "participant", verbose_name = "Образовательное учреждение", blank = True) 
    
    """???"""
    level           = models.CharField(choices = CHOICES_OF_LEVEL, default = CLASS_8, verbose_name = "Класс/курс", max_length = 20, blank = True)
    """???"""

    vkURL           = models.URLField(verbose_name= "Ссылка на vkontakte", blank = True)
    instURL         = models.URLField(verbose_name= "Ссылка на instagram", blank = True)
    fbURL           = models.URLField(verbose_name= "Ссылка на facebook", blank = True)
    passedTests     = models.ManyToManyField(Test, verbose_name = "Завершенные тесты", related_name= "participant", blank = True)
    events          = models.ForeignKey(Progress, on_delete = models.CASCADE, related_name= "participant", verbose_name = "Мероприятия", blank = True)
    progress        = models.FloatField(verbose_name = "Прогресс", default=0, blank = True)
    mailing         = models.BooleanField(default=False)
    

    class Meta:
        verbose_name        = "Участник"
        verbose_name_plural = "Участники"
