from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "index.html")


def aboutus(request):
    return render(request, "aboutus.html")


def team(request):
    return render(request, "team.html")


def news(request):
    return render(request, "news.html")


def quehacemos(request):
    return render(request, "quehacemos.html")


def contactus(request):
    return render(request, "contactus.html")


def admin(request):
    return render(request, "admin.html")


def admin_add_route(request):
    return render(request, "admin-add-route.html")


def admin_events(request):
    return render(request, "admin-events.html")


def admin_places(request):
    return render(request, "admin-places.html")


def admin_users(request):
    return render(request, "admin-users.html")


def contacts(request):
    return render(request, "contacts.html")


def events(request):
    return render(request, "events.html")


def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")


def user_profile(request):
    return render(request, "user-profile.html")
