from django.urls import path
from .views import foundations_view, donate_view

urlpatterns = [
    path("", foundations_view, name="foundations"),
    path("<int:foundation_id>/", donate_view, name="donate_foundation"),
]
