from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import uuid
from celebs.models import Celebrity
from .models import MembershipTier, MembershipPurchase
from celebrity_platform.notifications import notify_membership_purchase


def membership_list_view(request, slug):
    celeb = get_object_or_404(Celebrity, slug=slug, is_active=True)
    tiers = MembershipTier.objects.filter(celebrity=celeb, is_active=True)
    # Check which tiers the user already holds (active)
    user_tier_ids = set()
    if request.user.is_authenticated:
        user_tier_ids = set(
            MembershipPurchase.objects.filter(
                user=request.user,
                tier__celebrity=celeb,
                is_active=True,
                expires_at__gt=timezone.now(),
            ).values_list("tier_id", flat=True)
        )
    return render(request, "memberships/list.html", {
        "celeb": celeb,
        "tiers": tiers,
        "user_tier_ids": user_tier_ids,
    })


@login_required
def membership_purchase_view(request, tier_id):
    tier = get_object_or_404(MembershipTier, pk=tier_id, is_active=True)
    # Check if already active or pending
    already = MembershipPurchase.objects.filter(
        user=request.user, tier=tier,
        payment_status__in=["pending", "approved"],
    ).exists()
    if already:
        messages.warning(request, "You already have an active or pending membership for this tier.")
        return redirect("membership_list", slug=tier.celebrity.slug)

    if request.method == "POST":
        method = request.POST.get("payment_method", "bank_transfer")
        if method not in ("gift_card", "bank_transfer"):
            method = "bank_transfer"
        ref = f"MEM-{uuid.uuid4().hex[:12].upper()}"
        purchase = MembershipPurchase(
            user=request.user,
            tier=tier,
            transaction_ref=ref,
            amount_paid=tier.price,
            expires_at=timezone.now() + timedelta(days=tier.duration_days),
            payment_method=method,
            payment_status="pending",
            is_active=False,
        )
        if method == "gift_card":
            img = request.FILES.get("gift_card_image")
            if not img:
                messages.error(request, "Please upload your gift card image.")
                return render(request, "memberships/confirm.html", {"tier": tier})
            purchase.gift_card_image = img
            purchase.save()
            notify_membership_purchase(purchase)
            messages.success(request, f"Gift card received for {tier.name} membership. Your membership will activate once verified by our team.")
        else:
            purchase.save()
            notify_membership_purchase(purchase)
            messages.info(request, f"Your {tier.name} membership request (Ref: {ref}) has been saved. Please check your email — {request.user.email} — for our bank account details to complete the transfer.")
        return redirect("dashboard")

    return render(request, "memberships/confirm.html", {"tier": tier})
