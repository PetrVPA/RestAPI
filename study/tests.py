from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from study.models import Course, Lesson, Subscription
from users.models import Student


class StudyTest(APITestCase):

    def setUp(self):
        self.user = Student.objects.create(email='meteor@mail.ru', password='12345')
        self.course = Course.objects.create(title='Преступление и наказание', description = 'Разговоры за жизнь')
        self.lesson = Lesson.objects.create(title= 'Суть проблемы', description = 'Жизнь идет ничего не меняется', owner = self.user, course=self.course )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('study:lesson-detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get('title'), self.lesson.title)

    def test_lesson_create(self):
        url = reverse('study:lesson_create')
        data = {
            'title':'В гостях у сказки',
            'course': self.course.id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

    def test_lesson_update(self):
        url = reverse('study:lesson_update', args=(self.lesson.pk,))
        data = {
            'title': 'Сказание об Игоре',
            'course': self.course.id
        }
        response = self.client.patch(url, data=data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), 'Сказание об Игоре'
        )

    def test_lesson_delete(self):
        url = reverse('study:lesson_delete', args=(self.lesson.pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            0
        )

    def test_subscribe_to_course(self):
        """Пользователь может подписаться на курс."""
        self.client.force_authenticate(user=self.user)
        url = reverse('study:subscribe')
        data = {'course_id': self.course.id}

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')

        # Проверяем, что подписка есть в БД
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        """Повторный запрос на подписку удаляет её."""
        # Сначала создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        url = reverse('study:subscribe')
        data = {'course_id': self.course.id}

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')

        # Проверяем, что подписки больше нет
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
