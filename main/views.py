from datetime import datetime as ddt

from django.db.models import ProtectedError, Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .models import User, Waypoint, Area, Event, TrackingRequest, Session, Subject, Course
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
    return JsonResponse({"waypoints": {w.id: w.to_dict() for w in Waypoint.objects.all().order_by("id")}})


@csrf_exempt
def areas(request):
    return JsonResponse({"areas": {a.id: [a.latitude, a.longitude, a.name] for a in Area.objects.all().order_by("id")}})


@csrf_exempt
def events(request):
    return JsonResponse({"events": {e.id: e.to_dict()
                                    for e in
                                    Event.objects.filter(start_datetime__gt=timezone.now()).order_by("start_datetime")}
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
        today_index = ddt.today().isoweekday()  # Monday is 1 and Sunday is 7
        return JsonResponse(
            {"classes": [s.to_dict() for c in user.courses.all() for s in c.session_set.all() if s.day == today_index]})
    else:
        return JsonResponse({"classes": []})


@csrf_exempt
def my_events(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], blocked=False)
    if len(user) == 1:
        user = user[0]
        return JsonResponse(
            {"events": {e.id: e.to_dict()
                        for e in user.saved_events.all().order_by("start_datetime")
                        if e.start_datetime > timezone.now()}
             })
    else:
        return JsonResponse({"events": []})


@csrf_exempt
def add_my_event(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], blocked=False)
    if len(user) == 1:
        user = user[0]
        ev = Event.objects.get(id=request.POST["event"])
        user.saved_events.add(ev)
        user.save()
        return JsonResponse({"status": "OK"})
    else:
        return JsonResponse({"status": "ERROR"})


@csrf_exempt
def remove_my_event(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], blocked=False)
    if len(user) == 1:
        user = user[0]
        ev = Event.objects.get(id=request.POST["event"])
        user.saved_events.remove(ev)
        user.save()
        return JsonResponse({"status": "OK"})
    else:
        return JsonResponse({"status": "ERROR"})


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
def search_people(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], blocked=False)
    if len(user) == 1:
        user = user[0]
        term = request.POST["query"]
        candidates = User.objects.exclude(friends__in=[user]).filter(blocked=False).filter(
            Q(name__icontains=term) | Q(email__icontains=term))
        return JsonResponse({"found": [f.to_search_dict() for f in candidates]})
    else:
        return JsonResponse({"found": []})


@csrf_exempt
def add_friend(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], blocked=False)
    if len(user) == 1:
        user = user[0]
        user.friends.add(User.objects.get(email=request.POST["friend"]))
        user.save()
        return JsonResponse({"status": "OK"})
    else:
        return JsonResponse({"status": "ERROR"})


@csrf_exempt
def remove_friend(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], blocked=False)
    if len(user) == 1:
        user = user[0]
        user.friends.remove(User.objects.get(email=request.POST["no_longer_friend"]))
        user.save()
        return JsonResponse({"status": "OK"})
    else:
        return JsonResponse({"status": "ERROR"})


from icalendar import Calendar, Event
import datetime
import re


def removePracticals(classes):
    nonDupes = []
    for x in classes:
        hasDupe = False
        for y in nonDupes:
            if x.course.subject.name == y.course.subject.name and x.day == y.day:
                hasDupe = True
                x.delete()
        if not hasDupe:
            nonDupes.append(x)
    return nonDupes


def extractCourseParallel(text):
    regex = re.compile(r"^(\w+)\s+-\s+(.+)Paralelo N. (\d+) Aula: (.+)$")
    groups = regex.search(text)
    return groups[2].strip(), groups[3].strip()

def magicFindClosestWp(classroom):
    return 1 # HACK: do something to recognize more classrooms???

def findOrCreateSession(component):
    days = ["SU", "MO", "TU", "WE", "TH", "FR", "SA"]
    subject, _ = Subject.objects.get_or_create(name=extractCourseParallel(component.get("description"))[0])
    parallel, _ = Course.objects.get_or_create(subject_id=subject.id,
                                            number=extractCourseParallel(component.get("description"))[1])
    dtstart = component.get('dtstart').dt - datetime.timedelta(hours=5)
    session, _ = Session.objects.get_or_create(course=parallel, day=days.index(component.get('rrule')['BYDAY'][0]),
                                               start_time=datetime.time(hour=dtstart.hour, minute=dtstart.minute),
                                               classroom=component.get('location'),
                                               closest_waypoint_id=magicFindClosestWp(component.get('location')))

    return session

@csrf_exempt
def upload_calendar(request):
    classes = []

    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], blocked=False)
    if len(user) == 1:
        user = user[0]
        f = request.FILES["file"]
        f.seek(0)

        fcal = Calendar.from_ical(f.read())
        for component in fcal.walk():
            if component.name == "VEVENT":
                x = findOrCreateSession(component)
                if x not in classes:
                    classes.append(x)

        classes = removePracticals(classes)

        for x in classes:
            x.save()
            if x.course not in user.courses.all():
                user.courses.add(x.course)
                user.save()

    return redirect(request.POST["backurl"])


@csrf_exempt
def poll(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], blocked=False)
    if len(user) == 1:
        user = user[0]
        tr_requests = []
        for tr in user.directed_questions.filter(state=TrackingRequest.REQUEST_CREATED):
            if tr.is_expired():
                tr.delete()
            else:
                tr.state = TrackingRequest.REQUEST_DELIVERED
                tr.save()
                tr_requests.append(tr)

        tr_responses = user.asked_questions.filter(state=TrackingRequest.REQUEST_GRANTED)
        for tr in tr_responses:
            tr.delete()

        return JsonResponse({"requests": [tr.to_dict_request() for tr in tr_requests],
                             "responses": [tr.to_dict_response() for tr in tr_responses]})
    else:
        return JsonResponse({"requests": [], "responses": []})


@csrf_exempt
def ask_position(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], blocked=False)
    if len(user) == 1:
        user = user[0]
        target = User.objects.get(email=request.POST["friend_email"])
        if user not in target.friends.all():
            return JsonResponse({"status": "ERROR"})
        TrackingRequest.objects.create(target=target, source=user)
        return JsonResponse({"status": "OK"})
    else:
        return JsonResponse({"status": "ERROR"})


@csrf_exempt
def show_my_position(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], blocked=False)
    if len(user) == 1:
        user = user[0]
        tr_request = TrackingRequest.objects.get(target=user,
                                                 source__email=request.POST["friend_email"],
                                                 state=TrackingRequest.REQUEST_DELIVERED)
        if request.POST["decision"] == "ACCEPT":
            tr_request.state = TrackingRequest.REQUEST_GRANTED
            tr_request.answer_latitude = request.POST["latitude"]
            tr_request.answer_longitude = request.POST["longitude"]
            tr_request.save()
        else:
            tr_request.delete()
        return JsonResponse({"status": "OK"})
    else:
        return JsonResponse({"status": "ERROR"})


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
        try:
            Event.objects.get(id=request.POST["event_id"]).delete()
            return JsonResponse({"result": "OK"})
        except ProtectedError:
            return JsonResponse({"result": "PROTECTED_ERROR"})
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
        try:
            Waypoint.objects.get(id=request.POST["waypoint_id"]).delete()
        except ProtectedError:
            return JsonResponse({"result": "PROTECTED_ERROR"})
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
        try:
            Area.objects.get(id=request.POST["area_id"]).delete()
        except ProtectedError:
            return JsonResponse({"result": "PROTECTED_ERROR"})
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


@csrf_exempt
def admin_adminify_user(request):
    user = User.objects.filter(email=request.POST["username"], password=request.POST["password"], is_admin=True)
    if len(user) == 1:
        target = User.objects.get(email=request.POST["target"])
        target.is_admin = False if request.POST["action"] == "UNADMIN" else True
        target.save()
        return JsonResponse({"result": "OK"})
    else:
        return JsonResponse({})
