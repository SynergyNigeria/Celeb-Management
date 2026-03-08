from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Sum, Count
from django.utils import timezone

from celebs.models import Celebrity
from memberships.models import MembershipTier, MembershipPurchase
from donations.models import Foundation, Donation
from events.models import Event, EventRegistration
from users.models import User
from .panel_forms import CelebrityForm, MembershipTierForm, FoundationForm, EventForm
from .notifications import (
    notify_user_membership_decision,
    notify_user_donation_decision,
    notify_user_event_decision,
)


# ─── DASHBOARD ────────────────────────────────────────────────────────────────

@staff_member_required(login_url="/auth/login/")
def panel_dashboard(request):
    stats = {
        "celebrities":   Celebrity.objects.count(),
        "fans":          User.objects.filter(is_staff=False).count(),
        "events":        Event.objects.count(),
        "foundations":   Foundation.objects.count(),
        "tiers":         MembershipTier.objects.count(),
        "memberships":   MembershipPurchase.objects.count(),
        "donations":     Donation.objects.count(),
        "total_donated": Donation.objects.aggregate(t=Sum("amount"))["t"] or 0,
        "upcoming_events": Event.objects.filter(status="upcoming", event_date__gte=timezone.now()).count(),
    }
    recent_donations = Donation.objects.select_related("user", "foundation__celebrity").order_by("-donated_at")[:8]
    recent_fans = User.objects.filter(is_staff=False).order_by("-date_joined")[:8]
    upcoming_events = Event.objects.filter(status="upcoming").select_related("celebrity").order_by("event_date")[:5]
    return render(request, "panel/dashboard.html", {
        "stats": stats,
        "recent_donations": recent_donations,
        "recent_fans": recent_fans,
        "upcoming_events": upcoming_events,
    })


# ─── CELEBRITIES ──────────────────────────────────────────────────────────────

@staff_member_required(login_url="/auth/login/")
def panel_celebrities(request):
    celebs = Celebrity.objects.annotate(
        member_count=Count("membership_tiers__purchases", distinct=True),
        event_count=Count("events", distinct=True),
    ).order_by("-is_featured", "name")
    return render(request, "panel/celebrities.html", {"celebs": celebs})


@staff_member_required(login_url="/auth/login/")
def panel_celebrity_add(request):
    form = CelebrityForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        celeb = form.save(commit=False)
        if not celeb.slug:
            celeb.slug = slugify(celeb.name)
        celeb.save()
        messages.success(request, f"'{celeb.name}' added successfully.")
        return redirect("panel_celebrities")
    return render(request, "panel/celebrity_form.html", {"form": form, "action": "Add Celebrity"})


@staff_member_required(login_url="/auth/login/")
def panel_celebrity_edit(request, pk):
    celeb = get_object_or_404(Celebrity, pk=pk)
    form = CelebrityForm(request.POST or None, request.FILES or None, instance=celeb)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"'{celeb.name}' updated.")
        return redirect("panel_celebrities")
    return render(request, "panel/celebrity_form.html", {"form": form, "action": f"Edit — {celeb.name}", "obj": celeb})


@staff_member_required(login_url="/auth/login/")
def panel_celebrity_delete(request, pk):
    celeb = get_object_or_404(Celebrity, pk=pk)
    if request.method == "POST":
        name = celeb.name
        celeb.delete()
        messages.success(request, f"'{name}' deleted.")
        return redirect("panel_celebrities")
    return render(request, "panel/confirm_delete.html", {"obj": celeb, "obj_type": "Celebrity", "cancel_url": "panel_celebrities"})


# ─── EVENTS ───────────────────────────────────────────────────────────────────

@staff_member_required(login_url="/auth/login/")
def panel_events(request):
    events = Event.objects.select_related("celebrity").annotate(reg_count=Count("registrations")).order_by("event_date")
    return render(request, "panel/events.html", {"events": events})


@staff_member_required(login_url="/auth/login/")
def panel_event_add(request):
    form = EventForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        ev = form.save(commit=False)
        if not ev.slug:
            ev.slug = slugify(ev.title)
        ev.save()
        messages.success(request, f"Event '{ev.title}' created.")
        return redirect("panel_events")
    return render(request, "panel/event_form.html", {"form": form, "action": "Add Event"})


@staff_member_required(login_url="/auth/login/")
def panel_event_edit(request, pk):
    ev = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, request.FILES or None, instance=ev)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Event '{ev.title}' updated.")
        return redirect("panel_events")
    return render(request, "panel/event_form.html", {"form": form, "action": f"Edit — {ev.title}", "obj": ev})


@staff_member_required(login_url="/auth/login/")
def panel_event_delete(request, pk):
    ev = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        title = ev.title
        ev.delete()
        messages.success(request, f"Event '{title}' deleted.")
        return redirect("panel_events")
    return render(request, "panel/confirm_delete.html", {"obj": ev, "obj_type": "Event", "cancel_url": "panel_events"})


# ─── FOUNDATIONS ──────────────────────────────────────────────────────────────

@staff_member_required(login_url="/auth/login/")
def panel_foundations(request):
    foundations = Foundation.objects.select_related("celebrity").order_by("celebrity__name", "name")
    return render(request, "panel/foundations.html", {"foundations": foundations})


@staff_member_required(login_url="/auth/login/")
def panel_foundation_add(request):
    form = FoundationForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        f = form.save()
        messages.success(request, f"Foundation '{f.name}' created.")
        return redirect("panel_foundations")
    return render(request, "panel/foundation_form.html", {"form": form, "action": "Add Foundation"})


@staff_member_required(login_url="/auth/login/")
def panel_foundation_edit(request, pk):
    foundation = get_object_or_404(Foundation, pk=pk)
    form = FoundationForm(request.POST or None, request.FILES or None, instance=foundation)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Foundation '{foundation.name}' updated.")
        return redirect("panel_foundations")
    return render(request, "panel/foundation_form.html", {"form": form, "action": f"Edit — {foundation.name}", "obj": foundation})


@staff_member_required(login_url="/auth/login/")
def panel_foundation_delete(request, pk):
    foundation = get_object_or_404(Foundation, pk=pk)
    if request.method == "POST":
        name = foundation.name
        foundation.delete()
        messages.success(request, f"Foundation '{name}' deleted.")
        return redirect("panel_foundations")
    return render(request, "panel/confirm_delete.html", {"obj": foundation, "obj_type": "Foundation", "cancel_url": "panel_foundations"})


# ─── MEMBERSHIP TIERS ─────────────────────────────────────────────────────────

@staff_member_required(login_url="/auth/login/")
def panel_tiers(request):
    tiers = MembershipTier.objects.select_related("celebrity").annotate(purchase_count=Count("purchases")).order_by("celebrity__name", "price")
    return render(request, "panel/tiers.html", {"tiers": tiers})


@staff_member_required(login_url="/auth/login/")
def panel_tier_add(request):
    form = MembershipTierForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        tier = form.save()
        messages.success(request, f"Tier '{tier.name}' created.")
        return redirect("panel_tiers")
    return render(request, "panel/tier_form.html", {"form": form, "action": "Add Membership Tier"})


@staff_member_required(login_url="/auth/login/")
def panel_tier_edit(request, pk):
    tier = get_object_or_404(MembershipTier, pk=pk)
    form = MembershipTierForm(request.POST or None, instance=tier)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Tier '{tier.name}' updated.")
        return redirect("panel_tiers")
    return render(request, "panel/tier_form.html", {"form": form, "action": f"Edit — {tier.name}", "obj": tier})


@staff_member_required(login_url="/auth/login/")
def panel_tier_delete(request, pk):
    tier = get_object_or_404(MembershipTier, pk=pk)
    if request.method == "POST":
        name = tier.name
        tier.delete()
        messages.success(request, f"Tier '{name}' deleted.")
        return redirect("panel_tiers")
    return render(request, "panel/confirm_delete.html", {"obj": tier, "obj_type": "Membership Tier", "cancel_url": "panel_tiers"})


# ─── FANS ─────────────────────────────────────────────────────────────────────

@staff_member_required(login_url="/auth/login/")
def panel_fans(request):
    fans = User.objects.filter(is_staff=False).annotate(
        membership_count=Count("memberships", distinct=True),
        donation_count=Count("donations", distinct=True),
    ).order_by("-date_joined")
    return render(request, "panel/fans.html", {"fans": fans})


# ─── DONATIONS ────────────────────────────────────────────────────────────────

@staff_member_required(login_url="/auth/login/")
def panel_donations(request):
    donations = Donation.objects.select_related("user", "foundation__celebrity").order_by("-donated_at")
    total = donations.aggregate(t=Sum("amount"))["t"] or 0
    return render(request, "panel/donations.html", {"donations": donations, "total": total})


# ─── PAYMENTS ─────────────────────────────────────────────────────────────────

@staff_member_required(login_url="/auth/login/")
def panel_payments(request):
    if request.method == "POST":
        model_type = request.POST.get("model_type")
        pk = request.POST.get("pk")
        action = request.POST.get("action")  # "approve" or "reject"

        if model_type == "membership":
            obj = get_object_or_404(MembershipPurchase, pk=pk)
            if action == "approve":
                obj.payment_status = "approved"
                obj.is_active = True
                obj.save()
                notify_user_membership_decision(obj, approved=True)
                messages.success(request, f"Membership #{pk} approved. User notified by email.")
            elif action == "reject":
                obj.payment_status = "rejected"
                obj.is_active = False
                obj.save()
                notify_user_membership_decision(obj, approved=False)
                messages.warning(request, f"Membership #{pk} rejected. User notified by email.")

        elif model_type == "donation":
            obj = get_object_or_404(Donation, pk=pk)
            if action == "approve":
                obj.payment_status = "approved"
                obj.save()  # save() recalculates amount_raised
                notify_user_donation_decision(obj, approved=True)
                messages.success(request, f"Donation #{pk} approved. User notified by email.")
            elif action == "reject":
                obj.payment_status = "rejected"
                obj.save()
                notify_user_donation_decision(obj, approved=False)
                messages.warning(request, f"Donation #{pk} rejected. User notified by email.")

        elif model_type == "event":
            obj = get_object_or_404(EventRegistration, pk=pk)
            if action == "approve":
                obj.payment_status = "approved"
                obj.save()
                # Increment seats_booked on the event
                event = obj.event
                event.seats_booked = (event.seats_booked or 0) + 1
                event.save()
                notify_user_event_decision(obj, approved=True)
                messages.success(request, f"Event registration #{pk} approved. User notified by email.")
            elif action == "reject":
                obj.payment_status = "rejected"
                obj.save()
                notify_user_event_decision(obj, approved=False)
                messages.warning(request, f"Event registration #{pk} rejected. User notified by email.")

        return redirect("panel_payments")

    pending_memberships = MembershipPurchase.objects.filter(
        payment_status="pending"
    ).select_related("user", "tier__celebrity").order_by("-purchased_at")

    pending_donations = Donation.objects.filter(
        payment_status="pending"
    ).select_related("user", "foundation__celebrity").order_by("-donated_at")

    pending_events = EventRegistration.objects.filter(
        payment_status="pending"
    ).select_related("user", "event__celebrity").order_by("-registered_at")

    return render(request, "panel/payments.html", {
        "pending_memberships": pending_memberships,
        "pending_donations": pending_donations,
        "pending_events": pending_events,
    })
