from django.contrib import admin
from .models import WorkOrderTracker
from .models import Operation
from .models import MEs
from .models import JobNotes

admin.site.register(WorkOrderTracker)
admin.site.register(Operation)
admin.site.register(MEs)
admin.site.register(JobNotes)