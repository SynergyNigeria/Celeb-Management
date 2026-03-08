from django.urls import path
from .views import membership_list_view, membership_purchase_view

urlpatterns = [
    path("<slug:slug>/", membership_list_view, name="membership_list"),
    path("buy/<int:tier_id>/", membership_purchase_view, name="membership_purchase"),
]
