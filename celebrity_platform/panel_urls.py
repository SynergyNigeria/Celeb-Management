from django.urls import path
from .panel_views import (
    panel_dashboard,
    panel_celebrities, panel_celebrity_add, panel_celebrity_edit, panel_celebrity_delete,
    panel_events, panel_event_add, panel_event_edit, panel_event_delete,
    panel_foundations, panel_foundation_add, panel_foundation_edit, panel_foundation_delete,
    panel_tiers, panel_tier_add, panel_tier_edit, panel_tier_delete,
    panel_fans,
    panel_donations,
    panel_payments,
)

urlpatterns = [
    path("",                              panel_dashboard,          name="panel_dashboard"),
    # celebrities
    path("celebrities/",                  panel_celebrities,        name="panel_celebrities"),
    path("celebrities/add/",              panel_celebrity_add,      name="panel_celebrity_add"),
    path("celebrities/<int:pk>/edit/",    panel_celebrity_edit,     name="panel_celebrity_edit"),
    path("celebrities/<int:pk>/delete/",  panel_celebrity_delete,   name="panel_celebrity_delete"),
    # events
    path("events/",                       panel_events,             name="panel_events"),
    path("events/add/",                   panel_event_add,          name="panel_event_add"),
    path("events/<int:pk>/edit/",         panel_event_edit,         name="panel_event_edit"),
    path("events/<int:pk>/delete/",       panel_event_delete,       name="panel_event_delete"),
    # foundations
    path("foundations/",                  panel_foundations,        name="panel_foundations"),
    path("foundations/add/",              panel_foundation_add,     name="panel_foundation_add"),
    path("foundations/<int:pk>/edit/",    panel_foundation_edit,    name="panel_foundation_edit"),
    path("foundations/<int:pk>/delete/",  panel_foundation_delete,  name="panel_foundation_delete"),
    # membership tiers
    path("tiers/",                        panel_tiers,              name="panel_tiers"),
    path("tiers/add/",                    panel_tier_add,           name="panel_tier_add"),
    path("tiers/<int:pk>/edit/",          panel_tier_edit,          name="panel_tier_edit"),
    path("tiers/<int:pk>/delete/",        panel_tier_delete,        name="panel_tier_delete"),
    # fans, donations & payments
    path("fans/",                         panel_fans,               name="panel_fans"),
    path("donations/",                    panel_donations,          name="panel_donations"),
    path("payments/",                     panel_payments,           name="panel_payments"),
]
