from django.db import models

# Create your models here.

class WorkOrderTracker(models.Model):
    jobNumber =models.CharField(max_length=8,primary_key = True)
    customer = models.CharField(max_length=50)
    qty= models.CharField(max_length=5)
    dueDate = models.DateField()
    shippingThisMonth = models.BooleanField(blank=True,null=True)
    TA = models.CharField(max_length=5)
    notes1 = models.TextField(blank=True,null=True)
    incomingInspection = models.BooleanField(blank=True,null=True)
    ME = models.CharField(blank=True,max_length=2,null=True)
    rush = models.BooleanField(blank=True,null=True)
    notes2 = models.TextField(blank=True,null=True)


class Operation(models.Model):
    jobNumber= models.ForeignKey(WorkOrderTracker, on_delete=models.CASCADE)
    workCenter = models.CharField(max_length=25)
    description = models.TextField()
    estimatedHours = models.CharField(max_length=5)
    status = models.CharField(max_length=15)
    stepNumber = models.IntegerField()
    customNotes = models.TextField(blank=True,null=True)