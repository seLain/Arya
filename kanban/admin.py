from django.contrib import admin
from .models import Project, Stage, Task

# Register your models here.

admin.site.register(Project)
admin.site.register(Stage)
admin.site.register(Task)
