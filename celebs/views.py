from django.shortcuts import render, get_object_or_404
from .models import Celebrity


def home_view(request):
    celebs = Celebrity.objects.filter(is_active=True)
    category = request.GET.get("category", "")
    search = request.GET.get("q", "")
    if category:
        celebs = celebs.filter(category=category)
    if search:
        celebs = celebs.filter(name__icontains=search)
    featured = Celebrity.objects.filter(is_active=True, is_featured=True)

    # Stats
    from events.models import Event
    from donations.models import Foundation
    from memberships.models import MembershipPurchase
    total_events = Event.objects.count()
    total_foundations = Foundation.objects.filter(is_active=True).count()
    total_members = MembershipPurchase.objects.filter(is_active=True).count()

    return render(request, "celebs/home.html", {
        "celebs": celebs,
        "featured": featured,
        "category": category,
        "search": search,
        "categories": Celebrity.CATEGORY_CHOICES,
        "total_events": total_events,
        "total_foundations": total_foundations,
        "total_members": total_members,
    })


def celebrity_detail_view(request, slug):
    celeb = get_object_or_404(Celebrity, slug=slug, is_active=True)
    return render(request, "celebs/detail.html", {"celeb": celeb})
