from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def health_check(request):
    """Lightweight ping endpoint — used by Cloudflare Worker cron to keep the
    Render free-tier server warm and prevent cold starts."""
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("admin/", admin.site.urls),
    path("manage/", include("celebrity_platform.panel_urls")),
    path("auth/", include("users.urls")),
    path("", include("celebs.urls")),
    path("membership/", include("memberships.urls")),
    path("donations/", include("donations.urls")),
    path("events/", include("events.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
