from django.urls import path
from app_ads import views

app_name = "ads"

urlpatterns = [
    path("/create", views.AdsCreate.as_view(), name="create_ads"),
    path("/list", views.AdsList.as_view(), name="list_ads"),
]
