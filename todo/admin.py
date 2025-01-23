from django.contrib import admin
from .models import TODOO


@admin.register(TODOO)  
class TODOOAdmin(admin.ModelAdmin):
    list_display = ('srno', 'title', 'date', 'status', 'user')  
