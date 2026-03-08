from django.db import models
from celebs.models import Celebrity
from django.conf import settings


class Event(models.Model):
    EVENT_TYPES = [
        ("concert", "Concert"),
        ("meetgreet", "Meet & Greet"),
        ("charity", "Charity Event"),
        ("premiere", "Movie Premiere"),
        ("sports", "Sports Event"),
        ("workshop", "Workshop"),
        ("virtual", "Virtual Event"),
        ("other", "Other"),
    ]
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, default="other")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")
    event_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=300)
    venue = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_free = models.BooleanField(default=False)
    seats_total = models.PositiveIntegerField(default=0, help_text="0 means unlimited")
    seats_booked = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["event_date"]
        unique_together = [["celebrity", "slug"]]

    def __str__(self):
        return f"{self.celebrity.name} — {self.title}"

    @property
    def seats_available(self):
        if self.seats_total == 0:
            return None  # unlimited
        return max(0, self.seats_total - self.seats_booked)


class EventRegistration(models.Model):
    PAYMENT_METHODS = [
        ("gift_card", "Gift Card"),
        ("bank_transfer", "Bank Transfer"),
        ("free", "Free"),
    ]
    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="event_registrations")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    transaction_ref = models.CharField(max_length=100, unique=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="free")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")
    gift_card_image = models.ImageField(upload_to="gift_cards/events/", blank=True, null=True)

    class Meta:
        unique_together = [["user", "event"]]
        ordering = ["-registered_at"]

    def __str__(self):
        return f"{self.user.name} → {self.event.title}"
