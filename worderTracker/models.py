from django.db import models

# Create your models here.

class WorkOrderTracker(models.Model):
    jobNumber =models.CharField(max_length=8,primary_key = True)
    dueDate = models.DateField()
    # incomingInspection = models.BooleanField()
    # notes = models.TextField()
    # ME = models.CharField(max_length=2)
    # rush = models.BooleanField()
    # completed = models.FloatField()
    # dateCompleted=models.DateField()
