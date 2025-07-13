from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist


class MixinPaginator:
    """Оптимизированный класс для работы с пагинацией."""

    def __init__(self, object_list, per_page=10):
        """Инициализация с установкой размера страницы по умолчанию."""
        self.paginator = Paginator(object_list, per_page)

    def get_page(self, request):
        """Получение страницы с обработкой исключений."""
        try:
            page_number = int(request.GET.get("page", 1))
            return self.paginator.page(page_number)
        except (PageNotAnInteger, ObjectDoesNotExist):
            return self.paginator.page(1)
        except EmptyPage:
            return self.paginator.page(self.paginator.num_pages)