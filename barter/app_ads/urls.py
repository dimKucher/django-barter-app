from django.urls import path
from app_ads import views

app_name = "ads"

urlpatterns = [
    path("create", views.AdsCreate.as_view(), name="create"),
    path("list", views.AdsList.as_view(), name="list"),
    path("list/my", views.AdsUserList.as_view(), name="list_user"),
    path("<int:pk>/detail", views.AdsDetail.as_view(), name="detail"),
    path("<int:pk>/update", views.AdsUpdate.as_view(), name="update"),
    path("<int:pk>/delete", views.AdsDelete.as_view(), name="delete"),
]
