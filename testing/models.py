from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.admin import User
from datetime import datetime
import django.forms


class Course(models.Model):
    course_name=models.CharField(max_length=60)
    created_on = models.DateField(default=datetime.now)
    owner = models.ForeignKey(User)
    class Meta:
        ordering = ('created_on',)

    def __str__(self):
            return self.course_name


class Posts(models.Model):
    courseid = models.ForeignKey(Course)
    title=models.CharField(max_length=100)
    content=models.CharField(max_length=500)
    created_on = models.DateField(default=datetime.now)

    class Meta:
        ordering = ('created_on',)
    def __str__(self):
       return self.title



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    qualification = models.CharField(max_length=140)
    location = models.CharField(max_length=140)
    enrolled=models.ManyToManyField(Course)

    def __unicode__(self):
        return self.user.username
