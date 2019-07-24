"""staticserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
import staticserver.views as views

urlpatterns = [
    path('home', views.home, name="index_2"),
    path('', views.home, name="index"),
    path('aboutus', views.aboutus, name="aboutus"),
    path('team', views.team, name="team"),
    path('news', views.news, name="news"),
    path('quehacemos', views.quehacemos, name="quehacemos"),
    path('contactus', views.contactus, name="contactus"),
    path('admin_home', views.admin, name="admin_home"),
    path('admin-add-route', views.admin_add_route, name="admin_add_route"),
    path('admin-events', views.admin_events, name="admin_events"),
    path('admin-places', views.admin_places, name="admin_places"),
    path('admin-users', views.admin_users, name="admin_users"),
    path('contacts', views.contacts, name="contacts"),
    path('view_events', views.events, name="view_events"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('user-profile', views.user_profile, name="user_profile"),
]
