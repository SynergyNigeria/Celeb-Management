from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import RegisterForm, LoginForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.name}! Your account has been created.")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get("next") or request.GET.get("next") or "dashboard"
            return redirect(next_url)
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard_view(request):
    user = request.user
    memberships = user.memberships.select_related("tier__celebrity").order_by("-purchased_at")
    donations = user.donations.select_related("foundation__celebrity").order_by("-donated_at")
    event_regs = user.event_registrations.select_related("event__celebrity").order_by("-registered_at")
    now = timezone.now()
    return render(request, "users/dashboard.html", {
        "user": user,
        "memberships": memberships,
        "donations": donations,
        "event_regs": event_regs,
        "now": now,
    })
