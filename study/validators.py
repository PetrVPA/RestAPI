from django.core.exceptions import ValidationError
from urllib.parse import urlparse


class YouTubeValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        # Если пришел словарь (валидация всего объекта)
        if isinstance(value, dict):
            url = value.get(self.field)
        # Если пришла строка (валидация конкретного поля)
        else:
            url = value

        # Если поле пустое, пропускаем проверку
        if not url:
            return

        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        if domain and not domain.endswith('youtube.com'):
            raise ValidationError(
                'Ссылки на сторонние ресурсы запрещены. Разрешены только ссылки на youtube.com.'
            )