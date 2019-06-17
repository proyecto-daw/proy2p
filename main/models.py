from django.db import models


# Create your models here.
class Subject(models.Model):
    name = models.TextField(max_length=100)


class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()

    def to_dict(self):
        return {"NOMBRE": self.subject.name, "PARALELO": self.number}


class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
    career = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, null=True, blank=True)

    def to_dict(self):
        response_dict = {"NAMES": self.name, "LASTNAMES": "", "USERNAME": self.username, "EMAIL": self.email,
                         "PASSWORD": self.password, "CAREER": self.career,
                         "MATERIAS": [course.to_dict() for course in self.courses.all()]}
        if self.is_admin:
            response_dict["ADMIN"] = "true"
        return response_dict


class Waypoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)


class Area(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()
    name = models.CharField(max_length=100)
