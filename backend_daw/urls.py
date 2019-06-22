"""backend_daw URL Configuration

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
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/users.json', views.login, name="users"),
    path('areas', views.areas, name="areas"),
    path("waypoints", views.waypoints, name="waypoints"),
    path('events', views.events, name="events"),
    path('signup', views.signup, name="signup"),
    path('get_my_classes', views.my_classes, name="my_classes"),
    path('get_my_events', views.my_events, name="my_events"),
    path('add_my_event', views.add_my_event, name="add_my_event"),
    path('remove_my_event', views.remove_my_event, name="remove_my_event"),
    path('get_friends_groups', views.friends_groups, name="friends_groups"),
    path('poll', views.poll, name="poll"),
    path('ask_position', views.ask_position, name="ask_position"),
    path('publish_my_position', views.show_my_position, name="show_my_position"),
    path('api_admin/new_or_edit_event', views.admin_edit_event, name="admin_edit_event"),
    path('api_admin/delete_event', views.admin_delete_event, name="admin_delete_event"),
    path('api_admin/new_or_edit_waypoint', views.admin_edit_waypoint, name="admin_edit_waypoint"),
    path('api_admin/delete_waypoint', views.admin_delete_waypoint, name="admin_delete_waypoint"),
    path('api_admin/new_or_edit_area', views.admin_edit_area, name="admin_edit_area"),
    path('api_admin/delete_area', views.admin_delete_area, name="admin_delete_area"),
    path('api_admin/view_users', views.admin_view_users, name="admin_view_users"),
    path('api_admin/block_user', views.admin_block_user, name="admin_block_user"),
    path('api_admin/adminify_user', views.admin_adminify_user, name="admin_adminify_user"),
]
