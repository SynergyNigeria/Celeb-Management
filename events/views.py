from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import uuid
from celebs.models import Celebrity
from .models import Event, EventRegistration
from celebrity_platform.notifications import notify_event_registration


def events_list_view(request):
    slug = request.GET.get("celeb", "")
    status_filter = request.GET.get("status", "")
    search = request.GET.get("q", "")
    celebs = Celebrity.objects.filter(is_active=True)
    events = Event.objects.select_related("celebrity").all()
    if slug:
        events = events.filter(celebrity__slug=slug)
    if status_filter:
        events = events.filter(status=status_filter)
    if search:
        events = events.filter(title__icontains=search)
    return render(request, "events/list.html", {
        "events": events,
        "celebs": celebs,
        "selected_slug": slug,
        "status_filter": status_filter,
        "search": search,
        "status_choices": Event.STATUS_CHOICES,
    })


def event_detail_view(request, celeb_slug, slug):
    celeb = get_object_or_404(Celebrity, slug=celeb_slug, is_active=True)
    event = get_object_or_404(Event, celebrity=celeb, slug=slug)
    is_registered = False
    if request.user.is_authenticated:
        is_registered = EventRegistration.objects.filter(user=request.user, event=event).exists()
    return render(request, "events/detail.html", {
        "event": event,
        "celeb": celeb,
        "is_registered": is_registered,
    })


@login_required
def event_register_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if EventRegistration.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, "You are already registered for this event.")
        return redirect("event_detail", celeb_slug=event.celebrity.slug, slug=event.slug)
    if event.status != "upcoming":
        messages.error(request, "This event is not open for registration.")
        return redirect("event_detail", celeb_slug=event.celebrity.slug, slug=event.slug)
    if request.method == "POST":
        ref = f"EVT-{uuid.uuid4().hex[:12].upper()}"
        amount = 0 if event.is_free else event.ticket_price

        if event.is_free:
            # Free events: auto-approve, increment seats immediately
            reg_free = EventRegistration.objects.create(
                user=request.user,
                event=event,
                transaction_ref=ref,
                amount_paid=0,
                payment_method="free",
                payment_status="approved",
            )
            Event.objects.filter(pk=event.pk).update(seats_booked=event.seats_booked + 1)
            notify_event_registration(reg_free)
            messages.success(request, f"You're registered for {event.title}!")
            return redirect("dashboard")

        # Paid event: require payment method
        method = request.POST.get("payment_method", "bank_transfer")
        if method not in ("gift_card", "bank_transfer"):
            method = "bank_transfer"
        registration = EventRegistration(
            user=request.user,
            event=event,
            transaction_ref=ref,
            amount_paid=amount,
            payment_method=method,
            payment_status="pending",
        )
        if method == "gift_card":
            img = request.FILES.get("gift_card_image")
            if not img:
                messages.error(request, "Please upload your gift card image.")
                return render(request, "events/confirm.html", {"event": event})
            registration.gift_card_image = img
            registration.save()
            notify_event_registration(registration)
            messages.success(request, f"Gift card received for {event.title} registration. Your spot will be confirmed once verified.")
        else:
            registration.save()
            notify_event_registration(registration)
            messages.info(request, f"Your registration for {event.title} (Ref: {ref}) has been saved. Check your email — {request.user.email} — for our bank account details to complete the ${amount} payment.")
        return redirect("dashboard")
    return render(request, "events/confirm.html", {"event": event})
