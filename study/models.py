from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=25, verbose_name='Название курса', blank=True, null=True)
    preview = models.ImageField(upload_to='study/preview/', verbose_name='Аватар', blank=True, null=True,
                               help_text='Загрузите preview курса')
    description = models.TextField(verbose_name='Описание курса', blank=True, null=True)

class Lesson(models.Model):
    title = models.CharField(max_length=25, verbose_name='Название урока', blank=True, null=True)
    preview = models.ImageField(upload_to='study/preview/', verbose_name='Аватар', blank=True, null=True,
                               help_text='Загрузите preview урока')
    description = models.TextField(verbose_name='Описание урока', blank=True, null=True)

    video_url = models.URLField(max_length=200, verbose_name='Ссылка на видео урока', blank=True, null=True,)