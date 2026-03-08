from django.db import models
from celebs.models import Celebrity
from django.conf import settings


class MembershipTier(models.Model):
    BADGE_COLORS = [
        ("gray", "Gray - Standard"),
        ("blue", "Blue - Premium"),
        ("gold", "Gold - VIP"),
        ("platinum", "Platinum - Elite"),
    ]

    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE, related_name="membership_tiers")
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=365, help_text="Membership duration in days")
    benefits = models.TextField(
        blank=True, help_text="One benefit per line, e.g. VIP Access\nNewsletter"
    )
    badge_color = models.CharField(max_length=20, choices=BADGE_COLORS, default="gray")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return f"{self.celebrity.name} — {self.name}"

    def benefits_list(self):
        return [b.strip() for b in self.benefits.splitlines() if b.strip()]


class MembershipPurchase(models.Model):
    PAYMENT_METHODS = [
        ("gift_card", "Gift Card"),
        ("bank_transfer", "Bank Transfer"),
    ]
    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    tier = models.ForeignKey(MembershipTier, on_delete=models.PROTECT, related_name="purchases")
    transaction_ref = models.CharField(max_length=100, unique=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="bank_transfer")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")
    gift_card_image = models.ImageField(upload_to="gift_cards/memberships/", blank=True, null=True)

    class Meta:
        ordering = ["-purchased_at"]

    def __str__(self):
        return f"{self.user.name} → {self.tier.name} ({self.tier.celebrity.name})"
