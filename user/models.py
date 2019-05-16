from __future__ import unicode_literals
from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

from testing.models import *
from institution.models import Institution
from event.models import *
from user.models import *


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
    photo           = models.TextField(verbose_name="Фото", blank = True)
    phoneNumber     = models.TextField(max_length = 50, blank = True)
    role            = models.CharField(verbose_name = "Роль", choices = CHOICES_OF_ROLE, default = PARTICIPANT, max_length = 20)
    emailConfirmed  = models.BooleanField(verbose_name = "Email подтвержден", default = False)

    is_social       = models.BooleanField(default=False, verbose_name="Зарегистрирован через соц. сеть")
    is_active       = models.BooleanField(default=True, verbose_name="Аккаунт действует")
    is_staff        = models.BooleanField(default=False, verbose_name="Сотрудник")
    date_joined     = models.DateTimeField(default=timezone.now)

    objects         = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'role']

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

    progress    = models.IntegerField(verbose_name = "Прогресс", default = 0)
    competence  = models.ForeignKey(SideCompetence, on_delete = models.CASCADE, verbose_name = "Компетенция", related_name = "progress", blank = True, null = True)
    class Meta:
        verbose_name        = "Прогресс"
        verbose_name_plural = "Прогресс"

    def __str__(self):
        if self.competence != None:
            return "value:{} competence:{}".format(self.progress, self.competence.name)
        else:
            return "value:{}".format(self.progress)

class EventPoints(models.Model):
    """Модель баллов выставленных за мероприятие"""

    points = models.ManyToManyField(Progress, verbose_name = "Баллы", related_name = "event_points", blank = True)
    event  = models.ForeignKey(Event, verbose_name = "Мероприятия", related_name = "event_points", blank = True, on_delete = models.CASCADE)

    class Meta:
        verbose_name        = "Балл мероприятий"
        verbose_name_plural = "Баллы мероприятий"

    def __str__(self):
        return "id: event:{}".format(self.id, self.event.name)

class Participant(models.Model):
    """Модель участника"""

    s1 = "Ученик"
    s2 = "Студент"
    s3 = "Бакалавр"
    s4 = "Магистрант"
    s5 = "Аспирант"
    s6 = "Доцент"
    s7 = "Профессор"
    s8 = "Кандидат цифровых наук"
    s9 = "Доктор цифровых наук"

    CHOICES_OF_STATUS = (
        (s1,"Ученик"),
        (s2,"Студент"),
        (s3,"Бакалавр"),
        (s4,"Магистрант"),
        (s5,"Аспирант"),
        (s6,"Доцент"),
        (s7,"Профессор"),
        (s8,"Кандидат цифровых наук"),
        (s9,"Доктор цифровых наук"),
    )

    CLASS_8     = "8 класс"
    CLASS_9     = "9 класс"
    CLASS_10    = "10 класс"
    CLASS_11    = "11 класс"
    COURSE_1    = "1 курс"
    COURSE_2    = "2 курс"
    COURSE_3    = "3 курс"
    COURSE_4    = "Сотрудник"
    COURSE_5    = "Иное"


    CHOICES_OF_LEVEL = (
        (CLASS_8,"8 класс"), (CLASS_9, "9 класс"), (CLASS_10, "10 класс"),
        (CLASS_11,"11 класс"), (COURSE_1, "1 курс"), (COURSE_2, "2 курс"),
        (COURSE_3, "3 курс"), (COURSE_4, "Сотрудник"), (COURSE_5, "Иное"),
    )

    id              = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True, related_name = "participant", verbose_name = "Пользователь")
    eduInstitution  = models.CharField(max_length = 50,verbose_name = "Учебное учреждение", blank = True, null = True)
    level           = models.CharField(choices = CHOICES_OF_LEVEL, default = CLASS_8, verbose_name = "Класс/курс", max_length = 20, blank = True)
    status          = models.CharField(choices = CHOICES_OF_STATUS, default = s1, verbose_name = "Статус", max_length = 30, blank = True)

    mainCompetence  = models.ForeignKey(MainCompetence, verbose_name = "Основная компетенция", null = True, blank = True, on_delete = models.CASCADE, related_name= "participant" )
    points          = models.IntegerField(verbose_name = "Баллы по основной компетенции", blank = True, null = True)
    progressComp    = models.ManyToManyField(Progress, verbose_name = "Прогресс", blank = True, related_name= "participant")

    events          = models.ManyToManyField(Event, verbose_name = "Мероприятия", related_name = "participant", blank = True)
    pointsEvent     = models.ManyToManyField(EventPoints, verbose_name = "Баллы за мероприятия", related_name = "participant", blank = True)

    vkURL           = models.URLField(verbose_name= "Ссылка на vkontakte", blank = True)
    instURL         = models.URLField(verbose_name= "Ссылка на instagram", blank = True)
    fbURL           = models.URLField(verbose_name= "Ссылка на facebook", blank = True)
    #Временно
    passedTests     = models.ManyToManyField(ResultOfTest, verbose_name = "Результаты тестов", related_name= "participant", blank = True)
    #!!!!!!!!!!!!!
    mailing         = models.BooleanField(default=False)

    class Meta:
        verbose_name        = "Участник"
        verbose_name_plural = "Участники"
