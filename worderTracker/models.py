from django.db import models

# Create your models here.

class WorkOrderTracker(models.Model):
    jobNumber =models.CharField(max_length=8,primary_key = True)
    dueDate = models.DateField()
    incomingInspection = models.BooleanField(blank=True,null=True)
    ME = models.CharField(blank=True,max_length=2,null=True)
    rush = models.BooleanField(blank=True,null=True)
    notes1 = models.TextField(blank=True,null=True)
    notes2 = models.TextField(blank=True,null=True)

