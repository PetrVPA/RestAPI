from django.contrib.auth.models import AbstractUser
from django.db import models

import study
from config import settings


class Student(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    city = models.CharField(max_length=25, verbose_name="Город", blank=True, null=True)
    avatar = models.ImageField(
        upload_to="study/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите свой аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return self.email


class Payment(models.Model):
    TYPE_CHOICES = (
        ("course", "Курс"),
        ("lesson", "Урок"),
    )
    OPTION_CHOICES = (
        ("cash", "Наличные"),
        ("translation", "Перевод"),
        ("stripe", "Stripe (Карта)"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <--- Правильный способ для кастомных юзеров
        on_delete=models.CASCADE,
        verbose_name="Студент"
    )

    date_payment = models.DateField(null=True, blank=True)

    category_payment = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default="course"
    )
    study_course = models.ForeignKey(
        to = "study.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
    )
    study_lesson = models.ForeignKey(
        to ="study.Lesson",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
    )
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_option = models.CharField(
        max_length=20, choices=OPTION_CHOICES, default="stripe"
    )

    stripe_session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID сессии Stripe")
    payment_link = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на оплату")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
