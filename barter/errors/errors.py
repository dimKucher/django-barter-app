from django.views.generic import TemplateView


class ErrorBaseView(TemplateView):
    template_name = "errors/error.html"
    extra_context = {
        "title": "ERROR",
        "description": "Произошла ошибка"
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["exception"] = self.request.resolver_match
        context.setdefault('title', self.extra_context['title'])
        context.setdefault('description', self.extra_context['description'])
        context.update(self.extra_context)
        return context


class Error403View(ErrorBaseView):
    extra_context = {
        "title": "403 ERROR",
        "description": "Недостаточно прав доступа"
    }


class Error404View(ErrorBaseView):
    extra_context = {
        "title": "404 ERROR",
        "description": "Ничего не найдено"
    }


class Error500View(ErrorBaseView):
    extra_context = {
        "title": "500 ERROR",
        "description": "Ошибка на сервере"
    }
