from django.db import models
from django.conf import settings
from django.utils import timezone

# Static variables



# Create your models here.

class Project(models.Model):
	#
	title = models.CharField(max_length=128, unique=True)
	description = models.TextField(blank=True, null=True)
	membres = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True)
	#
	create_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title

class Stage(models.Model):
	#
	title = models.CharField(max_length=64)
	project = models.ForeignKey(Project)
	order = models.PositiveSmallIntegerField(default=0)

	class Meta:
		 unique_together = (('project', 'title'), ('project', 'order'), )

	def __str__(self):
		return self.title

class Task(models.Model):
	title = models.CharField(max_length=128)
	description = models.TextField(blank=True, null=True)
	time_effort = models.PositiveSmallIntegerField(default=0)
	project = models.ForeignKey(Project, null=True)
	stage = models.ForeignKey(Stage, null=True)
	creator = models.ForeignKey(settings.AUTH_USER_MODEL)
	create_date = models.DateTimeField(default=timezone.now)
	lastupate_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title

class ActivityLog(models.Model):
	#
	actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
	project = models.ForeignKey(Project, null=True)
	content = models.TextField(blank=True)
	date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		if self.actor:
			return ' '.join([str(self.actor.get_username()), str(self.content)])
		else:
			return ' '.join(['Ayra', str(content)])