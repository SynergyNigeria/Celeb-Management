from django.urls import path
from .views import events_list_view, event_detail_view, event_register_view

urlpatterns = [
    path("", events_list_view, name="events_list"),
    path("register/<int:event_id>/", event_register_view, name="event_register"),
    path("<slug:celeb_slug>/<slug:slug>/", event_detail_view, name="event_detail"),
]
