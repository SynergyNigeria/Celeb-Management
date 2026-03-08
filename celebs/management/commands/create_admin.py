import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create a superuser from environment variables if none exists."

    def handle(self, *args, **kwargs):
        User = get_user_model()
        email    = os.environ.get("ADMIN_EMAIL",    "admin@gmail.com")
        password = os.environ.get("ADMIN_PASSWORD", "1998runs")
        name     = os.environ.get("ADMIN_NAME",     "Admin")
        country  = os.environ.get("ADMIN_COUNTRY",  "Nigeria")

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("Superuser already exists — skipping.")
            return

        User.objects.create_superuser(email=email, name=name, country=country, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{email}' created successfully."))
