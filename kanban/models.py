from django.db import models
from django.conf import settings

import datetime

# Create your models here.

class Project(models.Model):
	#
	title = models.CharField(max_length=128, unique=True)
	description = models.TextField(blank=True, null=True)
	membres = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True)
	#
	create_date = models.DateTimeField(default=datetime.datetime.now)

class Task(models.Model):
	# 
	title = models.CharField(max_length=128)
	description = models.TextField(blank=True, null=True)
	time_effort = models.PositiveSmallIntegerField(default=0)
	project = models.ForeignKey(Project, null=True)
	# 
	creator = models.ForeignKey(settings.AUTH_USER_MODEL)
	create_date = models.DateTimeField(default=datetime.datetime.now)
	lastupate_date = models.DateTimeField(default=datetime.datetime.now)