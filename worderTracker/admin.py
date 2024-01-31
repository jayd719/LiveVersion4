from django.contrib import admin
from .models import WorkOrderTracker
from .models import Operation

admin.site.register(WorkOrderTracker)
admin.site.register(Operation)