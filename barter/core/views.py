from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from app_ads import models
from errors import errors


class MainPage(TemplateView):
    template_name = "main.html"


def http_403(request, exception):
    view = errors.Error403View.as_view()
    return view(request, status=403)


def http_404(request, exception):
    view = errors.Error404View.as_view()
    return view(request, status=404)


def http_500(request):
    view = errors.Error500View.as_view()
    return view(request, status=500)
