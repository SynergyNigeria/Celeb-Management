from django.db import models
from celebs.models import Celebrity
from django.conf import settings


class Foundation(models.Model):
    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE, related_name="foundations")
    name = models.CharField(max_length=200)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount_raised = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cover_image = models.ImageField(upload_to="foundations/", blank=True, null=True)
    cause_type = models.CharField(max_length=100, blank=True, help_text="E.g. Education, Health, Disaster Relief")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.celebrity.name} — {self.name}"

    @property
    def progress_pct(self):
        if self.target_amount == 0:
            return 0
        return round((float(self.amount_raised) / float(self.target_amount)) * 100, 1)


class Donation(models.Model):
    PAYMENT_METHODS = [
        ("gift_card", "Gift Card"),
        ("bank_transfer", "Bank Transfer"),
    ]
    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="donations")
    foundation = models.ForeignKey(Foundation, on_delete=models.CASCADE, related_name="donations")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True)
    transaction_ref = models.CharField(max_length=100, unique=True)
    donated_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="bank_transfer")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")
    gift_card_image = models.ImageField(upload_to="gift_cards/donations/", blank=True, null=True)

    class Meta:
        ordering = ["-donated_at"]

    def __str__(self):
        name = "Anonymous" if self.is_anonymous else (self.user.name if self.user else "Deleted User")
        return f"{name} donated ${self.amount} to {self.foundation.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Only count approved donations toward amount_raised
        from django.db.models import Sum
        total = self.foundation.donations.filter(payment_status="approved").aggregate(total=Sum("amount"))["total"] or 0
        Foundation.objects.filter(pk=self.foundation_id).update(amount_raised=total)
