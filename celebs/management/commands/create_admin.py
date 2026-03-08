import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create a superuser from environment variables if none exists."

    def handle(self, *args, **kwargs):
        User = get_user_model()
        email    = os.environ.get("ADMIN_EMAIL",    "admin@gmail.com")
        password = os.environ.get("ADMIN_PASSWORD", "1998runs")
        username = email.split("@")[0]

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("Superuser already exists — skipping.")
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{email}' created successfully."))
