from datetime import datetime, timedelta

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import User, Waypoint, Area, Event
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def login(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"])
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
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"])
    if len(user) == 1:
        user = user[0]
        today_index = datetime.today().isoweekday()  # Monday is 1 and Sunday is 7
        return JsonResponse(
            {"classes": [s.to_dict() for c in user.courses.all() for s in c.session_set.all() if s.day == today_index]})
    else:
        return JsonResponse({"classes": []})


@csrf_exempt
def friends_groups(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"])
    if len(user) == 1:
        user = user[0]
        return JsonResponse({"friends": [f.to_friend_dict() for f in user.friends.all()],
                             "groups": []})
    else:
        return JsonResponse({"friends": [], "groups": []})
