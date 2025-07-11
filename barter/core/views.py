from django.views.generic import TemplateView


class MainPage(TemplateView):
    """Класс-представление для отображения главной страницы."""

    template_name = "index.html"
