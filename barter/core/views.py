from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from app_ads import models
from errors import errors


class MainPage(TemplateView):
    template_name = "main.html"


# class MainPage(ListView):
#     """Класс-представление для отображения главной страницы."""
#     model = models.AdsItem
#     template_name = "ads/ads_list.html"
#     paginate_by = 5
#     extra_context = {
#         "title": "Список всех товаров",
#         "empty_message": "Тут ничего нет 🙁"
#     }
#
#     def get_queryset(self) -> QuerySet[models.AdsItem]:
#         """Функция возвращает список товаров из БД."""
#         try:
#             if self.request.user.is_authenticated:
#                 object_list = (models.AdsItem.objects
#                                .exclude(user=self.request.user)
#                                .order_by("-created_at"))
#             else:
#                 object_list = (models.AdsItem.objects.
#                                order_by("-created_at"))
#             return object_list
#         except ObjectDoesNotExist:
#             raise Http404("Объявлений нет")
#

def http_403(request, exception):
    view = errors.Error403View.as_view()
    return view(request, status=403)


def http_404(request, exception):
    view = errors.Error404View.as_view()
    return view(request, status=404)


def http_500(request):
    view = errors.Error500View.as_view()
    return view(request, status=500)
