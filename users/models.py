from django.contrib.auth.models import AbstractUser
from django.db import models


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
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_payment = models.DateField()