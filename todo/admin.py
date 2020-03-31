from django.contrib import admin
from .models import Todo

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('creating_date', )

admin.site.register(Todo, TodoAdmin)
# Register your models here.
