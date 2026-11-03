from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from study.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

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
        fields = ('id', 'title', 'description', 'count_lesson_course')


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'