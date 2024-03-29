from django.contrib import admin
from .models import *


# Register your models here.
class RouteInline(admin.TabularInline):
    model = Route
    fk_name = "target"
    extra = 1


@admin.register(Waypoint)
class WaypointAdmin(admin.ModelAdmin):
    inlines = (RouteInline,)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass

@admin.register(TrackingRequest)
class TrackingRequestAdmin(admin.ModelAdmin):
    pass