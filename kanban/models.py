from django.db import models
from django.conf import settings

import datetime

# Create your models here.

class Task(models.Model):
	# 
	title = models.CharField(max_length=128)
	description = models.TextField(blank=True, null=True)
	time_effort = models.PositiveSmallIntegerField(default=0)
	# 
	creator = models.ForeignKey(settings.AUTH_USER_MODEL)
	create_date = models.DateTimeField(default=datetime.datetime.now)
	lastupate_date = models.DateTimeField(default=datetime.datetime.now)