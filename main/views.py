from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import User, Waypoint, Area
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def login(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"])
    if len(user) == 1:
        user = user[0]
        return JsonResponse(user.to_dict())
    else:
        return JsonResponse({})


@csrf_exempt
def waypoints(request):
    return JsonResponse({"waypoints": {w.id: [w.latitude, w.longitude, w.name] for w in Waypoint.objects.all()}})


@csrf_exempt
def areas(request):
    return JsonResponse({"areas": {a.id: [a.latitude, a.longitude, a.name] for a in Area.objects.all()}})
