from django.contrib import admin
from .models import Tasks, Results


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    pass


@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    pass

# Register your models here.
