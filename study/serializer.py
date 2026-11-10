from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from study.models import Lesson, Course, Subscription
from study.validators import YouTubeValidator



class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            YouTubeValidator(field='materials') # Укажите ваше поле
        ]


class CourseSerializer(ModelSerializer):
    count_lesson_course = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = SerializerMethodField()
    class Meta:
        model = Course
        fields = ('id', 'title', 'preview', 'description', 'count_lesson_course', 'lessons', 'is_subscribed')

    def get_count_lesson_course(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """
        Проверяет, подписан ли текущий пользователь на данный курс.
        obj - это текущий экземпляр курса.
        """
        request = self.context.get('request')
        # Если запроса нет или пользователь не авторизован - он ни на что не подписан
        if not request or request.user.is_anonymous:
            return False

        # Проверяем наличие подписки в базе
        return Subscription.objects.filter(user=request.user, course=obj).exists()




class CourseCountLessonSerializer(ModelSerializer):
    # Имя переменной должно совпадать с тем, что мы добавим в fields
    count_lesson_course = SerializerMethodField()

    def get_count_lesson_course(self, obj):
        # obj — это текущий объект Course
        # Используем related_name='lessons' из вашей модели Lesson
        return obj.lessons.count()

    class Meta:
        model = Course
        # Убедитесь, что 'id' и 'preview' тоже здесь, если они нужны в ответе
        fields = ("id", "title", "description", "count_lesson_course")



