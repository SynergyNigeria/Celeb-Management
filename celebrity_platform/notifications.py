"""
Notification helpers — sends admin alert emails whenever a user submits
a payment (membership, donation, event registration).

All functions are fire-and-forget: they swallow exceptions so that a
broken email config never crashes the user-facing request.
"""
import logging
import threading
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

ADMIN_EMAIL = getattr(settings, "ADMIN_NOTIFICATION_EMAIL", "")


def _send(subject: str, body: str) -> None:
    """Internal sender — runs in a background thread so it never blocks the request."""
    if not ADMIN_EMAIL:
        logger.warning("ADMIN_NOTIFICATION_EMAIL is not configured. Skipping notification.")
        return

    def _do_send():
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as exc:
            logger.exception("Failed to send admin notification email: %s", exc)

    threading.Thread(target=_do_send, daemon=True).start()


# ─────────────────────────────────────────────────────────────────────────────
# MEMBERSHIP
# ─────────────────────────────────────────────────────────────────────────────

def notify_membership_purchase(purchase) -> None:
    """Fired after a new MembershipPurchase is saved."""
    user  = purchase.user
    tier  = purchase.tier
    celeb = tier.celebrity
    method_display = "Gift Card" if purchase.payment_method == "gift_card" else "Bank Transfer"

    subject = f"[StarHub] New Membership — {user.name or user.email} → {tier.name} ({celeb.name})"
    body = f"""A new membership purchase is awaiting verification.

User:        {user.name or '—'} <{user.email}>
Celebrity:   {celeb.name}
Tier:        {tier.name}
Amount:      ${tier.price}
Duration:    {tier.duration_days} days
Ref:         {purchase.transaction_ref}
Method:      {method_display}
Status:      {purchase.payment_status.upper()}

{'A gift card image was uploaded — check the admin panel to review it.' if purchase.payment_method == 'gift_card' else 'User is awaiting your bank account details.'}

Admin panel: {settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS[0] != '*' else 'your-domain.com'}/manage/
"""
    _send(subject, body)


# ─────────────────────────────────────────────────────────────────────────────
# DONATION
# ─────────────────────────────────────────────────────────────────────────────

def notify_donation(donation) -> None:
    """Fired after a new Donation is saved."""
    user       = donation.user
    foundation = donation.foundation
    celeb      = foundation.celebrity
    donor_name = "Anonymous" if donation.is_anonymous else (user.name or user.email)
    method_display = "Gift Card" if donation.payment_method == "gift_card" else "Bank Transfer"

    subject = f"[StarHub] New Donation — {donor_name} → ${donation.amount} to {foundation.name}"
    body = f"""A new donation is awaiting verification.

Donor:       {donor_name} <{user.email}>
Foundation:  {foundation.name}
Celebrity:   {celeb.name}
Amount:      ${donation.amount}
Ref:         {donation.transaction_ref}
Method:      {method_display}
Status:      {donation.payment_status.upper()}
Anonymous:   {'Yes' if donation.is_anonymous else 'No'}
{f'Message:     {donation.message}' if donation.message else ''}

{'A gift card image was uploaded — check the admin panel to review it.' if donation.payment_method == 'gift_card' else 'User is awaiting your bank account details.'}

Admin panel: {settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS[0] != '*' else 'your-domain.com'}/manage/
"""
    _send(subject, body)


# ─────────────────────────────────────────────────────────────────────────────
# EVENT REGISTRATION
# ─────────────────────────────────────────────────────────────────────────────

def notify_event_registration(registration) -> None:
    """Fired after a new EventRegistration is saved."""
    user   = registration.user
    event  = registration.event
    celeb  = event.celebrity
    method_display = {
        "free":          "Free",
        "gift_card":     "Gift Card",
        "bank_transfer": "Bank Transfer",
    }.get(registration.payment_method, registration.payment_method)

    subject = f"[StarHub] Event Registration — {user.name or user.email} → {event.title}"
    body = f"""A new event registration has been submitted.

User:        {user.name or '—'} <{user.email}>
Event:       {event.title}
Celebrity:   {celeb.name}
Date:        {event.event_date.strftime('%B %d, %Y at %I:%M %p')}
Location:    {event.location}{f', {event.city}' if event.city else ''}{f', {event.country}' if event.country else ''}
Ticket:      {'Free' if event.is_free else f'${registration.amount_paid}'}
Ref:         {registration.transaction_ref}
Method:      {method_display}
Status:      {registration.payment_status.upper()}

{'Automatically approved (free event).' if event.is_free else ('A gift card image was uploaded — check the admin panel to review it.' if registration.payment_method == 'gift_card' else 'User is awaiting your bank account details.')}

Admin panel: {settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS[0] != '*' else 'your-domain.com'}/manage/
"""
    _send(subject, body)


# ─────────────────────────────────────────────────────────────────────────────
# USER-FACING: payment decision notifications
# Called by the admin panel after approving or rejecting a payment.
# Emails go TO the user, not to the admin.
# ─────────────────────────────────────────────────────────────────────────────

def _send_to_user(subject: str, body: str, user_email: str) -> None:
    """Send an email to the user in a background thread so it never blocks the request."""
    def _do_send():
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )
        except Exception as exc:
            logger.exception("Failed to send user notification email to %s: %s", user_email, exc)

    threading.Thread(target=_do_send, daemon=True).start()


def notify_user_membership_decision(purchase, approved: bool) -> None:
    """Email the user after admin approves or rejects their membership."""
    user  = purchase.user
    tier  = purchase.tier
    celeb = tier.celebrity
    status_word = "Approved" if approved else "Rejected"

    subject = f"[StarHub] Membership {status_word} — {tier.name} ({celeb.name})"
    if approved:
        body = f"""Hi {user.name or user.email},

Great news! Your {tier.name} membership for {celeb.name} has been approved.

Details:
  Membership:   {tier.name}
  Celebrity:    {celeb.name}
  Duration:     {tier.duration_days} days
  Ref:          {purchase.transaction_ref}
  Amount Paid:  ${purchase.amount_paid}

Your membership is now active. Enjoy the exclusive benefits!

Thanks for being a fan,
The StarHub Team
"""
    else:
        body = f"""Hi {user.name or user.email},

We're sorry to inform you that your {tier.name} membership request for {celeb.name} could not be verified.

Ref: {purchase.transaction_ref}

If you believe this is a mistake or need assistance, please reply to this email.

The StarHub Team
"""
    _send_to_user(subject, body, user.email)


def notify_user_donation_decision(donation, approved: bool) -> None:
    """Email the user after admin approves or rejects their donation."""
    user       = donation.user
    foundation = donation.foundation
    celeb      = foundation.celebrity
    status_word = "Confirmed" if approved else "Rejected"

    subject = f"[StarHub] Donation {status_word} — ${donation.amount} to {foundation.name}"
    if approved:
        body = f"""Hi {user.name or user.email},

Thank you! Your donation to {foundation.name} has been confirmed.

Details:
  Foundation:  {foundation.name}
  Celebrity:   {celeb.name}
  Amount:      ${donation.amount}
  Ref:         {donation.transaction_ref}

Your generosity makes a real difference. Thank you for your support!

The StarHub Team
"""
    else:
        body = f"""Hi {user.name or user.email},

We were unable to verify your ${donation.amount} donation to {foundation.name}.

Ref: {donation.transaction_ref}

If you believe this is a mistake or need assistance, please reply to this email.

The StarHub Team
"""
    _send_to_user(subject, body, user.email)


def notify_user_event_decision(registration, approved: bool) -> None:
    """Email the user after admin approves or rejects their event registration."""
    user  = registration.user
    event = registration.event
    celeb = event.celebrity
    status_word = "Confirmed" if approved else "Rejected"

    subject = f"[StarHub] Registration {status_word} — {event.title}"
    if approved:
        body = f"""Hi {user.name or user.email},

You're all set! Your registration for {event.title} has been confirmed.

Details:
  Event:       {event.title}
  Celebrity:   {celeb.name}
  Date:        {event.event_date.strftime('%B %d, %Y at %I:%M %p')}
  Location:    {event.location}{f', {event.city}' if event.city else ''}{f', {event.country}' if event.country else ''}
  Ticket Ref:  {registration.transaction_ref}
  Amount:      {'Free' if event.is_free else f'${registration.amount_paid}'}

See you there!

The StarHub Team
"""
    else:
        body = f"""Hi {user.name or user.email},

We were unable to verify your payment for {event.title}.

Ref: {registration.transaction_ref}

If you believe this is a mistake or need assistance, please reply to this email.

The StarHub Team
"""
    _send_to_user(subject, body, user.email)
