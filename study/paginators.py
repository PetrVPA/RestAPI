# study/paginators.py (или users/paginators.py)
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    # Количество элементов на странице по умолчанию
    page_size = 3

    # Позволяет клиенту самому задавать размер страницы через GET-параметр (например, ?page_size=10)
    page_size_query_param = 'page_size'

    # Максимальное количество элементов на странице (чтобы клиент не запросил сразу 100000 записей)
    max_page_size = 50