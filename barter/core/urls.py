from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from barter.core.views import MainPage

handler403 = "core.views.http_403"
handler404 = "core.views.http_404"
handler500 = "core.views.http_500"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", MainPage.as_view(), name="main"),
    path("accounts/", include(("app_user.urls", "ads"), namespace="app_user")),
    path("ads/", include(("app_ads.urls", "ads"), namespace="app_ads")),
    path("proposal/", include(("app_proposal.urls", "proposal"), namespace="app_proposal")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
