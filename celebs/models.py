from django.db import models


class Celebrity(models.Model):
    CATEGORY_CHOICES = [
        ("music", "Music"),
        ("sports", "Sports"),
        ("acting", "Acting"),
        ("comedy", "Comedy"),
        ("politics", "Politics"),
        ("business", "Business"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=255, blank=True)
    bio = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="other")
    photo = models.ImageField(upload_to="celebs/photos/", blank=True, null=True)
    cover_image = models.ImageField(upload_to="celebs/covers/", blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Celebrities"
        ordering = ["-is_featured", "name"]

    def __str__(self):
        return self.name
