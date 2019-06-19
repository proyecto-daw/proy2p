from datetime import datetime, timedelta

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.dateparse import parse_datetime

from .models import User, Waypoint, Area, Event
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
@csrf_exempt
def login(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], blocked=False)
    if len(user) == 1:
        user = user[0]
        return JsonResponse({"members": [user.to_dict()]})
    else:
        return JsonResponse({"members": []})


@csrf_exempt
def waypoints(request):
    return JsonResponse({"waypoints": {w.id: [w.latitude, w.longitude, w.name] for w in Waypoint.objects.all()}})


@csrf_exempt
def areas(request):
    return JsonResponse({"areas": {a.id: [a.latitude, a.longitude, a.name] for a in Area.objects.all()}})


@csrf_exempt
def events(request):
    return JsonResponse({"events": {e.id: e.to_dict()
                                    for e in Event.objects.filter(start_datetime__gt=datetime.now(),
                                                                  start_datetime__lt=datetime.now() + timedelta(
                                                                      days=7))}
                         })


@csrf_exempt
def signup(request):
    user = User(username=request.POST["USERNAME"],
                name=request.POST["NAMES"] + " " + request.POST["LASTNAMES"],
                email=request.POST["EMAIL"],
                password=request.POST["PASSWORD"],
                career=request.POST["CAREER"])
    user.save()
    return JsonResponse({"members": [user.to_dict()]})


@csrf_exempt
def my_classes(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], blocked=False)
    if len(user) == 1:
        user = user[0]
        today_index = datetime.today().isoweekday()  # Monday is 1 and Sunday is 7
        return JsonResponse(
            {"classes": [s.to_dict() for c in user.courses.all() for s in c.session_set.all() if s.day == today_index]})
    else:
        return JsonResponse({"classes": []})


@csrf_exempt
def friends_groups(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], blocked=False)
    if len(user) == 1:
        user = user[0]
        return JsonResponse({"friends": [f.to_friend_dict() for f in user.friends.all()],
                             "groups": []})
    else:
        return JsonResponse({"friends": [], "groups": []})


@csrf_exempt
def admin_edit_event(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], is_admin=True)
    if len(user) == 1:
        desired_event = json.loads(request.POST["event"])
        if list(desired_event.keys())[0] == "-1":  # Create new event
            event = Event()
        else:  # Edit existing event
            event = Event.objects.get(id=list(desired_event.keys())[0])
        event.name = list(desired_event.values())[0][0]
        event.place = list(desired_event.values())[0][1]
        event.closest_waypoint = Waypoint.objects.get(id=list(desired_event.values())[0][2])
        event.start_datetime = parse_datetime(list(desired_event.values())[0][3])
        event.save()
        return JsonResponse({"event": {event.id: event.to_dict()}})
    else:
        return JsonResponse({})


@csrf_exempt
def admin_delete_event(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], is_admin=True)
    if len(user) == 1:
        Event.objects.get(id=request.POST["event_id"]).delete()
        return JsonResponse({"result": "OK"})
    else:
        return JsonResponse({})


@csrf_exempt
def admin_edit_waypoint(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], is_admin=True)
    if len(user) == 1:
        desired_waypoint = json.loads(request.POST["waypoint"])
        if list(desired_waypoint.keys())[0] == "-1":  # Create new waypoint
            waypoint = Waypoint()
        else:  # Edit existing waypoint
            waypoint = Waypoint.objects.get(id=list(desired_waypoint.keys())[0])
        waypoint.name = list(desired_waypoint.values())[0][2]
        waypoint.latitude = list(desired_waypoint.values())[0][0]
        waypoint.longitude = list(desired_waypoint.values())[0][1]
        waypoint.save()
        return JsonResponse({"waypoint": {waypoint.id: waypoint.to_dict()}})
    else:
        return JsonResponse({})


@csrf_exempt
def admin_delete_waypoint(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], is_admin=True)
    if len(user) == 1:
        Waypoint.objects.get(id=request.POST["waypoint_id"]).delete()
        return JsonResponse({"result": "OK"})
    else:
        return JsonResponse({})


@csrf_exempt
def admin_edit_area(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], is_admin=True)
    if len(user) == 1:
        desired_area = json.loads(request.POST["area"])
        if list(desired_area.keys())[0] == "-1":  # Create new area
            area = Area()
        else:  # Edit existing area
            area = Area.objects.get(id=list(desired_area.keys())[0])
        area.name = list(desired_area.values())[0][2]
        area.latitude = list(desired_area.values())[0][0]
        area.longitude = list(desired_area.values())[0][1]
        area.radius = 50
        area.save()
        return JsonResponse({"area": {area.id: area.to_dict()}})
    else:
        return JsonResponse({})


@csrf_exempt
def admin_delete_area(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], is_admin=True)
    if len(user) == 1:
        Area.objects.get(id=request.POST["area_id"]).delete()
        return JsonResponse({"result": "OK"})
    else:
        return JsonResponse({})


@csrf_exempt
def admin_view_users(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], is_admin=True)
    if len(user) == 1:
        return JsonResponse({"users": [u.to_admin_dict() for u in User.objects.all()]})
    else:
        return JsonResponse({})


@csrf_exempt
def admin_block_user(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], is_admin=True)
    if len(user) == 1:
        target = User.objects.get(email=request.POST["target"])
        target.blocked = False if request.POST["action"] == "UNLOCK" else True
        target.save()
        return JsonResponse({"result": "OK"})
    else:
        return JsonResponse({})
