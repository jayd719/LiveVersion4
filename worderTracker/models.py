from django.db import models

# Create your models here.

class WorkOrderTracker(models.Model):
    jobNumber =models.CharField(max_length=8,primary_key = True)
    dueDate = models.DateField()
    incomingInspection = models.BooleanField(blank=True)
    ME = models.CharField(blank=True,max_length=2)
    rush = models.BooleanField(blank=True,)
    notes1 = models.TextField(blank=True)
    notes2 = models.TextField(blank=True)

