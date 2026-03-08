from django.urls import path
from .views import home_view, celebrity_detail_view

urlpatterns = [
    path("", home_view, name="home"),
    path("celebrity/<slug:slug>/", celebrity_detail_view, name="celeb_detail"),
]
