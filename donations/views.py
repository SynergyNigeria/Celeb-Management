from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import uuid
from celebs.models import Celebrity
from .models import Foundation, Donation
from .forms import DonationForm
from celebrity_platform.notifications import notify_donation


def foundations_view(request):
    """All foundations, optionally filtered by celebrity."""
    slug = request.GET.get("celeb", "")
    celebs = Celebrity.objects.filter(is_active=True)
    foundations = Foundation.objects.filter(is_active=True).select_related("celebrity")
    if slug:
        foundations = foundations.filter(celebrity__slug=slug)
    return render(request, "donations/foundations.html", {
        "foundations": foundations,
        "celebs": celebs,
        "selected_slug": slug,
    })


@login_required
def donate_view(request, foundation_id):
    foundation = get_object_or_404(Foundation, pk=foundation_id, is_active=True)
    recent = Donation.objects.filter(foundation=foundation, payment_status="approved").order_by("-donated_at")[:10]
    if request.method == "POST":
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            method = request.POST.get("payment_method", "bank_transfer")
            if method not in ("gift_card", "bank_transfer"):
                method = "bank_transfer"
            ref = f"DON-{uuid.uuid4().hex[:12].upper()}"
            donation = Donation(
                user=request.user,
                foundation=foundation,
                amount=form.cleaned_data["amount"],
                message=form.cleaned_data.get("message", ""),
                is_anonymous=form.cleaned_data.get("is_anonymous", False),
                transaction_ref=ref,
                payment_method=method,
                payment_status="pending",
            )
            if method == "gift_card":
                img = request.FILES.get("gift_card_image")
                if not img:
                    messages.error(request, "Please upload your gift card image.")
                    return render(request, "donations/donate.html", {"foundation": foundation, "form": form, "recent": recent})
                donation.gift_card_image = img
                donation.save()
                notify_donation(donation)
                messages.success(request, f"Gift card received for your ${form.cleaned_data['amount']} donation to {foundation.name}. It will be confirmed once verified.")
            else:
                donation.save()
                notify_donation(donation)
                messages.info(request, f"Your donation of ${form.cleaned_data['amount']} to {foundation.name} (Ref: {ref}) has been saved. Check your email — {request.user.email} — for our bank account details.")
            return redirect("donate_foundation", foundation_id=foundation_id)
    else:
        form = DonationForm(initial={"foundation": foundation})
    return render(request, "donations/donate.html", {
        "foundation": foundation,
        "form": form,
        "recent": recent,
    })
