from django.db import models


# Create your models here.
class Waypoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"WP {self.name}"

    def to_dict(self):
        return [self.latitude, self.longitude, self.name]


class Area(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Area {self.name}"

    def to_dict(self):
        return [self.latitude, self.longitude, self.name]


class Subject(models.Model):
    name = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()

    def to_dict(self):
        return {"NOMBRE": self.subject.name, "PARALELO": self.number}

    def __str__(self):
        return f"{self.subject.name}#{self.number}"


class Session(models.Model):
    classroom = models.CharField(max_length=100)
    closest_waypoint = models.ForeignKey(Waypoint, on_delete=models.PROTECT)
    day = models.PositiveIntegerField()
    start_time = models.TimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def to_dict(self):
        return {"NOMBRE": self.course.subject.name,
                "PARALELO": self.course.number,
                "AULA": self.classroom,
                "BLOQUE": self.closest_waypoint.id,
                "HORA": f"{self.start_time.hour}:{self.start_time.minute}"
                }

    def __str__(self):
        return f"Session of {self.course} on day #{self.day} at {self.start_time}"


class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
    career = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, blank=True)
    friends = models.ManyToManyField('self')
    blocked = models.BooleanField(default=False)

    def to_dict(self):
        response_dict = {"NAMES": self.name, "LASTNAMES": "", "USERNAME": self.username, "EMAIL": self.email,
                         "PASSWORD": self.password, "CAREER": self.career,
                         "MATERIAS": [course.to_dict() for course in self.courses.all()]}
        if self.is_admin:
            response_dict["ADMIN"] = "true"
        return response_dict

    def to_friend_dict(self):
        return {"NAMES": self.name, "LASTNAMES": "", "CAREER": self.career}

    def to_admin_dict(self):
        return {"NAMES": self.name, "LASTNAMES": "", "USERNAME": self.username, "EMAIL": self.email,
                "CAREER": self.career, "BLOCKED": self.blocked, "ADMIN": self.is_admin, "ID": self.id}

    def __str__(self):
        return self.email


class Event(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=200)
    closest_waypoint = models.ForeignKey(Waypoint, related_name="events_closest", on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()

    def to_dict(self):
        return [self.name, self.place, self.closest_waypoint.id, str(self.start_datetime)]

    def __str__(self):
        return f"Event {self.name} at {self.place}"
