from django.db import models

from django.conf import settings


class Course(models.Model):
    title = models.CharField(
        max_length=55, verbose_name="Название курса", blank=True, null=True
    )
    preview = models.ImageField(
        upload_to="study/preview/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите preview курса",
    )
    description = models.TextField(verbose_name="Описание курса", blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name="Владелец",
        null=True,  # Сначала ставим null=True, чтобы миграция прошла без ошибок, если есть старые данные
        blank=True
    )
    stripe_price_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID цены в Stripe",
        help_text="Сюда нужно вставить price_... из панели Stripe"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена курса",
        default=0.00
    )

    def __str__(self):
        return self.title or "Без названия"


class Lesson(models.Model):
    title = models.CharField(
        max_length=55, verbose_name="Название урока", blank=True, null=True
    )
    preview = models.ImageField(
        upload_to="study/preview/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите preview урока",
    )
    description = models.TextField(verbose_name="Описание урока", blank=True, null=True)

    video_url = models.URLField(
        max_length=200,
        verbose_name="Ссылка на видео урока",
        blank=True,
        null=True,
    )

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="Владелец",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Курс'
    )

    stripe_session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID сессии Stripe")
    payment_link = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на оплату")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user} - {self.course}'
