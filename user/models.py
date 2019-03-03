from __future__ import unicode_literals
from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

from testing.models import Test
from institution.models import Institution



class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя"""

    PARTICIPANT     = "PARTICIPANT"
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

    email           = models.CharField(max_length = 50, verbose_name = "Логин", unique = True)
    firstName       = models.CharField(max_length = 20, verbose_name = "Имя")
    lastName        = models.CharField(max_length = 20, verbose_name = "Фамилия")
    patronymic      = models.CharField(max_length = 20, verbose_name = "Отчество", blank = True)
    password        = models.TextField(verbose_name = "Пароль")
    photo           = models.URLField(verbose_name="Фото", blank = True)
    phoneNumber     = models.CharField(max_length = 18, blank = True)
    role            = models.CharField(verbose_name = "Роль", choices = CHOICES_OF_ROLE, default = PARTICIPANT, max_length = 20)
    emailConfirmed  = models.BooleanField(verbose_name = "Email подтвержден", default = False)

    is_active       = models.BooleanField(default=True, verbose_name="Аккаунт действует")
    is_staff        = models.BooleanField(default=False, verbose_name="Сотрудник")
    date_joined     = models.DateTimeField(default=timezone.now)

    objects         = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'phoneNumber', 'role']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

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
    eduInstitution  = models.OneToOneField(Institution, on_delete = models.CASCADE, related_name = "participant", verbose_name = "Образовательное учреждение", blank = True, null = True) 

    """???"""
    level           = models.CharField(choices = CHOICES_OF_LEVEL, default = CLASS_8, verbose_name = "Класс/курс", max_length = 20, blank = True)
    """???"""

    vkURL           = models.URLField(verbose_name= "Ссылка на vkontakte", blank = True)
    instURL         = models.URLField(verbose_name= "Ссылка на instagram", blank = True)
    fbURL           = models.URLField(verbose_name= "Ссылка на facebook", blank = True)
    passedTests     = models.ManyToManyField(Test, verbose_name = "Завершенные тесты", related_name= "participant", blank = True)
    events          = models.ForeignKey(Progress, on_delete = models.CASCADE, related_name= "participant", verbose_name = "Мероприятия", blank = True, null = True)
    progress        = models.FloatField(verbose_name = "Прогресс", default=0, blank = True)
    mailing         = models.BooleanField(default=False)


    class Meta:
        verbose_name        = "Участник"
        verbose_name_plural = "Участники"
